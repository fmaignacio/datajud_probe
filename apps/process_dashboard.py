from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st


DEFAULT_PROCESSED_DIR = Path(os.getenv("DATAJUD_PROCESSED_DIR", "data/processed"))


st.set_page_config(
    page_title="STJ Processos",
    page_icon="⚖️",
    layout="wide",
)


def as_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float) and pd.isna(value):
        return ""
    return str(value)


def column_or_empty(frame: pd.DataFrame, column: str) -> pd.Series:
    if column in frame.columns:
        return frame[column]
    return pd.Series([""] * len(frame), index=frame.index, dtype="object")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_json_path(raw_path: Any, processed_dir: Path) -> Path:
    """Resolve JSON paths saved in Colab when the dashboard runs locally."""
    path_text = as_text(raw_path)
    path = Path(path_text).expanduser()
    if path.exists():
        return path

    # The demo index may contain absolute Colab paths such as
    # /content/drive/MyDrive/.../data/processed/process_json/<file>.json.
    # Locally, keep the filename and anchor it to the selected processed dir.
    fallback = processed_dir / "process_json" / path.name
    if fallback.exists():
        return fallback

    return path


@st.cache_data(show_spinner=False)
def load_index(index_path: str) -> pd.DataFrame:
    path = Path(index_path)
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def optional_filter(
    frame: pd.DataFrame,
    column: str,
    label: str,
    *,
    allow_multiple: bool = False,
) -> pd.DataFrame:
    if column not in frame.columns:
        return frame
    values = sorted(
        {
            as_text(value).strip()
            for value in frame[column].dropna().tolist()
            if as_text(value).strip() and as_text(value).strip().lower() != "nan"
        }
    )
    if not values:
        return frame
    if allow_multiple:
        selected = st.sidebar.multiselect(label, values)
        if selected:
            return frame[frame[column].astype(str).isin(selected)]
        return frame
    selected = st.sidebar.selectbox(label, ["Todos"] + values)
    if selected != "Todos":
        return frame[frame[column].astype(str).eq(selected)]
    return frame


def metric_row(processo: dict[str, Any], payload: dict[str, Any]) -> None:
    st.subheader("Resumo")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Registro STJ", as_text(processo.get("numero_registro_stj")) or "-")
    c2.metric("Classe", as_text(processo.get("classe_stj")) or "-")
    c3.metric("Partes", len(payload.get("partes", [])))
    c4.metric("Documentos", len(payload.get("documentos", [])))
    c5.metric("Eventos", as_text(payload.get("metadados_pipeline", {}).get("n_eventos_timeline")) or "-")


def show_process_header(payload: dict[str, Any]) -> None:
    processo = payload.get("processo", {})
    st.title("STJ Processos")
    st.caption("Vida útil processual no STJ com ATA, DataJud STJ, partes, advogados, documentos e timeline consolidada.")
    metric_row(processo, payload)

    cols = st.columns(2)
    with cols[0]:
        st.write("**Número CNJ**")
        st.code(as_text(processo.get("numero_processo")) or "-")
    with cols[1]:
        st.write("**Chave de agregação**")
        st.code(as_text(processo.get("chave_agregacao")) or "-")

    details = {
        "classe_stj": processo.get("classe_stj"),
        "classe_datajud": processo.get("classe_datajud"),
        "assunto_cnj_ata": processo.get("assunto_cnj_ata"),
        "ano_origem_cnj": processo.get("ano_origem_cnj"),
        "segmento_cnj": processo.get("segmento_cnj"),
        "tribunal_cnj": processo.get("tribunal_cnj"),
        "origem_cnj": processo.get("origem_cnj"),
        "relator_ata_principal": processo.get("relator_ata_principal"),
        "primeira_aparicao_corpus": processo.get("primeira_aparicao_corpus"),
        "anos_entre_origem_e_corpus": processo.get("anos_entre_origem_e_corpus"),
    }
    st.dataframe(pd.DataFrame([details]), use_container_width=True, hide_index=True)


def show_stj(payload: dict[str, Any]) -> None:
    st.subheader("STJ")
    stj = payload.get("stj", {})
    st.dataframe(pd.DataFrame([stj]), use_container_width=True, hide_index=True)


