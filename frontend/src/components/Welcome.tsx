interface Props {
  onSend: (message: string, language: string) => void;
}

export default function Welcome({ onSend }: Props) {
  const suggestions = [
    {
      icon: "🌱",
      title: "Cultivation",
      question: "What are the best practices for cultivating trees?",
    },
    {
      icon: "💧",
      title: "Irrigation",
      question: "How should trees be irrigated?",
    },
    {
      icon: "🌿",
      title: "Diseases",
      question: "What are some common diseases that affect trees?",
    },
    {
      icon: "🌳",
      title: "Windbreak",
      question: "Which trees are suitable for use as windbreaks?",
    },
  ];

  return (
    <div className="flex flex-1 flex-col items-center justify-center py-16">

      <div className="mb-5 text-7xl">🌳</div>

      <h1 className="mb-3 text-center text-5xl font-bold text-stone-800">
        TreeTalk
      </h1>

      <p className="mb-3 text-center text-lg text-stone-500">
        AI Assistant for IFGTB TreeGenie
      </p>

      <p className="mb-10 max-w-xl px-4 text-center text-stone-500">
        Ask questions about trees, cultivation, irrigation, diseases,
        windbreaks, and more — in English or Tamil.
      </p>

      <div className="grid w-full max-w-2xl gap-4 px-4 md:grid-cols-2">
        {suggestions.map((suggestion) => (
          <button
            key={suggestion.title}
            type="button"
            onClick={() => onSend(suggestion.question, "en")}
            className="
              rounded-2xl
              border
              border-stone-200
              bg-white
              px-6
              py-5
              text-left
              shadow-sm
              transition
              hover:-translate-y-0.5
              hover:border-green-700
              hover:shadow-md
              active:translate-y-0
            "
          >
            <div className="mb-2 text-2xl">
              {suggestion.icon}
            </div>

            <div className="font-semibold text-stone-800">
              {suggestion.title}
            </div>

            <div className="mt-1 text-sm text-stone-500">
              {suggestion.question}
            </div>
          </button>
        ))}
      </div>

      <p className="mt-10 text-center text-sm text-stone-400">
        Choose a question above or ask anything about trees below.
      </p>

    </div>
  );
}