
import React from 'react';

const LoadingDots: React.FC = () => {
  return (
    <div className="flex space-x-1.5 items-center h-6 px-2">
      <div className="w-2 h-2 bg-brand-400 animate-bounce [animation-delay:-0.3s]"></div>
      <div className="w-2 h-2 bg-brand-400 animate-bounce [animation-delay:-0.15s]"></div>
      <div className="w-2 h-2 bg-brand-400 animate-bounce"></div>
    </div>
  );
};

export default LoadingDots;
