import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SARVAM_API_KEY")

if not API_KEY:
    raise RuntimeError("SARVAM_API_KEY not found in .env")

URL = "https://api.sarvam.ai/translate"


def translate_text(
    text: str,
    source_language: str,
    target_language: str
) -> str:

    headers = {
        "api-subscription-key": API_KEY,
        "Content-Type": "application/json",
    }

    data = {
        "input": text,
        "source_language_code": source_language,
        "target_language_code": target_language,
        "model": "mayura:v1",
    }

    last_error = None

    for attempt in range(3):

        try:
            response = requests.post(
                URL,
                headers=headers,
                json=data,
                timeout=30,
            )

            response.raise_for_status()

            result = response.json()

            return result["translated_text"]

        except requests.exceptions.RequestException as error:

            last_error = error

            if attempt < 2:
                time.sleep(2)

    raise RuntimeError(
        f"Sarvam translation failed after 3 attempts: {last_error}"
    )