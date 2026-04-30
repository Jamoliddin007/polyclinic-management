export default function Table({ columns, data, onRowClick, emptyText = 'Maʼlumot yoʻq' }) {
  if (!data || data.length === 0) {
    return (
      <div className="card p-12 text-center text-slate-500">
        {emptyText}
      </div>
    );
  }

  return (
    <div className="card overflow-hidden">
      <table className="min-w-full divide-y divide-slate-200">
        <thead className="bg-slate-50">
          <tr>
            {columns.map((col) => (
              <th
                key={col.key}
                className="table-cell text-left font-semibold text-slate-700 uppercase tracking-wider"
              >
                {col.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-slate-200">
          {data.map((row, rIdx) => (
            <tr
              key={row.id ?? rIdx}
              onClick={() => onRowClick?.(row)}
              className={onRowClick ? 'cursor-pointer hover:bg-slate-50' : ''}
            >
              {columns.map((col) => (
                <td key={col.key} className="table-cell text-slate-700">
                  {col.render ? col.render(row) : row[col.key]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
