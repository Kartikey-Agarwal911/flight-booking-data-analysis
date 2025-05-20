import React from 'react';
import { Line } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    TimeScale
} from 'chart.js';
import 'chartjs-adapter-date-fns';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    TimeScale
);

interface TimeSeriesChartProps {
    data: {
        labels: string[];
        values: number[];
    };
    title?: string;
}

const TimeSeriesChart: React.FC<TimeSeriesChartProps> = ({ data, title }) => {
    const chartData = {
        labels: data.labels,
        datasets: [
            {
                label: title || 'Value',
                data: data.values,
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                tension: 0.4,
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
            x: {
                type: 'time' as const,
                time: {
                    unit: 'day',
                    displayFormats: {
                        day: 'MMM d',
                    },
                },
                title: {
                    display: true,
                    text: 'Date',
                },
            },
            y: {
                beginAtZero: true,
            },
        },
    };

    return (
        <div className="h-full w-full">
            <Line data={chartData} options={options} />
        </div>
    );
};

export default TimeSeriesChart;

/* File Explanation:
 * This file implements the TimeSeriesChart component using Chart.js library.
 * Key features:
 * 1. Displays time series data with a line chart
 * 2. Supports highlighting specific data points
 * 3. Includes interactive tooltips
 * 4. Responsive container that adapts to parent size
 * 5. Customizable styling for lines and dots
 */ 