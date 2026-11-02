
import React, { useState } from 'react';
import { MentorProfile } from '../types';
import { motion as mot, AnimatePresence } from 'motion/react';
import { AlertTriangle, Trash2 } from 'lucide-react';

interface MentorOnboardingProps {
  onComplete: (profile: MentorProfile) => void;
  initialName?: string;
  initialEmail?: string;
  initialPhoto?: string;
  initialProfile?: MentorProfile;
  onCancel?: () => void;
  onBack?: () => void;
  onDeleteAccount?: () => void;
}

const MentorOnboarding: React.FC<MentorOnboardingProps> = ({ 
    onComplete, 
    initialName = '', 
    initialEmail = '', 
    initialPhoto = '', 
    initialProfile,
    onCancel,
    onBack,
    onDeleteAccount
}) => {
  const [step, setStep] = useState(1);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [formData, setFormData] = useState<Partial<MentorProfile>>({
    name: initialProfile?.name || initialName,
    email: initialProfile?.email || initialEmail,
    photoUrl: initialProfile?.photoUrl || initialPhoto,
    university: initialProfile?.university || '',
    major: initialProfile?.major || '',
    bio: initialProfile?.bio || '',
    linkedin: initialProfile?.linkedin || '',
    studentsGuided: initialProfile?.studentsGuided || 0,
    isAvailable: initialProfile?.isAvailable ?? true,
    tags: initialProfile?.tags || []
  });
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
        const reader = new FileReader();
        reader.onload = (ev) => {
            setFormData(prev => ({ ...prev, photoUrl: ev.target?.result as string }));
        };
        reader.readAsDataURL(e.target.files[0]);
    }
  };

  const handleNext = () => {
    setError(null);
    if (step === 1) {
        if (!formData.name) {
            setError("Display Name is required.");
            return;
        }
        if (!formData.photoUrl) {
            setError("Headshot is required. Please upload an image or provide a URL.");
            return;
        }
        setStep(2);
    } else if (step === 2) {
        if (!formData.university || !formData.major) {
            setError("University and Major/Role are required.");
            return;
        }
        setStep(3);
    } else if (step === 3) {
        if (!formData.bio) {
            setError("Bio is required.");
            return;
        }
        setStep(4);
    } else if (step === 4) {
        // URL Validation for LinkedIn
        const linkedinRegex = /^(http(s)?:\/\/)?([\w]+\.)?linkedin\.com\/(pub|in|profile)/;
        if (!formData.linkedin || !linkedinRegex.test(formData.linkedin)) {
            setError("Please enter a valid LinkedIn URL.");
            return;
        }
        if (!formData.email) {
            setError("Email is required.");
            return;
        }
        
        // Complete
        const finalProfile: MentorProfile = {
            id: initialProfile?.id || Date.now().toString(),
            name: formData.name!,
            photoUrl: formData.photoUrl!,
            university: formData.university!,
            major: formData.major!,
            bio: formData.bio!,
            email: formData.email!,
            linkedin: formData.linkedin!,
            isAvailable: formData.isAvailable ?? true,
            studentsGuided: initialProfile?.studentsGuided || 0,
            tags: formData.tags && formData.tags.length > 0 ? formData.tags : [formData.major!, "Alumni"]
        };
        onComplete(finalProfile);
    }
  };

  return (
    <div className="min-h-screen bg-beige-50 flex flex-col items-center justify-center p-4 font-sans">
      <div className="w-full max-w-xl bg-white shadow-xl rounded-none border border-slate-200 overflow-hidden">
        <div className="h-1.5 bg-slate-100 w-full">
            <div className="h-full bg-brand-700 transition-all duration-500" style={{ width: `${(step / 4) * 100}%` }}></div>
        </div>

        <div className="p-8 md:p-12">
             <div className="mb-8 text-center">
                <span className="text-xs font-bold uppercase tracking-widest text-brand-600 mb-2 block">
                    {initialProfile ? 'Update Profile' : 'Mentor Profile Setup'}
                </span>
                <h2 className="text-3xl font-serif font-bold text-slate-900">
                    {step === 1 && "Identity & Presence"}
                    {step === 2 && "Academic Background"}
                    {step === 3 && "Your Story"}
                    {step === 4 && "Contact & Visibility"}
                </h2>
             </div>

             {error && (
                <div className="mb-6 bg-red-50 text-red-700 border border-red-200 p-3 text-sm font-bold rounded-none">
                    {error}
                </div>
             )}

             <div className="min-h-[200px]">
                {step === 1 && (
                    <div className="space-y-5">
                        <div>
                            <label className="block text-sm font-bold text-slate-700 mb-2 uppercase tracking-wider">Display Name</label>
                            <input 
                                type="text" 
                                value={formData.name || ''}
                                onChange={(e) => setFormData({...formData, name: e.target.value})}
                                className="w-full p-4 border border-slate-300 focus:border-brand-600 outline-none bg-white"
                                placeholder="e.g. Dr. Jane Doe"
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-bold text-slate-700 mb-2 uppercase tracking-wider">Headshot</label>
                            
                            <div className="flex items-center gap-4 mb-3">
                                <div className="w-20 h-20 bg-slate-100 border border-slate-300 overflow-hidden shrink-0">
                                    {formData.photoUrl ? (
                                        <img src={formData.photoUrl} alt="Preview" className="w-full h-full object-cover" />
                                    ) : (
                                        <div className="w-full h-full flex items-center justify-center text-slate-400">
                                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="w-8 h-8">
                                                <path fillRule="evenodd" d="M1 8a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 018.07 3h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0016.07 6H17a2 2 0 012 2v10a2 2 0 01-2 2H3a2 2 0 01-2-2V8zm13.5 3a4.5 4.5 0 11-9 0 4.5 4.5 0 019 0zM10 14a3 3 0 100-6 3 3 0 000 6z" clipRule="evenodd" />
                                            </svg>
                                        </div>
                                    )}
                                </div>
                                <div className="flex-1">
                                    <label className="cursor-pointer bg-brand-50 hover:bg-brand-100 text-brand-700 text-xs font-bold uppercase tracking-widest px-4 py-2 transition-colors border border-brand-200 block w-max mb-2">
                                        Upload Photo
                                        <input type="file" accept="image/*" className="hidden" onChange={handleFileChange} />
                                    </label>
                                    <p className="text-[10px] text-slate-400">Recommended: Square JPG/PNG, max 2MB</p>
                                </div>
                            </div>
                            <input 
                                type="text" 
                                value={formData.photoUrl || ''}
                                onChange={(e) => setFormData({...formData, photoUrl: e.target.value})}
                                className="w-full p-3 border border-slate-300 focus:border-brand-600 outline-none bg-white text-xs"
                                placeholder="Or paste image URL directly..."
                            />
                        </div>
                    </div>
                )}

                {step === 2 && (
                     <div className="space-y-5">
                        <div>
                            <label className="block text-sm font-bold text-slate-700 mb-2 uppercase tracking-wider">University / Institution</label>
                            <input 
                                type="text" 
                                value={formData.university || ''}
                                onChange={(e) => setFormData({...formData, university: e.target.value})}
                                className="w-full p-4 border border-slate-300 focus:border-brand-600 outline-none bg-white"
                                placeholder="e.g. Stanford University"
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-bold text-slate-700 mb-2 uppercase tracking-wider">Major / Professional Role</label>
                            <input 
                                type="text" 
                                value={formData.major || ''}
                                onChange={(e) => setFormData({...formData, major: e.target.value})}
                                className="w-full p-4 border border-slate-300 focus:border-brand-600 outline-none bg-white"
                                placeholder="e.g. Computer Science, Admissions Officer"
                            />
                        </div>
                    </div>
                )}

                {step === 3 && (
                    <div>
                         <label className="block text-sm font-bold text-slate-700 mb-2 uppercase tracking-wider">Short Bio</label>
                         <textarea 
                            value={formData.bio || ''}
                            onChange={(e) => setFormData({...formData, bio: e.target.value})}
                            className="w-full p-4 border border-slate-300 focus:border-brand-600 outline-none bg-white h-40 resize-none"
                            placeholder="Tell students about your experience and how you can help them..."
                        />
                    </div>
                )}

                {step === 4 && (
                    <div className="space-y-5">
                         <div>
                            <label className="block text-sm font-bold text-slate-700 mb-2 uppercase tracking-wider">Contact Email</label>
                            <input 
                                type="email" 
                                value={formData.email || ''}
                                onChange={(e) => setFormData({...formData, email: e.target.value})}
                                className="w-full p-4 border border-slate-300 focus:border-brand-600 outline-none bg-white"
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-bold text-slate-700 mb-2 uppercase tracking-wider">LinkedIn Profile URL</label>
                            <input 
                                type="text" 
                                value={formData.linkedin || ''}
                                onChange={(e) => setFormData({...formData, linkedin: e.target.value})}
                                className="w-full p-4 border border-slate-300 focus:border-brand-600 outline-none bg-white"
                                placeholder="https://linkedin.com/in/..."
                            />
                        </div>
                        <div className="pt-4 border-t border-slate-100">
                            <label className="flex items-center gap-3 cursor-pointer">
                                <div className="relative">
                                    <input 
                                        type="checkbox" 
                                        className="sr-only peer"
                                        checked={formData.isAvailable}
                                        onChange={(e) => setFormData({...formData, isAvailable: e.target.checked})}
                                    />
                                    <div className="w-11 h-6 bg-slate-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-brand-600"></div>
                                </div>
                                <span className="text-sm font-bold text-slate-700 uppercase tracking-wider">
                                    Accepting New Students
                                </span>
                            </label>
                            <p className="text-xs text-slate-500 mt-2 ml-14">
                                If disabled, you will not appear in student searches.
                            </p>
                        </div>

                        {initialProfile && (
                            <div className="pt-8 mt-8 border-t border-red-50">
                                <h3 className="text-xs font-bold text-red-900 uppercase tracking-widest mb-3 flex items-center gap-2">
                                    <AlertTriangle size={14} />
                                    Danger Zone
                                </h3>
                                <p className="text-[10px] text-red-600/70 mb-4 font-medium italic">
                                    Deleting your account is permanent. All mentor profile data and student guidance history will be lost.
                                </p>
                                <button 
                                    onClick={() => setShowDeleteConfirm(true)}
                                    className="text-[10px] font-bold uppercase tracking-widest text-red-600 hover:text-white hover:bg-red-600 border border-red-200 hover:border-red-600 px-4 py-2.5 transition-all flex items-center gap-2"
                                >
                                    <Trash2 size={12} />
                                    Delete My Account
                                </button>
                            </div>
                        )}
                    </div>
                )}
             </div>

             <div className="flex justify-between mt-10 pt-6 border-t border-slate-100 items-center">
                <div className="flex gap-4">
                     {onCancel && (
                        <button 
                            onClick={onCancel}
                            className="text-slate-400 font-bold uppercase tracking-wider text-sm hover:text-red-600"
                        >
                            Cancel
                        </button>
                     )}
                     <button 
                        onClick={() => {
                            if (step > 1) setStep(s => s - 1);
                            else if (onBack) onBack();
                        }}
                        className={`text-slate-500 font-bold uppercase tracking-wider text-sm hover:text-slate-800 ${step === 1 && !onBack ? 'opacity-0 pointer-events-none' : ''}`}
                    >
                        Back
                    </button>
                </div>
               
                <button 
                    onClick={handleNext}
                    className="px-8 py-3 bg-brand-700 text-white font-bold uppercase tracking-widest text-sm hover:bg-brand-800 transition-colors shadow-lg"
                >
                    {step === 4 ? (initialProfile ? 'Save Changes' : 'Create Profile') : 'Next Step'}
                </button>
             </div>
        </div>
      </div>

      {/* Delete Confirmation Modal for Mentors */}
      <AnimatePresence>
        {showDeleteConfirm && (
          <div className="fixed inset-0 z-[110] flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm">
            <mot.div 
              initial={{ opacity: 0, scale: 0.95, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: 20 }}
              className="bg-white rounded-none shadow-2xl w-full max-w-md overflow-hidden flex flex-col border border-slate-200"
            >
              <div className="p-10 text-center">
                <div className="w-16 h-16 bg-red-50 text-red-600 rounded-none flex items-center justify-center mx-auto mb-6 border border-red-100">
                  <AlertTriangle size={32} />
                </div>
                <h3 className="text-2xl font-serif font-bold text-slate-900 mb-2">Delete Account?</h3>
                <p className="text-slate-500 mb-8 font-medium text-sm">
                  This action is irreversible. All your mentor records and data will be permanently purged from the Gradwyn archives.
                </p>
                
                <div className="flex flex-col gap-3">
                  <button 
                    onClick={() => {
                       onDeleteAccount?.();
                       setShowDeleteConfirm(false);
                    }}
                    className="w-full py-4 bg-red-600 text-white font-bold uppercase tracking-widest text-xs hover:bg-red-700 transition-all shadow-lg flex items-center justify-center gap-3"
                  >
                    <Trash2 size={16} />
                    Yes, Delete Permanently
                  </button>
                  <button 
                    onClick={() => setShowDeleteConfirm(false)}
                    className="w-full py-4 bg-white border border-slate-200 text-slate-400 font-bold uppercase tracking-widest text-xs hover:text-slate-900 hover:border-slate-900 transition-all"
                  >
                    No, Cancel
                  </button>
                </div>
              </div>
            </mot.div>
          </div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default MentorOnboarding;
