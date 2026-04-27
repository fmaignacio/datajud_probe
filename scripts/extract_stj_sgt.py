#!/usr/bin/env python3
"""Extract useful lookup tables from STJ SGT files stored in docs/."""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.sgt_stj import parse_vocabulary_files, save_vocabulary_outputs

DOCS_DIR = PROJECT_ROOT / "docs"
OUTPUT_DIR = PROJECT_ROOT / "data" / "reference" / "sgt_stj" / "processed"
REPORT_PATH = DOCS_DIR / "SGT_STJ_INVENTARIO.md"


def count_dump_inserts(path: Path) -> Counter[str]:
    """Count INSERT statements by destination table in a MySQL dump."""
    counts: Counter[str] = Counter()
    pattern = re.compile(r"^INSERT INTO sgt_consulta\.([a-z_]+)\b")
    with path.open(encoding="latin-1", errors="replace") as handle:
        for line in handle:
            match = pattern.match(line)
            if match:
                counts[match.group(1)] += 1
    return counts


def list_schema_tables(path: Path) -> list[str]:
    """List table names declared in the structure dump."""
    pattern = re.compile(r"^CREATE TABLE `([^`]+)`")
    tables: list[str] = []
    with path.open(encoding="latin-1", errors="replace") as handle:
        for line in handle:
            match = pattern.match(line)
            if match:
                tables.append(match.group(1))
    return tables


def summarize_dataframe(name: str, df: pd.DataFrame) -> dict[str, object]:
    """Build a compact summary for a parsed vocabulary DataFrame."""
    label_column = df.columns[0]
    root_count = int(df["codigo_pai"].isna().sum()) if "codigo_pai" in df else 0
    inactive_count = (
        int(df["data_inativacao"].notna().sum())
        if "data_inativacao" in df
        else 0
    )
    changed_count = (
        int(df["data_alteracao"].notna().sum())
        if "data_alteracao" in df
        else 0
    )
    glossary_count = (
        int(df["glossario"].notna().sum())
        if "glossario" in df
        else 0
    )
    examples = (
        df[["codigo", "codigo_pai", label_column, "caminho_rotulos"]]
        .head(8)
        .to_markdown(index=False)
    )
    return {
        "name": name,
        "label_column": label_column,
        "rows": len(df),
        "unique_codes": df["codigo"].nunique(),
        "roots": root_count,
        "max_level": int(df["nivel_visual"].max()) if "nivel_visual" in df else None,
        "changed": changed_count,
        "inactive": inactive_count,
        "glossary": glossary_count,
        "columns": ", ".join(df.columns),
        "examples": examples,
    }


def build_report(
    frames: dict[str, pd.DataFrame],
    outputs: dict[str, dict[str, Path]],
    dump_counts: Counter[str],
    schema_tables: list[str],
) -> str:
    """Render a Markdown inventory of the extracted STJ SGT material."""
    source_files = sorted([*DOCS_DIR.glob("78_Tabela_*.sql"), *DOCS_DIR.glob("78_Tabela_*.xls")])
    source_lines = "\n".join(
        f"- `{path.name}`: {path.stat().st_size:,} bytes" for path in source_files
    )

    dump_lines = "\n".join(
        f"- `{table}`: {count:,} inserts" for table, count in sorted(dump_counts.items())
    )
    schema_line = ", ".join(f"`{table}`" for table in schema_tables)

    summary_table = pd.DataFrame(
        [
            {
                "vocabulario": item["name"],
                "linhas": item["rows"],
                "codigos_unicos": item["unique_codes"],
                "raizes_sem_pai": item["roots"],
                "nivel_maximo_visual": item["max_level"],
                "com_alteracao": item["changed"],
                "inativos": item["inactive"],
                "com_glossario": item["glossary"],
            }
            for item in (summarize_dataframe(name, df) for name, df in frames.items())
        ]
    ).sort_values("vocabulario")

    output_lines = []
    for name, paths in sorted(outputs.items()):
        output_lines.append(f"- `{name}`: `{paths['csv'].relative_to(PROJECT_ROOT)}`")
        output_lines.append(f"- `{name}` parquet: `{paths['parquet'].relative_to(PROJECT_ROOT)}`")

    detail_sections = []
    for name, df in sorted(frames.items()):
        item = summarize_dataframe(name, df)
        detail_sections.append(
            "\n".join(
                [
                    f"## {name.title()}",
                    "",
                    f"- Linhas extraidas: {item['rows']:,}",
                    f"- Coluna de rotulo principal: `{item['label_column']}`",
                    f"- Colunas: {item['columns']}",
                    "",
                    "Amostra inicial:",
                    "",
                    str(item["examples"]),
                ]
            )
        )

    return "\n\n".join(
        [
            "# Inventario SGT/STJ",
            "Este arquivo foi gerado por `scripts/extract_stj_sgt.py` a partir dos documentos colocados em `docs/`.",
            "Os arquivos `78_Tabela_*.sql` e `78_Tabela_*.xls` sao exports HTML; os arquivos `dump_*.sql` sao dumps MySQL do schema `sgt_consulta`.",
            "## Fontes HTML lidas",
            source_lines,
            "## Saidas geradas",
            "\n".join(output_lines),
            "## Resumo dos vocabulários STJ",
            summary_table.to_markdown(index=False),
            "## Dump MySQL",
            f"Tabelas declaradas em `dump_estrutura.sql`: {schema_line}.",
            "Contagem de inserts em `dump_dados.sql`:",
            dump_lines,
            "## Observacoes uteis",
            "\n".join(
                [
                    "- `codigo` e `codigo_pai` permitem reconstruir hierarquias de assuntos, classes, documentos e movimentos.",
                    "- `tipo_item` segue a codificacao do SGT: `A` assunto, `C` classe, `D` documento processual, `M` movimento.",
                    "- Os exports HTML do STJ sao subconjuntos/visoes de impressao; o dump MySQL contem tambem tabelas auxiliares, complementos, ODS e temporariedade.",
                    "- Para enriquecer a EDA do STJ, os arquivos mais imediatamente uteis sao `sgt_stj_assuntos.parquet`, `sgt_stj_classes.parquet` e `sgt_stj_movimentos.parquet`.",
                ]
            ),
            *detail_sections,
            "",
        ]
    )


def main() -> None:
    html_sources = sorted([*DOCS_DIR.glob("78_Tabela_*.sql"), *DOCS_DIR.glob("78_Tabela_*.xls")])
    frames = parse_vocabulary_files(html_sources)
    outputs = save_vocabulary_outputs(frames, OUTPUT_DIR)

    dump_counts = count_dump_inserts(DOCS_DIR / "dump_dados.sql")
    schema_tables = list_schema_tables(DOCS_DIR / "dump_estrutura.sql")
    REPORT_PATH.write_text(
        build_report(frames, outputs, dump_counts, schema_tables),
        encoding="utf-8",
    )

    print(f"Extraidos {len(frames)} vocabularios em {OUTPUT_DIR.relative_to(PROJECT_ROOT)}")
    print(f"Inventario escrito em {REPORT_PATH.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
