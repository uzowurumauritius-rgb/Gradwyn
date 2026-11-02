
import React, { useState, useEffect } from 'react';

interface LoadingScreenProps {
  messages: string[];
}

const LoadingScreen: React.FC<LoadingScreenProps> = ({ messages }) => {
  const [currentMessageIndex, setCurrentMessageIndex] = useState(0);
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const messageInterval = setInterval(() => {
      setCurrentMessageIndex((prev) => (prev + 1) % messages.length);
    }, 2500);

    const progressInterval = setInterval(() => {
        setProgress(prev => {
            if (prev >= 100) return 100;
            return prev + 1;
        });
    }, 50);

    return () => {
        clearInterval(messageInterval);
        clearInterval(progressInterval);
    };
  }, [messages]);

  return (
    <div className="h-screen w-full flex flex-col items-center justify-center bg-beige-100 text-brand-900 font-sans z-50 relative overflow-hidden">
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-5 pointer-events-none" 
           style={{ backgroundImage: 'radial-gradient(#162714 1px, transparent 1px)', backgroundSize: '30px 30px' }}>
      </div>

      <div className="relative z-10 flex flex-col items-center max-w-lg w-full px-8">
        {/* Logo Mark */}
        <div className="w-16 h-16 bg-brand-700 flex items-center justify-center text-white font-serif text-3xl font-bold shadow-none mb-12 animate-pulse">
             G
        </div>

        {/* Title */}
        <h2 className="text-3xl md:text-4xl font-bold text-brand-900 font-serif mb-8 tracking-tight text-center">
            Gradwyn Intelligence
        </h2>

        {/* Progress Bar */}
        <div className="w-full h-1 bg-brand-200 mb-6 relative overflow-hidden">
            <div 
                className="absolute top-0 left-0 h-full bg-brand-700 transition-all duration-100 ease-linear"
                style={{ width: `${progress}%` }}
            ></div>
        </div>

        {/* Dynamic Text */}
        <div className="h-8 flex items-center justify-center w-full">
             <p key={currentMessageIndex} className="text-accent-olive font-heading font-bold uppercase tracking-widest text-sm animate-fade-in text-center">
                {messages[currentMessageIndex]}
            </p>
        </div>
      </div>
    </div>
  );
};

export default LoadingScreen;
