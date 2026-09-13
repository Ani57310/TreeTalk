export default function Loading() {
  return (
    <div className="mb-8 flex justify-start">
      <div className="max-w-3xl">
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

        <div
          className="
            flex
            items-center
            gap-2
            rounded-3xl
            border
            border-stone-200
            bg-white
            px-6
            py-5
            shadow-sm
          "
        >
          <span className="text-sm text-stone-500">
            Thinking
          </span>

          <span className="flex gap-1">
            <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-stone-400 [animation-delay:-0.3s]" />
            <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-stone-400 [animation-delay:-0.15s]" />
            <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-stone-400" />
          </span>
        </div>
      </div>
    </div>
  );
}