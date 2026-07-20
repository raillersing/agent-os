export default function Home() {
  return (
    <main className="min-h-screen bg-gray-900 text-white">
      <div className="container mx-auto px-4 py-16">
        <h1 className="text-4xl font-bold mb-8">
          🚀 Agent OS — Mission Control
        </h1>
        <p className="text-xl text-gray-400 mb-8">
          Vendor-neutral orchestration, governance, and observability for AI agents
        </p>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="bg-gray-800 rounded-lg p-6">
            <h2 className="text-lg font-semibold mb-2">🤖 Agents</h2>
            <p className="text-gray-400">Manage your AI agents</p>
          </div>
          <div className="bg-gray-800 rounded-lg p-6">
            <h2 className="text-lg font-semibold mb-2">▶️ Runs</h2>
            <p className="text-gray-400">Monitor execution runs</p>
          </div>
          <div className="bg-gray-800 rounded-lg p-6">
            <h2 className="text-lg font-semibold mb-2">🧠 Memory</h2>
            <p className="text-gray-400">Manage agent memory</p>
          </div>
          <div className="bg-gray-800 rounded-lg p-6">
            <h2 className="text-lg font-semibold mb-2">🔧 Tools</h2>
            <p className="text-gray-400">Configure agent tools</p>
          </div>
        </div>
        <div className="mt-12">
          <a
            href="/docs"
            className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          >
            API Documentation →
          </a>
        </div>
      </div>
    </main>
  )
}
