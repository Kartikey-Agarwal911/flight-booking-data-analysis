export interface ApiResponse {
  id: string;
  status: 'processing' | 'complete' | 'error';
  error?: string;
  intermediate_result: any | null; 
  result?: {
    type: 'bar_chart' | 'pie_chart' | 'line_chart' | 'time_series' | 'text' | 'error' | 'table';
    data: any; 
    title?: string;
    message?: string; 
  };
}

export interface VisualizationData {
  type: 'bar' | 'pie' | 'line' | 'table' | 'text';
  title: string;
  description?: string;
  data: any; 
}

export interface BarChartData {
  labels: string[]; 
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
  dates: string[]; 
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