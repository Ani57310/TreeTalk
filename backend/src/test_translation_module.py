from src.translation import translate_text


text = "How often should I irrigate teak?"

translated = translate_text(
    text,
    "en-IN",
    "ta-IN"
)

print("English:", text)
print("Tamil:", translated)