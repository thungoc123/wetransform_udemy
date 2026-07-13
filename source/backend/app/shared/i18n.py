import json
import os

from fastapi import Request

LOCALES_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "locales")


def load_locales() -> dict[str, dict[str, str]]:
    locales: dict[str, dict[str, str]] = {}
    if not os.path.exists(LOCALES_DIR):
        return locales

    for filename in os.listdir(LOCALES_DIR):
        if filename.endswith(".json"):
            lang_code = filename.split(".")[0]
            with open(os.path.join(LOCALES_DIR, filename), encoding="utf-8") as f:
                locales[lang_code] = json.load(f)
    return locales


_translations = load_locales()


def t(request: Request, key: str, default: str = "") -> str:
    """Translate a key based on the Accept-Language header."""
    lang = request.headers.get("accept-language", "en").split(",")[0].split("-")[0]

    if lang not in _translations:
        lang = "en"

    return _translations.get(lang, {}).get(key, default or key)
