interface ResultsTableProps {
    sql: string | null;
    columns: string[];
    rows: string[][];
  }
  
  export function ResultsTable({ sql, columns, rows }: ResultsTableProps) {
    if (!sql) {
      return null;
    }
  
    return (
      <div className="space-y-3 mt-6">
        <div>
          <h2 className="text-sm font-semibold text-slate-200 mb-1">
            Generated SQL
          </h2>
          <pre className="rounded-md bg-slate-900 border border-slate-700 p-3 text-xs overflow-x-auto">
            {sql}
          </pre>
        </div>
  
        <div>
          <h2 className="text-sm font-semibold text-slate-200 mb-1">
            Results
          </h2>
          {rows.length === 0 ? (
            <p className="text-sm text-slate-400">No rows returned.</p>
          ) : (
            <div className="overflow-x-auto rounded-md border border-slate-700">
              <table className="min-w-full text-xs">
                <thead className="bg-slate-900">
                  <tr>
                    {columns.map((col) => (
                      <th
                        key={col}
                        className="px-3 py-2 text-left font-semibold text-slate-300"
                      >
                        {col}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800 bg-slate-950">
                  {rows.map((row, i) => (
                    <tr key={i}>
                      {row.map((cell, j) => (
                        <td key={j} className="px-3 py-2 text-slate-200">
                          {cell}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    );
  }
  