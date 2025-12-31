import { useState } from "react";
import axios from "axios";
import { QueryForm } from "./components/QueryForm";
import { ResultsTable } from "./components/ResultsTable";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL as string;

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
      const res = await axios.post<QueryResponse>(`${API_BASE_URL}/api/query`, {
        question,
      });
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
    <div className="min-h-screen flex items-center justify-center px-4">
      <div className="max-w-4xl w-full space-y-6">
        <header className="space-y-2">
          <h1 className="text-2xl font-bold text-white">
            GENAI SQL – Natural language to Postgres
          </h1>
          <p className="text-sm text-slate-400">
            Ask questions in English, get SQL + results from your Neon database.
          </p>
        </header>

        <QueryForm onSubmit={handleSubmit} loading={loading} />

        {error && (
          <div className="mt-4 rounded-md border border-red-700 bg-red-950 px-3 py-2 text-sm text-red-200">
            {error}
          </div>
        )}

        <ResultsTable sql={sql} columns={columns} rows={rows} />
      </div>
    </div>
  );
}

export default App;
