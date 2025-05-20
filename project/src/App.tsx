import React, { useState, useEffect } from 'react';
import ChatInterface from './components/ChatInterface';
import VisualizationPanel from './components/visualizations/VisualizationPanel';
import { ApiResponse } from './types';
// import { submitQuery, checkQueryStatus } from './services/api'; // Removed unused imports

function App() {
  const [visualizationData, setVisualizationData] = useState<ApiResponse | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [currentQueryId, setCurrentQueryId] = useState<string | null>(null);

  useEffect(() => {
    let intervalId: NodeJS.Timeout;

    const checkStatus = async () => {
      if (currentQueryId && isProcessing) {
        try {
          const response = await fetch(`http://localhost:8000/api/query/status/${currentQueryId}`);
          if (!response.ok) {
            console.error('Error checking query status:', response.status);
            setIsProcessing(false);
            setCurrentQueryId(null);
            return;
          }
          const data: ApiResponse = await response.json();
          if (data.status === 'complete' || data.status === 'error') {
            setVisualizationData(data);
            setIsProcessing(false);
            setCurrentQueryId(null);
          }
        } catch (error) {
          console.error('Error checking query status:', error);
          setIsProcessing(false);
          setCurrentQueryId(null);
        }
      }
    };

    if (isProcessing && currentQueryId) {
      intervalId = setInterval(checkStatus, 1000);
    }

    return () => {
      if (intervalId) {
        clearInterval(intervalId);
      }
    };
  }, [isProcessing, currentQueryId]);

  const handleVisualizationUpdate = async (query: string) => {
    try {
      setIsProcessing(true);
      const response = await fetch('http://localhost:8000/api/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query }),
      });
      if (!response.ok) {
        console.error('Error submitting query:', response.status);
        setIsProcessing(false);
        return;
      }
      const data: ApiResponse = await response.json();
      setCurrentQueryId(data.id);
      setVisualizationData(null); // Reset previous data
    } catch (error) {
      console.error('Error submitting query:', error);
      setIsProcessing(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-4 md:p-6">
      <header className="mb-6">
        <h1 className="text-2xl md:text-3xl font-bold text-gray-800">Flight Booking Data Analysis</h1>
        <p className="text-gray-600">Ask questions about flight data to see insights and visualizations</p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="h-[70vh] lg:h-[80vh]">
          <ChatInterface
            onVisualizationUpdate={handleVisualizationUpdate}
            isProcessing={isProcessing}
            latestResponse={visualizationData} // Pass the response data
          />
        </div>

        <div className="h-[70vh] lg:h-[80vh]">
          <VisualizationPanel data={visualizationData} />
        </div>
      </div>
    </div>
  );
}

export default App;