def show_datajud(payload: dict[str, Any]) -> None:
    st.subheader("DataJud STJ")
    datajud = payload.get("datajud", {})
    top = {
        "status": datajud.get("status"),
        "tribunal": datajud.get("tribunal"),
        "grau": datajud.get("grau"),
        "data_ajuizamento": datajud.get("data_ajuizamento"),
        "data_ultima_atualizacao": datajud.get("data_ultima_atualizacao"),
        "nivel_sigilo": datajud.get("nivel_sigilo"),
    }
    st.dataframe(pd.DataFrame([top]), use_container_width=True, hide_index=True)

    classe = datajud.get("classe") or {}
    orgao = datajud.get("orgao_julgador") or {}
    meta = {
        "classe_codigo": classe.get("codigo"),
        "classe_nome": classe.get("nome"),
        "orgao_julgador_codigo": orgao.get("codigo"),
        "orgao_julgador_nome": orgao.get("nome"),
    }
    st.dataframe(pd.DataFrame([meta]), use_container_width=True, hide_index=True)

    assuntos = datajud.get("assuntos") or []
    if assuntos:
        st.write("**Assuntos**")
        st.dataframe(pd.DataFrame(assuntos), use_container_width=True, hide_index=True)


def show_partes(payload: dict[str, Any]) -> None:
    st.subheader("Partes e Advogados")
    rows = []
    for parte in payload.get("partes", []):
        advogados = parte.get("advogados") or []
        rows.append(
            {
                "tipo": parte.get("tipo"),
                "nome": parte.get("nome"),
                "documento": parte.get("documento"),
                "advogados": "; ".join(
                    f"{adv.get('nome', '').strip()} ({adv.get('oab', '')})".strip()
                    for adv in advogados
                ),
            }
        )
    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.info("Sem partes carregadas para este processo.")


def show_timeline(payload: dict[str, Any]) -> None:
    st.subheader("Timeline")
    timeline = payload.get("timeline", [])
    if not timeline:
        st.info("Sem eventos na timeline.")
        return
    frame = pd.DataFrame(timeline)
    frame = prepare_timeline(frame)

    cols = st.columns([1, 1, 1, 1, 1])
    cols[0].metric("Eventos", len(frame))
    cols[1].metric("Data inicial", as_text(frame["event_date"].min()) or "-")
    cols[2].metric("Data final", as_text(frame["event_date"].max()) or "-")
    cols[3].metric("Fases", frame["fase_processual"].nunique())
    cols[4].metric("Decisórios", int(frame["eh_evento_decisorio"].sum()))

    filter_cols = st.columns([1, 1, 1, 1])
    with filter_cols[0]:
        if "event_source" in frame.columns:
            sources = sorted(frame["event_source"].dropna().astype(str).unique().tolist())
            selected_sources = st.multiselect("Fontes", sources, default=sources)
            if selected_sources:
                frame = frame[frame["event_source"].astype(str).isin(selected_sources)]
    with filter_cols[1]:
        phases = sorted(frame["fase_processual"].dropna().astype(str).unique().tolist())
        selected_phases = st.multiselect("Fases", phases, default=phases)
        if selected_phases:
            frame = frame[frame["fase_processual"].astype(str).isin(selected_phases)]
    with filter_cols[2]:
        only_decision = st.checkbox("Somente eventos decisórios")
        if only_decision:
            frame = frame[frame["eh_evento_decisorio"]]
    with filter_cols[3]:
        search_event = st.text_input("Busca livre na timeline")
        if search_event:
            combined_text = (
                frame["event_type_text"].fillna("")
                + " "
                + frame["event_description"].fillna("")
                + " "
                + frame["document_kind"].fillna("")
            )
            frame = frame[combined_text.str.contains(search_event, case=False, na=False)]

    if "event_dt" in frame.columns:
        frame = frame.sort_values("event_dt")
    st.dataframe(frame, use_container_width=True, hide_index=True)


def show_documentos(payload: dict[str, Any]) -> None:
    st.subheader("Documentos")
    documentos = payload.get("documentos", [])
    if not documentos:
        st.info("Sem documentos textuais neste JSON.")
        return

    doc_options = [
        f"{doc.get('data_documento', '-') or '-'} | {doc.get('tipo_documento', '-') or '-'} | {doc.get('seq_documento', '-')}"
        for doc in documentos
    ]
    selected_label = st.selectbox("Documento", doc_options)
    selected_doc = documentos[doc_options.index(selected_label)]

    meta_cols = st.columns(4)
    meta_cols[0].metric("SeqDocumento", as_text(selected_doc.get("seq_documento")) or "-")
    meta_cols[1].metric("Tipo", as_text(selected_doc.get("tipo_documento")) or "-")
    meta_cols[2].metric("Ministro", as_text(selected_doc.get("ministro")) or "-")
    meta_cols[3].metric("Palavras", as_text(selected_doc.get("n_words_limpo")) or "-")

    st.write("**Texto limpo**")
    text = as_text(selected_doc.get("texto_limpo"))
    if text:
        st.text_area("Texto", text, height=420, label_visibility="collapsed")
    else:
        st.info("Este documento não tem texto no JSON carregado.")


def show_raw(payload: dict[str, Any]) -> None:
    with st.expander("JSON bruto"):
        st.json(payload)


