import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SARVAM_API_KEY")

if not API_KEY:
    raise RuntimeError("SARVAM_API_KEY not found in .env")

url = "https://api.sarvam.ai/translate"

headers = {
    "api-subscription-key": API_KEY,
    "Content-Type": "application/json",
}

data = {
    "input": "How often should I irrigate teak?",
    "source_language_code": "en-IN",
    "target_language_code": "ta-IN",
    "model": "mayura:v1",
}

response = requests.post(
    url,
    headers=headers,
    json=data,
)

print("Status:", response.status_code)
print("Response:", response.text)