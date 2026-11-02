
import React, { useState, useEffect } from 'react';
import { Application, University, Scholarship, UserProfile } from '../types';

interface ApplicationFormModalProps {
  isOpen: boolean;
  onClose: () => void;
  application: Application | null;
  university: University | null; 
  scholarship?: Scholarship | null; // Added support for scholarship
  userProfile: UserProfile;
  onSave: (app: Application) => void;
}

const STEPS = [
  { id: 1, title: 'Personal Info' },
  { id: 2, title: 'Academics' },
  { id: 3, title: 'Essay' },
  { id: 4, title: 'Review' }
];

const ApplicationFormModal: React.FC<ApplicationFormModalProps> = ({ 
  isOpen, 
  onClose, 
  application, 
  university,
  scholarship,
  userProfile,
  onSave 
}) => {
  // Initialize state
  const [currentStep, setCurrentStep] = useState(1);
  const [formData, setFormData] = useState<Application['formData']>({
    personal: {},
    academic: {},
    essay: ''
  });

  // Load existing data when modal opens
  useEffect(() => {
    if (isOpen) {
      if (application) {
        setCurrentStep(application.currentStep || 1);
        setFormData(application.formData || { personal: {}, academic: {}, essay: '' });
      } else {
        // Pre-fill from user profile for new applications
        setFormData({
          personal: {
            fullName: userProfile.name || '',
            email: userProfile.email || '',
          },
          academic: {
            major: userProfile.fieldOfStudy || ''
          },
          essay: ''
        });
        setCurrentStep(1);
      }
    }
  }, [isOpen, application, userProfile, university, scholarship]);

  if (!isOpen) return null;

  // Determine target entity (University or Scholarship)
  const isScholarship = !!scholarship || application?.type === 'scholarship';
  const targetName = isScholarship ? (application?.scholarship?.name || scholarship?.name) : (application?.university?.name || university?.name);

  if (!targetName) return null;

  const handleSaveAndClose = () => {
    const progress = Math.round(((currentStep - 1) / STEPS.length) * 100);
    
    const updatedApp: Application = {
      id: application?.id || Date.now().toString(),
      type: isScholarship ? 'scholarship' : 'university',
      university: isScholarship ? undefined : (application?.university || university!),
      scholarship: isScholarship ? (application?.scholarship || scholarship!) : undefined,
      status: 'draft',
      lastUpdated: new Date(),
      progress: progress === 0 ? 10 : progress, // Minimum 10% if started
      currentStep,
      formData
    };
    
    onSave(updatedApp);
    onClose();
  };

  const handleSubmit = () => {
    const updatedApp: Application = {
      id: application?.id || Date.now().toString(),
      type: isScholarship ? 'scholarship' : 'university',
      university: isScholarship ? undefined : (application?.university || university!),
      scholarship: isScholarship ? (application?.scholarship || scholarship!) : undefined,
      status: 'submitted',
      submittedDate: new Date(),
      lastUpdated: new Date(),
      progress: 100,
      currentStep: 4,
      formData
    };
    
    onSave(updatedApp);
    onClose();
  };

  const updateField = (section: 'personal' | 'academic', field: string, value: string) => {
    setFormData(prev => ({
      ...prev,
      [section]: { ...prev[section], [field]: value }
    }));
  };

  return (
    <div className="fixed inset-0 z-50 bg-white flex flex-col animate-fade-in overflow-hidden h-screen h-[100dvh]">
        
        {/* Top Navigation Bar with Progress */}
        <div className="bg-white border-b border-slate-50 sticky top-0 z-20">
            <div className="max-w-6xl mx-auto px-6 md:px-10 py-6">
                <div className="flex items-center justify-between mb-6">
                    <div className="flex items-center gap-6">
                        <button 
                            onClick={handleSaveAndClose}
                            className="p-3 -ml-3 hover:bg-slate-50 rounded-full text-slate-400 hover:text-slate-900 transition-all"
                            title="Save & Exit"
                        >
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-6 h-6">
                                <path fillRule="evenodd" d="M11.03 3.97a.75.75 0 010 1.06l-6.22 6.22H21a.75.75 0 010 1.5H4.81l6.22 6.22a.75.75 0 11-1.06 1.06l-7.5-7.5a.75.75 0 010-1.06l7.5-7.5a.75.75 0 011.06 0z" clipRule="evenodd" />
                            </svg>
                        </button>
                        <div>
                            <p className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">
                                {isScholarship ? 'Scholarship Application' : 'University Application'}
                            </p>
                            <h1 className="text-2xl font-bold text-slate-900 tracking-tight break-words line-clamp-2">{targetName}</h1>
                        </div>
                    </div>
                    <div className="flex items-center gap-6">
                         <span className="text-sm font-bold text-slate-300 hidden md:inline-block uppercase tracking-widest">Step {currentStep} of {STEPS.length}</span>
                         <button onClick={handleSaveAndClose} className="text-sm font-bold text-slate-400 hover:text-slate-900 px-6 py-2.5 rounded-full hover:bg-slate-50 transition-all">
                             Save & Exit
                         </button>
                    </div>
                </div>

                {/* Progress Bars */}
                <div className="flex gap-3">
                    {STEPS.map((step) => {
                        const isActive = step.id === currentStep;
                        const isCompleted = step.id < currentStep;
                        return (
                            <div key={step.id} className="flex-1 flex flex-col gap-2">
                                <div className={`h-1.5 rounded-full transition-all duration-500 ${
                                    isActive ? 'bg-slate-900' : 
                                    isCompleted ? 'bg-slate-900' : 'bg-slate-100'
                                }`}></div>
                                <span className={`text-[10px] font-bold uppercase hidden md:block tracking-widest ${
                                    isActive ? 'text-slate-900' : 
                                    isCompleted ? 'text-slate-900' : 'text-slate-300'
                                }`}>{step.title}</span>
                            </div>
                        )
                    })}
                </div>
            </div>
        </div>

        {/* Main Content Area */}
        <div className="flex-1 overflow-y-auto bg-white">
            <div className="max-w-4xl mx-auto p-6 md:p-16">
                <div className="min-h-[60vh] flex flex-col">
                    
                    {currentStep === 1 && (
                        <div className="space-y-12 animate-fade-in">
                            <div>
                                <h2 className="text-4xl font-bold text-slate-900 tracking-tight mb-4">Let's start with the basics.</h2>
                                <p className="text-slate-500 text-lg font-medium">Please verify your personal contact information.</p>
                            </div>
                            
                            <div className="space-y-8">
                                <div>
                                    <label className="block text-sm font-bold text-slate-400 uppercase tracking-widest mb-3">Full Legal Name</label>
                                    <input 
                                        type="text" 
                                        className="w-full p-5 rounded-2xl border border-slate-50 bg-slate-50 focus:bg-white focus:border-slate-900 outline-none transition-all text-slate-900 font-bold text-lg"
                                        value={formData.personal?.fullName || ''}
                                        onChange={e => updateField('personal', 'fullName', e.target.value)}
                                    />
                                </div>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                                    <div>
                                        <label className="block text-sm font-bold text-slate-400 uppercase tracking-widest mb-3">Email Address</label>
                                        <input 
                                            type="email" 
                                            className="w-full p-5 rounded-2xl border border-slate-50 bg-slate-50 focus:bg-white focus:border-slate-900 outline-none transition-all text-slate-900 font-bold text-lg"
                                            value={formData.personal?.email || ''}
                                            onChange={e => updateField('personal', 'email', e.target.value)}
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-bold text-slate-400 uppercase tracking-widest mb-3">Phone Number</label>
                                        <input 
                                            type="tel" 
                                            className="w-full p-5 rounded-2xl border border-slate-50 bg-slate-50 focus:bg-white focus:border-slate-900 outline-none transition-all text-slate-900 font-bold text-lg"
                                            placeholder="+1 (555) 000-0000"
                                            value={formData.personal?.phone || ''}
                                            onChange={e => updateField('personal', 'phone', e.target.value)}
                                        />
                                    </div>
                                </div>
                                <div>
                                    <label className="block text-sm font-bold text-slate-400 uppercase tracking-widest mb-3">Mailing Address</label>
                                    <textarea 
                                        className="w-full p-5 rounded-2xl border border-slate-50 bg-slate-50 focus:bg-white focus:border-slate-900 outline-none transition-all text-slate-900 font-bold text-lg h-40 resize-none"
                                        placeholder="Street Address, City, State, Zip Code, Country"
                                        value={formData.personal?.address || ''}
                                        onChange={e => updateField('personal', 'address', e.target.value)}
                                    />
                                </div>
                            </div>
                        </div>
                    )}

                    {currentStep === 2 && (
                         <div className="space-y-12 animate-fade-in">
                             <div>
                                <h2 className="text-4xl font-bold text-slate-900 tracking-tight mb-4">Academic Profile</h2>
                                <p className="text-slate-500 text-lg font-medium">Share your educational background.</p>
                            </div>
                            <div className="space-y-8">
                                <div>
                                    <label className="block text-sm font-bold text-slate-400 uppercase tracking-widest mb-3">Intended Major</label>
                                    <input 
                                        type="text" 
                                        className="w-full p-5 rounded-2xl border border-slate-50 bg-slate-50 focus:bg-white focus:border-slate-900 outline-none transition-all text-slate-900 font-bold text-lg"
                                        value={formData.academic?.major || ''}
                                        onChange={e => updateField('academic', 'major', e.target.value)}
                                    />
                                </div>
                                <div>
                                    <label className="block text-sm font-bold text-slate-400 uppercase tracking-widest mb-3">Current GPA</label>
                                    <input 
                                        type="text" 
                                        className="w-full p-5 rounded-2xl border border-slate-50 bg-slate-50 focus:bg-white focus:border-slate-900 outline-none transition-all text-slate-900 font-bold text-lg"
                                        placeholder="e.g. 3.8/4.0 (or N/A)"
                                        value={formData.academic?.gpa || ''}
                                        onChange={e => updateField('academic', 'gpa', e.target.value)}
                                    />
                                </div>
                                <div className="border-2 border-dashed border-slate-100 rounded-3xl p-12 flex flex-col items-center justify-center text-center hover:bg-slate-50 transition-all cursor-pointer group">
                                    <div className="w-16 h-16 bg-slate-900 text-white rounded-full flex items-center justify-center mb-4 group-hover:scale-110 transition-transform shadow-xl shadow-slate-900/10">
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-6 h-6">
                                            <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5" />
                                        </svg>
                                    </div>
                                    <h4 className="text-xl font-bold text-slate-900">Upload Transcript</h4>
                                    <p className="text-slate-400 font-medium mt-2">Drag & drop or click to browse (PDF, DOCX)</p>
                                </div>
                            </div>
                         </div>
                    )}

                    {currentStep === 3 && (
                        <div className="space-y-8 animate-fade-in h-full flex flex-col">
                             <div>
                                <h2 className="text-4xl font-bold text-slate-900 tracking-tight mb-4">
                                    {isScholarship ? 'Statement of Purpose' : 'Personal Statement'}
                                </h2>
                                <p className="text-slate-500 text-lg font-medium">This is your chance to tell your story.</p>
                            </div>
                            <div className="bg-slate-50 p-6 rounded-2xl text-slate-600 text-lg leading-relaxed font-medium">
                                <strong className="text-slate-900 block mb-2 font-bold uppercase tracking-widest text-xs">Prompt:</strong> 
                                {isScholarship 
                                    ? `Explain why you are an ideal candidate for the ${targetName} and how this funding will impact your academic journey.`
                                    : `Why do you want to study at ${targetName} and how will this degree help you achieve your future goals?`
                                }
                            </div>
                            <textarea 
                                className="flex-1 w-full p-8 rounded-3xl border border-slate-50 bg-slate-50 focus:bg-white focus:border-slate-900 outline-none resize-none text-xl leading-relaxed transition-all font-bold text-slate-900 min-h-[400px]"
                                placeholder="Start writing your essay here..."
                                value={formData.essay}
                                onChange={e => setFormData(prev => ({ ...prev, essay: e.target.value }))}
                            />
                            <div className="flex justify-between items-center text-sm font-bold uppercase tracking-widest text-slate-300 pt-6">
                                <span>Recommended: 500 words</span>
                                <span className={`${(formData.essay?.length || 0) > 0 ? 'text-slate-900' : ''}`}>
                                    {formData.essay ? formData.essay.trim().split(/\s+/).filter(w => w.length > 0).length : 0} words
                                </span>
                            </div>
                        </div>
                    )}

                    {currentStep === 4 && (
                         <div className="space-y-12 animate-fade-in flex flex-col items-center justify-center h-full py-10">
                             <div className="w-24 h-24 bg-slate-900 text-white rounded-full flex items-center justify-center mb-8 shadow-2xl shadow-slate-900/20">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2.5} stroke="currentColor" className="w-10 h-10">
                                    <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                </svg>
                            </div>
                            <div className="text-center max-w-xl">
                                <h2 className="text-5xl font-bold text-slate-900 tracking-tight mb-6">Ready to Submit?</h2>
                                <p className="text-slate-500 text-xl font-medium">Please review your application details one last time before sending it.</p>
                            </div>

                            <div className="w-full bg-slate-50 rounded-3xl p-8 space-y-6 max-w-xl">
                                <div className="flex justify-between items-center border-b border-slate-100 pb-4">
                                    <span className="text-slate-400 font-bold uppercase tracking-widest text-xs">Full Name</span>
                                    <span className="font-bold text-slate-900 text-lg">{formData.personal?.fullName}</span>
                                </div>
                                <div className="flex justify-between items-center border-b border-slate-100 pb-4">
                                    <span className="text-slate-400 font-bold uppercase tracking-widest text-xs">Major</span>
                                    <span className="font-bold text-slate-900 text-lg">{formData.academic?.major}</span>
                                </div>
                                <div className="flex justify-between items-center">
                                    <span className="text-slate-400 font-bold uppercase tracking-widest text-xs">Essay Status</span>
                                    <span className="font-bold text-slate-900 flex items-center gap-2 text-lg">
                                        <div className="w-2 h-2 bg-slate-900 rounded-full"></div>
                                        Complete
                                    </span>
                                </div>
                            </div>

                            <label className="flex items-start gap-6 p-6 rounded-3xl cursor-pointer hover:bg-slate-50 transition-all max-w-xl text-left border border-transparent hover:border-slate-100">
                                <input type="checkbox" className="mt-1.5 w-6 h-6 text-slate-900 rounded-lg focus:ring-slate-900 border-slate-200" />
                                <span className="text-sm font-medium text-slate-500 leading-relaxed">
                                    I certify that all information submitted in the admission process—including this application and any other supporting materials—is my own work, factually true, and honestly presented.
                                </span>
                            </label>
                         </div>
                    )}

                    {/* Navigation Buttons */}
                    <div className="mt-auto pt-16 flex justify-between items-center">
                        {currentStep > 1 ? (
                             <button 
                                onClick={() => setCurrentStep(prev => prev - 1)}
                                className="px-10 py-4 rounded-full font-bold text-slate-400 hover:text-slate-900 hover:bg-slate-50 transition-all"
                            >
                                Back
                            </button>
                        ) : (
                            <div></div>
                        )}
                       
                        {currentStep < 4 ? (
                             <button 
                                onClick={() => setCurrentStep(prev => prev + 1)}
                                className="px-12 py-5 rounded-full bg-slate-900 text-white font-bold shadow-2xl shadow-slate-900/10 hover:bg-slate-800 hover:scale-105 transition-all flex items-center gap-3 text-lg"
                            >
                                Next Step
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2.5} stroke="currentColor" className="w-5 h-5">
                                    <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
                                </svg>
                            </button>
                        ) : (
                             <button 
                                onClick={handleSubmit}
                                className="px-12 py-5 rounded-full bg-slate-900 text-white font-bold shadow-2xl shadow-slate-900/10 hover:bg-slate-800 hover:scale-105 transition-all flex items-center gap-3 text-lg"
                            >
                                Submit Application
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-6 h-6">
                                    <path fillRule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12zm13.36-1.814a.75.75 0 10-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 00-1.06 1.06l2.25 2.25a.75.75 0 001.14-.094l3.75-5.25z" clipRule="evenodd" />
                                </svg>
                            </button>
                        )}
                    </div>
                </div>
            </div>
        </div>
    </div>
  );
};

export default ApplicationFormModal;
