
import React, { useState, useRef, useEffect } from 'react';
import { ChatMessage, UserProfile, University } from '../types';
import MessageBubble from './MessageBubble';
import EditProfileModal from './EditProfileModal';
import UniversityCard from './UniversityCard';
import { sendMessageToGeminiStream, updateChatProfile } from '../services/geminiService';
import LoadingDots from './LoadingDots';

interface ChatInterfaceProps {
  profile: UserProfile;
  messages: ChatMessage[];
  setMessages: React.Dispatch<React.SetStateAction<ChatMessage[]>>;
  onUpdateProfile: (newProfile: UserProfile) => void;
  onSaveSchool: (school: University) => void;
  onDiscardSchool: (schoolId: string) => void;
  savedSchools: University[];
  discardedSchools: string[];
  onGoToDashboard: () => void;
  embeddedInDashboard?: boolean;
  onDeleteAccount?: () => void;
}

const LOADING_PHRASES = [
  "Consulting academic archives...",
  "Analyzing global rankings...",
  "Cross-referencing student forums...",
  "Evaluating endowment opportunities...",
  "Synthesizing campus sentiments...",
  "Checking research outputs...",
  "Verifying accreditation status...",
  "Curating your shortlist..."
];

const ChatInterface: React.FC<ChatInterfaceProps> = ({ 
    profile, 
    messages,
    setMessages, 
    onUpdateProfile,
    onSaveSchool,
    onDiscardSchool,
    savedSchools,
    discardedSchools,
    onGoToDashboard,
    embeddedInDashboard = false,
    onDeleteAccount = () => {}
}) => {
  const [inputText, setInputText] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const loadingIntervalRef = useRef<any>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Rotate loading text
  useEffect(() => {
    if (isProcessing) {
      let index = 0;
      loadingIntervalRef.current = setInterval(() => {
        index = (index + 1) % LOADING_PHRASES.length;
        setMessages(prev => {
          const lastMsg = prev[prev.length - 1];
          if (lastMsg && lastMsg.isThinking) {
             const newMessages = [...prev];
             newMessages[newMessages.length - 1] = { ...lastMsg, text: LOADING_PHRASES[index] };
             return newMessages;
          }
          return prev;
        });
      }, 2500);
    } else {
      if (loadingIntervalRef.current) clearInterval(loadingIntervalRef.current);
    }
    return () => {
      if (loadingIntervalRef.current) clearInterval(loadingIntervalRef.current);
    };
  }, [isProcessing, setMessages]);

  const handleSendMessage = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!inputText.trim() || isProcessing) return;

    const userText = inputText.trim();
    setInputText('');
    setIsProcessing(true);

    const userMsg: ChatMessage = {
        id: Date.now().toString(),
        role: 'user',
        text: userText,
        timestamp: new Date()
    };

    // Add user message and thinking placeholder
    setMessages(prev => [
        ...prev, 
        userMsg,
        {
            id: 'thinking',
            role: 'model',
            text: LOADING_PHRASES[0],
            timestamp: new Date(),
            isThinking: true
        }
    ]);

    try {
        const response = await sendMessageToGeminiStream(userText, (streamedText) => {
            setMessages(prev => {
                const lastMsg = prev[prev.length - 1];
                if (lastMsg && lastMsg.isThinking) {
                    // Replace thinking with streaming
                    const newMessages = [...prev];
                    newMessages[newMessages.length - 1] = { 
                        ...lastMsg, 
                        id: 'streaming-' + userMsg.id,
                        text: streamedText,
                        isThinking: false
                    };
                    return newMessages;
                } else if (lastMsg && lastMsg.id === 'streaming-' + userMsg.id) {
                    // Update current streaming message
                    const newMessages = [...prev];
                    newMessages[newMessages.length - 1] = { ...lastMsg, text: streamedText };
                    return newMessages;
                }
                return prev;
            });
        });
        
        setMessages(prev => {
            // Finalize message with sources and recommendations
            const filtered = prev.filter(m => m.id !== 'thinking' && m.id !== 'streaming-' + userMsg.id);
            return [
                ...filtered,
                {
                    id: Date.now().toString(),
                    role: 'model',
                    text: response.text,
                    sources: response.sources,
                    recommendations: response.recommendations,
                    timestamp: new Date()
                }
            ];
        });
    } catch (error) {
        console.error("Chat error", error);
        setMessages(prev => {
            const filtered = prev.filter(m => m.id !== 'thinking');
            return [
                ...filtered,
                {
                    id: Date.now().toString(),
                    role: 'model',
                    text: "I encountered a temporary issue connecting to the research database. Please try again.",
                    timestamp: new Date()
                }
            ];
        });
    } finally {
        setIsProcessing(false);
    }
  };

  const handleProfileUpdate = async (newProfile: UserProfile) => {
      onUpdateProfile(newProfile);
      setIsEditModalOpen(false);
      
      // Notify user and trigger AI update
      setMessages(prev => [...prev, {
          id: 'sys-update-' + Date.now(),
          role: 'user',
          text: "I've updated my preferences. Can you recommend universities based on my new profile?",
          timestamp: new Date()
      }, {
          id: 'thinking',
          role: 'model',
          text: "Recalibrating recommendations...",
          timestamp: new Date(),
          isThinking: true
      }]);
      
      setIsProcessing(true);
      
      try {
          const response = await updateChatProfile(newProfile, [], (streamedText) => {
            setMessages(prev => {
                const lastMsg = prev[prev.length - 1];
                if (lastMsg && lastMsg.isThinking) {
                    const newMessages = [...prev];
                    newMessages[newMessages.length - 1] = { 
                        ...lastMsg, 
                        id: 'streaming-update',
                        text: streamedText,
                        isThinking: false
                    };
                    return newMessages;
                } else if (lastMsg && lastMsg.id === 'streaming-update') {
                    const newMessages = [...prev];
                    newMessages[newMessages.length - 1] = { ...lastMsg, text: streamedText };
                    return newMessages;
                }
                return prev;
            });
          });
          setMessages(prev => {
            const filtered = prev.filter(m => m.id !== 'thinking' && m.id !== 'streaming-update');
            return [
                ...filtered,
                {
                    id: Date.now().toString(),
                    role: 'model',
                    text: response.text,
                    sources: response.sources,
                    recommendations: response.recommendations,
                    timestamp: new Date()
                }
            ];
        });
      } catch (error) {
          console.error(error);
      } finally {
          setIsProcessing(false);
      }
  };

  return (
    <div className={`flex flex-col h-full bg-white min-w-0 ${!embeddedInDashboard ? 'fixed inset-0' : 'relative'}`}>
      <EditProfileModal 
        isOpen={isEditModalOpen} 
        onClose={() => setIsEditModalOpen(false)} 
        profile={profile} 
        onSave={handleProfileUpdate}
        onDeleteAccount={onDeleteAccount}
      />

      {/* Header (only if not embedded) */}
      {!embeddedInDashboard && (
          <header className="bg-white border-b border-slate-50 p-6 flex justify-between items-center z-10">
            <div className="flex items-center gap-3">
                <span className="font-bold text-2xl text-slate-900 tracking-tight">Gradwyn Intelligence</span>
            </div>
            <div className="flex items-center gap-4">
                <button 
                    onClick={() => setIsEditModalOpen(true)}
                    className="text-sm font-bold text-slate-400 hover:text-slate-900 transition-all"
                >
                    Preferences
                </button>
                <button 
                    onClick={onGoToDashboard}
                    className="bg-slate-900 text-white text-sm font-bold px-6 py-2.5 rounded-full hover:bg-slate-800 transition-all shadow-xl shadow-slate-900/10"
                >
                    Dashboard
                </button>
            </div>
          </header>
      )}

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 md:p-6 lg:p-10 bg-white scroll-smooth">
        <div className="max-w-4xl mx-auto">
            {messages.map((msg, idx) => (
                <div key={msg.id || idx}>
                    <MessageBubble message={msg} />
                    
                    {/* Render Cards if present */}
                    {msg.recommendations && msg.recommendations.length > 0 && (
                        <div className="mb-12 ml-0 md:ml-16 animate-fade-in overflow-hidden">
                            <div className="flex overflow-x-auto gap-4 md:gap-6 pb-6 snap-x snap-mandatory -mx-4 px-4 md:mx-0 md:px-0 no-scrollbar">
                                {msg.recommendations.map((uni) => (
                                    <UniversityCard 
                                        key={uni.id} 
                                        university={uni} 
                                        onSave={onSaveSchool}
                                        onDiscard={onDiscardSchool}
                                        isSaved={savedSchools.some(s => s.id === uni.id)}
                                        isDiscarded={discardedSchools.includes(uni.id)}
                                        className="snap-center shrink-0 w-[260px] md:w-[320px]"
                                    />
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            ))}
            <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Floating Dashboard Button */}
      {!embeddedInDashboard && savedSchools.length >= 2 && (
         <div className="fixed bottom-24 md:bottom-32 right-4 md:right-8 z-20 animate-fade-in-up">
            <button 
                onClick={onGoToDashboard}
                className="bg-slate-900 hover:bg-slate-800 text-white px-6 md:px-8 py-4 md:py-5 rounded-full font-bold shadow-2xl flex items-center gap-3 md:gap-4 transition-all hover:scale-105 group"
            >
                <span className="text-sm md:text-lg">Go to Dashboard</span>
                <span className="bg-white text-slate-900 w-6 h-6 md:w-7 md:h-7 rounded-full flex items-center justify-center text-xs md:text-sm font-bold group-hover:bg-slate-50 transition-all">
                    {savedSchools.length}
                </span>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="w-5 h-5 md:w-6 md:h-6">
                    <path fillRule="evenodd" d="M3 10a.75.75 0 01.75-.75h10.638L10.23 5.29a.75.75 0 111.04-1.08l5.5 5.25a.75.75 0 010 1.08l-5.5 5.25a.75.75 0 11-1.04-1.08l4.158-3.96H3.75A.75.75 0 013 10z" clipRule="evenodd" />
                </svg>
            </button>
         </div>
      )}

      {/* Input Area */}
      <div className="p-4 md:p-8 lg:p-10 bg-white z-10">
        <div className="max-w-4xl mx-auto relative">
            <form onSubmit={handleSendMessage} className="relative flex items-end gap-2 md:gap-3 bg-slate-50 p-2 md:p-3 rounded-2xl md:rounded-3xl border border-slate-50 focus-within:border-slate-200 focus-within:bg-white focus-within:shadow-2xl focus-within:shadow-slate-900/5 transition-all">
                <textarea
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                    onKeyDown={(e) => {
                        if (e.key === 'Enter' && !e.shiftKey) {
                            e.preventDefault();
                            handleSendMessage();
                        }
                    }}
                    placeholder="Ask Gradwyn..."
                    className="w-full max-h-32 md:max-h-48 p-3 md:p-4 bg-transparent border-none outline-none resize-none text-slate-900 placeholder:text-slate-300 font-medium text-base md:text-lg"
                    rows={1}
                    style={{ minHeight: '48px' }}
                />
                <button 
                    type="submit"
                    disabled={!inputText.trim() || isProcessing}
                    className={`p-3 md:p-4 rounded-xl md:rounded-2xl flex items-center justify-center transition-all ${
                        !inputText.trim() || isProcessing 
                            ? 'bg-slate-100 text-slate-300 cursor-not-allowed' 
                            : 'bg-slate-900 text-white hover:bg-slate-800 shadow-xl shadow-slate-900/10'
                    }`}
                >
                    {isProcessing ? (
                        <LoadingDots />
                    ) : (
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="w-5 h-5 md:w-6 md:h-6">
                            <path d="M3.105 2.289a.75.75 0 00-.826.95l1.414 4.925A1.5 1.5 0 005.135 9.25h6.115a.75.75 0 010 1.5H5.135a1.5 1.5 0 00-1.442 1.086l-1.414 4.926a.75.75 0 00.826.95 28.896 28.896 0 0015.293-7.154.75.75 0 000-1.115A28.897 28.897 0 003.105 2.289z" />
                        </svg>
                    )}
                </button>
            </form>
            <div className="text-center mt-2 md:mt-4">
                 <p className="text-[10px] text-slate-300 font-bold uppercase tracking-widest">AI can make mistakes. Verify important info.</p>
            </div>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
