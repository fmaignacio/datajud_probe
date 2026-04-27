"""Parse STJ SGT vocabulary exports stored as HTML-like SQL/XLS files."""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup


DATE_COLUMNS = [
    "data_publicacao",
    "data_alteracao",
    "data_inativacao",
    "data_reativacao",
]


@dataclass(frozen=True)
class VocabularySpec:
    name: str
    label_column: str
    type_code: str
    total_columns: int
    columns: list[str]
    source_glossary_row: bool = False


VOCABULARIES: dict[str, VocabularySpec] = {
    "assuntos": VocabularySpec(
        name="assuntos",
        label_column="assunto",
        type_code="A",
        total_columns=14,
        source_glossary_row=True,
        columns=[
            "codigo",
            "codigo_pai",
            "dispositivo_legal",
            "artigo",
            "ods",
            *DATE_COLUMNS,
        ],
    ),
    "classes": VocabularySpec(
        name="classes",
        label_column="classe",
        type_code="C",
        total_columns=19,
        columns=[
            "codigo",
            "codigo_pai",
            "dispositivo_legal",
            "artigo",
            "sigla",
            "alteracoes",
            "glossario",
            *DATE_COLUMNS,
            "tipo_procedimento",
            "originario_recursal",
            "criminal",
        ],
    ),
    "documentos": VocabularySpec(
        name="documentos",
        label_column="documento",
        type_code="D",
        total_columns=11,
        columns=[
            "codigo",
            "codigo_pai",
            *DATE_COLUMNS,
        ],
    ),
    "movimentos": VocabularySpec(
        name="movimentos",
        label_column="movimento_nome",
        type_code="M",
        total_columns=18,
        columns=[
            "codigo",
            "codigo_pai",
            "complemento",
            "movimento",
            "visibilidade_externa",
            "dispositivo_legal",
            "artigo",
            "alteracoes",
            "glossario",
            *DATE_COLUMNS,
        ],
    ),
    "movimentos_impressao": VocabularySpec(
        name="movimentos",
        label_column="movimento_nome",
        type_code="M",
        total_columns=13,
        source_glossary_row=True,
        columns=[
            "codigo",
            "codigo_pai",
            "dispositivo_legal",
            "artigo",
            *DATE_COLUMNS,
        ],
    ),
}


def clean_cell_text(value: object) -> str | None:
    """Normalize whitespace and blank values extracted from HTML cells."""
    if value is None:
        return None

    text = str(value).replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text or None


def is_export_header_label(label: str | None) -> bool:
    """Return True for non-item title labels accidentally mixed into rows."""
    return bool(
        label
        and label
        in {
            "Assuntos processuais do STJ",
            "Classes processuais do STJ",
            "Documentos processuais",
            "Movimentos processuais do STJ",
        }
    )


def normalize_codigo(value: object, *, max_digits: int = 5) -> str | None:
    """Normalize SGT codes as strings without losing identity to floats."""
    text = clean_cell_text(value)
    if text is None:
        return None

    text = text.replace(".", "")
    if text.endswith(",0") or text.endswith(".0"):
        text = text[:-2]

    digits = re.sub(r"\D", "", text)
    if not digits or len(digits) > max_digits:
        return None
    return digits


def infer_vocabulary_from_filename(path: str | Path) -> str:
    """Infer the vocabulary kind from the official export filename."""
    name = Path(path).name.lower()
    if "assuntos" in name:
        return "assuntos"
    if "classes" in name:
        return "classes"
    if "documentos" in name:
        return "documentos"
    if "movimentos" in name:
        if "impressao" in name and name.endswith(".xls"):
            return "movimentos_impressao"
        return "movimentos"
    raise ValueError(f"Nao foi possivel inferir o tipo de vocabulario de {path}")


def expand_colspans(cells: Iterable) -> list:
    """Repeat cells according to colspan so visual hierarchy columns align."""
    expanded = []
    for cell in cells:
        try:
            colspan = int(cell.get("colspan", 1))
        except (TypeError, ValueError):
            colspan = 1
        expanded.extend([cell] * max(colspan, 1))
    return expanded


def iter_table_cell_groups(table) -> Iterable[list]:
    """Yield row-like cell groups from STJ/CNJ HTML exports."""
    for row in table.find_all("tr"):
        cells = row.find_all("td", recursive=False)
        if cells:
            yield cells


def extract_item_segments(texts: list[str], spec: VocabularySpec) -> Iterable[tuple[list[str], int]]:
    """Extract item segments from rows that sometimes contain two logical rows."""
    idx = 0
    while idx < len(texts):
        code_index = None
        for candidate in range(idx, len(texts)):
            code = normalize_codigo(texts[candidate])
            if code is None:
                continue

            previous_window = texts[max(idx, candidate - 6) : candidate]
            label_index = next(
                (pos for pos in range(len(previous_window) - 1, -1, -1) if previous_window[pos]),
                None,
            )
            if label_index is None:
                continue
            label = previous_window[label_index]
            if label.startswith(("Itens existentes", "Itens adicionados", "Código ", "Legenda")):
                continue

            code_index = candidate
            break

        if code_index is None:
            break

        label_window_start = max(idx, code_index - 6)
        label_window = texts[label_window_start:code_index]
        label_position = next(
            pos for pos in range(len(label_window) - 1, -1, -1) if label_window[pos]
        )
        label = label_window[label_position]
        nivel_visual = label_position + 1

        tail_length = len(spec.columns)
        tail = texts[code_index : code_index + tail_length]
        tail = tail + [""] * max(0, tail_length - len(tail))
        yield [label, *tail], nivel_visual

        idx = code_index + max(2, tail_length)


