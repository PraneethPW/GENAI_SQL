import { useState } from "react";

interface QueryFormProps {
  onSubmit: (question: string) => void;
  loading: boolean;
}

export function QueryForm({ onSubmit, loading }: QueryFormProps) {
  const [question, setQuestion] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim()) return;
    onSubmit(question.trim());
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-3">
      <label className="block text-sm font-medium text-slate-200">
        Ask your database in plain English
      </label>
      <textarea
        className="w-full rounded-md bg-slate-900 border border-slate-700 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
        rows={3}
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="e.g. Show the total sales by month for 2024"
      />
      <button
        type="submit"
        disabled={loading}
        className="inline-flex items-center rounded-md bg-emerald-500 px-4 py-2 text-sm font-semibold text-white hover:bg-emerald-600 disabled:opacity-60"
      >
        {loading ? "Thinking..." : "Run query"}
      </button>
    </form>
  );
}
