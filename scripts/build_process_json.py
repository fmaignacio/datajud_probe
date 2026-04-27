#!/usr/bin/env python3
"""Build per-process JSON files from the STJ processed parquet layer."""

from __future__ import annotations

import argparse
import json
from datetime import date, datetime
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


DEFAULT_PROCESSED = Path("data/processed")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate process-level JSON artifacts from STJ processed parquet files."
    )
    parser.add_argument(
        "--data-root",
        type=Path,
        default=None,
        help="Data root containing processed/. Example: /content/drive/MyDrive/Mestrado/2026/llms/data",
    )
    parser.add_argument(
        "--processed-dir",
        type=Path,
        default=None,
        help="Directory with processed parquet files. Overrides --data-root.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output directory for JSON files. Default: <processed>/process_json",
    )
    parser.add_argument(
        "--demo-dir",
        type=Path,
        default=None,
        help="Output directory for demo JSONL/index files. Default: <processed>/demo",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Maximum number of processes to export.",
    )
    parser.add_argument(
        "--only-linked",
        action="store_true",
        help="Export only processes linked to corpus documents (n_documentos_corpus > 0).",
    )
    parser.add_argument(
        "--only-with-text",
        action="store_true",
        help="Export only processes that have rows in stj_documentos_por_processo.parquet.",
    )
    parser.add_argument(
        "--sort-by-text",
        action="store_true",
        help="Sort selected processes by available text-document count, descending.",
    )
    parser.add_argument(
        "--numero-registro-stj",
        default=None,
        help="Export a single process by STJ registry number.",
    )
    parser.add_argument(
        "--numero-processo",
        default=None,
        help="Export a single process by CNJ number.",
    )
    parser.add_argument(
        "--include-full-text",
        action="store_true",
        help="Include full clean document text. By default text is truncated.",
    )
    parser.add_argument(
        "--max-text-chars",
        type=int,
        default=4000,
        help="Maximum clean-text characters per document when --include-full-text is not used.",
    )
    parser.add_argument(
        "--jsonl-name",
        default="processos_demo.jsonl",
        help="Name of the JSONL file written to demo-dir.",
    )
    return parser.parse_args()


def processed_dir_from_args(args: argparse.Namespace) -> Path:
    if args.processed_dir:
        return args.processed_dir
    if args.data_root:
        return args.data_root / "processed"
    return DEFAULT_PROCESSED


