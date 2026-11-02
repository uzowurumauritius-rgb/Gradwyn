import React, { useState, useRef, useEffect } from 'react';
import { UserProfile, University, Mentor, Application, Scholarship, Guide } from '../types';
import { MOCK_MENTORS, MOCK_DATABASE_UNIVERSITIES, AUTOCOMPLETE_UNIVERSITIES, MOCK_SCHOLARSHIPS, MOCK_GUIDES } from '../constants';
import UniversityCard from './UniversityCard';
import EditProfileModal from './EditProfileModal';
import ApplicationFormModal from './ApplicationFormModal';
import FeedbackModal from './FeedbackModal';

interface DashboardProps {
  profile: UserProfile;
  savedSchools: University[];
  applications: Application[];
  onDiscardSchool: (id: string) => void;
  onSaveSchool: (school: University) => void;
  onUpdateApplication: (app: Application) => void;
  onWithdrawApplication: (appId: string) => void;
  renderChat: () => React.ReactNode;
  onUpdateProfile: (newProfile: UserProfile) => void;
  onLogout: () => void;
  onDeleteAccount: () => void;
}

type DashboardView = 'schools' | 'mentors' | 'chat' | 'scholarships' | 'tracker' | 'forum' | 'guides' | 'prep';

const SidebarItem: React.FC<{ 
  view: DashboardView; 
  currentView: DashboardView; 
  label: string; 
  icon: React.ReactNode; 
  onClick: () => void 
}> = ({ view, currentView, label, icon, onClick }) => (
    <button 
        onClick={onClick}
        className={`w-full flex items-center gap-3 px-4 py-2.5 transition-all text-sm font-medium rounded-full
            ${currentView === view 
                ? 'bg-slate-100 text-slate-900' 
                : 'text-slate-500 hover:bg-slate-50 hover:text-slate-700'}`}
    >
        <span className="opacity-70">{icon}</span>
        <span>{label}</span>
    </button>
);

const ScholarshipDetailModal = ({
    scholarship,
    onClose,
    onApply
}: {
    scholarship: Scholarship;
    onClose: () => void;
    onApply: (scholarship: Scholarship) => void;
}) => {
    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/10 backdrop-blur-xl animate-fade-in">
            <div className="bg-white rounded-[40px] shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto flex flex-col relative border border-slate-50">
                <button onClick={onClose} className="absolute top-8 right-8 text-slate-400 hover:text-slate-900 p-3 z-10 hover:bg-slate-50 rounded-full transition-all">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2.5} stroke="currentColor" className="w-5 h-5">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>

                <div className="h-64 bg-slate-900 relative overflow-hidden shrink-0">
                    <div className="absolute inset-0 bg-gradient-to-t from-slate-900/90 via-slate-900/40 to-transparent"></div>
                    <div className="absolute bottom-0 left-0 p-12">
                        <p className="text-white/60 font-bold uppercase tracking-[0.2em] text-[10px] mb-3">{scholarship.provider}</p>
                        <h2 className="text-4xl md:text-5xl font-bold text-white tracking-tight leading-tight break-words line-clamp-3">{scholarship.name}</h2>
                    </div>
                </div>

                <div className="p-12 space-y-12">
                    <div className="flex flex-wrap gap-4">
                        <div className="bg-slate-900 text-white px-8 py-4 rounded-3xl font-bold text-lg shadow-2xl shadow-slate-900/20">
                            {scholarship.amount}
                        </div>
                        <div className="bg-slate-50 text-slate-600 px-6 py-4 rounded-3xl font-bold border border-slate-50 flex items-center gap-3">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-5 h-5 opacity-40">
                                <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            Deadline: {scholarship.deadline}
                        </div>
                    </div>

                    <div className="space-y-6">
                        <h3 className="text-sm font-bold text-slate-400 uppercase tracking-widest">About the Scholarship</h3>
                        <p className="text-xl text-slate-600 leading-relaxed font-medium break-words">{scholarship.description}</p>
                    </div>

                    <div className="space-y-6">
                         <h3 className="text-sm font-bold text-slate-400 uppercase tracking-widest">Eligibility & Focus</h3>
                         <div className="flex flex-wrap gap-3">
                             {scholarship.tags?.map(tag => (
                                 <span key={tag} className="px-6 py-3 bg-white border border-slate-100 rounded-full text-slate-900 font-bold shadow-sm">
                                     {tag}
                                 </span>
                             ))}
                         </div>
                    </div>
                </div>

                <div className="p-10 border-t border-slate-50 bg-white/80 backdrop-blur-md flex justify-end gap-6 sticky bottom-0">
                    <button onClick={onClose} className="px-8 py-4 font-bold text-slate-400 hover:text-slate-900 transition-all">Close</button>
                    <button 
                        onClick={() => onApply(scholarship)}
                        className="px-12 py-4 bg-slate-900 text-white font-bold rounded-full shadow-2xl shadow-slate-900/20 hover:bg-slate-800 transition-all hover:scale-105 text-lg"
                    >
                        Apply Now
                    </button>
                </div>
            </div>
        </div>
    )
}

