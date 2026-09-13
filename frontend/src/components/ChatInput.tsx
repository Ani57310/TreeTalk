"use client";

import { useRef, useState } from "react";

interface Props {
  onSend: (message: string, language: string) => void;
}

export default function ChatInput({ onSend }: Props) {
  const [input, setInput] = useState("");
  const [recording, setRecording] = useState(false);
  const [transcribing, setTranscribing] = useState(false);
  const [error, setError] = useState("");

  const [language, setLanguage] = useState("en");

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  async function startRecording() {
    if (transcribing) return;

    setError("");

    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: true,
      });

      const recorder = new MediaRecorder(stream);

      mediaRecorderRef.current = recorder;
      audioChunksRef.current = [];

      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      recorder.onstop = async () => {
        stream.getTracks().forEach((track) => track.stop());

        const audioBlob = new Blob(audioChunksRef.current, {
          type: recorder.mimeType,
        });

        const formData = new FormData();
        formData.append("file", audioBlob, "recording.webm");

        setTranscribing(true);

        try {
          const response = await fetch(
            `http://127.0.0.1:8000/speech-to-text?language_code=${language}`,
            {
              method: "POST",
              body: formData,
            }
          );

          if (!response.ok) {
            throw new Error("Speech-to-text request failed");
          }

          const data = await response.json();

          if (!data.text || !data.text.trim()) {
            throw new Error("No speech was detected");
          }

          setInput(data.text);
        } catch (error) {
          console.error("Speech-to-text error:", error);

          setError(
            "⚠️ Could not understand the recording. Please try again."
          );
        } finally {
          setTranscribing(false);
        }
      };

      recorder.start();
      setRecording(true);
    } catch (error) {
      console.error("Microphone error:", error);

      setError(
        "⚠️ Microphone access failed. Please allow microphone access and try again."
      );
    }
  }

  function stopRecording() {
    if (mediaRecorderRef.current && recording) {
      mediaRecorderRef.current.stop();
      setRecording(false);
    }
  }

  function handleMicClick() {
    if (transcribing) return;

    if (recording) {
      stopRecording();
    } else {
      startRecording();
    }
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    if (!input.trim() || transcribing || recording) return;

    onSend(input, language);
    setInput("");
    setError("");
  }

  return (
    <div className="sticky bottom-0 w-full bg-[#F4F1EA] py-6">
      <form
        onSubmit={handleSubmit}
        className="mx-auto flex max-w-4xl flex-col gap-2 px-4"
      >
        <div className="flex items-center gap-3">
          <select
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            disabled={recording || transcribing}
            className="
              rounded-full
              border
              border-stone-300
              bg-white
              px-4
              py-4
              text-stone-700
              shadow-sm
              outline-none
              focus:border-green-700
              disabled:cursor-not-allowed
              disabled:opacity-60
            "
          >
            <option value="en">🇬🇧 English</option>
            <option value="ta">🇮🇳 தமிழ்</option>
          </select>

          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={recording || transcribing}
            placeholder={
              transcribing
                ? "Transcribing..."
                : language === "ta"
                ? "மரங்களைப் பற்றி கேளுங்கள்..."
                : "Ask anything about trees..."
            }
            className="
              flex-1
              rounded-full
              border
              border-stone-300
              bg-white
              px-6
              py-4
              text-stone-700
              shadow-sm
              outline-none
              focus:border-green-700
              disabled:cursor-not-allowed
              disabled:bg-stone-100
            "
          />

          <button
            type="button"
            onClick={handleMicClick}
            disabled={transcribing}
            className={`
              flex
              h-14
              w-14
              shrink-0
              items-center
              justify-center
              rounded-full
              text-xl
              text-white
              transition
              disabled:cursor-not-allowed
              disabled:opacity-60
              ${
                recording
                  ? "bg-red-600 hover:bg-red-700"
                  : "bg-green-700 hover:bg-green-800"
              }
            `}
          >
            {transcribing ? "⏳" : recording ? "⏹" : "🎤"}
          </button>

          <button
            type="submit"
            disabled={!input.trim() || recording || transcribing}
            className="
              flex
              h-14
              w-14
              shrink-0
              items-center
              justify-center
              rounded-full
              bg-green-700
              text-xl
              text-white
              transition
              hover:bg-green-800
              disabled:cursor-not-allowed
              disabled:opacity-50
            "
          >
            ➜
          </button>
        </div>

        {(recording || transcribing || error) && (
          <div className="px-4 text-sm text-stone-600">
            {recording && "🔴 Recording... Click ⏹ when you're finished."}

            {transcribing && "⏳ Transcribing your recording..."}

            {error && !recording && !transcribing && (
              <span className="text-red-700">{error}</span>
            )}
          </div>
        )}
      </form>
    </div>
  );
}