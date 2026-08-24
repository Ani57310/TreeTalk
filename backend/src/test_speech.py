import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ELEVENLABS_API_KEY")

if not API_KEY:
    raise RuntimeError("ELEVENLABS_API_KEY not found in .env")

url = "https://api.elevenlabs.io/v1/speech-to-text"

headers = {
    "xi-api-key": API_KEY,
}

with open("tamil3.m4a", "rb") as audio_file:

    files = {
        "file": audio_file,
    }

    data = {
        "model_id": "scribe_v2",
        "language_code":"ta",
    }

    response = requests.post(
        url,
        headers=headers,
        files=files,
        data=data,
        timeout=60,
    )

print("Status:", response.status_code)
print("Response:", response.text)