import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

load_dotenv()

client = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY")
)

audio = client.text_to_speech.convert(
    text="In the initial stage, teak plants need to be watered weekly.",
    voice_id="6hdbJqwWGxXDZDEK7Yqa",
    model_id="eleven_multilingual_v2",
    output_format="mp3_44100_128",
)

with open("test_output.mp3", "wb") as f:
    for chunk in audio:
        f.write(chunk)

print("Audio generated successfully!")