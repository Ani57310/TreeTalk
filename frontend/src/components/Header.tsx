export default function Header() {
  return (
    <div className="flex flex-col items-center gap-3 py-10">

      <div className="text-6xl">
        🌳
      </div>

      <h1 className="text-4xl font-bold text-stone-800">
        TreeTalk
      </h1>

      <p className="text-center text-stone-500 max-w-xl">

        AI Assistant for IFGTB TreeGenie

      </p>

      <p className="text-center text-stone-500 max-w-xl">

        Ask about cultivation, irrigation, diseases,
        windbreaks and plantation management.

      </p>

    </div>
  );
}