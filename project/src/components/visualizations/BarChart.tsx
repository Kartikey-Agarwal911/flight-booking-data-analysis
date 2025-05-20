import React from 'react';
import { Bar } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
} from 'chart.js';

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
);

interface BarChartProps {
    data: {
        labels: string[];
        values: number[];
    };
    title?: string;
}

const BarChart: React.FC<BarChartProps> = ({ data, title }) => {
    const chartData = {
        labels: data.labels,
        datasets: [
            {
                label: title || 'Value',
                data: data.values,
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1,
      },
        ],
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false,
    },
    title: {
                display: !!title,
                text: title,
      },
    },
        scales: {
            y: {
                beginAtZero: true,
    },
        },
  };

  return (
        <div className="h-full w-full">
            <Bar data={chartData} options={options} />
    </div>
  );
};

export default BarChart;

/* File Explanation:
 * This file implements the BarChart component using Recharts library.
 * Key features:
 * 1. Displays data in a bar chart format
 * 2. Includes grid lines for better readability
 * 3. Interactive tooltips for detailed information
 * 4. Rounded corners on bars for modern look
 * 5. Responsive container that adapts to parent size
 */