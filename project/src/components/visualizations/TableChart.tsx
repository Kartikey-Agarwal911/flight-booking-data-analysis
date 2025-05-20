// components/visualizations/TableChart.tsx

import React from 'react';
import { TableData } from '../../types';

interface TableChartProps {
  data: TableData;
  title?: string;
}

const TableChart: React.FC<TableChartProps> = ({ data, title }) => {
  if (!data || !data.headers || !data.rows) {
    return <div>Error: Invalid table data.</div>;
  }

  return (
    <div className="overflow-x-auto">
      {title && <h3 className="text-lg font-semibold mb-2">{title}</h3>}
      <table className="min-w-full leading-normal">
        <thead>
          <tr>
            {data.headers.map((header) => (
              <th key={header} className="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                {header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.rows.map((row, index) => (
            <tr key={index}>
              {row.map((cell, cellIndex) => (
                <td key={cellIndex} className="px-5 py-5 border-b border-gray-200 bg-white text-sm">
                  {cell}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default TableChart;
