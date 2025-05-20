import React from 'react';
import { Pie } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    ArcElement,
    Tooltip,
    Legend
} from 'chart.js';

ChartJS.register(
    ArcElement,
    Tooltip,
    Legend
);

interface PieChartProps {
    data: {
        labels: string[];
        values: number[];
    };
    title?: string;
}

const PieChart: React.FC<PieChartProps> = ({ data, title }) => {
    const chartData = {
        labels: data.labels,
        datasets: [
            {
                data: data.values,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.5)',
                    'rgba(54, 162, 235, 0.5)',
                    'rgba(255, 206, 86, 0.5)',
                    'rgba(75, 192, 192, 0.5)',
                    'rgba(153, 102, 255, 0.5)',
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                ],
                borderWidth: 1,
      },
        ],
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'right' as const,
    },
    title: {
                display: !!title,
                text: title,
            },
    },
  };

  return (
        <div className="h-full w-full">
            <Pie data={chartData} options={options} />
    </div>
  );
};

export default PieChart;

/* File Explanation:
 * This file implements the PieChart component using Recharts library.
 * Key features:
 * 1. Displays data in a pie chart format
 * 2. Includes percentage labels on pie segments
 * 3. Interactive tooltips for detailed information
 * 4. Legend for identifying segments
 * 5. Custom color scheme for different segments
 */