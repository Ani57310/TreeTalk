"use client";

import { useState } from "react";

interface Props {
  onSend: (message: string) => void;
}

export default function ChatInput({ onSend }: Props) {
  const [input, setInput] = useState("");

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    if (!input.trim()) return;

    onSend(input);
    setInput("");
  }

  return (
    <div className="sticky bottom-0 w-full bg-[#F4F1EA] py-6">
      <form
        onSubmit={handleSubmit}
        className="mx-auto flex max-w-4xl items-center gap-3"
      >
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask anything about trees..."
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