def phase_from_text(text: str) -> str:
    lowered = text.lower()
    if any(token in lowered for token in ("distrib", "autua", "registro", "cadastr")):
        return "01 - Registro/Distribuição"
    if any(token in lowered for token in ("juntad", "peti", "exped", "protoc")):
        return "02 - Instrução/Tramitação"
    if any(token in lowered for token in ("relator", "conclus", "voto", "sess", "pauta")):
        return "03 - Relatoria/Julgamento"
    if any(token in lowered for token in ("acórd", "decis", "senten", "homolog", "baixa")):
        return "04 - Decisão/Encerramento"
    return "99 - Outros"


def is_decision_event(text: str) -> bool:
    lowered = text.lower()
    markers = (
        "acórd",
        "acordao",
        "decis",
        "julg",
        "senten",
        "homolog",
        "trânsito",
        "transito",
        "baixa",
    )
    return any(marker in lowered for marker in markers)


def prepare_timeline(frame: pd.DataFrame) -> pd.DataFrame:
    local = frame.copy()
    local["event_datetime"] = column_or_empty(local, "event_datetime").astype(str)
    local["event_date"] = local["event_datetime"].str[:10]
    local["event_dt"] = pd.to_datetime(local["event_datetime"], errors="coerce", utc=True)
    local["event_text_join"] = (
        column_or_empty(local, "event_type_text").fillna("").astype(str)
        + " "
        + column_or_empty(local, "event_description").fillna("").astype(str)
        + " "
        + column_or_empty(local, "document_kind").fillna("").astype(str)
    ).str.strip()
    local["event_type_text"] = column_or_empty(local, "event_type_text").fillna("").astype(str)
    local["event_description"] = column_or_empty(local, "event_description").fillna("").astype(str)
    local["document_kind"] = column_or_empty(local, "document_kind").fillna("").astype(str)
    local["event_source"] = column_or_empty(local, "event_source").fillna("").astype(str)
    local["fase_processual"] = local["event_text_join"].map(phase_from_text)
    local["eh_evento_decisorio"] = local["event_text_join"].map(is_decision_event)
    return local


def show_vida_util(payload: dict[str, Any]) -> None:
    st.subheader("Vida útil detalhada do processo")
    timeline = payload.get("timeline", [])
    if not timeline:
        st.info("Sem timeline para reconstruir a vida útil.")
        return

    frame = prepare_timeline(pd.DataFrame(timeline)).sort_values("event_dt")
    frame_non_null = frame[frame["event_dt"].notna()].copy()
    if frame_non_null.empty:
        st.warning("Os eventos não possuem data válida para cálculo da vida útil.")
        return

    first_event = frame_non_null.iloc[0]
    decision_events = frame_non_null[frame_non_null["eh_evento_decisorio"]]
    last_event = frame_non_null.iloc[-1]
    decision_anchor = decision_events.iloc[-1] if not decision_events.empty else last_event

    cycle_days = int((decision_anchor["event_dt"] - first_event["event_dt"]).days)
    cols = st.columns(5)
    cols[0].metric("Primeiro registro", as_text(first_event["event_date"]))
    cols[1].metric("Marco decisório", as_text(decision_anchor["event_date"]))
    cols[2].metric("Dias até decisão", cycle_days if cycle_days >= 0 else "-")
    cols[3].metric("Eventos no ciclo", len(frame_non_null))
    cols[4].metric("Eventos decisórios", len(decision_events))

    st.write("**Linha do tempo por fase (do primeiro registro ao marco decisório)**")
    cycle_slice = frame_non_null[
        (frame_non_null["event_dt"] >= first_event["event_dt"])
        & (frame_non_null["event_dt"] <= decision_anchor["event_dt"])
    ].copy()
    phase_summary = (
        cycle_slice.groupby("fase_processual", dropna=False)
        .agg(
            eventos=("event_datetime", "count"),
            primeiro_evento=("event_date", "min"),
            ultimo_evento=("event_date", "max"),
            fontes=("event_source", lambda s: ", ".join(sorted(set(s.dropna().astype(str))))),
        )
        .reset_index()
        .sort_values("fase_processual")
    )
    st.dataframe(phase_summary, use_container_width=True, hide_index=True)

    st.write("**Eventos críticos do ciclo**")
    critical = cycle_slice[
        cycle_slice["eh_evento_decisorio"]
        | cycle_slice["fase_processual"].isin(
            ["01 - Registro/Distribuição", "03 - Relatoria/Julgamento", "04 - Decisão/Encerramento"]
        )
    ].copy()
    keep_cols = [
        "event_datetime",
        "event_source",
        "fase_processual",
        "event_type_text",
        "event_description",
        "document_kind",
    ]
    show_cols = [col for col in keep_cols if col in critical.columns]
    st.dataframe(critical[show_cols], use_container_width=True, hide_index=True)


