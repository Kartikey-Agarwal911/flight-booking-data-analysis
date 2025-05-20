import React from 'react';
import { ApiResponse } from '../../types';
import BarChart from './BarChart';
import LineChart from './LineChart';
import PieChart from './PieChart';
import TimeSeriesChart from './TimeSeriesChart';
import TableChart from './TableChart';
interface VisualizationPanelProps {
  data: ApiResponse | null;
}

const VisualizationPanel: React.FC<VisualizationPanelProps> = ({ data }) => {
  if (!data || data.status === 'processing') {
    return (
      <div className="bg-white rounded-lg shadow-lg p-4 h-full flex items-center justify-center">
        <p className="text-blue-500">Processing your query...</p>
      </div>
    );
  }

  if (data.status === 'error') {
    return (
      <div className="bg-white rounded-lg shadow-lg p-4 h-full flex items-center justify-center">
        <p className="text-red-500">{data.error || 'An error occurred while processing your query'}</p>
      </div>
    );
  }

  if (!data.result) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-4 h-full flex items-center justify-center">
        <p className="text-gray-500">No data to display</p>
      </div>
    );
  }

  const renderVisualization = () => {
    if (!data?.result) { // Check if result exists
        return (
          <div className="flex items-center justify-center h-full">
            <p className="text-gray-500">No visualization data available</p>
          </div>
        );
      }
    switch (data.result.type) {
      case 'bar_chart':
        return <BarChart data={data.result.data || { labels: [], values: [] }} title={data.result.data?.title} />;
      case 'line_chart':
        return <LineChart data={data.result.data || { series: [], dates: [], title: '' }} title={data.result.data?.title} />;
      case 'pie_chart':
        return <PieChart data={data.result.data || { labels: [], values: [] }} title={data.result.data?.title} />;
      case 'time_series':
        return <TimeSeriesChart data={data.result.data || { labels: [], values: [], title: '', highlight: '' }} title={data.result.data?.title} />;
      case 'text':
        return (
          <div className="flex items-center justify-center h-full">
            <p className="text-gray-700">{data.result.data}</p>
          </div>
        );
      case 'table':
        return <TableChart data={data.result.data || { headers: [], rows: [] }} title={data.result.data?.title} />;
      default:
        return (
          <div className="flex items-center justify-center h-full">
            <p className="text-gray-500">Unsupported visualization type: {data.result.type}</p>
          </div>
        );
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-4 h-full flex flex-col">
      {data.result.type !== 'text' && data.result.data?.title && (
        <h2 className="text-xl font-semibold mb-4">{data.result.data.title}</h2>
      )}
      <div className="flex-1">
        {renderVisualization()}
      </div>
    </div>
  );
};

export default VisualizationPanel;
