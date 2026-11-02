
import React, { useState } from 'react';
import { MentorProfile } from '../types';
import MentorOnboarding from './MentorOnboarding'; 

interface MentorDashboardProps {
  profile: MentorProfile;
  onUpdateProfile: (profile: MentorProfile) => void;
  onLogout: () => void;
  onDeleteAccount: () => void;
}

const MentorDashboard: React.FC<MentorDashboardProps> = ({ profile, onUpdateProfile, onLogout, onDeleteAccount }) => {
  const [isEditing, setIsEditing] = useState(false);

  const handleToggleStatus = () => {
    onUpdateProfile({
        ...profile,
        isAvailable: !profile.isAvailable
    });
  };

  return (
    <div className="min-h-screen bg-beige-100 font-sans">
       {isEditing && (
           <div className="fixed inset-0 z-50 bg-black/60 flex items-center justify-center overflow-y-auto p-4 backdrop-blur-sm animate-fade-in">
               <div className="w-full max-w-xl relative bg-white shadow-2xl">
                   {/* Prominent Close Button */}
                   <button 
                     onClick={() => setIsEditing(false)} 
                     className="absolute -top-12 right-0 md:-right-12 text-white hover:text-slate-200 p-2 transition-transform hover:scale-110"
                     title="Close Modal"
                   >
                     <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2.5} stroke="currentColor" className="w-8 h-8">
                       <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                     </svg>
                   </button>
                   
                   {/* Mobile Close Button (Inside) */}
                   <button 
                     onClick={() => setIsEditing(false)} 
                     className="absolute top-2 right-2 md:hidden text-slate-400 hover:text-slate-600 p-2 z-10 bg-white/80 rounded-full"
                   >
                     <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-6 h-6">
                       <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                     </svg>
                   </button>
                   
                   <MentorOnboarding 
                        initialProfile={profile}
                        onComplete={(updated) => {
                            // Preserve the original ID when updating
                            onUpdateProfile({ ...profile, ...updated, id: profile.id }); 
                            setIsEditing(false);
                        }}
                        onCancel={() => setIsEditing(false)}
                        onDeleteAccount={onDeleteAccount}
                   />
               </div>
           </div>
       )}

       <nav className="bg-white border-b border-slate-200 px-6 py-4 flex justify-between items-center shadow-sm">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-brand-900 flex items-center justify-center text-white font-serif font-bold text-xl shadow-md">G</div>
            <div>
                <h1 className="font-serif text-xl font-bold text-brand-900 leading-tight">Gradwyn</h1>
                <p className="text-xs text-accent-gold font-heading uppercase tracking-wider">Mentor Portal</p>
            </div>
          </div>
          <button onClick={onLogout} className="text-xs font-bold uppercase tracking-widest text-brand-900 hover:text-accent-rust border border-slate-300 px-4 py-2 hover:bg-white transition-colors">Log Out</button>
       </nav>

       <div className="max-w-5xl mx-auto p-6 md:p-12">
           
           <div className="mb-8">
               <h2 className="text-3xl font-serif font-bold text-brand-900">Welcome back, {profile.name.split(' ')[0]}.</h2>
               <p className="text-slate-500 mt-1">Here is your impact overview for this semester.</p>
           </div>

           {/* Header Stats */}
           <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
                <div className="bg-white p-8 border-t-4 border-brand-700 shadow-sm flex flex-col items-center text-center hover:shadow-md transition-shadow">
                    <span className="text-5xl font-serif font-bold text-brand-900 mb-2">{profile.studentsGuided}</span>
                    <span className="text-xs font-bold text-slate-400 uppercase tracking-widest font-heading">Students Guided</span>
                </div>
                <div className="bg-white p-8 border-t-4 border-accent-gold shadow-sm flex flex-col items-center text-center hover:shadow-md transition-shadow">
                    <div className={`w-4 h-4 rounded-full mb-4 ${profile.isAvailable ? 'bg-green-500 animate-pulse shadow-[0_0_10px_rgba(34,197,94,0.5)]' : 'bg-red-400'}`}></div>
                    <span className="text-xl font-serif font-bold text-slate-700 mb-1">
                        {profile.isAvailable ? 'Active' : 'Busy'}
                    </span>
                    <button onClick={handleToggleStatus} className="text-xs underline text-slate-400 hover:text-brand-700 uppercase tracking-wider font-bold mt-2">
                        {profile.isAvailable ? 'Set to Busy' : 'Set to Available'}
                    </button>
                </div>
                <div className="bg-brand-900 p-8 border-t-4 border-brand-700 shadow-lg flex flex-col items-center text-center text-white relative overflow-hidden group">
                    <div className="absolute inset-0 bg-brand-800 opacity-0 group-hover:opacity-100 transition-opacity"></div>
                    <div className="relative z-10">
                        <span className="text-lg font-serif font-bold mb-2 block">Profile Visibility</span>
                        <p className="text-xs text-brand-200 mb-6">Your profile is currently <strong>{profile.isAvailable ? 'visible' : 'hidden'}</strong> in student searches.</p>
                        <button onClick={() => setIsEditing(true)} className="bg-white text-brand-900 px-6 py-3 text-xs font-bold uppercase tracking-widest hover:bg-brand-100 shadow-md">
                            Edit Profile
                        </button>
                    </div>
                </div>
           </div>

           {/* Profile Preview */}
           <div className="bg-white border border-slate-200 overflow-hidden shadow-sm">
               <div className="bg-beige-100 px-8 py-4 border-b border-slate-200 flex justify-between items-center">
                   <h3 className="font-heading font-bold uppercase tracking-widest text-slate-500 text-sm">Public Profile Preview</h3>
                   <span className="text-[10px] bg-brand-100 text-brand-700 px-2 py-1 font-bold uppercase tracking-wider">Live View</span>
               </div>
               <div className="p-10 flex flex-col md:flex-row gap-10">
                   <div className="shrink-0">
                       <img src={profile.photoUrl} alt={profile.name} className="w-40 h-40 object-cover border-4 border-white shadow-lg" />
                   </div>
                   <div className="flex-1">
                       <h2 className="text-3xl font-serif font-bold text-brand-900 mb-2">{profile.name}</h2>
                       <div className="flex flex-wrap gap-3 mb-6">
                           <span className="bg-brand-50 text-brand-800 px-3 py-1 text-xs font-bold uppercase tracking-wider border border-brand-100">{profile.university}</span>
                           <span className="bg-slate-50 text-slate-600 px-3 py-1 text-xs font-bold uppercase tracking-wider border border-slate-200">{profile.major}</span>
                       </div>
                       
                       <h4 className="font-bold text-slate-800 text-sm uppercase tracking-wider mb-2 border-b border-slate-100 pb-1 inline-block">About</h4>
                       <p className="text-slate-600 leading-relaxed mb-8 text-lg">{profile.bio}</p>

                       <div className="flex gap-6 pt-4 border-t border-slate-100">
                            <a href={profile.linkedin} target="_blank" rel="noreferrer" className="flex items-center gap-2 text-brand-700 font-bold text-xs uppercase tracking-widest border-b-2 border-transparent hover:border-brand-700 transition-all">
                                LinkedIn Profile
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="w-3 h-3">
                                    <path fillRule="evenodd" d="M5.22 14.78a.75.75 0 001.06 0l7.22-7.22v5.69a.75.75 0 001.5 0v-7.5a.75.75 0 00-.75-.75h-7.5a.75.75 0 000 1.5h5.69l-7.22 7.22a.75.75 0 000 1.06z" clipRule="evenodd" />
                                </svg>
                            </a>
                            <span className="text-slate-300">|</span>
                             <a href={`mailto:${profile.email}`} className="flex items-center gap-2 text-brand-700 font-bold text-xs uppercase tracking-widest border-b-2 border-transparent hover:border-brand-700 transition-all">
                                Contact Email
                            </a>
                       </div>
                   </div>
               </div>
           </div>

       </div>
    </div>
  );
};

export default MentorDashboard;
