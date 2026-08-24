from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import UploadFile, File
from fastapi import Response
import os
import requests

from src.chatbot import answer_question

app = FastAPI(title="TreeTalk API")


# Allow the Next.js frontend to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]


@app.get("/")
def root():
    return {
        "message": "🌳 TreeTalk API is running!"
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    answer, docs = answer_question(request.message)

    seen = set()
    sources = []

    for doc in docs:

        tree = doc.metadata["tree"]

        if tree not in seen:

            seen.add(tree)
            sources.append(tree)

    return ChatResponse(
        answer=answer,
        sources=sources,
    )

@app.post("/speech-to-text")
async def speech_to_text(file: UploadFile = File(...),language_code:str="en",):
    audio = await file.read()

    temp_path = "temp_audio.m4a"

    with open(temp_path, "wb") as f:
        f.write(audio)

    try:
        with open(temp_path, "rb") as audio_file:
            response = requests.post(
                "https://api.elevenlabs.io/v1/speech-to-text",
                headers={
                    "xi-api-key": os.getenv("ELEVENLABS_API_KEY")
                },
                files={
                    "file": audio_file
                },
                data={
                    "model_id": "scribe_v2",
                    "language_code":language_code,
                },
                timeout=60
            )

        response.raise_for_status()

        result = response.json()

        return {
            "text": result["text"]
        }

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)



@app.post("/text-to-speech")
async def text_to_speech(request: dict):
    text = request.get("text")

    if not text:
        return {"error": "Text is required"}

    from elevenlabs.client import ElevenLabs

    client = ElevenLabs(
        api_key=os.getenv("ELEVENLABS_API_KEY")
    )

    audio = client.text_to_speech.convert(
        text=text,
        voice_id=os.getenv("ELEVENLABS_VOICE_ID"),
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )

    audio_data = b"".join(audio)

    return Response(
        content=audio_data,
        media_type="audio/mpeg"
    )



print("\n=== REGISTERED ROUTES ===")
for route in app.routes:
    print(route.path, route.methods)
print("=========================\n")