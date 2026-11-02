
import React, { useState, useEffect } from 'react';
import { ONBOARDING_STEPS } from '../constants';
import { UserProfile } from '../types';

interface OnboardingProps {
  onComplete: (profile: UserProfile) => void;
  initialName?: string;
  onExit?: () => void;
}

const Onboarding: React.FC<OnboardingProps> = ({ onComplete, initialName = '', onExit }) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [profile, setProfile] = useState<Partial<UserProfile>>({
    preferredLocations: [],
    vibe: [],
    name: initialName
  });
  const [inputValue, setInputValue] = useState(initialName);

  const question = ONBOARDING_STEPS[currentStep];
  const isLastStep = currentStep === ONBOARDING_STEPS.length - 1;

  // If initialName is provided, and we are on the name step (index 0), ensure input is populated
  useEffect(() => {
      if (currentStep === 0 && initialName && !inputValue) {
          setInputValue(initialName);
          // Auto-advance could be annoying if they want to change it, so we just pre-fill
      }
  }, [initialName, currentStep]);

  const handleNext = () => {
    // Save current input for text fields
    if (question.type === 'text') {
      setProfile(prev => ({ ...prev, [question.id]: inputValue }));
    }
    
    if (isLastStep) {
        // For the last step (text), we need to make sure we save the input value before completing
        const finalProfile = {
            ...profile,
            [question.id]: question.type === 'text' ? inputValue : profile[question.id as keyof UserProfile]
        } as UserProfile;
        onComplete(finalProfile);
    } else {
      setInputValue(''); // Reset input for next text question
      setCurrentStep(prev => prev + 1);
    }
  };

  const handleOptionSelect = (option: string) => {
    if (question.type === 'button-group') {
      setProfile(prev => ({ ...prev, [question.id]: option }));
      setTimeout(handleNext, 200); // Auto advance for single select
    } else if (question.type === 'multiselect') {
      setProfile(prev => {
        const currentList = (prev[question.id as keyof UserProfile] as string[]) || [];
        
        // Logic for 'Doesn't matter to me'
        if (option === "Doesn't matter to me") {
          // If checking "doesn't matter", clear everything else and just select it
          if (!currentList.includes(option)) {
             return { ...prev, [question.id]: [option] };
          }
          // If unchecking it, just return empty
          return { ...prev, [question.id]: [] };
        }

        // If selecting a normal option, make sure "Doesn't matter" is removed
        const listWithoutDoesntMatter = currentList.filter(item => item !== "Doesn't matter to me");

        if (listWithoutDoesntMatter.includes(option)) {
          return { ...prev, [question.id]: listWithoutDoesntMatter.filter(item => item !== option) };
        } else {
          // Limit vibes to 3
          if (question.id === 'vibe' && listWithoutDoesntMatter.length >= 3) return prev;
          return { ...prev, [question.id]: [...listWithoutDoesntMatter, option] };
        }
      });
    }
  };

  const handleBack = () => {
    if (currentStep > 0) {
        setCurrentStep(prev => prev - 1);
    } else if (onExit) {
        onExit();
    }
  };

  const isNextDisabled = () => {
    if (question.type === 'text') return inputValue.trim().length === 0;
    if (question.type === 'button-group') return !profile[question.id as keyof UserProfile];
    if (question.type === 'multiselect') return (profile[question.id as keyof UserProfile] as string[] || []).length === 0;
    return false;
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4 bg-white">
      <div className="w-full max-w-2xl transition-all duration-500">
        {/* Progress Bar */}
        <div className="w-full bg-slate-100 h-1 rounded-full mb-16 overflow-hidden">
          <div 
            className="bg-slate-900 h-full transition-all duration-700 ease-out"
            style={{ width: `${((currentStep + 1) / ONBOARDING_STEPS.length) * 100}%` }}
          ></div>
        </div>

        {/* Question */}
        <div className="mb-12">
          <h2 className="text-4xl md:text-5xl font-bold text-slate-900 mb-4 tracking-tight leading-tight">
            {question.question}
          </h2>
          {question.subtext && (
            <p className="text-slate-500 text-xl font-medium">{question.subtext}</p>
          )}
        </div>

        {/* Input Area */}
        <div className="min-h-[300px] flex flex-col justify-start">
          {question.type === 'text' && (
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && !isNextDisabled() && handleNext()}
              placeholder={question.placeholder}
              className="w-full text-3xl py-6 border-b border-slate-200 focus:border-slate-900 outline-none bg-transparent transition-all placeholder:text-slate-200 text-slate-900 font-bold"
              autoFocus
            />
          )}

          {question.type === 'button-group' && question.options && (
            <div className="grid grid-cols-1 gap-4">
              {question.options.map((opt) => (
                <button
                  key={opt}
                  onClick={() => handleOptionSelect(opt)}
                  className={`p-6 text-left rounded-2xl border transition-all duration-300 font-bold text-xl
                    ${profile[question.id as keyof UserProfile] === opt 
                      ? 'border-slate-900 bg-slate-900 text-white shadow-xl shadow-slate-900/10' 
                      : 'border-slate-100 hover:border-slate-300 text-slate-500 hover:text-slate-900 hover:bg-slate-50'
                    }`}
                >
                  {opt}
                </button>
              ))}
            </div>
          )}

          {question.type === 'multiselect' && question.options && (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {question.options.map((opt) => {
                const isSelected = (profile[question.id as keyof UserProfile] as string[])?.includes(opt);
                return (
                  <button
                    key={opt}
                    onClick={() => handleOptionSelect(opt)}
                    className={`p-5 rounded-2xl border transition-all duration-300 font-bold text-lg text-left
                      ${isSelected
                        ? 'border-slate-900 bg-slate-900 text-white shadow-xl shadow-slate-900/10' 
                        : 'border-slate-100 hover:border-slate-300 text-slate-500 hover:text-slate-900 hover:bg-slate-50'
                      }`}
                  >
                    {opt}
                  </button>
                );
              })}
            </div>
          )}
        </div>

        {/* Navigation */}
        <div className="flex justify-between mt-12 pt-8 border-t border-slate-100">
          <button
            onClick={handleBack}
            disabled={currentStep === 0 && !onExit}
            className={`px-8 py-4 rounded-full font-bold transition-all text-lg
              ${currentStep === 0 && !onExit ? 'opacity-0 pointer-events-none' : 'text-slate-400 hover:text-slate-900'}`}
          >
            Back
          </button>
          <button
            onClick={handleNext}
            disabled={isNextDisabled()}
            className={`px-12 py-4 rounded-full bg-slate-900 text-white font-bold text-lg shadow-xl shadow-slate-900/10 transition-all
              ${isNextDisabled() ? 'opacity-20 cursor-not-allowed' : 'hover:bg-slate-800 hover:translate-y-[-2px]'}`}
          >
            {isLastStep ? 'Start Exploring' : 'Next'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Onboarding;
