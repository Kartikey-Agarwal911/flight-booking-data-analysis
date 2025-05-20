import React, { useState, FormEvent, useRef, useEffect } from 'react';
import { Send } from 'lucide-react';

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  disabled: boolean;
}

const ChatInput: React.FC<ChatInputProps> = ({ onSendMessage, disabled }) => {
  const [message, setMessage] = useState('');
  const inputRef = useRef<HTMLTextAreaElement>(null);

  // Auto-resize textarea as content grows
  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.style.height = 'auto';
      inputRef.current.style.height = `${inputRef.current.scrollHeight}px`;
    }
  }, [message]);

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (message.trim() && !disabled) {
      onSendMessage(message);
      setMessage('');
      
      // Reset height after sending
      if (inputRef.current) {
        inputRef.current.style.height = 'auto';
      }
    }
  };

  // Handle Ctrl+Enter or Command+Enter to submit
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      handleSubmit(e);
    }
  };

  return (
    <form 
      onSubmit={handleSubmit} 
      className="flex items-end bg-white border border-gray-200 rounded-lg shadow-sm overflow-hidden transition-all duration-200 focus-within:border-blue-400 focus-within:ring-2 focus-within:ring-blue-100"
    >
      <textarea
        ref={inputRef}
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Ask about flight data (e.g., 'Which airline has the most flights?')"
        disabled={disabled}
        className="flex-1 py-3 px-4 outline-none resize-none max-h-32 min-h-[50px]"
        rows={1}
      />
      <button
        type="submit"
        disabled={!message.trim() || disabled}
        className={`p-3 mr-1 mb-1 text-white rounded-full transition-all duration-200 ${
          message.trim() && !disabled
            ? 'bg-blue-500 hover:bg-blue-600'
            : 'bg-gray-300 cursor-not-allowed'
        }`}
        aria-label="Send message"
      >
        <Send size={20} />
      </button>
    </form>
  );
};

export default ChatInput;