const SchoolProfileView = ({ 
    uni, 
    onClose, 
    profile, 
    onStartApplication 
}: { 
    uni: University; 
    onClose: () => void; 
    profile: UserProfile;
    onStartApplication: (uni: University) => void; 
}) => {
  const [coverError, setCoverError] = useState(false);
  const [logoError, setLogoError] = useState(false);

  // Get initials for fallback
  const initials = uni.name
    .split(' ')
    .filter(word => !['of', 'the', 'and', '&', 'at'].includes(word.toLowerCase()))
    .map(word => word[0])
    .join('')
    .toUpperCase()
    .slice(0, 3);

  return (
  <div className="bg-white animate-fade-in flex flex-col w-full min-h-full overflow-x-hidden">
      {/* Header Image & Title */}
      <div className="min-h-[500px] md:h-[450px] lg:h-[550px] relative bg-slate-950 flex items-center justify-center overflow-hidden">
         <div className="absolute inset-0 bg-gradient-to-t from-slate-900/90 via-slate-900/50 to-slate-900/30 z-10"></div>
         
         {(!coverError && uni.images && uni.images[0]) ? (
           <img 
              src={uni.images[0]} 
              alt="Campus" 
              className="absolute inset-0 w-full h-full object-cover opacity-50"
              onError={() => setCoverError(true)}
           />
         ) : (
           <div className="absolute inset-0 flex flex-col items-center justify-center p-8 opacity-20">
              <span className="font-serif italic text-[20vw] text-white tracking-tighter select-none leading-none">
                {initials}
              </span>
           </div>
         )}
         
         <button 
            onClick={onClose}
            className="absolute top-6 left-6 md:top-8 md:left-8 bg-slate-900/60 hover:bg-black text-white p-3 md:p-4 rounded-full shadow-2xl transition-all backdrop-blur-xl border border-white/20 z-50 cursor-pointer group"
            aria-label="Back to Dashboard"
         >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2.5} stroke="currentColor" className="w-5 h-5 md:w-6 md:h-6 group-hover:-translate-x-1 transition-transform">
                <path strokeLinecap="round" strokeLinejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
            </svg>
         </button>

          <div className="absolute inset-x-0 bottom-8 md:bottom-16 px-6 md:px-16 flex flex-col lg:flex-row lg:items-end justify-between gap-8">
            <div className="flex flex-col items-center text-center lg:flex-row lg:items-center lg:text-left gap-4 md:gap-8 min-w-0 w-full lg:w-auto">
                <div className="w-20 h-20 md:w-32 md:h-32 bg-slate-950 p-1.5 md:p-2 rounded-2xl md:rounded-3xl shadow-2xl shrink-0 border border-white/10 flex items-center justify-center overflow-hidden">
                    {(!logoError && uni.logo) ? (
                        <img 
                            src={uni.logo} 
                            alt={uni.name} 
                            className="w-full h-full object-contain"
                            onError={() => setLogoError(true)}
                        />
                    ) : (
                        <span className="font-serif italic text-2xl md:text-4xl text-white/80 select-none">
                           {initials}
                        </span>
                    )}
                </div>
                <div className="flex-1 min-w-0">
                    <h1 className="text-3xl md:text-5xl lg:text-6xl font-bold text-white tracking-tight mb-2 md:mb-4 break-words leading-tight drop-shadow-lg">{uni.name}</h1>
                    <div className="flex items-center justify-center lg:justify-start gap-2 md:gap-3 text-white/80 font-bold uppercase tracking-widest text-[10px] md:text-xs">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="w-3 h-3 md:w-4 md:h-4 shrink-0">
                            <path fillRule="evenodd" d="M9.69 18.933l.003.001C9.89 19.02 10 19 10 19s.11.02.308-.066l.002-.001.006-.003.018-.008a5.741 5.741 0 00.281-.14c.186-.096.446-.24.757-.433.62-.384 1.445-.966 2.274-1.765C15.302 14.988 17 12.493 17 9A7 7 0 103 9c0 3.492 1.698 5.988 3.355 7.584a13.731 13.731 0 002.273 1.765 11.842 11.842 0 00.976.544l.062.029.018.008.006.003zM10 11.25a2.25 2.25 0 100-4.5 2.25 2.25 0 000 4.5z" clipRule="evenodd" />
                        </svg>
                        <span>{uni.location}</span>
                    </div>
                </div>
            </div>
            <div className="flex flex-col sm:flex-row items-stretch lg:items-center gap-4 shrink-0 w-full lg:w-auto">
                <button 
                    onClick={() => onStartApplication(uni)}
                    className="bg-white text-slate-900 px-8 md:px-10 py-4 md:py-5 rounded-full font-bold text-base md:text-lg shadow-2xl hover:bg-slate-50 transition-all hover:scale-105"
                >
                    Start Application
                </button>
                {uni.website && (
                    <a 
                        href={uni.website}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="bg-white/10 backdrop-blur-xl text-white border border-white/20 px-8 md:px-10 py-4 md:py-5 rounded-full font-bold text-base md:text-lg shadow-2xl hover:bg-white/20 transition-all hover:scale-105 flex items-center justify-center gap-3"
                    >
                        Visit Website
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="w-5 h-5 opacity-50">
                            <path fillRule="evenodd" d="M4.25 5.5a.75.75 0 00-.75.75v8.5c0 .414.336.75.75.75h8.5a.75.75 0 00.75-.75v-4a.75.75 0 011.5 0v4A2.25 2.25 0 0112.75 17h-8.5A2.25 2.25 0 012 14.75v-8.5A2.25 2.25 0 014.25 4h5a.75.75 0 010 1.5h-5z" clipRule="evenodd" />
                            <path fillRule="evenodd" d="M6.194 12.753a.75.75 0 001.06.053L16.5 4.44v2.81a.75.75 0 001.5 0v-4.5a.75.75 0 00-.75-.75h-4.5a.75.75 0 000 1.5h2.553l-9.056 8.194a.75.75 0 00-.053 1.06z" clipRule="evenodd" />
                        </svg>
                    </a>
                )}
            </div>
         </div>
      </div>

      <div className="p-6 md:p-10 lg:p-16 bg-white w-full">
          <div className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-10 md:gap-16 w-full">
              <div className="lg:col-span-2 space-y-10 md:space-y-16">
                  <section>
                      <h3 className="text-[10px] md:text-sm font-bold text-slate-400 uppercase tracking-widest mb-4 md:mb-6">About the University</h3>
                      <p className="text-lg md:text-xl text-slate-600 leading-relaxed font-medium">{uni.description}</p>
                  </section>

                  <section className="grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-8">
                      {[
                          { label: 'Acceptance Rate', value: uni.acceptanceRate },
                          { label: 'Avg. Tuition', value: uni.tuition },
                          { label: 'Ranking', value: uni.ranking },
                          { label: 'Student Body', value: uni.studentBody }
                      ].map(stat => (
                          <div key={stat.label} className="p-4 md:p-6 bg-slate-50 rounded-2xl md:rounded-3xl border border-slate-50">
                              <p className="text-[8px] md:text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-1 md:mb-2">{stat.label}</p>
                              <p className="text-lg md:text-xl lg:text-2xl font-bold text-slate-900 break-words" title={stat.value}>{stat.value}</p>
                          </div>
                      ))}
                  </section>

                  <section>
                      <h3 className="text-sm font-bold text-slate-400 uppercase tracking-widest mb-6">Popular Programs</h3>
                      <div className="flex flex-wrap gap-3">
                          {uni.programs?.map(prog => (
                              <span key={prog} className="px-6 py-3 bg-white border border-slate-100 rounded-full text-slate-900 font-bold shadow-sm">
                                  {prog}
                              </span>
                          ))}
                      </div>
                  </section>
              </div>

              <div className="space-y-12">
                  <div className="p-8 bg-slate-900 rounded-[40px] text-white shadow-2xl shadow-slate-900/20">
                      <h3 className="text-2xl font-bold mb-6 tracking-tight">Intelligence Match</h3>
                      <div className="space-y-6">
                          <div className="flex items-center justify-between">
                              <span className="text-slate-400 font-bold uppercase tracking-widest text-[10px]">Overall Score</span>
                              <span className="text-3xl font-bold">{uni.matchScore}%</span>
                          </div>
                          <div className="h-2 bg-white/10 rounded-full overflow-hidden">
                              <div className="h-full bg-white rounded-full" style={{ width: `${uni.matchScore}%` }}></div>
                          </div>
                          <p className="text-slate-400 text-sm leading-relaxed font-medium">
                              Based on your profile in {profile.fieldOfStudy}, this university offers exceptional alignment with your academic and career goals.
                          </p>
                      </div>
                  </div>

                  <div className="p-8 bg-slate-50 rounded-[40px] border border-slate-50">
                      <h3 className="text-xl font-bold text-slate-900 mb-6 tracking-tight">Key Deadlines</h3>
                      <div className="space-y-6">
                          <div className="flex items-center gap-4">
                              <div className="w-10 h-10 bg-white rounded-2xl flex items-center justify-center text-slate-900 shadow-sm border border-slate-100">
                                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-5 h-5">
                                      <path strokeLinecap="round" strokeLinejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 012.25-2.25h13.5A2.25 2.25 0 0121 7.5v11.25m-18 0A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75m-18 0v-7.5A2.25 2.25 0 015.25 9h13.5A2.25 2.25 0 0121 11.25v7.5" />
                                  </svg>
                              </div>
                              <div>
                                  <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Early Action</p>
                                  <p className="font-bold text-slate-900">Nov 1, 2024</p>
                              </div>
                          </div>
                          <div className="flex items-center gap-4">
                              <div className="w-10 h-10 bg-white rounded-2xl flex items-center justify-center text-slate-900 shadow-sm border border-slate-100">
                                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-5 h-5">
                                      <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
                                  </svg>
                              </div>
                              <div>
                                  <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Regular Decision</p>
                                  <p className="font-bold text-slate-900">Jan 15, 2025</p>
                              </div>
                          </div>
                      </div>
                  </div>
              </div>
          </div>
      </div>
  </div>
  );
};

