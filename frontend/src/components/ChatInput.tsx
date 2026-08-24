"use client";

import { useRef, useState } from "react";

interface Props {
  onSend: (message: string, language: string) => void;
}

export default function ChatInput({ onSend }: Props) {
  const [input, setInput] = useState("");
  const [recording, setRecording] = useState(false);
  const [language, setLanguage] = useState("en");

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  async function startRecording() {
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

          setInput(data.text);
        } catch (error) {
          console.error("Speech-to-text error:", error);
        }
      };

      recorder.start();
      setRecording(true);
    } catch (error) {
      console.error("Microphone error:", error);
    }
  }

  function stopRecording() {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      setRecording(false);
    }
  }

  function handleMicClick() {
    if (recording) {
      stopRecording();
    } else {
      startRecording();
    }
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    if (!input.trim()) return;

    onSend(input, language);
    setInput("");
  }

  return (
    <div className="sticky bottom-0 w-full bg-[#F4F1EA] py-6">
      <form
        onSubmit={handleSubmit}
        className="mx-auto flex max-w-4xl items-center gap-3"
      >
        {/* Language selector */}
        <select
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
          className="
            rounded-full
            border
            border-stone-300
            bg-white
            px-4
            py-4
            text-stone-700
            shadow-sm
            focus:border-green-700
            outline-none
          "
        >
          <option value="en">🇬🇧 English</option>
          <option value="ta">🇮🇳 தமிழ்</option>
        </select>

        {/* Text input */}
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={
            language === "ta"
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
            focus:border-green-700
          "
        />

        {/* Microphone */}
        <button
          type="button"
          onClick={handleMicClick}
          className={`
            flex
            h-14
            w-14
            items-center
            justify-center
            rounded-full
            text-xl
            text-white
            transition
            ${
              recording
                ? "bg-red-600 hover:bg-red-700"
                : "bg-green-700 hover:bg-green-800"
            }
          `}
        >
          {recording ? "⏹" : "🎤"}
        </button>

        {/* Send */}
        <button
          type="submit"
          className="
            flex
            h-14
            w-14
            items-center
            justify-center
            rounded-full
            bg-green-700
            text-xl
            text-white
            transition
            hover:bg-green-800
          "
        >
          ➜
        </button>
      </form>
    </div>
  );
}