def read_parquet_if_exists(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_parquet(path)


def clean_key(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, float) and np.isnan(value):
        return None
    text = str(value).strip()
    if not text or text.lower() in {"nan", "none", "<na>", "nat"}:
        return None
    return text


def as_json_value(value: Any) -> Any:
    if value is None:
        return None
    if pd.isna(value):
        return None
    if isinstance(value, pd.Timestamp):
        return value.isoformat() if not pd.isna(value) else None
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    if isinstance(value, np.bool_):
        return bool(value)
    return value


def row_value(row: pd.Series, column: str) -> Any:
    if column not in row.index:
        return None
    return as_json_value(row[column])


def split_joined(value: Any) -> list[str]:
    text = clean_key(value)
    if not text:
        return []
    return [part.strip() for part in text.split("|") if part.strip()]


def first_joined(value: Any) -> str | None:
    parts = split_joined(value)
    return parts[0] if parts else None


def records_for_process(
    frame: pd.DataFrame,
    numero_processo: str | None,
    numero_registro_stj: str | None,
) -> pd.DataFrame:
    if frame.empty:
        return pd.DataFrame()
    masks = []
    if numero_processo and "numero_processo" in frame.columns:
        masks.append(frame["numero_processo"].astype("string").eq(numero_processo))
    if numero_registro_stj and "numero_registro_stj" in frame.columns:
        masks.append(frame["numero_registro_stj"].astype("string").eq(numero_registro_stj))
    if not masks:
        return pd.DataFrame(columns=frame.columns)
    mask = masks[0]
    for extra in masks[1:]:
        mask = mask | extra
    return frame.loc[mask].copy()


def first_record_for_process(
    frame: pd.DataFrame,
    numero_processo: str | None,
    numero_registro_stj: str | None,
) -> pd.Series | None:
    records = records_for_process(frame, numero_processo, numero_registro_stj)
    if records.empty:
        return None
    return records.iloc[0]


def process_key_counts(frame: pd.DataFrame) -> pd.Series:
    if frame.empty:
        return pd.Series(dtype="int64")
    pieces = []
    if "numero_registro_stj" in frame.columns:
        pieces.append(frame["numero_registro_stj"].dropna().astype("string"))
    if "numero_processo" in frame.columns:
        pieces.append(frame["numero_processo"].dropna().astype("string"))
    if not pieces:
        return pd.Series(dtype="int64")
    keys = pd.concat(pieces, ignore_index=True)
    keys = keys[keys.notna() & ~keys.isin(["", "nan", "None", "<NA>"])]
    return keys.value_counts()


def add_text_counts(processes: pd.DataFrame, documentos: pd.DataFrame) -> pd.DataFrame:
    processes = processes.copy()
    counts = process_key_counts(documentos)
    if counts.empty:
        processes["n_documentos_texto_disponiveis"] = 0
        return processes
    by_registro = (
        processes["numero_registro_stj"].astype("string").map(counts).fillna(0)
        if "numero_registro_stj" in processes.columns
        else pd.Series(0, index=processes.index)
    )
    by_cnj = (
        processes["numero_processo"].astype("string").map(counts).fillna(0)
        if "numero_processo" in processes.columns
        else pd.Series(0, index=processes.index)
    )
    processes["n_documentos_texto_disponiveis"] = by_registro.astype(int) + by_cnj.astype(int)
    return processes


def add_advogado_counts(processes: pd.DataFrame, advogados: pd.DataFrame) -> pd.DataFrame:
    processes = processes.copy()
    counts = process_key_counts(advogados)
    if counts.empty:
        processes["n_advogados"] = 0
        return processes
    by_registro = (
        processes["numero_registro_stj"].astype("string").map(counts).fillna(0)
        if "numero_registro_stj" in processes.columns
        else pd.Series(0, index=processes.index)
    )
    by_cnj = (
        processes["numero_processo"].astype("string").map(counts).fillna(0)
        if "numero_processo" in processes.columns
        else pd.Series(0, index=processes.index)
    )
    processes["n_advogados"] = by_registro.astype(int) + by_cnj.astype(int)
    return processes


def decode_json_list(value: Any) -> list[dict[str, Any]]:
    text = clean_key(value)
    if not text:
        return []
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return []
    if isinstance(data, list):
        return data
    return []


def build_source_counts(events: pd.DataFrame) -> pd.DataFrame:
    if events.empty or "processo_agregacao" not in events.columns or "event_source" not in events.columns:
        return pd.DataFrame()
    counts = (
        events.groupby(["processo_agregacao", "event_source"])
        .size()
        .unstack(fill_value=0)
        .rename_axis(index="processo_agregacao", columns=None)
        .reset_index()
    )
    rename_map = {
        col: f"n_eventos_{str(col).lower()}"
        for col in counts.columns
        if col != "processo_agregacao"
    }
    return counts.rename(columns=rename_map)


def build_partes(partes: pd.DataFrame, advogados: pd.DataFrame) -> list[dict[str, Any]]:
    if partes.empty:
        return []
    result = []
    for _, parte in partes.sort_values("parte_idx").iterrows():
        parte_idx = parte.get("parte_idx")
        advs = advogados
        if not advs.empty and "parte_idx" in advs.columns:
            advs = advs.loc[advs["parte_idx"].eq(parte_idx)]
        adv_records = []
        for _, adv in advs.sort_values("advogado_idx").iterrows() if not advs.empty else []:
            adv_records.append(
                {
                    "nome": row_value(adv, "nomeAdvogado"),
                    "oab": clean_key(row_value(adv, "codigoOAB")),
                }
            )
        result.append(
            {
                "parte_idx": row_value(parte, "parte_idx"),
                "tipo": row_value(parte, "descTipoParte"),
                "nome": row_value(parte, "nomeParte"),
                "documento": row_value(parte, "numeroCNPJ"),
                "advogados": adv_records,
            }
        )
    return result


def build_documentos(docs: pd.DataFrame, include_full_text: bool, max_text_chars: int) -> list[dict[str, Any]]:
    if docs.empty:
        return []
    sort_cols = [col for col in ["data_documento", "seq_documento"] if col in docs.columns]
    if sort_cols:
        docs = docs.sort_values(sort_cols)
    result = []
    for _, doc in docs.iterrows():
        texto = row_value(doc, "texto_limpo")
        texto_preview = None
        if isinstance(texto, str):
            texto_preview = texto if include_full_text else texto[:max_text_chars]
        result.append(
            {
                "seq_documento": row_value(doc, "seq_documento"),
                "data_documento": row_value(doc, "data_documento"),
                "tipo_documento": row_value(doc, "tipo_documento"),
                "ministro": row_value(doc, "ministro_documento"),
                "assuntos_raw": row_value(doc, "assuntos_raw"),
                "lote": row_value(doc, "lote"),
                "metadata_file": row_value(doc, "metadata_file"),
                "txt_path": row_value(doc, "txt_path"),
                "n_words_limpo": row_value(doc, "n_words_limpo"),
                "texto_vazio": row_value(doc, "texto_vazio"),
                "texto_limpo": texto_preview,
                "texto_truncado": bool(isinstance(texto, str) and not include_full_text and len(texto) > max_text_chars),
            }
        )
    return result


def build_timeline(row: pd.Series, docs: pd.DataFrame) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    data_dist = row_value(row, "data_primeira_distribuicao_stj")
    if data_dist:
        events.append(
            {
                "data": data_dist,
                "fonte": "ata_stj",
                "tipo": "distribuicao",
                "descricao": " | ".join(
                    part
                    for part in [
                        clean_key(row_value(row, "formas_distribuicao_stj")),
                        clean_key(row_value(row, "destinos_stj")),
                    ]
                    if part
                ),
            }
        )
    if not docs.empty:
        sort_cols = [col for col in ["data_documento", "seq_documento"] if col in docs.columns]
        if sort_cols:
            docs = docs.sort_values(sort_cols)
        for _, doc in docs.iterrows():
            data_doc = row_value(doc, "data_documento")
            if not data_doc:
                continue
            events.append(
                {
                    "data": data_doc,
                    "fonte": "integra_stj",
                    "tipo": "documento",
                    "descricao": " | ".join(
                        part
                        for part in [
                            clean_key(row_value(doc, "tipo_documento")),
                            clean_key(row_value(doc, "ministro_documento")),
                        ]
                        if part
                    ),
                    "seq_documento": row_value(doc, "seq_documento"),
                }
            )
    return sorted(events, key=lambda item: item.get("data") or "")


def build_datajud_block(
    numero_processo: str | None,
    numero_registro_stj: str | None,
    datajud_processos: pd.DataFrame,
    datajud_assuntos: pd.DataFrame,
) -> dict[str, Any]:
    processo_datajud = first_record_for_process(
        datajud_processos, numero_processo, numero_registro_stj
    )
    assuntos_proc = records_for_process(datajud_assuntos, numero_processo, numero_registro_stj)
    assuntos = []
    if not assuntos_proc.empty:
        assuntos = [
            {
                "codigo": row_value(assunto, "assunto_codigo_datajud"),
                "nome": row_value(assunto, "assunto_nome_datajud"),
            }
            for _, assunto in assuntos_proc.drop_duplicates().iterrows()
        ]

    if processo_datajud is None:
        return {
            "status": "pendente",
            "tribunal": None,
            "grau": None,
            "classe": None,
            "orgao_julgador": None,
            "nivel_sigilo": None,
            "data_ajuizamento": None,
            "data_ultima_atualizacao": None,
            "assuntos": assuntos,
        }

    return {
        "status": "disponivel",
        "tribunal": row_value(processo_datajud, "tribunal_datajud"),
        "grau": row_value(processo_datajud, "grau_datajud"),
        "classe": {
            "codigo": row_value(processo_datajud, "classe_codigo_datajud"),
            "nome": row_value(processo_datajud, "classe_nome_datajud"),
        },
        "orgao_julgador": {
            "codigo": row_value(processo_datajud, "orgao_julgador_codigo_datajud"),
            "nome": row_value(processo_datajud, "orgao_julgador_nome_datajud"),
        },
        "nivel_sigilo": row_value(processo_datajud, "nivel_sigilo_datajud"),
        "data_ajuizamento": row_value(processo_datajud, "data_ajuizamento_datajud"),
        "data_ultima_atualizacao": row_value(processo_datajud, "data_ultima_atualizacao_datajud"),
        "assuntos": assuntos,
    }


def build_process_json(
    row: pd.Series,
    partes: pd.DataFrame,
    advogados: pd.DataFrame,
    documentos: pd.DataFrame,
    timelines: pd.DataFrame,
    datajud_processos: pd.DataFrame,
    datajud_assuntos: pd.DataFrame,
    args: argparse.Namespace,
) -> dict[str, Any]:
    numero_processo = clean_key(row_value(row, "numero_processo"))
    numero_registro_stj = clean_key(row_value(row, "numero_registro_stj"))
    partes_proc = records_for_process(partes, numero_processo, numero_registro_stj)
    advs_proc = records_for_process(advogados, numero_processo, numero_registro_stj)
    docs_proc = records_for_process(documentos, numero_processo, numero_registro_stj)
    timeline_row = first_record_for_process(timelines, numero_processo, numero_registro_stj)
    timeline = decode_json_list(row_value(timeline_row, "timeline_json")) if timeline_row is not None else []
    timeline_start = row_value(timeline_row, "timeline_start") if timeline_row is not None else None
    timeline_end = row_value(timeline_row, "timeline_end") if timeline_row is not None else None
    timeline_event_count = row_value(timeline_row, "timeline_event_count") if timeline_row is not None else None
    timeline_sources = sorted(
        {clean_key(event.get("event_source")) for event in timeline if clean_key(event.get("event_source"))}
    )
    fontes = ["ata_stj", "integra_stj"]
    if any(source == "datajud_stj" for source in timeline_sources):
        fontes.append("datajud_stj")

    return {
        "processo": {
            "numero_processo": numero_processo,
            "numero_registro_stj": numero_registro_stj,
            "chave_agregacao": numero_registro_stj or numero_processo,
            "classe_stj": row_value(row, "classes_stj"),
            "classe_datajud": row_value(row, "classe_nome_datajud"),
            "assunto_cnj_ata": row_value(row, "assunto_cnj_ata"),
            "ano_origem_cnj": row_value(row, "ano_origem_cnj"),
            "segmento_cnj": row_value(row, "segmento_cnj"),
            "tribunal_cnj": row_value(row, "tribunal_cnj"),
            "origem_cnj": row_value(row, "origem_cnj"),
            "relator_ata_principal": first_joined(row_value(row, "relatores_stj")),
            "primeira_aparicao_corpus": row_value(row, "primeira_aparicao_corpus"),
            "ja_existia_antes_da_primeira_aparicao_corpus": row_value(
                row, "ja_existia_antes_da_primeira_aparicao_corpus"
            ),
            "ano_primeira_aparicao_corpus": row_value(row, "ano_primeira_aparicao_corpus"),
            "anos_entre_origem_e_corpus": row_value(row, "anos_entre_origem_e_corpus"),
        },
        "stj": {
            "data_primeira_distribuicao": row_value(row, "data_primeira_distribuicao_stj"),
            "data_ultima_distribuicao": row_value(row, "data_ultima_distribuicao_stj"),
            "n_eventos_distribuicao": row_value(row, "n_eventos_distribuicao_stj"),
            "formas_distribuicao": split_joined(row_value(row, "formas_distribuicao_stj")),
            "relatores": split_joined(row_value(row, "relatores_stj")),
            "destinos": split_joined(row_value(row, "destinos_stj")),
        },
        "partes": build_partes(partes_proc, advs_proc),
        "documentos": build_documentos(docs_proc, args.include_full_text, args.max_text_chars),
        "timeline": timeline or build_timeline(row, docs_proc),
        "datajud": build_datajud_block(
            numero_processo, numero_registro_stj, datajud_processos, datajud_assuntos
        ),
        "metadados_pipeline": {
            "fontes": fontes,
            "versao_schema": "process_json_v2",
            "n_documentos_corpus": row_value(row, "n_documentos_corpus"),
            "n_documentos_texto_disponiveis": row_value(row, "n_documentos_texto_disponiveis"),
            "n_advogados": row_value(row, "n_advogados"),
            "n_eventos_timeline": timeline_event_count,
            "timeline_start": timeline_start,
            "timeline_end": timeline_end,
            "timeline_sources": timeline_sources,
            "n_eventos_ata_stj": row_value(row, "n_eventos_ata_stj"),
            "n_eventos_datajud_stj": row_value(row, "n_eventos_datajud_stj"),
            "n_eventos_integra_stj": row_value(row, "n_eventos_integra_stj"),
            "ja_existia_antes_da_primeira_aparicao_corpus": row_value(
                row, "ja_existia_antes_da_primeira_aparicao_corpus"
            ),
        },
    }


def safe_file_stem(row: pd.Series) -> str:
    return clean_key(row_value(row, "numero_registro_stj")) or clean_key(row_value(row, "numero_processo")) or "processo"


def main() -> None:
    args = parse_args()
    processed = processed_dir_from_args(args)
    output_dir = args.output_dir or processed / "process_json"
    demo_dir = args.demo_dir or processed / "demo"
    output_dir.mkdir(parents=True, exist_ok=True)
    demo_dir.mkdir(parents=True, exist_ok=True)

    process_spine = read_parquet_if_exists(processed / "stj_processos_ciclo_vida.parquet")
    partes = read_parquet_if_exists(processed / "stj_ata_partes.parquet")
    advogados = read_parquet_if_exists(processed / "stj_ata_advogados.parquet")
    documentos = read_parquet_if_exists(processed / "stj_documentos_por_processo.parquet")
    timelines = read_parquet_if_exists(processed / "stj_process_timeline.parquet")
    events = read_parquet_if_exists(processed / "stj_process_events.parquet")
    datajud_processos = read_parquet_if_exists(processed / "stj_datajud_processos.parquet")
    datajud_assuntos = read_parquet_if_exists(processed / "stj_datajud_assuntos.parquet")
    if documentos.empty:
        documentos = read_parquet_if_exists(processed / "stj_integras_documentos_manifest.parquet")

    if process_spine.empty:
        raise FileNotFoundError(f"Missing or empty process spine: {processed / 'stj_processos_ciclo_vida.parquet'}")

    selected = process_spine.copy()
    if not datajud_processos.empty:
        selected = selected.merge(
            datajud_processos,
            on=["numero_processo", "numero_registro_stj"],
            how="left",
        )
    if not timelines.empty:
        timeline_meta = timelines[
            [
                "numero_processo",
                "numero_registro_stj",
                "timeline_event_count",
                "timeline_start",
                "timeline_end",
            ]
        ].drop_duplicates()
        selected = selected.merge(
            timeline_meta,
            on=["numero_processo", "numero_registro_stj"],
            how="left",
        )
    source_counts = build_source_counts(events)
    if not source_counts.empty:
        selected = selected.merge(
            source_counts,
            left_on="numero_processo",
            right_on="processo_agregacao",
            how="left",
        ).drop(columns=["processo_agregacao"])
    selected = add_text_counts(selected, documentos)
    selected = add_advogado_counts(selected, advogados)
    if args.only_linked and "n_documentos_corpus" in selected.columns:
        selected = selected[selected["n_documentos_corpus"].fillna(0).gt(0)]
    if args.only_with_text:
        selected = selected[selected["n_documentos_texto_disponiveis"].fillna(0).gt(0)]
    if args.numero_registro_stj:
        selected = selected[selected["numero_registro_stj"].astype("string").eq(args.numero_registro_stj)]
    if args.numero_processo:
        selected = selected[selected["numero_processo"].astype("string").eq(args.numero_processo)]
    if args.sort_by_text:
        selected = selected.sort_values("n_documentos_texto_disponiveis", ascending=False)
    if args.limit is not None:
        selected = selected.head(args.limit)

    jsonl_path = demo_dir / args.jsonl_name
    index_rows = []
    with jsonl_path.open("w", encoding="utf-8") as jsonl:
        for _, row in selected.iterrows():
            payload = build_process_json(
                row,
                partes,
                advogados,
                documentos,
                timelines,
                datajud_processos,
                datajud_assuntos,
                args,
            )
            stem = safe_file_stem(row)
            json_path = output_dir / f"{stem}.json"
            json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            jsonl.write(json.dumps(payload, ensure_ascii=False) + "\n")
            index_rows.append(
                {
                    "json_path": str(json_path),
                    "numero_processo": payload["processo"]["numero_processo"],
                    "numero_registro_stj": payload["processo"]["numero_registro_stj"],
                    "classe_stj": payload["processo"]["classe_stj"],
                    "classe_datajud": payload["processo"]["classe_datajud"],
                    "segmento_cnj": payload["processo"]["segmento_cnj"],
                    "tribunal_cnj": payload["processo"]["tribunal_cnj"],
                    "assunto_cnj_ata": payload["processo"]["assunto_cnj_ata"],
                    "ano_origem_cnj": payload["processo"]["ano_origem_cnj"],
                    "relator_ata_principal": payload["processo"]["relator_ata_principal"],
                    "n_partes": len(payload["partes"]),
                    "n_advogados": row_value(row, "n_advogados"),
                    "n_documentos": len(payload["documentos"]),
                    "n_documentos_texto_disponiveis": row_value(row, "n_documentos_texto_disponiveis"),
                    "n_eventos_timeline": len(payload["timeline"]),
                    "timeline_start": payload["metadados_pipeline"]["timeline_start"],
                    "timeline_end": payload["metadados_pipeline"]["timeline_end"],
                    "n_eventos_ata_stj": payload["metadados_pipeline"]["n_eventos_ata_stj"],
                    "n_eventos_datajud_stj": payload["metadados_pipeline"]["n_eventos_datajud_stj"],
                    "n_eventos_integra_stj": payload["metadados_pipeline"]["n_eventos_integra_stj"],
                    "tem_datajud": payload["datajud"]["status"] == "disponivel",
                    "tem_documentos_textuais": len(payload["documentos"]) > 0,
                    "fontes_timeline": " | ".join(payload["metadados_pipeline"]["timeline_sources"]),
                }
            )

    index = pd.DataFrame(index_rows)
    index_path = demo_dir / "processos_demo_index.csv"
    index.to_csv(index_path, index=False)

    print("Processed dir:", processed)
    print("Processes exported:", len(index))
    print("JSON dir:", output_dir)
    print("JSONL:", jsonl_path)
    print("Index:", index_path)


if __name__ == "__main__":
    main()
