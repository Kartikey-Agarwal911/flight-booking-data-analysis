import React from 'react';
import ReactMarkdown from 'react-markdown';

interface TextDisplayProps {
  data: {
    text: string;
  };
}

const TextDisplay: React.FC<TextDisplayProps> = ({ data }) => {
  return (
    <div className="prose prose-blue max-w-none">
      <ReactMarkdown>{data.text}</ReactMarkdown>
    </div>
  );
};

export default TextDisplay;