def parse_vocabulary_html_table(
    path: str | Path,
    *,
    vocabulary: str | None = None,
    encoding: str = "latin-1",
) -> pd.DataFrame:
    """Parse one STJ SGT HTML export into a normalized DataFrame."""
    input_path = Path(path)
    spec = VOCABULARIES[vocabulary or infer_vocabulary_from_filename(input_path)]

    html = input_path.read_text(encoding=encoding, errors="replace")
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    if table is None:
        raise ValueError(f"Nenhuma tabela HTML encontrada em {input_path}")

    rows: list[dict[str, object]] = []

    for cells in iter_table_cell_groups(table):
        expanded_cells = expand_colspans(cells)
        texts = [clean_cell_text(cell.get_text(" ", strip=True)) or "" for cell in expanded_cells]
        if spec.source_glossary_row and rows and len(texts) < len(spec.columns) + 1:
            glossary_text = clean_cell_text(" ".join(texts))
            if glossary_text:
                if glossary_text.startswith("Glossário:"):
                    glossary_text = clean_cell_text(glossary_text.replace("Glossário:", "", 1))
                if glossary_text and not normalize_codigo(glossary_text):
                    current = rows[-1].get("glossario")
                    rows[-1]["glossario"] = clean_cell_text(
                        f"{current} {glossary_text}" if current else glossary_text
                    )
            continue

        for segment, nivel_visual in extract_item_segments(texts, spec):
            values = dict(zip(spec.columns, segment[1:], strict=True))
            codigo = normalize_codigo(values.get("codigo"))
            if codigo is None:
                continue
            values["codigo"] = codigo
            values["codigo_pai"] = normalize_codigo(values.get("codigo_pai"))

            row = {
                spec.label_column: clean_cell_text(segment[0]),
                "codigo": values.pop("codigo"),
                "codigo_pai": values.pop("codigo_pai"),
                **{key: clean_cell_text(value) for key, value in values.items()},
                "nivel_visual": nivel_visual,
                "tipo_item": spec.type_code,
                "fonte": input_path.name,
            }
            if is_export_header_label(row[spec.label_column]):
                continue
            if spec.source_glossary_row:
                row.setdefault("glossario", None)
            rows.append(row)

    columns = [
        spec.label_column,
        "codigo",
        "codigo_pai",
        *[column for column in spec.columns if column not in {"codigo", "codigo_pai"}],
        "glossario" if spec.source_glossary_row else None,
        "nivel_visual",
        "tipo_item",
        "fonte",
    ]
    columns = [column for column in columns if column is not None]
    df = pd.DataFrame(rows, columns=columns)
    if df.empty:
        return df

    df = df.drop_duplicates(subset=["codigo", "tipo_item", "fonte"]).reset_index(drop=True)
    for column in DATE_COLUMNS:
        if column in df.columns:
            df[column] = pd.to_datetime(df[column], errors="coerce", format="mixed")

    return add_hierarchy_paths(df, label_column=spec.label_column)


def parse_vocabulary_files(paths: Iterable[str | Path]) -> dict[str, pd.DataFrame]:
    """Parse several vocabulary files, grouped by inferred vocabulary type."""
    grouped: dict[str, list[pd.DataFrame]] = {}
    source_paths = sorted(
        map(Path, paths),
        key=lambda path: (path.suffix.lower() != ".sql", path.name),
    )
    for path in source_paths:
        vocabulary = infer_vocabulary_from_filename(path)
        output_name = VOCABULARIES[vocabulary].name
        grouped.setdefault(output_name, []).append(parse_vocabulary_html_table(path, vocabulary=vocabulary))

    result: dict[str, pd.DataFrame] = {}
    for vocabulary, frames in grouped.items():
        if not frames:
            result[vocabulary] = pd.DataFrame()
            continue

        df = pd.concat(frames, ignore_index=True)
        if {"codigo", "tipo_item"}.issubset(df.columns):
            df = df.drop_duplicates(subset=["codigo", "tipo_item"]).reset_index(drop=True)
        result[vocabulary] = df

    return result


def add_hierarchy_paths(df: pd.DataFrame, *, label_column: str) -> pd.DataFrame:
    """Add code and label paths based on ``codigo_pai`` relationships."""
    if df.empty:
        return df.copy()

    result = df.copy()
    by_code = (
        result.drop_duplicates(subset=["codigo"])
        .set_index("codigo")[[label_column, "codigo_pai"]]
        .to_dict("index")
    )

    def build_path(code: str, field: str) -> str:
        values: list[str] = []
        seen: set[str] = set()
        current = code

        while current and current not in seen:
            seen.add(current)
            item = by_code.get(current)
            if item is None:
                values.append(current)
                break

            values.append(str(item[field] if field == label_column else current))
            parent = item.get("codigo_pai")
            current = "" if parent is None or pd.isna(parent) else str(parent)

        return " > ".join(reversed(values))

    result["caminho_codigos"] = result["codigo"].map(lambda code: build_path(code, "codigo"))
    result["caminho_rotulos"] = result["codigo"].map(lambda code: build_path(code, label_column))
    return result


def save_vocabulary_outputs(
    dataframes: dict[str, pd.DataFrame],
    output_dir: str | Path,
) -> dict[str, dict[str, Path]]:
    """Save parsed vocabularies as CSV and Parquet files."""
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)

    outputs: dict[str, dict[str, Path]] = {}
    for vocabulary, df in dataframes.items():
        csv_path = destination / f"sgt_stj_{vocabulary}.csv"
        parquet_path = destination / f"sgt_stj_{vocabulary}.parquet"
        df.to_csv(csv_path, index=False)
        df.to_parquet(parquet_path, index=False)
        outputs[vocabulary] = {"csv": csv_path, "parquet": parquet_path}

    return outputs
