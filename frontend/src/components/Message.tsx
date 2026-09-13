"use client";

import { useState } from "react";

import { Message as MessageType } from "@/types/chat";

interface Props {
  message: MessageType;
}

export default function Message({ message }: Props) {
  const isUser = message.sender === "user";
  const [playing, setPlaying] = useState(false);

  async function playAudio() {
    try {
      setPlaying(true);

      const response = await fetch(
        "http://127.0.0.1:8000/text-to-speech",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            text: message.text,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Text-to-speech request failed");
      }

      const audioBlob = await response.blob();
      const audioUrl = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrl);

      audio.onended = () => {
        setPlaying(false);
        URL.revokeObjectURL(audioUrl);
      };

      audio.onerror = () => {
        setPlaying(false);
        URL.revokeObjectURL(audioUrl);
      };

      await audio.play();
    } catch (error) {
      console.error("Text-to-speech error:", error);
      setPlaying(false);
    }
  }

  return (
    <div
      className={`mb-8 flex ${
        isUser ? "justify-end" : "justify-start"
      }`}
    >
      <div
        className={`w-full ${
          isUser ? "max-w-2xl" : "max-w-3xl"
        }`}
      >
        {!isUser && (
          <div className="mb-2 flex items-center gap-2">
            <div
              className="
                flex h-8 w-8 items-center justify-center
                rounded-full
                bg-green-700
                text-sm
                text-white
                shadow-sm
              "
            >
              🌳
            </div>

            <span className="font-semibold text-stone-700">
              TreeTalk
            </span>
          </div>
        )}

        <div
          className={`rounded-3xl px-6 py-5 shadow-sm ${
            isUser
              ? "bg-green-700 text-white"
              : "border border-stone-200 bg-white text-stone-800"
          }`}
        >
          <p className="whitespace-pre-wrap text-[15px] leading-7">
            {message.text}
          </p>

          {!isUser && (
            <div className="mt-5">
              <button
                type="button"
                onClick={playAudio}
                disabled={playing}
                aria-label={
                  playing
                    ? "Playing response"
                    : "Listen to response"
                }
                className="
                  inline-flex
                  items-center
                  gap-2
                  rounded-full
                  bg-green-700
                  px-4
                  py-2
                  text-sm
                  font-medium
                  text-white
                  shadow-sm
                  transition
                  hover:bg-green-800
                  hover:shadow
                  focus:outline-none
                  focus:ring-2
                  focus:ring-green-700
                  focus:ring-offset-2
                  disabled:cursor-default
                  disabled:opacity-60
                "
              >
                {playing ? (
                  <>
                    <span className="animate-pulse">🔊</span>
                    Playing...
                  </>
                ) : (
                  <>
                    🔊
                    Listen
                  </>
                )}
              </button>
            </div>
          )}

          {message.sources && message.sources.length > 0 && (
            <div className="mt-6 border-t border-stone-200 pt-4">
              <p className="mb-3 text-sm font-semibold text-stone-700">
                Sources
              </p>

              <div className="flex flex-wrap gap-2">
                {message.sources.map((source) => (
                  <span
                    key={source}
                    className="
                      rounded-full
                      bg-stone-100
                      px-3
                      py-1.5
                      text-sm
                      text-stone-600
                    "
                  >
                    🌳 {source}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}