const Dashboard: React.FC<DashboardProps> = ({ 
    profile, 
    savedSchools, 
    applications,
    onDiscardSchool, 
    onSaveSchool, 
    onUpdateApplication,
    onWithdrawApplication,
    renderChat, 
    onUpdateProfile, 
    onLogout,
    onDeleteAccount
}) => {
  const [currentView, setCurrentView] = useState<DashboardView>('schools');
  const [selectedSchool, setSelectedSchool] = useState<University | null>(null);
  const [selectedScholarship, setSelectedScholarship] = useState<Scholarship | null>(null); // New state for scholarship modal

  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [isFeedbackModalOpen, setIsFeedbackModalOpen] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isProfileDropdownOpen, setIsProfileDropdownOpen] = useState(false);
  
  // Scholarship State
  const [scholarshipTab, setScholarshipTab] = useState<'all' | 'forYou'>('all');
  const [scholarshipFilter, setScholarshipFilter] = useState<string>('All');
  
  // Tracker State
  const [trackerTab, setTrackerTab] = useState<'universities' | 'scholarships'>('universities');

  // Application Modal State
  const [isAppModalOpen, setIsAppModalOpen] = useState(false);
  const [currentApp, setCurrentApp] = useState<Application | null>(null);
  const [appUniversity, setAppUniversity] = useState<University | null>(null);
  const [appScholarship, setAppScholarship] = useState<Scholarship | null>(null); // New state for scholarship app

  // Search State
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<University[]>([]);
  const [isSearchFocused, setIsSearchFocused] = useState(false);
  const searchRef = useRef<HTMLDivElement>(null);
  const profileDropdownRef = useRef<HTMLDivElement>(null);

  // Handle Search Logic
  useEffect(() => {
    if (searchQuery.trim().length > 1) {
        const query = searchQuery.toLowerCase();
        const results = AUTOCOMPLETE_UNIVERSITIES.filter(uni => 
            uni.name.toLowerCase().includes(query) || 
            uni.location.toLowerCase().includes(query)
        );
        setSearchResults(results.slice(0, 5)); // Limit to 5 results
    } else {
        setSearchResults([]);
    }
  }, [searchQuery]);

  // Click outside search or profile dropdown to close
  useEffect(() => {
      const handleClickOutside = (event: MouseEvent) => {
          if (searchRef.current && !searchRef.current.contains(event.target as Node)) {
              setIsSearchFocused(false);
          }
          if (profileDropdownRef.current && !profileDropdownRef.current.contains(event.target as Node)) {
              setIsProfileDropdownOpen(false);
          }
      };
      document.addEventListener('mousedown', handleClickOutside);
      return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSearchResultClick = (uni: University) => {
      // Check if already saved
      if (!savedSchools.some(s => s.id === uni.id)) {
          onSaveSchool(uni);
      }
      setSelectedSchool(uni);
      setSearchQuery('');
      setSearchResults([]);
      setIsSearchFocused(false);
  };

  const handleStartApplication = (uni: University) => {
      // Check if we already have an application
      const existingApp = applications.find(a => a.university?.id === uni.id);
      
      if (existingApp) {
          setCurrentApp(existingApp);
          setAppUniversity(null);
          setAppScholarship(null);
      } else {
          setCurrentApp(null);
          setAppUniversity(uni);
          setAppScholarship(null);
      }
      
      setIsAppModalOpen(true);
      setSelectedSchool(null); // Close profile view if open
  };
  
  const handleStartScholarshipApplication = (scholarship: Scholarship) => {
      const existingApp = applications.find(a => a.scholarship?.id === scholarship.id);

      if (existingApp) {
          setCurrentApp(existingApp);
          setAppScholarship(null);
          setAppUniversity(null);
      } else {
          setCurrentApp(null);
          setAppScholarship(scholarship);
          setAppUniversity(null);
      }

      setIsAppModalOpen(true);
      setSelectedScholarship(null);
  };

  const handleResumeApplication = (app: Application) => {
      setCurrentApp(app);
      setAppUniversity(null);
      setAppScholarship(null);
      setIsAppModalOpen(true);
  };

  // If user has no saved schools, show some recommendations from "database"
  const displaySchools = savedSchools.length > 0 ? savedSchools : MOCK_DATABASE_UNIVERSITIES;
  const isFallback = savedSchools.length === 0;

  const handleSidebarClick = (view: DashboardView) => {
      setCurrentView(view);
      setSelectedSchool(null);
      setSelectedScholarship(null);
      setIsMobileMenuOpen(false); // Close menu on mobile
  };

  const handleProfileUpdateWithRedirect = (newProfile: UserProfile) => {
      onUpdateProfile(newProfile);
      // Force redirect to Chat View to engage with AI
      setCurrentView('chat');
  };

  // Scholarship Filtering Logic
  const getScholarships = () => {
      let filtered = MOCK_SCHOLARSHIPS;
      
      // For You Logic: Strict match on Degree Level + loose match on location/keywords
      if (scholarshipTab === 'forYou') {
          // Normalize the profile degree to match common tag formats
          const userDegreeTag = profile.degreeLevel === "Bachelor's" 
              ? "Bachelors" 
              : profile.degreeLevel === "Master's" 
                  ? "Masters" 
                  : profile.degreeLevel;

          filtered = filtered.filter(sch => {
              const hasDegreeMatch = sch.tags.some(t => t === userDegreeTag || t === 'All Fields');
              const locationMatch = profile.preferredLocations.some(loc => sch.location?.includes(loc) || sch.tags.some(t => t.includes(loc)));
              return hasDegreeMatch || (locationMatch && hasDegreeMatch);
          });
      }

      if (scholarshipFilter !== 'All') {
          filtered = filtered.filter(sch => sch.tags.includes(scholarshipFilter));
      }

      return filtered;
  };
  
  // Filter applications for tracker
  const displayedApplications = applications.filter(app => {
      if (trackerTab === 'universities') return app.type === 'university' || (!app.type && app.university); // Handle legacy
      if (trackerTab === 'scholarships') return app.type === 'scholarship';
      return true;
  });

  const SidebarContent = () => (
    <div className="flex flex-col h-full bg-white">
        <div className="p-8">
            <div className="flex items-center gap-4 mb-10">
                <div 
                    onClick={() => setIsEditModalOpen(true)}
                    className="w-12 h-12 rounded-full overflow-hidden border-2 border-slate-100 shrink-0 cursor-pointer hover:border-brand-200 transition-colors"
                >
                    <img 
                        src={profile.photoUrl || `https://ui-avatars.com/api/?name=${profile.name || 'User'}&background=f1f5f9&color=475569`} 
                        alt="User" 
                        className="w-full h-full object-cover"
                    />
                </div>
                <div>
                    <h1 className="text-2xl font-bold tracking-tight text-slate-900 leading-none">Gradwyn</h1>
                    <p className="text-[10px] text-slate-400 font-bold uppercase tracking-widest mt-1">Intelligent Search</p>
                </div>
            </div>
        </div>
        
        <nav className="flex-1 px-4 space-y-1 overflow-y-auto no-scrollbar">
            <SidebarItem 
                view="schools"
                currentView={currentView} 
                label="Institutions" 
                onClick={() => handleSidebarClick('schools')}
                icon={<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-5 h-5"><path strokeLinecap="round" strokeLinejoin="round" d="M12 21v-8.25M15.75 21v-8.25M8.25 21v-8.25M3 9l9-6 9 6m-1.5 12V10.332A48.36 48.36 0 0012 9.75c-2.551 0-5.056.2-7.5.582V21M3 21h18M12 6.75h.008v.008H12V6.75z" /></svg>}
            />
            <SidebarItem 
                view="tracker" 
                currentView={currentView}
                label="Applications" 
                onClick={() => handleSidebarClick('tracker')}
                icon={<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-5 h-5"><path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" /></svg>}
            />
            <SidebarItem 
                view="mentors" 
                currentView={currentView}
                label="Mentorship" 
                onClick={() => handleSidebarClick('mentors')}
                icon={<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-5 h-5"><path strokeLinecap="round" strokeLinejoin="round" d="M18 18.72a9.094 9.094 0 003.741-.479 3 3 0 00-4.656-5.64 9.039 9.039 0 00-6.225 9.24M15 12a3 3 0 11-6 0 3 3 0 016 0zm-9 6a9 9 0 1118 0 9 9 0 01-18 0z" /></svg>}
            />
            <SidebarItem 
                view="scholarships" 
                currentView={currentView}
                label="Scholarships" 
                onClick={() => handleSidebarClick('scholarships')}
                icon={<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-5 h-5"><path strokeLinecap="round" strokeLinejoin="round" d="M12 6v12m-3-2.818l.879.659c1.171.879 3.07.879 4.242 0 1.172-.879 1.172-2.303 0-3.182C13.536 12.219 12.768 12 12 12c-.725 0-1.45-.22-2.003-.659-1.106-.879-1.106-2.303 0-3.182s2.9-.879 4.006 0l.415.33M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>}
            />
            <SidebarItem 
                view="chat" 
                currentView={currentView}
                label="Intelligence" 
                onClick={() => handleSidebarClick('chat')}
                icon={<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-5 h-5"><path strokeLinecap="round" strokeLinejoin="round" d="M12 18.75a6 6 0 006-6v-1.5m-6 7.5a6 6 0 01-6-6v-1.5m6 7.5v3.75m-3.75 0h7.5M12 15.75a3 3 0 01-3-3V4.5a3 3 0 116 0v8.25a3 3 0 01-3 3z" /></svg>}
            />
            <SidebarItem 
                view="prep" 
                currentView={currentView}
                label="Prep Suite" 
                onClick={() => handleSidebarClick('prep')}
                icon={<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-5 h-5"><path strokeLinecap="round" strokeLinejoin="round" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18c-2.305 0-4.408.867-6 2.292m0-14.25v14.25" /></svg>}
            />
            <SidebarItem 
                view="guides" 
                currentView={currentView}
                label="Guides" 
                onClick={() => handleSidebarClick('guides')}
                icon={<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-5 h-5"><path strokeLinecap="round" strokeLinejoin="round" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18c-2.305 0-4.408.867-6 2.292m0-14.25v14.25" /></svg>}
            />
        </nav>

        <div className="p-6 mt-auto border-t border-slate-50">
            <SidebarItem 
                view="tracker" 
                currentView={currentView}
                label="Settings" 
                onClick={() => setIsEditModalOpen(true)}
                icon={<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-5 h-5"><path strokeLinecap="round" strokeLinejoin="round" d="M10.5 6h9.75M10.5 6a1.5 1.5 0 11-3 0m3 0a1.5 1.5 0 10-3 0M3.75 6H7.5m3 12h9.75m-9.75 0a1.5 1.5 0 11-3 0m3 0a1.5 1.5 0 10-3 0m-3.75 0H7.5m9-6h3.75m-3.75 0a1.5 1.5 0 11-3 0m3 0a1.5 1.5 0 10-3 0M3.75 12h12.75" /></svg>}
            />
            <button 
                onClick={() => onLogout()}
                className="w-full mt-2 flex items-center gap-3 px-4 py-3 text-red-500 hover:text-red-700 hover:bg-red-50 rounded-xl transition-all font-bold text-sm text-left"
            >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-5 h-5">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6A2.25 2.25 0 005.25 5.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15M12 9l-3 3m0 0l3 3m-3-3h12.75" />
                </svg>
                Sign Out
            </button>
        </div>
    </div>
  );

  return (
    <div className="flex h-screen h-[100dvh] bg-white font-sans overflow-hidden">
      <EditProfileModal 
        isOpen={isEditModalOpen} 
        onClose={() => setIsEditModalOpen(false)} 
        profile={profile} 
        onSave={handleProfileUpdateWithRedirect}
        onDeleteAccount={onDeleteAccount}
      />

      <FeedbackModal 
        isOpen={isFeedbackModalOpen}
        onClose={() => setIsFeedbackModalOpen(false)}
        userEmail={profile.email}
      />

      <ApplicationFormModal
         isOpen={isAppModalOpen}
         onClose={() => setIsAppModalOpen(false)}
         application={currentApp}
         university={appUniversity}
         scholarship={appScholarship}
         userProfile={profile}
         onSave={onUpdateApplication}
      />

      {selectedScholarship && (
          <ScholarshipDetailModal 
             scholarship={selectedScholarship}
             onClose={() => setSelectedScholarship(null)}
             onApply={handleStartScholarshipApplication}
          />
      )}

      {/* Mobile Menu Backdrop */}
      {isMobileMenuOpen && (
        <div 
            className="fixed inset-0 bg-slate-900/70 z-50 md:hidden backdrop-blur-sm transition-opacity"
            onClick={() => setIsMobileMenuOpen(false)}
        />
      )}

      {/* Responsive Sidebar */}
      <aside className={`
        fixed md:relative z-50 h-full w-64 bg-white border-r border-slate-100 transition-transform duration-300 ease-in-out
        ${isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'}
      `}>
         <SidebarContent />
      </aside>

      {/* Main Content */}
      <main className={`flex-1 flex flex-col h-full relative min-w-0 bg-white ${selectedSchool ? 'overflow-y-auto' : 'overflow-hidden'}`}>
          {/* Top Bar matching image */}
          <header className={`h-20 border-b border-slate-100 items-center justify-between px-4 md:px-8 flex-shrink-0 bg-white z-[60] sticky top-0 ${selectedSchool ? 'hidden md:flex' : 'flex'}`}>
              <div className="md:hidden">
                  <button onClick={() => setIsMobileMenuOpen(true)} className="p-2 text-slate-600">
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-6 h-6">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
                      </svg>
                  </button>
              </div>

              {/* Search Bar */}
              <div className="flex-1 max-w-xl mx-auto relative px-4 md:px-0" ref={searchRef}>
                  <div className="relative w-full">
                      <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                          <svg className="h-4 w-4 text-slate-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                          </svg>
                      </div>
                      <input 
                          type="text"
                          placeholder="Search universities"
                          value={searchQuery}
                          onChange={(e) => setSearchQuery(e.target.value)}
                          onFocus={() => setIsSearchFocused(true)}
                          className="block w-full pl-10 pr-4 py-2 bg-slate-100 border-none rounded-full text-sm focus:ring-2 focus:ring-slate-200 transition-all placeholder-slate-400"
                      />
                  </div>

                  {/* Search Results Dropdown */}
                  {isSearchFocused && searchQuery.trim().length > 1 && (
                      <div className="absolute top-full left-0 mt-2 w-full bg-white shadow-xl rounded-2xl overflow-hidden z-50 border border-slate-100">
                          {searchResults.length > 0 ? (
                              searchResults.map((uni) => (
                                  <button
                                      key={uni.id}
                                      onClick={() => handleSearchResultClick(uni)}
                                      className="w-full text-left p-4 hover:bg-slate-50 border-b border-slate-50 last:border-0 transition-colors"
                                  >
                                      <div className="font-bold text-slate-900">{uni.name}</div>
                                      <div className="text-xs text-slate-500">{uni.location}</div>
                                  </button>
                              ))
                          ) : (
                              <div className="p-4 text-slate-400 text-sm italic">No results found</div>
                          )}
                      </div>
                  )}
              </div>

              {/* User Profile */}
              <div className="flex items-center gap-2 md:gap-3 relative" ref={profileDropdownRef}>
                  <button 
                    onClick={() => setIsProfileDropdownOpen(!isProfileDropdownOpen)}
                    className="flex items-center gap-2 md:gap-3 hover:bg-slate-50 p-1 rounded-full transition-colors"
                  >
                      <div className="hidden sm:block text-right">
                          <p className="text-xs md:text-sm font-bold text-slate-900 truncate max-w-[150px]">{profile.name || 'Account'}</p>
                      </div>
                      <div className="w-8 h-8 md:w-10 md:h-10 rounded-full bg-slate-100 flex items-center justify-center overflow-hidden border border-slate-200 shrink-0">
                          <img 
                              src={profile.photoUrl || `https://ui-avatars.com/api/?name=${profile.name || 'User'}&background=f1f5f9&color=475569`} 
                              alt="User" 
                              className="w-full h-full object-cover"
                          />
                      </div>
                  </button>

                  {/* Profile Dropdown */}
                  {isProfileDropdownOpen && (
                      <div className="absolute top-full right-0 mt-2 w-48 bg-white shadow-xl rounded-2xl overflow-hidden z-[70] border border-slate-100 py-2 animate-in fade-in slide-in-from-top-2 duration-200">
                          <button 
                              onClick={() => {
                                  setIsEditModalOpen(true);
                                  setIsProfileDropdownOpen(false);
                              }}
                              className="w-full text-left px-4 py-3 text-sm font-medium text-slate-700 hover:bg-slate-50 flex items-center gap-3 transition-colors"
                          >
                              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-4 h-4">
                                  <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z" />
                              </svg>
                              My Profile
                          </button>
                          <button 
                              onClick={() => {
                                  setIsFeedbackModalOpen(true);
                                  setIsProfileDropdownOpen(false);
                              }}
                              className="w-full text-left px-4 py-3 text-sm font-medium text-slate-700 hover:bg-slate-50 flex items-center gap-3 transition-colors"
                          >
                              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-4 h-4 text-emerald-500">
                                  <path strokeLinecap="round" strokeLinejoin="round" d="M12 20.25c4.97 0 9-3.694 9-8.25s-4.03-8.25-9-8.25S3 7.444 3 12c0 2.104.859 4.023 2.273 5.48.432.447.74 1.04.586 1.641a4.483 4.483 0 01-.923 1.785 0.5.5 0 00.412.774 7.75 7.75 0 003.078-.714 0.612 0.612 0 01.554.041c1.246.732 2.68 1.154 4.195 1.154z" />
                              </svg>
                              Give Feedback
                          </button>
                          <div className="h-px bg-slate-100 my-1 mx-2" />
                          <button 
                              onClick={() => {
                                  onLogout();
                                  setIsProfileDropdownOpen(false);
                              }}
                              className="w-full text-left px-4 py-3 text-sm font-medium text-red-600 hover:bg-red-50 flex items-center gap-3 transition-colors"
                          >
                              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-4 h-4">
                                  <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6A2.25 2.25 0 005.25 5.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15M12 9l-3 3m0 0l3 3m-3-3h12.75" />
                              </svg>
                              Sign Out
                          </button>
                      </div>
                  )}
              </div>
          </header>

          {/* View Content */}
          <div className={`flex-1 ${currentView === 'chat' ? 'overflow-hidden flex flex-col' : (selectedSchool ? '' : 'overflow-y-auto')} ${selectedSchool || currentView === 'chat' ? 'p-0' : 'p-4 md:p-12'}`}>
              {selectedSchool ? (
                  <SchoolProfileView 
                    uni={selectedSchool} 
                    onClose={() => setSelectedSchool(null)} 
                    profile={profile}
                    onStartApplication={handleStartApplication}
                  />
              ) : (
                  <>
                    {currentView === 'schools' && (
                        <div className="max-w-7xl mx-auto animate-fade-in">
                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-8 gap-y-12">
                                {displaySchools.map(uni => (
                                    <UniversityCard 
                                        key={uni.id}
                                        university={uni}
                                        onSave={onSaveSchool}
                                        isSaved={!isFallback}
                                        minimal={false}
                                        onClick={() => setSelectedSchool(uni)}
                                        onDiscard={!isFallback ? onDiscardSchool : undefined}
                                    />
                                ))}
                            </div>
                            {isFallback && (
                                <div className="w-full bg-slate-50 rounded-3xl p-12 text-center text-slate-500 mt-12 border border-slate-100">
                                    <p className="font-medium text-lg">Consult the Gradwyn Intelligence Chat to curate a personalized list.</p>
                                </div>
                            )}
                        </div>
                    )}

                    {currentView === 'scholarships' && (
                         <div className="max-w-7xl mx-auto animate-fade-in">
                            <div className="mb-8">
                                <h2 className="text-4xl font-bold text-brand-900 font-serif tracking-tight mb-3">Financial Aid & Funding</h2>
                                <p className="text-slate-600 text-lg font-light">Explore scholarships matching your profile and academic goals.</p>
                            </div>

                            <div className="flex flex-col md:flex-row gap-6 mb-8">
                                {/* Tabs */}
                                <div className="flex bg-white border border-slate-200 rounded-lg p-1">
                                    <button 
                                        onClick={() => setScholarshipTab('all')}
                                        className={`px-6 py-2 text-sm font-bold uppercase tracking-widest rounded-md transition-all ${scholarshipTab === 'all' ? 'bg-brand-700 text-white' : 'text-slate-500 hover:bg-slate-50'}`}
                                    >
                                        All Grants
                                    </button>
                                    <button 
                                        onClick={() => setScholarshipTab('forYou')}
                                        className={`px-6 py-2 text-sm font-bold uppercase tracking-widest rounded-md transition-all flex items-center gap-2 ${scholarshipTab === 'forYou' ? 'bg-accent-gold text-white' : 'text-slate-500 hover:bg-slate-50'}`}
                                    >
                                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="w-3 h-3">
                                            <path d="M10 8a3 3 0 100-6 3 3 0 000 6zM3.465 14.493a1.23 1.23 0 00.41 1.412A9.957 9.957 0 0010 18c2.31 0 4.438-.784 6.131-2.1.43-.333.604-.903.408-1.41a7.002 7.002 0 00-13.074.003z" />
                                        </svg>
                                        For You
                                    </button>
                                </div>
                                
                                {/* Filter Dropdown */}
                                <select 
                                    className="p-2 bg-white border border-slate-200 text-slate-700 font-medium text-sm outline-none focus:border-brand-500"
                                    value={scholarshipFilter}
                                    onChange={(e) => setScholarshipFilter(e.target.value)}
                                >
                                    <option value="All">All Tags</option>
                                    <option value="Bachelors">Bachelor's</option>
                                    <option value="Masters">Master's</option>
                                    <option value="PhD">PhD / Research</option>
                                    <option value="Africa Specific">Africa Specific</option>
                                    <option value="Fully-funded">Fully Funded</option>
                                    <option value="Part-funded">Part Funded</option>
                                    <option value="Global">Global</option>
                                    <option value="Women">Women in STEM</option>
                                </select>
                            </div>

                            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                                {getScholarships().length > 0 ? getScholarships().map(sch => (
                                    <div key={sch.id} className="bg-white border border-slate-200 p-6 shadow-sm hover:shadow-md hover:border-brand-300 transition-all flex flex-col group">
                                        <div className="flex justify-between items-start mb-2">
                                            <div className="bg-green-50 text-green-800 text-[10px] font-bold uppercase tracking-widest px-2 py-1 border border-green-100 inline-block mb-2">
                                                {sch.amount}
                                            </div>
                                            <span className="text-slate-400 text-xs font-bold uppercase tracking-widest">Deadline: {sch.deadline}</span>
                                        </div>
                                        <h3 className="text-xl font-serif font-bold text-brand-900 mb-1 group-hover:text-brand-700 transition-colors">{sch.name}</h3>
                                        <p className="text-xs text-accent-gold font-bold uppercase tracking-widest mb-4 font-heading">{sch.provider}</p>
                                        <p className="text-slate-600 text-sm mb-6 flex-1 leading-relaxed">{sch.description}</p>
                                        <div className="flex justify-between items-center pt-4 border-t border-slate-100 mt-auto">
                                            <div className="flex gap-2 flex-wrap">
                                                {sch.tags?.slice(0, 3).map(tag => (
                                                    <span key={tag} className="text-[10px] bg-beige-100 text-slate-600 px-2 py-1 rounded-none border border-beige-200">{tag}</span>
                                                ))}
                                            </div>
                                            <div className="flex gap-2">
                                                <button 
                                                    onClick={() => handleStartScholarshipApplication(sch)}
                                                    className="text-white bg-brand-700 hover:bg-brand-800 px-3 py-1.5 font-bold text-xs uppercase tracking-widest transition-colors"
                                                >
                                                    Apply
                                                </button>
                                                <button 
                                                    onClick={() => setSelectedScholarship(sch)}
                                                    className="text-brand-700 hover:text-brand-900 font-bold text-xs uppercase tracking-widest border-b-2 border-transparent hover:border-brand-700 transition-all pb-0.5"
                                                >
                                                    Details
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                )) : (
                                    <div className="col-span-full p-12 text-center bg-white border border-slate-200 border-dashed">
                                        <p className="text-slate-400 font-medium">No scholarships found matching criteria.</p>
                                    </div>
                                )}
                            </div>
                         </div>
                    )}

                    {currentView === 'guides' && (
                         <div className="max-w-7xl mx-auto animate-fade-in">
                            <div className="mb-8">
                                <h2 className="text-4xl font-bold text-brand-900 font-serif tracking-tight mb-3">Resource Library</h2>
                                <p className="text-slate-600 text-lg font-light">Expert guides and strategies for navigating the admissions landscape.</p>
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                                {MOCK_GUIDES.map(guide => (
                                    <div key={guide.id} className="bg-white border border-slate-200 shadow-sm hover:shadow-lg transition-all group cursor-pointer overflow-hidden">
                                        <div className="h-48 overflow-hidden relative">
                                            <img src={guide.image} alt={guide.title} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-700" />
                                            <div className="absolute top-4 left-4 bg-white/90 backdrop-blur-md px-3 py-1 text-[10px] font-bold uppercase tracking-widest text-brand-800 shadow-sm">
                                                {guide.category}
                                            </div>
                                        </div>
                                        <div className="p-6">
                                            <div className="flex items-center gap-2 mb-3 text-slate-400 text-xs font-bold uppercase tracking-widest">
                                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="w-3 h-3">
                                                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm.75-13a.75.75 0 00-1.5 0v5c0 .414.336.75.75.75h4a.75.75 0 000-1.5h-3.25V5z" clipRule="evenodd" />
                                                </svg>
                                                {guide.readTime}
                                            </div>
                                            <h3 className="text-xl font-bold font-serif text-brand-900 mb-3 group-hover:text-brand-600 transition-colors leading-tight">{guide.title}</h3>
                                            <p className="text-slate-600 text-sm leading-relaxed mb-6">{guide.description}</p>
                                            <span className="text-brand-700 text-xs font-bold uppercase tracking-widest flex items-center gap-2 group-hover:gap-3 transition-all">
                                                Read Article
                                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="w-3 h-3">
                                                    <path fillRule="evenodd" d="M3 10a.75.75 0 01.75-.75h10.638L10.23 5.29a.75.75 0 111.04-1.08l5.5 5.25a.75.75 0 010 1.08l-5.5 5.25a.75.75 0 11-1.04-1.08l4.158-3.96H3.75A.75.75 0 013 10z" clipRule="evenodd" />
                                                </svg>
                                            </span>
                                        </div>
                                    </div>
                                ))}
                            </div>
                         </div>
                    )}

                    {currentView === 'tracker' && (
                         <div className="max-w-7xl mx-auto animate-fade-in">
                            <div className="mb-8">
                                <h2 className="text-4xl font-bold text-brand-900 font-serif tracking-tight mb-3">Candidacy Tracker</h2>
                                <p className="text-slate-600 text-lg font-light">Monitor the status of your active applications.</p>
                            </div>

                            {/* Tracker Tabs */}
                            <div className="flex gap-4 mb-8 border-b border-slate-200">
                                <button
                                    onClick={() => setTrackerTab('universities')}
                                    className={`pb-3 px-2 text-sm font-bold uppercase tracking-widest transition-all relative
                                        ${trackerTab === 'universities' ? 'text-brand-700' : 'text-slate-400 hover:text-slate-600'}`}
                                >
                                    Universities
                                    {trackerTab === 'universities' && <div className="absolute bottom-0 left-0 w-full h-1 bg-brand-700"></div>}
                                </button>
                                <button
                                    onClick={() => setTrackerTab('scholarships')}
                                    className={`pb-3 px-2 text-sm font-bold uppercase tracking-widest transition-all relative
                                        ${trackerTab === 'scholarships' ? 'text-brand-700' : 'text-slate-400 hover:text-slate-600'}`}
                                >
                                    Scholarships
                                    {trackerTab === 'scholarships' && <div className="absolute bottom-0 left-0 w-full h-1 bg-brand-700"></div>}
                                </button>
                            </div>

                            {displayedApplications.length === 0 ? (
                                <div className="bg-white border border-slate-200 p-20 text-center shadow-sm">
                                    <div className="w-24 h-24 bg-beige-100 text-brand-400 flex items-center justify-center mx-auto mb-8 border border-beige-200">
                                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1} stroke="currentColor" className="w-12 h-12">
                                            <path strokeLinecap="round" strokeLinejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
                                        </svg>
                                    </div>
                                    <h3 className="text-2xl font-bold text-brand-900 mb-3 font-serif">No {trackerTab === 'universities' ? 'University' : 'Scholarship'} Applications</h3>
                                    <p className="text-slate-500 mb-8 max-w-md mx-auto">
                                        Begin an application from the {trackerTab === 'universities' ? 'Institutions' : 'Scholarships'} page.
                                    </p>
                                    <button 
                                        onClick={() => handleSidebarClick(trackerTab === 'universities' ? 'schools' : 'scholarships')}
                                        className="px-10 py-4 bg-brand-700 text-white font-bold font-heading uppercase tracking-widest hover:bg-brand-800 transition-colors"
                                    >
                                        Browse {trackerTab === 'universities' ? 'Institutions' : 'Opportunities'}
                                    </button>
                                </div>
                            ) : (
                                <div className="space-y-6">
                                    {displayedApplications.map(app => {
                                        const entityName = app.university?.name || app.scholarship?.name || "Unknown Application";
                                        const entityInitials = entityName
                                            .split(' ')
                                            .filter(word => !['of', 'the', 'and', '&', 'at'].includes(word.toLowerCase()))
                                            .map(word => word[0])
                                            .join('')
                                            .toUpperCase()
                                            .slice(0, 3);
                                        const isScholarshipApp = app.type === 'scholarship';

                                        return (
                                            <div key={app.id} className="bg-white border border-slate-200 p-8 shadow-sm hover:shadow-md transition-shadow flex flex-col md:flex-row gap-10 items-start md:items-center group">
                                                <div className={`w-20 h-20 flex flex-col items-center justify-center shrink-0 shadow-lg ${isScholarshipApp ? 'bg-slate-900 text-white' : 'bg-slate-950 text-white'}`}>
                                                    <span className="font-serif italic text-3xl select-none leading-none">
                                                        {entityInitials}
                                                    </span>
                                                    <div className="h-0.5 w-6 bg-white/20 mt-2" />
                                                </div>
                                                
                                                <div className="flex-1 w-full">
                                                    <div className="flex justify-between items-start mb-4">
                                                        <h3 className="text-xl font-bold text-slate-900 font-serif">{entityName}</h3>
                                                        <span className={`px-3 py-1 text-xs font-bold uppercase tracking-widest border ${
                                                            app.status === 'submitted' ? 'bg-green-50 text-green-700 border-green-200' :
                                                            app.status === 'draft' ? 'bg-slate-50 text-slate-600 border-slate-200' :
                                                            'bg-brand-50 text-brand-700 border-brand-200'
                                                        }`}>
                                                            {app.status.replace('_', ' ')}
                                                        </span>
                                                    </div>
                                                    
                                                    <div className="w-full bg-slate-100 h-2 rounded-full mb-4 overflow-hidden">
                                                        <div className="bg-brand-600 h-full rounded-full transition-all duration-500" style={{ width: `${app.progress}%` }}></div>
                                                    </div>
                                                    
                                                    <div className="flex justify-between text-xs text-slate-500 font-medium mb-6">
                                                        <span>Progress: {app.progress}%</span>
                                                        <span>Last Updated: {app.lastUpdated.toLocaleDateString()}</span>
                                                    </div>
                                                    
                                                    <div className="flex gap-4">
                                                        {app.status !== 'submitted' && (
                                                            <button 
                                                                onClick={() => handleResumeApplication(app)}
                                                                className="text-brand-700 font-bold text-sm uppercase tracking-wider hover:text-brand-900 hover:underline underline-offset-4"
                                                            >
                                                                Resume Application
                                                            </button>
                                                        )}
                                                        <button 
                                                            onClick={() => onWithdrawApplication(app.id)}
                                                            className="text-slate-400 font-bold text-sm uppercase tracking-wider hover:text-red-600"
                                                        >
                                                            Withdraw
                                                        </button>
                                                    </div>
                                                </div>
                                            </div>
                                        );
                                    })}
                                </div>
                            )}
                         </div>
                    )}

                    {currentView === 'mentors' && (
                        <div className="max-w-7xl mx-auto animate-fade-in">
                            <div className="mb-8">
                                <h2 className="text-4xl font-bold text-brand-900 font-serif tracking-tight mb-3">Mentorship Network</h2>
                                <p className="text-slate-600 text-lg font-light">Connect with alumni and current students for guidance.</p>
                            </div>
                            
                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                                {MOCK_MENTORS.map(mentor => (
                                    <div key={mentor.id} className="bg-white border border-slate-200 flex flex-col group hover:border-brand-500 transition-all shadow-sm hover:shadow-lg">
                                        <div className="p-6 flex items-start gap-4 border-b border-slate-100">
                                            <img src={mentor.image} alt={mentor.name} className="w-16 h-16 object-cover border border-slate-200" />
                                            <div>
                                                <h3 className="text-lg font-bold text-brand-900 font-serif leading-tight">{mentor.name}</h3>
                                                <p className="text-xs text-slate-500 uppercase tracking-wider font-bold mt-1">{mentor.role}</p>
                                                <p className="text-xs text-accent-gold font-bold mt-1">{mentor.university}</p>
                                            </div>
                                        </div>
                                        <div className="p-6 flex-1">
                                            <p className="text-slate-600 text-sm leading-relaxed mb-4">{mentor.bio}</p>
                                            <div className="flex flex-wrap gap-2 mb-6">
                                                {mentor.tags?.map(tag => (
                                                    <span key={tag} className="text-[10px] bg-beige-100 text-slate-600 px-2 py-1 border border-beige-200">{tag}</span>
                                                ))}
                                            </div>
                                            <div className="flex items-center gap-2 text-xs text-slate-500 font-medium mb-6">
                                                <span className={`w-2 h-2 rounded-full ${mentor.isAvailable ? 'bg-green-500' : 'bg-slate-300'}`}></span>
                                                {mentor.isAvailable ? `Available: ${mentor.availability}` : 'Currently Unavailable'}
                                            </div>
                                        </div>
                                        <div className="p-4 bg-slate-50 border-t border-slate-200 flex justify-between items-center">
                                            <a 
                                                href={mentor.linkedin} 
                                                target="_blank" 
                                                rel="noreferrer"
                                                className="text-brand-700 text-xs font-bold uppercase tracking-widest hover:underline"
                                            >
                                                LinkedIn
                                            </a>
                                            {mentor.isAvailable ? (
                                                 <a href={`mailto:${mentor.email}`} className="bg-brand-700 text-white px-4 py-2 text-xs font-bold uppercase tracking-widest hover:bg-brand-800 transition-colors">
                                                    Contact
                                                </a>
                                            ) : (
                                                <button disabled className="bg-slate-200 text-slate-400 px-4 py-2 text-xs font-bold uppercase tracking-widest cursor-not-allowed">
                                                    Busy
                                                </button>
                                            )}
                                           
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {currentView === 'chat' && (
                        <div className="h-full flex flex-col">
                             {/* The Chat Interface handles its own layout, we just render it here */}
                             {renderChat()}
                        </div>
                    )}
                    
                    {currentView === 'prep' && (
                        <div className="max-w-4xl mx-auto text-center py-20">
                            <div className="w-24 h-24 bg-brand-100 text-brand-500 mx-auto flex items-center justify-center rounded-full mb-6">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-12 h-12">
                                    <path strokeLinecap="round" strokeLinejoin="round" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25" />
                                </svg>
                            </div>
                            <h2 className="text-3xl font-bold text-brand-900 font-serif mb-4">Preparation Suite Coming Soon</h2>
                            <p className="text-slate-600 max-w-md mx-auto">We are building a comprehensive suite of tools including interview simulators, standardized test prep planners, and document editors.</p>
                        </div>
                    )}
                  </>
              )}
          </div>
      </main>
    </div>
  );
};

export default Dashboard;