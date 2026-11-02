
import React, { useState } from 'react';
import { motion as m, AnimatePresence } from 'motion/react';
import { X, Send, CheckCircle2, AlertCircle } from 'lucide-react';
import { useForm, ValidationError } from '@formspree/react';

interface FeedbackModalProps {
  isOpen: boolean;
  onClose: () => void;
  userEmail?: string;
}

const FeedbackModal: React.FC<FeedbackModalProps> = ({ isOpen, onClose, userEmail }) => {
  const formsPreeId = (import.meta as any).env.VITE_FORMSPREE_ID || 'maqapqan';
  const [state, handleSubmit] = useForm(formsPreeId);
  const [subject, setSubject] = useState('');
  const [message, setMessage] = useState('');

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[110] flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm">
      <m.div 
        initial={{ opacity: 0, scale: 0.95, y: 20 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        exit={{ opacity: 0, scale: 0.95, y: 20 }}
        className="bg-white rounded-[2.5rem] shadow-2xl w-full max-w-lg overflow-hidden flex flex-col border border-slate-100"
      >
        <div className="p-8 border-b border-slate-50 flex justify-between items-center bg-slate-50/50">
          <div>
            <h2 className="text-2xl font-bold text-slate-900 tracking-tight">Send Feedback</h2>
            <p className="text-sm text-slate-500 mt-1">Help us make Gradwyn better for everyone.</p>
          </div>
          <button onClick={onClose} className="p-3 text-slate-400 hover:text-slate-900 hover:bg-white rounded-full transition-all shadow-sm">
            <X size={20} />
          </button>
        </div>

        <div className="p-8">
          <AnimatePresence mode="wait">
            {state.succeeded ? (
              <m.div 
                key="success"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="py-12 text-center"
              >
                <div className="w-20 h-20 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center mx-auto mb-6 shadow-inner">
                  <CheckCircle2 size={40} />
                </div>
                <h3 className="text-2xl font-bold text-slate-900 mb-2">Thank You!</h3>
                <p className="text-slate-500 mb-8">Your feedback has been received. We read everything!</p>
                <button 
                  onClick={onClose}
                  className="px-10 py-4 bg-slate-900 text-white rounded-full font-bold hover:bg-slate-800 transition-all shadow-xl shadow-slate-900/10"
                >
                    Back to Gradwyn
                </button>
              </m.div>
            ) : (
              <m.form 
                key="form"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                onSubmit={handleSubmit} 
                className="space-y-6"
              >
                <input type="hidden" name="email" value={userEmail || 'anonymous@user.com'} />
                
                <div>
                  <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-3">Topic</label>
                  <input 
                    required
                    name="subject"
                    type="text" 
                    value={subject} 
                    onChange={(e) => setSubject(e.target.value)}
                    placeholder="E.g. Feature Request, Bug Report..."
                    className="w-full p-5 rounded-2xl border border-slate-100 focus:border-slate-900 outline-none bg-slate-50 text-slate-900 font-bold transition-all placeholder-slate-300"
                  />
                  <ValidationError prefix="Subject" field="subject" errors={state.errors} className="text-red-500 text-xs mt-2 font-bold" />
                </div>

                <div>
                  <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-3">Your Message</label>
                  <textarea 
                    required
                    name="message"
                    value={message} 
                    onChange={(e) => setMessage(e.target.value)}
                    placeholder="Tell us what's on your mind..."
                    className="w-full p-5 rounded-2xl border border-slate-100 focus:border-slate-900 outline-none min-h-[160px] bg-slate-50 text-slate-900 font-bold transition-all placeholder-slate-300"
                  />
                  <ValidationError prefix="Message" field="message" errors={state.errors} className="text-red-500 text-xs mt-2 font-bold" />
                </div>

                {state.errors && (state.errors as any).length > 0 && (
                  <div className="flex items-center gap-2 text-red-500 text-sm font-bold bg-red-50 p-4 rounded-xl border border-red-100 animate-shake">
                    <AlertCircle size={16} />
                    <span>Failed to send. Please check your fields and try again.</span>
                  </div>
                )}

                <button 
                  disabled={state.submitting}
                  type="submit" 
                  className={`w-full py-5 rounded-full font-bold flex items-center justify-center gap-3 transition-all shadow-xl
                    ${state.submitting 
                      ? 'bg-slate-100 text-slate-400 cursor-not-allowed shadow-none' 
                      : 'bg-slate-900 text-white hover:bg-slate-800 shadow-slate-900/10'}`}
                >
                  {state.submitting ? (
                    <div className="w-5 h-5 border-2 border-slate-300 border-t-slate-400 rounded-full animate-spin" />
                  ) : (
                    <>
                      <Send size={18} />
                      <span>Send via Secure Email</span>
                    </>
                  )}
                </button>
              </m.form>
            )}
          </AnimatePresence>
        </div>
      </m.div>
    </div>
  );
};

export default FeedbackModal;