def main() -> None:
    st.sidebar.title("Dados")
    processed_dir = Path(
        st.sidebar.text_input("Pasta processed", value=str(DEFAULT_PROCESSED_DIR))
    ).expanduser()
    index_path = processed_dir / "demo" / "processos_demo_index.csv"
    index = load_index(str(index_path))

    st.sidebar.caption(f"Índice: `{index_path}`")
    if index.empty:
        st.warning("Índice de demonstração não encontrado ou vazio.")
        st.code(
            "python scripts/build_process_json.py "
            "--data-root /caminho/para/data --only-linked --only-with-text --sort-by-text --limit 20"
        )
        return

    search = st.sidebar.text_input("Buscar registro STJ ou CNJ")
    filtered = index.copy()
    if search:
        mask = (
            filtered.get("numero_registro_stj", pd.Series("", index=filtered.index))
            .astype(str)
            .str.contains(search, case=False, na=False)
            | filtered.get("numero_processo", pd.Series("", index=filtered.index))
            .astype(str)
            .str.contains(search, case=False, na=False)
        )
        filtered = filtered[mask]

    st.sidebar.divider()
    st.sidebar.subheader("Filtros")
    filtered = optional_filter(filtered, "classe_stj", "Classe STJ")
    filtered = optional_filter(filtered, "classe_datajud", "Classe DataJud")
    filtered = optional_filter(filtered, "segmento_cnj", "Segmento CNJ")
    filtered = optional_filter(filtered, "tribunal_cnj", "Tribunal CNJ")
    filtered = optional_filter(filtered, "relator_ata_principal", "Relator ATA")
    filtered = optional_filter(filtered, "ano_origem_cnj", "Ano de origem")
    filtered = optional_filter(filtered, "assunto_cnj_ata", "Assunto CNJ")
    filtered = optional_filter(filtered, "fontes_timeline", "Fonte na timeline", allow_multiple=True)

    if "n_eventos_timeline" in filtered.columns and not filtered["n_eventos_timeline"].dropna().empty:
        max_events = int(filtered["n_eventos_timeline"].dropna().max())
        min_events = st.sidebar.slider("Mínimo de eventos na timeline", 0, max_events, 0)
        filtered = filtered[filtered["n_eventos_timeline"].fillna(0) >= min_events]

    if "n_documentos_texto_disponiveis" in filtered.columns and not filtered["n_documentos_texto_disponiveis"].dropna().empty:
        max_docs = int(filtered["n_documentos_texto_disponiveis"].dropna().max())
        min_docs = st.sidebar.slider("Mínimo de documentos com texto", 0, max_docs, 0)
        filtered = filtered[filtered["n_documentos_texto_disponiveis"].fillna(0) >= min_docs]

    if "tem_datajud" in filtered.columns:
        only_datajud = st.sidebar.checkbox("Somente com DataJud")
        if only_datajud:
            filtered = filtered[filtered["tem_datajud"].fillna(False)]
    if "tem_documentos_textuais" in filtered.columns:
        only_text = st.sidebar.checkbox("Somente com documentos textuais")
        if only_text:
            filtered = filtered[filtered["tem_documentos_textuais"].fillna(False)]

    if filtered.empty:
        st.warning("Nenhum processo encontrado para o filtro.")
        return

    with st.sidebar.expander("Campos disponíveis no índice"):
        st.write(sorted(filtered.columns.tolist()))

    label_map = {}
    for row in filtered.itertuples(index=False):
        label = (
            f"{row.numero_registro_stj} | {row.numero_processo} | "
            f"classe={getattr(row, 'classe_stj', '-') or '-'} | "
            f"docs={row.n_documentos} | eventos={getattr(row, 'n_eventos_timeline', '-')}"
        )
        label_map[label] = resolve_json_path(row.json_path, processed_dir)
    selected = st.sidebar.selectbox("Processo", list(label_map))
    json_path = label_map[selected]
    if not json_path.exists():
        st.error("JSON do processo não encontrado.")
        st.code(str(json_path))
        st.info("Confira se a pasta process_json foi sincronizada para o Google Drive for Desktop.")
        return

    payload = load_json(json_path)

    show_process_header(payload)

    tabs = st.tabs(["Vida útil", "Timeline", "Partes", "Documentos", "STJ", "DataJud", "JSON"])
    with tabs[0]:
        show_vida_util(payload)
    with tabs[1]:
        show_timeline(payload)
    with tabs[2]:
        show_partes(payload)
    with tabs[3]:
        show_documentos(payload)
    with tabs[4]:
        show_stj(payload)
    with tabs[5]:
        show_datajud(payload)
    with tabs[6]:
        show_raw(payload)


if __name__ == "__main__":
    main()
