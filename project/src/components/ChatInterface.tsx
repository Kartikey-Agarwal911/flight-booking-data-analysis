import React, { useState, useRef, useEffect } from 'react';
import { ApiResponse } from '../types';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'system';
  timestamp: Date;
  response?: ApiResponse;
}

interface ChatInterfaceProps {
  onVisualizationUpdate: (query: string) => void;
  isProcessing: boolean;
  latestResponse: ApiResponse | null; // Add this prop
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({ onVisualizationUpdate, isProcessing, latestResponse }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [query, setQuery] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (latestResponse && latestResponse.status === 'complete') {
      const newMessage: Message = {
        id: Date.now().toString(),
        text: query, // The query that led to this response
        sender: 'system',
        timestamp: new Date(),
        response: latestResponse,
      };
      setMessages(prev => [...prev, newMessage]);
    } else if (latestResponse && latestResponse.status === 'error') {
      const errorMessage: Message = {
        id: Date.now().toString(),
        text: query, // The query that led to this error
        sender: 'system',
        timestamp: new Date(),
        response: latestResponse,
      };
      setMessages(prev => [...prev, errorMessage]);
    }
  }, [latestResponse, query]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim() && !isProcessing) {
      const newUserMessage: Message = {
        id: Date.now().toString(),
        text: query,
        sender: 'user',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, newUserMessage]);
      onVisualizationUpdate(query);
      setQuery('');
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-4 h-full flex flex-col">
      <div className="flex-1 overflow-y-auto mb-4">
        <div className="space-y-4">
          <div className="bg-blue-50 p-4 rounded-lg">
            <p className="text-blue-800">
              Welcome! Ask me questions about flight data, such as:
            </p>
            <ul className="list-disc list-inside mt-2 text-blue-700">
              <li>Which airline has the most flights?</li>
              <li>What are the top 3 most frequent departure dates?</li>
              <li>What are the top 3 most frequent arrival dates?</li>
              <li>What is the distribution of flight classes?</li>
              <li>What are the descriptive statistics of fare?</li>
              <li>What are the most common extras purchased?</li>
              <li>What are the counts of different booking statuses?</li>
              <li>What are the most frequent gates?</li>
              <li>What are the most frequent terminals?</li>
              <li>What are the counts of flights with different numbers of layovers?</li>
              <li>What are the most frequent layover locations?</li>
              <li>What are the counts of different aircraft types?</li>
              <li>What is the distribution of reward program members vs. non-members?</li>
              <li>What is the average fare for each airline?</li>
              <li>What is the average duration of flights for each airline?</li>
              {/* Add more suggestions based on the "Directly Using Columns" list */}
            </ul>
            <p className="mt-2 text-sm text-blue-700">
              You can also ask about flight failures if failure data is available.
            </p>
          </div>
          {messages.map((msg) => (
            <div key={msg.id} className={`p-3 rounded-lg ${msg.sender === 'user' ? 'bg-gray-100 text-gray-800 self-start' : 'bg-blue-100 text-blue-800 self-end'}`}>
              <p className="text-sm italic">{msg.sender === 'user' ? 'You' : 'System'}</p>
              <p>{msg.text}</p>
              {msg.response && msg.response.status === 'complete' && msg.response.result && (
                <div className="mt-2">
                  {msg.response.result.type === 'text' ? (
                    <p className="font-semibold">{msg.response.result.data}</p>
                  ) : (
                    <p className="font-semibold">[Visualization Available Below]</p>
                  )}
                </div>
              )}
              {msg.response && msg.response.status === 'error' && (
                <div className="mt-2 bg-red-100 border border-red-400 text-red-700 px-3 py-2 rounded">
                  <p className="font-semibold">Error:</p>
                  <p>{msg.response.error || 'An error occurred.'}</p>
                </div>
              )}
              <p className="text-xs text-gray-500 mt-1">{msg.timestamp.toLocaleTimeString()}</p>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>
      </div>

      <form onSubmit={handleSubmit} className="mt-auto">
        <div className="flex gap-2">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask a question about flight data..."
            className="flex-1 p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isProcessing}
          />
          <button
            type="submit"
            disabled={!query.trim() || isProcessing}
            className={`px-4 py-2 rounded-lg ${
              !query.trim() || isProcessing
                ? 'bg-gray-300 cursor-not-allowed'
                : 'bg-blue-500 hover:bg-blue-600 text-white'
            }`}
          >
            {isProcessing ? 'Processing...' : 'Ask'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default ChatInterface;

/* File Explanation:
 * This file implements the ChatInterface component which provides the main interaction
 * point for users to query flight data. Key features:
 * 1. Real-time message history with user and system messages
 * 2. Integration with the polling state hook for async responses
 * 3. Automatic scrolling to latest messages
 * 4. Loading states and error handling
 * 5. Responsive design with Tailwind CSS
 * The component manages the chat state and coordinates with the visualization panel.
 */