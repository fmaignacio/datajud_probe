import json
from collections import Counter

from client import post_search
from queries import query_basica, query_exists, query_grau, query_grau_exists
from config import RAW_DIR, REPORT_DIR

FIELDS_TO_CHECK = [
    "numeroProcesso",
    "classe",
    "assuntos",
    "orgaoJulgador",
    "grau",
    "movimentos",
    "dataAjuizamento",
    "dataJulgamento",
    "dataPublicacao",
    "relator",
    "txtEmenta",
    "txtDecisao",
    "txtObservacao",
    "tipoDecisao",
    "resultadoJulgamento",
    "valorCausa",
]

# TESTS = [
#     ("tjsp_basica", query_basica(size=20)),
#     ("tjsp_g2", query_grau("G2", size=20)),
#     ("tjsp_relator", query_exists("relator", size=20)),
#     ("tjsp_data_publicacao", query_exists("dataPublicacao", size=20)),
#     ("tjsp_txtementa", query_exists("txtEmenta", size=20)),
#     ("tjsp_txtdecisao", query_exists("txtDecisao", size=20)),
#     ("tjsp_g2_txtementa", query_grau_exists("G2", "txtEmenta", size=20)),
# ]

TESTS = [
    ("stj_basica", query_basica(size=20)),
    ("stj_relator", query_exists("relator", size=20)),
    ("stj_data_publicacao", query_exists("dataPublicacao", size=20)),
    ("stj_txtementa", query_exists("txtEmenta", size=20)),
    ("stj_txtdecisao", query_exists("txtDecisao", size=20)),
]

def has_value(v):
    if v is None:
        return False
    if isinstance(v, str) and not v.strip():
        return False
    if isinstance(v, (list, dict)) and len(v) == 0:
        return False
    return True

def run_one_test(test_name: str, payload: dict):
    result = post_search(payload)

    raw_file = RAW_DIR / f"{test_name}_raw.json"
    report_file = REPORT_DIR / f"{test_name}_summary.json"

    raw_file.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    hits = result.get("hits", {}).get("hits", [])
    coverage = Counter()
    grau_counter = Counter()

    for hit in hits:
        source = hit.get("_source", {})
        grau = source.get("grau")
        if grau:
            grau_counter[grau] += 1

        for field in FIELDS_TO_CHECK:
            if has_value(source.get(field)):
                coverage[field] += 1

    summary = {
        "test_name": test_name,
        "total_retornado": len(hits),
        "distribuicao_grau": dict(grau_counter),
        "campos_verificados": FIELDS_TO_CHECK,
        "cobertura_absoluta": dict(coverage),
        "cobertura_percentual": {
            k: round(v / len(hits), 4) if hits else 0
            for k, v in coverage.items()
        }
    }

    report_file.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"[OK] {test_name}: {len(hits)} hits")
    return {
        "test_name": test_name,
        "hits": len(hits),
        "graus": dict(grau_counter),
        "campos_com_cobertura": list(coverage.keys()),
    }

def main():
    final_report = []

    for test_name, payload in TESTS:
        try:
            output = run_one_test(test_name, payload)
            final_report.append(output)
        except Exception as e:
            print(f"[ERRO] {test_name}: {e}")
            final_report.append({
                "test_name": test_name,
                "erro": str(e),
            })

    consolidated_file = REPORT_DIR / "consolidated_report.json"
    consolidated_file.write_text(
        json.dumps(final_report, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("\nResumo consolidado:")
    for item in final_report:
        print(item)

if __name__ == "__main__":
    main()