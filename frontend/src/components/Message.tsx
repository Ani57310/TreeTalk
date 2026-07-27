import { Message as MessageType } from "@/types/chat";

interface Props {
  message: MessageType;
}

export default function Message({ message }: Props) {
  const isUser = message.sender === "user";

  return (
    <div
      className={`mb-8 flex ${
        isUser ? "justify-end" : "justify-start"
      }`}
    >
      <div className="max-w-3xl">

        {!isUser && (
          <div className="mb-2 flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-full bg-green-700 text-white">
              🌳
            </div>

            <span className="font-semibold text-stone-700">
              TreeTalk
            </span>
          </div>
        )}

        <div
          className={`rounded-3xl px-6 py-4 shadow-sm ${
            isUser
              ? "bg-green-700 text-white"
              : "bg-white text-stone-800"
          }`}
        >
          <p className="whitespace-pre-wrap leading-7">
            {message.text}
          </p>

          {message.sources &&
            message.sources.length > 0 && (
              <div className="mt-5 border-t border-stone-200 pt-3">

                <p className="mb-2 text-sm font-semibold">
                  Sources
                </p>

                <ul className="list-disc pl-5 text-sm">
                  {message.sources.map((source) => (
                    <li key={source}>
                      {source}
                    </li>
                  ))}
                </ul>

              </div>
            )}
        </div>

      </div>
    </div>
  );
}