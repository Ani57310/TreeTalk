"use client";

import { useState } from "react";

import Header from "./Header";
import Message from "./Message";
import ChatInput from "./ChatInput";
import Loading from "./Loading";
import Welcome from "./Welcome";

import { Message as MessageType } from "@/types/chat";

export default function Chat() {
  const [messages, setMessages] = useState<MessageType[]>([]);
  const [loading, setLoading] = useState(false);

  async function handleSend(text: string, language: string) {
    const userMessage: MessageType = {
      id: crypto.randomUUID(),
      sender: "user",
      text,
    };

    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: text,
        }),
      });

      const data = await response.json();

      const botMessage: MessageType = {
        id: crypto.randomUUID(),
        sender: "bot",
        text: data.answer,
        sources: data.sources,
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      const botMessage: MessageType = {
        id: crypto.randomUUID(),
        sender: "bot",
        text: "⚠️ Unable to reach the TreeTalk backend.",
      };

      setMessages((prev) => [...prev, botMessage]);

      console.error(error);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex min-h-screen flex-col">
      <Header />

      <div className="mx-auto flex w-full max-w-5xl flex-1 flex-col px-6">
        {messages.length === 0 ? (
          <Welcome  onSend={handleSend} />
        ) : (
          <>
            <div className="flex-1 py-8">
              {messages.map((message) => (
                <Message key={message.id} message={message} />
              ))}

              {loading && <Loading />}
            </div>
          </>
        )}
      </div>

      <ChatInput onSend={handleSend} />
    </div>
  );
}