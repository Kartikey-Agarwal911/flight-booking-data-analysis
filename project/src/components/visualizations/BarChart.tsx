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
