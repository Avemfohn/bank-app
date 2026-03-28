"use client";
import { useState } from 'react';

export default function Home() {
  const [accountId, setAccountId] = useState('');
  const [amount, setAmount] = useState('10000');
  const [logs, setLogs] = useState<any>(null);

  // EKSİK OLAN KISIM BURASIYDI:
  const [note, setNote] = useState('');

  const launchAttack = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch('http://localhost:8000/api/transfer/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ account_id: accountId, amount: amount })
      });
      const data = await res.json();
      setLogs(data);
    } catch (error) {
      console.error("Attack failed to send:", error);
    }
  };

  const updateNote = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/update-note/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ account_id: accountId, note: note })
      });
      const data = await res.json();
      setLogs(data);
    } catch (error) {
      console.error("Note update failed:", error);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-zinc-950 text-white font-mono">
      <div className="z-10 max-w-2xl w-full border border-zinc-800 p-8 rounded-lg bg-zinc-900 shadow-2xl shadow-red-900/20">
        <h1 className="text-2xl font-bold mb-6 text-red-500">Project Aegis: XSS & SQLi Vector</h1>

        <form onSubmit={launchAttack} className="space-y-4">
          <div>
            <label className="block text-zinc-400 mb-2">Target Account ID (UUID):</label>
            <input
              type="text"
              value={accountId}
              onChange={(e) => setAccountId(e.target.value)}
              className="w-full bg-zinc-950 border border-zinc-700 p-3 rounded text-green-400 focus:outline-none focus:border-red-500"
              placeholder="Enter UUID..."
            />
          </div>

          <div>
            <label className="block text-zinc-400 mb-2">Amount to Drain:</label>
            <input
              type="number"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              className="w-full bg-zinc-950 border border-zinc-700 p-3 rounded text-green-400 focus:outline-none focus:border-red-500"
            />
          </div>

          <button type="submit" className="w-full bg-red-600 hover:bg-red-700 text-white font-bold py-3 px-4 rounded transition-colors">
            Execute SQL Query (Transfer)
          </button>
        </form>

        {/* XSS Vulnerability */}
        <div className="mt-6 border-t border-zinc-700 pt-6">
          <label className="block text-zinc-400 mb-2">Add/Update Account Note:</label>
          <textarea
            value={note}
            onChange={(e) => setNote(e.target.value)}
            className="w-full bg-zinc-950 border border-zinc-700 p-3 rounded text-green-400 mb-2 focus:outline-none focus:border-blue-500"
            placeholder="Write a note for your account..."
          />
          <button
            onClick={updateNote}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded transition-colors"
          >
            Save Note
          </button>

          {/* Vulnerable Render: Displaying incoming data as raw HTML */}
          {logs?.note && (
            <div className="mt-4 p-4 bg-zinc-800 border border-zinc-700 rounded">
              <h3 className="text-zinc-400 font-bold mb-2">Your Updated Note:</h3>
              <div className="text-white">
                {logs.note}
              </div>
            </div>
          )}
        </div>

        {logs && !logs.note && (
          <div className="mt-8 p-4 bg-black border border-zinc-800 rounded">
            <h3 className="text-zinc-500 mb-2">Server Response:</h3>
            <pre className="text-xs text-green-500 whitespace-pre-wrap break-all">
              {JSON.stringify(logs, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </main>
  );
}