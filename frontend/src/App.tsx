import { useState } from "react";
import axios from "axios";
import { QueryForm } from "./components/QueryForm";
import { ResultsTable } from "./components/ResultsTable";

// Prefer env var, but safely fall back to your Railway URL
const API_BASE_URL =
  (import.meta.env.VITE_API_BASE_URL as string | undefined) ??
  "https://web-production-62235.up.railway.app";

interface QueryResponse {
  sql: string;
  columns: string[];
  rows: string[][];
}

function App() {
  const [loading, setLoading] = useState(false);
  const [sql, setSql] = useState<string | null>(null);
  const [columns, setColumns] = useState<string[]>([]);
  const [rows, setRows] = useState<string[][]>([]);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (question: string) => {
    setLoading(true);
    setError(null);
    setSql(null);
    setColumns([]);
    setRows([]);

    try {
      const res = await axios.post<QueryResponse>(
        `${API_BASE_URL}/api/query`,
        { question },
      );
      setSql(res.data.sql);
      setColumns(res.data.columns);
      setRows(res.data.rows);
    } catch (err: any) {
      const detail = err?.response?.data?.detail ?? "Something went wrong.";
      setError(String(detail));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative min-h-screen overflow-hidden bg-slate-950 text-slate-50">
      {/* Animated gradient background */}
      <div className="pointer-events-none absolute inset-0 -z-10 bg-[radial-gradient(circle_at_top,_#22d3ee_0,_transparent_55%),radial-gradient(circle_at_bottom,_#6366f1_0,_transparent_55%)] animate-[gradient-shift_18s_ease_infinite] opacity-80" />

      {/* Floating blobs */}
      <div className="pointer-events-none absolute -left-32 top-10 h-72 w-72 rounded-full bg-cyan-500/20 blur-3xl" />
      <div className="pointer-events-none absolute -right-20 bottom-0 h-80 w-80 rounded-full bg-indigo-500/25 blur-3xl" />

      {/* Main content */}
      <div className="relative flex min-h-screen items-center justify-center px-4 py-10">
        <div className="mx-auto w-full max-w-4xl space-y-8">
          {/* Header / hero */}
          <header className="space-y-4 text-center">
            <p className="inline-flex items-center gap-2 rounded-full border border-cyan-400/40 bg-slate-900/60 px-4 py-1 text-xs font-medium uppercase tracking-[0.25em] text-cyan-200/80 backdrop-blur-md">
              AI + SQL + Neon
            </p>

            <h1 className="text-balance text-3xl font-semibold tracking-tight text-slate-50 sm:text-4xl md:text-5xl">
              GENAI SQL – Natural language to Postgres
            </h1>

            <p className="mx-auto max-w-xl text-sm text-slate-300/80 sm:text-base">
              Ask your database in plain English and get runnable SQL with live
              results from your Neon instance.
            </p>

            {/* Quote block */}
            <div className="mx-auto flex max-w-xl items-center justify-between gap-3 rounded-2xl border border-slate-700/60 bg-slate-900/70 px-4 py-3 text-left text-xs text-slate-300/80 backdrop-blur-md sm:text-sm">
              <p className="italic">
                “Data is the new oil; SQL is the refinery. Ask better questions,
                get better insights.”
              </p>
              <span className="hidden text-[10px] font-semibold uppercase tracking-widest text-cyan-300 sm:inline">
                genai sql
              </span>
            </div>
          </header>

          {/* Glassmorphism card */}
          <main className="grid gap-6 md:grid-cols-[minmax(0,3fr)_minmax(0,2fr)]">
            {/* Left: query card */}
            <section className="group rounded-3xl border border-slate-700/60 bg-slate-900/60 p-5 shadow-[0_18px_60px_rgba(15,23,42,0.8)] backdrop-blur-xl transition-transform duration-300 hover:-translate-y-1 sm:p-7">
              <div className="mb-4 flex items-center justify-between gap-3">
                <div className="space-y-1">
                  <h2 className="text-sm font-semibold text-slate-100 sm:text-base">
                    Ask your database in English
                  </h2>
                  <p className="text-xs text-slate-400 sm:text-sm">
                    Describe what you want; GENAI SQL will craft the query and
                    stream the results.
                  </p>
                </div>
                <div className="flex gap-2">
                  <span className="rounded-full bg-emerald-500/20 px-3 py-1 text-[10px] font-semibold uppercase tracking-widest text-emerald-300">
                    Live
                  </span>
                  <span className="hidden rounded-full bg-slate-800/80 px-3 py-1 text-[10px] font-medium text-slate-300 sm:inline">
                    Neon + Postgres
                  </span>
                </div>
              </div>

              <QueryForm onSubmit={handleSubmit} loading={loading} />

              {error && (
                <div className="mt-4 rounded-md border border-red-700 bg-red-950/90 px-3 py-2 text-xs text-red-200">
                  {error}
                </div>
              )}

              {/* Helper examples */}
              <div className="mt-4 space-y-2">
                <p className="text-[11px] font-medium uppercase tracking-[0.2em] text-slate-500">
                  Try asking
                </p>
                <div className="flex flex-wrap gap-2">
                  {[
                    "Total sales amount by month",
                    "Top 5 customers by revenue",
                    "List all orders placed today",
                  ].map((example) => (
                    <button
                      key={example}
                      type="button"
                      onClick={() => handleSubmit(example)}
                      className="rounded-full border border-slate-600/70 bg-slate-900/70 px-3 py-1 text-[11px] text-slate-300 transition hover:border-cyan-400/70 hover:text-cyan-200"
                    >
                      {example}
                    </button>
                  ))}
                </div>
              </div>
            </section>

            {/* Right: results / info card */}
            <section className="space-y-4">
              <div className="h-full rounded-3xl border border-slate-700/60 bg-slate-900/70 p-4 backdrop-blur-xl sm:p-5">
                <h3 className="mb-2 text-xs font-semibold uppercase tracking-[0.2em] text-slate-400">
                  SQL & results
                </h3>
                <ResultsTable sql={sql} columns={columns} rows={rows} />

                {!sql && !loading && (
                  <p className="mt-4 text-xs text-slate-400">
                    Results will appear here as soon as your first query
                    completes.
                  </p>
                )}
              </div>

             
            </section>
          </main>
        </div>
      </div>
    </div>
  );
}

export default App;
