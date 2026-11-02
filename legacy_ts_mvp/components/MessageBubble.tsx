
import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { ChatMessage } from '../types';

interface MessageBubbleProps {
  message: ChatMessage;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const isUser = message.role === 'user';

  return (
    <div className={`flex w-full mb-10 ${isUser ? 'justify-end' : 'justify-start'} overflow-hidden`}>
      <div
        className={`flex flex-col max-w-[92%] md:max-w-[80%] min-w-0 ${
          isUser ? 'items-end' : 'items-start'
        }`}
      >
        {/* Bubble */}
        <div
          className={`px-5 py-4 md:px-8 md:py-6 text-base md:text-lg shadow-sm leading-relaxed overflow-hidden transition-all rounded-2xl md:rounded-3xl
            ${
              isUser
                ? 'bg-slate-900 text-white shadow-2xl shadow-slate-900/10'
                : message.isThinking
                  ? 'bg-slate-50 text-slate-500 border border-slate-50 italic'
                  : 'bg-slate-50 border border-slate-50 text-slate-900'
            }`}
        >
          {message.isThinking ? (
            <div className="flex items-center gap-4">
               <div className="w-4 h-4 border-2 border-slate-300 border-t-slate-900 rounded-full animate-spin"></div>
               <span className="font-bold uppercase tracking-widest text-xs">{message.text || "Analyzing..."}</span>
            </div>
          ) : (
            <div className="markdown-content space-y-4 font-medium break-words [word-break:break-word] overflow-hidden">
                <ReactMarkdown 
                    remarkPlugins={[remarkGfm]}
                    components={{
                        ul: ({node, ...props}) => <ul className="list-disc pl-6 space-y-2 marker:text-slate-400" {...props} />,
                        ol: ({node, ...props}) => <ol className="list-decimal pl-6 space-y-2 marker:text-slate-400" {...props} />,
                        li: ({node, ...props}) => <li className="mb-1" {...props} />,
                        strong: ({node, ...props}) => <strong className="font-bold text-inherit" {...props} />,
                        a: ({node, ...props}) => <a className="underline decoration-slate-300 underline-offset-4 font-bold hover:text-slate-500 transition-all" {...props} target="_blank" rel="noopener noreferrer" />,
                        p: ({node, ...props}) => <p className="mb-4 last:mb-0 leading-relaxed" {...props} />,
                        table: ({node, ...props}) => (
                            <div className="overflow-x-auto my-6 border border-slate-200 rounded-xl">
                                <table className="w-full text-sm text-left border-collapse" {...props} />
                            </div>
                        ),
                        thead: ({node, ...props}) => <thead className="bg-slate-100/50 border-b border-slate-200" {...props} />,
                        th: ({node, ...props}) => <th className="px-4 py-3 font-bold text-slate-900" {...props} />,
                        td: ({node, ...props}) => <td className="px-4 py-3 border-b border-slate-100 last:border-0" {...props} />,
                        code: ({node, className, children, ...props}) => {
                            const match = /language-(\w+)/.exec(className || '');
                            const isInline = !match;
                            return isInline 
                                ? <code className="bg-slate-200/50 px-1.5 py-0.5 rounded text-sm font-mono break-all" {...props}>{children}</code>
                                : <pre className="bg-slate-900 text-slate-100 p-4 rounded-xl overflow-x-auto text-sm font-mono my-4 max-w-full"><code className={className} {...props}>{children}</code></pre>
                        }
                    }}
                >
                    {message.text}
                </ReactMarkdown>
            </div>
          )}
        </div>

        {/* Grounding Sources */}
        {!isUser && message.sources && message.sources.length > 0 && !message.isThinking && (
          <div className="mt-4 w-full animate-fade-in px-2">
            <p className="text-[10px] font-bold text-slate-300 uppercase tracking-widest mb-3 flex items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-3 h-3">
                <path fillRule="evenodd" d="M10.5 3.75a6.75 6.75 0 100 13.5 6.75 6.75 0 000-13.5zM2.25 10.5a8.25 8.25 0 1114.59 5.28l4.69 4.69a.75.75 0 11-1.06 1.06l-4.69-4.69A8.25 8.25 0 012.25 10.5z" clipRule="evenodd" />
              </svg>
              Researched Sources
            </p>
            <div className="flex flex-wrap gap-2">
              {message.sources.map((source, idx) => (
                <a
                  key={idx}
                  href={source.uri}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center max-w-full truncate text-[10px] bg-slate-50 hover:bg-slate-100 text-slate-500 hover:text-slate-900 px-4 py-2 rounded-full border border-slate-50 transition-all font-bold uppercase tracking-wider"
                  title={source.title}
                >
                   <span className="truncate max-w-[150px] md:max-w-[200px]">{source.title}</span>
                   <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="w-3 h-3 ml-2 flex-shrink-0 opacity-30">
                      <path fillRule="evenodd" d="M4.25 5.5a.75.75 0 00-.75.75v8.5c0 .414.336.75.75.75h8.5a.75.75 0 00.75-.75v-4a.75.75 0 011.5 0v4A2.25 2.25 0 0112.75 17h-8.5A2.25 2.25 0 012 14.75v-8.5A2.25 2.25 0 014.25 4h5a.75.75 0 010 1.5h-5z" clipRule="evenodd" />
                      <path fillRule="evenodd" d="M6.194 12.753a.75.75 0 001.06.053L16.5 4.44v2.81a.75.75 0 001.5 0v-4.5a.75.75 0 00-.75-.75h-4.5a.75.75 0 000 1.5h2.553l-9.056 8.194a.75.75 0 00-.053 1.06z" clipRule="evenodd" />
                   </svg>
                </a>
              ))}
            </div>
          </div>
        )}
        
        {/* Timestamp */}
        <span className="text-[10px] text-slate-200 mt-2 px-2 font-bold uppercase tracking-widest">
          {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </span>
      </div>
    </div>
  );
};

export default MessageBubble;
