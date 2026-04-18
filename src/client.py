import requests
from config import BASE_URL, TRIBUNAL_ALIAS, API_KEY, TIMEOUT

def post_search(payload: dict) -> dict:
    if not API_KEY:
        raise RuntimeError("DATAJUD_API_KEY não encontrada no .env")

    url = f"{BASE_URL}/{TRIBUNAL_ALIAS}/_search"
    headers = {
        "Authorization": f"APIKey {API_KEY}",
        "Content-Type": "application/json",
    }

    resp = requests.post(url, headers=headers, json=payload, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()