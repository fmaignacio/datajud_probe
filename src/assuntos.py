"""Parse CNJ/STJ subject lookup tables exported as HTML-like XLS files."""

from __future__ import annotations

import re
from collections.abc import Iterable
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup


SUBJECT_COLUMNS = [
    "assunto",
    "codigo",
    "codigo_pai",
    "dispositivo_legal",
    "artigo",
    "alteracoes",
    "glossario",
    "ods",
    "data_publicacao",
    "data_alteracao",
    "data_inativacao",
    "data_reativacao",
    "nivel_visual",
    "fonte",
    "instancia",
]

DATE_COLUMNS = [
    "data_publicacao",
    "data_alteracao",
    "data_inativacao",
    "data_reativacao",
]


def clean_cell_text(value: object) -> str | None:
    """Normalize whitespace and blank values from HTML table cells."""
    if value is None:
        return None

    text = str(value).replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text or None


def normalize_codigo(value: object, width: int = 5) -> str | None:
    """Normalize subject codes as strings, preserving leading zeroes."""
    text = clean_cell_text(value)
    if text is None:
        return None

    text = text.replace(".", "")
    if text.endswith(",0"):
        text = text[:-2]
    if text.endswith(".0"):
        text = text[:-2]

    digits = re.sub(r"\D", "", text)
    if not digits:
        return None
    if len(digits) > width:
        return None

    return digits.zfill(width)


def infer_instancia_from_filename(path: str | Path) -> str:
    """Infer the court instance label from exported table filenames."""
    stem = Path(path).stem
    stem = re.sub(r"^\d+_", "", stem)
    stem = stem.replace("_", " ")
    stem = re.sub(r"\bTabela Assuntos\b", "", stem, flags=re.IGNORECASE)
    stem = re.sub(r"\s+", " ", stem).strip()

    replacements = {
        "Justica": "Justiça",
        "Federal": "Federal",
        "1 Grau": "1º Grau",
        "2 Grau": "2º Grau",
    }
    for source, target in replacements.items():
        stem = stem.replace(source, target)

    return stem or "Nao identificada"


def parse_assuntos_html_table(
    path: str | Path,
    *,
    instancia: str | None = None,
    encoding: str = "latin-1",
) -> pd.DataFrame:
    """Parse one HTML-like XLS subject table into a normalized DataFrame."""
    input_path = Path(path)
    html = input_path.read_text(encoding=encoding, errors="replace")
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    if table is None:
        raise ValueError(f"Nenhuma tabela HTML encontrada em {input_path}")

    rows: list[dict[str, object]] = []
    instance_label = instancia or infer_instancia_from_filename(input_path)

    pending_cells = []

    def expand_colspans(cells: list) -> list:
        expanded = []
        for cell in cells:
            try:
                colspan = int(cell.get("colspan", 1))
            except (TypeError, ValueError):
                colspan = 1
            expanded.extend([cell] * max(colspan, 1))
        return expanded

    def add_row_from_cells(cells: list) -> None:
        cells = expand_colspans(cells)
        if len(cells) < 16:
            return

        texts = [clean_cell_text(cell.get_text(" ", strip=True)) or "" for cell in cells]
        assunto_levels = texts[:5]
        assunto_index = next(
            (idx for idx, text in enumerate(assunto_levels) if text),
            None,
        )
        if assunto_index is None:
            return

        codigo = normalize_codigo(texts[5])
        if codigo is None:
            return

        rows.append(
            {
                "assunto": assunto_levels[assunto_index],
                "codigo": codigo,
                "codigo_pai": normalize_codigo(texts[6]),
                "dispositivo_legal": clean_cell_text(texts[7]),
                "artigo": clean_cell_text(texts[8]),
                "alteracoes": clean_cell_text(texts[9]),
                "glossario": clean_cell_text(texts[10]),
                "ods": clean_cell_text(texts[11]),
                "data_publicacao": clean_cell_text(texts[12]),
                "data_alteracao": clean_cell_text(texts[13]),
                "data_inativacao": clean_cell_text(texts[14]),
                "data_reativacao": clean_cell_text(texts[15]),
                "nivel_visual": assunto_index + 1,
                "fonte": input_path.name,
                "instancia": instance_label,
            }
        )

    for child in table.children:
        name = getattr(child, "name", None)
        if name == "tr":
            if pending_cells:
                add_row_from_cells(pending_cells[:16])
                pending_cells = pending_cells[16:]

            add_row_from_cells(child.find_all("td", recursive=False))
        elif name == "td":
            pending_cells.append(child)
            if len(pending_cells) == 16:
                add_row_from_cells(pending_cells)
                pending_cells = []

    if pending_cells:
        add_row_from_cells(pending_cells[:16])

    df = pd.DataFrame(rows, columns=SUBJECT_COLUMNS)
    if df.empty:
        return df

    df = df.drop_duplicates(subset=["codigo", "fonte"]).reset_index(drop=True)
    for column in DATE_COLUMNS:
        df[column] = pd.to_datetime(df[column], errors="coerce")

    return df


def parse_assuntos_files(paths: Iterable[str | Path]) -> pd.DataFrame:
    """Parse one or more subject table files and concatenate them."""
    frames = [parse_assuntos_html_table(path) for path in sorted(map(Path, paths))]
    if not frames:
        return pd.DataFrame(columns=SUBJECT_COLUMNS)

    return pd.concat(frames, ignore_index=True)


def add_hierarchy_paths(df: pd.DataFrame) -> pd.DataFrame:
    """Add code and label paths based on ``codigo_pai`` relationships."""
    if df.empty:
        return df.copy()

    result = df.copy()
    by_code = (
        result.drop_duplicates(subset=["codigo"])
        .set_index("codigo")[["assunto", "codigo_pai"]]
        .to_dict("index")
    )

    def build_path(code: str, label_field: str) -> str:
        values: list[str] = []
        seen: set[str] = set()
        current = code

        while current and current not in seen:
            seen.add(current)
            item = by_code.get(current)
            if item is None:
                values.append(current)
                break

            values.append(str(item[label_field] if label_field == "assunto" else current))
            parent = item.get("codigo_pai")
            current = "" if parent is None or pd.isna(parent) else str(parent)

        return " > ".join(reversed(values))

    result["caminho_codigos"] = result["codigo"].map(lambda code: build_path(code, "codigo"))
    result["caminho_assuntos"] = result["codigo"].map(lambda code: build_path(code, "assunto"))
    return result


def save_assuntos_lookup(
    df: pd.DataFrame,
    output_dir: str | Path,
    *,
    stem: str = "assuntos_lookup",
) -> dict[str, Path]:
    """Save the parsed lookup table as CSV and Parquet."""
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)

    csv_path = destination / f"{stem}.csv"
    parquet_path = destination / f"{stem}.parquet"

    df.to_csv(csv_path, index=False)
    df.to_parquet(parquet_path, index=False)

    return {"csv": csv_path, "parquet": parquet_path}
