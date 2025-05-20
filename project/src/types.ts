export interface ApiResponse {
  id: string;
  status: 'processing' | 'complete' | 'error';
  error?: string;
  intermediate_result: any | null; // Add this if your backend uses it
  result?: {
    type: 'bar_chart' | 'pie_chart' | 'line_chart' | 'time_series' | 'text' | 'error' | 'table';
    data: any; // The structure of 'data' will vary based on 'type'
    title?: string;
    message?: string; // For error messages within the 'result'
  };
}

export interface VisualizationData {
  type: 'bar' | 'pie' | 'line' | 'table' | 'text';
  title: string;
  description?: string;
  data: any; // This will be strongly typed based on chart type
}

export interface BarChartData {
  labels: string[]; // Changed from categories to labels for consistency with backend
  values: number[];
  title?: string;
}

export interface PieChartData {
  labels: string[];
  values: number[];
  title?: string;
}

export interface LineChartSeries {
  name: string;
  data: number[];
}

export interface LineChartData {
  series: LineChartSeries[];
  dates: string[]; // Assuming your backend provides dates for the line chart
  title?: string;
}

export interface TimeSeriesData {
  labels: string[];
  values: number[];
  title?: string;
  highlight?: string;
}

export interface TableData {
  headers: string[];
  rows: any[][];
}

/* File Explanation:
 * This file defines TypeScript interfaces for the application.
 * Key types:
 * 1. ApiResponse - Defines the structure of responses from the backend API
 * - Now includes the 'result' property that contains the actual response data and type.
 * - Supports different visualization types (text, charts, etc.) within the 'result'.
 * - Handles error messages within the 'result'.
 */