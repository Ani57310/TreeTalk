export default function Welcome() {
  return (
    <div className="flex flex-1 flex-col items-center justify-center py-20">

      <div className="mb-6 text-7xl">
        🌳
      </div>

      <h1 className="mb-3 text-5xl font-bold text-stone-800">
        TreeTalk
      </h1>

      <p className="mb-10 text-center text-lg text-stone-500">
        AI Assistant for IFGTB TreeGenie
      </p>

      <div className="grid gap-4 text-center text-stone-700 md:grid-cols-2">

        <div className="rounded-2xl bg-white px-8 py-5 shadow-sm">
          🌱 <strong>Cultivation</strong>
        </div>

        <div className="rounded-2xl bg-white px-8 py-5 shadow-sm">
          💧 <strong>Irrigation</strong>
        </div>

        <div className="rounded-2xl bg-white px-8 py-5 shadow-sm">
          🌿 <strong>Diseases</strong>
        </div>

        <div className="rounded-2xl bg-white px-8 py-5 shadow-sm">
          🌳 <strong>Windbreak</strong>
        </div>

      </div>

      <p className="mt-10 text-center text-stone-500">
        Ask anything about trees to get started.
      </p>

    </div>
  );
}