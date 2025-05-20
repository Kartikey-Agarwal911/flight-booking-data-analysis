import { ApiResponse } from '../types';

const API_BASE_URL = 'http://localhost:8000/api';

export const submitQuery = async (query: string): Promise<ApiResponse> => {
    try {
        const response = await fetch(`${API_BASE_URL}/query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error submitting query:', error);
        throw error;
    }
};

export const checkQueryStatus = async (queryId: string): Promise<ApiResponse> => {
    try {
        const response = await fetch(`${API_BASE_URL}/query/status/${queryId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error checking query status:', error);
        throw error;
    }
}; 