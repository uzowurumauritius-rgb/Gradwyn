
import React, { useState } from 'react';

interface LandingPageProps {
  onGetStarted: (role: 'applicant' | 'mentor' | 'university') => void;
}

const LandingPage: React.FC<LandingPageProps> = ({ onGetStarted }) => {
  const [hoveredRole, setHoveredRole] = useState<'applicant' | 'mentor' | 'university' | null>(null);

  const getFlexClass = (role: 'applicant' | 'mentor' | 'university') => {
    if (!hoveredRole) return 'flex-[1]';
    return hoveredRole === role ? 'flex-[2]' : 'flex-[0.5]';
  };

  const getOpacityClass = (role: 'applicant' | 'mentor' | 'university') => {
      if (!hoveredRole) return 'opacity-100';
      return hoveredRole === role ? 'opacity-100' : 'opacity-50';
  };

  return (
    <div className="h-screen bg-white flex flex-col font-sans overflow-hidden relative">
        {/* Header Overlay */}
        <div className="absolute top-0 left-0 w-full p-8 z-20 flex justify-between items-center pointer-events-none">
             <div className="flex items-center gap-3 pointer-events-auto">
                <span className="text-3xl font-bold tracking-tight text-slate-900">Gradwyn</span>
             </div>
        </div>

        <div className="flex-1 flex flex-col md:flex-row w-full h-full overflow-y-auto md:overflow-hidden">
            {/* STUDENT PANEL */}
            <div 
                className={`${getFlexClass('applicant')} bg-slate-50 relative transition-all duration-700 ease-in-out cursor-pointer group border-b md:border-b-0 md:border-r border-slate-100 overflow-hidden flex flex-col justify-end min-h-[40vh] md:min-h-0`}
                onMouseEnter={() => setHoveredRole('applicant')}
                onMouseLeave={() => setHoveredRole(null)}
                onClick={() => onGetStarted('applicant')}
            >
                <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1523050854058-8df90110c9f1?q=80&w=1200&auto=format&fit=crop')] bg-cover bg-center opacity-0 group-hover:opacity-10 transition-opacity duration-700"></div>
                
                <div className={`p-8 md:p-12 relative z-10 ${getOpacityClass('applicant')} transition-opacity duration-500`}>
                    <h2 className="text-4xl md:text-7xl font-bold text-slate-900 mb-4 md:mb-6 leading-tight tracking-tighter">
                        Find Your <br/> Perfect Match
                    </h2>
                    <p className="text-slate-500 text-lg md:text-xl mb-6 md:mb-10 max-w-md leading-relaxed font-medium">
                        Research elite universities and optimize your candidacy for the world's top institutions.
                    </p>
                    <button className="px-8 md:px-10 py-3 md:py-4 bg-slate-900 text-white font-bold rounded-full hover:bg-slate-800 transition-all flex items-center gap-3 shadow-xl shadow-slate-900/10 w-fit">
                        Begin Journey
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-5 h-5">
                            <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
                        </svg>
                    </button>
                </div>
            </div>

            {/* MENTOR PANEL */}
            <div 
                className={`${getFlexClass('mentor')} bg-slate-100 relative transition-all duration-700 ease-in-out cursor-pointer group border-b md:border-b-0 md:border-r border-slate-200 overflow-hidden flex flex-col justify-end min-h-[40vh] md:min-h-0`}
                onMouseEnter={() => setHoveredRole('mentor')}
                onMouseLeave={() => setHoveredRole(null)}
                onClick={() => onGetStarted('mentor')}
            >
                <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1544531586-fde5298cdd40?q=80&w=1200&auto=format&fit=crop')] bg-cover bg-center opacity-0 group-hover:opacity-10 transition-opacity duration-700"></div>

                <div className={`p-8 md:p-12 relative z-10 ${getOpacityClass('mentor')} transition-opacity duration-500`}>
                    <h2 className="text-4xl md:text-7xl font-bold text-slate-900 mb-4 md:mb-6 leading-tight tracking-tighter">
                        Guide the <br/> Next Gen
                    </h2>
                    <p className="text-slate-500 text-lg md:text-xl mb-6 md:mb-10 max-w-md leading-relaxed font-medium">
                        Connect with aspiring scholars, share your academic journey, and shape future leaders.
                    </p>
                    <button className="px-8 md:px-10 py-3 md:py-4 bg-white text-slate-900 border border-slate-200 font-bold rounded-full hover:bg-slate-50 transition-all flex items-center gap-3 shadow-lg w-fit">
                        Join as Mentor
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-5 h-5">
                            <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
                        </svg>
                    </button>
                </div>
            </div>

            {/* UNIVERSITY PANEL */}
            <div 
                className={`${getFlexClass('university')} bg-slate-200 relative transition-all duration-700 ease-in-out cursor-pointer group overflow-hidden flex flex-col justify-end min-h-[40vh] md:min-h-0`}
                onMouseEnter={() => setHoveredRole('university')}
                onMouseLeave={() => setHoveredRole(null)}
                onClick={() => onGetStarted('university')}
            >
                 <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1492538368677-f6e0afe31dcc?q=80&w=1200&auto=format&fit=crop')] bg-cover bg-center opacity-0 group-hover:opacity-10 transition-opacity duration-700"></div>

                <div className={`p-8 md:p-12 relative z-10 ${getOpacityClass('university')} transition-opacity duration-500`}>
                    <h2 className="text-4xl md:text-7xl font-bold text-slate-900 mb-4 md:mb-6 leading-tight tracking-tighter">
                        Recruit <br/> Top Talent
                    </h2>
                    <p className="text-slate-500 text-lg md:text-xl mb-6 md:mb-10 max-w-md leading-relaxed font-medium">
                        Partner with Gradwyn to identify and engage with high-potential global candidates.
                    </p>
                    <button className="px-8 md:px-10 py-3 md:py-4 bg-white text-slate-900 border border-slate-200 font-bold rounded-full hover:bg-slate-50 transition-all flex items-center gap-3 shadow-lg w-fit">
                        Partner Access
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="w-5 h-5">
                            <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
                        </svg>
                    </button>
                </div>
            </div>
        </div>
    </div>
  );
};

export default LandingPage;
