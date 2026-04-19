from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

BASE_URL = "https://api-publica.datajud.cnj.jus.br"
TRIBUNAL_ALIAS = "api_publica_stj"
API_KEY = os.getenv("DATAJUD_API_KEY")
TIMEOUT = 60

RAW_DIR = Path("data/raw")
REPORT_DIR = Path("data/reports")
RAW_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def require_api_key() -> str:
    if not API_KEY:
        raise RuntimeError("DATAJUD_API_KEY nao encontrada no arquivo .env")
    return API_KEY
