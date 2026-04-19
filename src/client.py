import requests

from .config import BASE_URL, TIMEOUT, TRIBUNAL_ALIAS, require_api_key


def post_search(payload: dict) -> dict:
    api_key = require_api_key()

    url = f"{BASE_URL}/{TRIBUNAL_ALIAS}/_search"
    headers = {
        "Authorization": f"APIKey {api_key}",
        "Content-Type": "application/json",
    }

    resp = requests.post(url, headers=headers, json=payload, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()