
import React, { useState } from 'react';
import { University } from '../types';

interface UniversityCardProps {
  university: University;
  onSave: (university: University) => void;
  onDiscard?: (universityId: string) => void;
  isSaved?: boolean;
  isDiscarded?: boolean;
  minimal?: boolean;
  onClick?: () => void;
  className?: string;
}

const UniversityCard: React.FC<UniversityCardProps> = ({ 
  university, 
  onSave, 
  onDiscard, 
  isSaved = false,
  isDiscarded = false,
  minimal = false,
  onClick,
  className = ''
}) => {
  const [imgError, setImgError] = useState(false);
  const [logoError, setLogoError] = useState(false);

  if (isDiscarded) return null;

  // Determine accent color based on match score
  const scoreColorClass = university.matchScore >= 90 ? 'text-brand-700 border-brand-700' : 
                     university.matchScore >= 80 ? 'text-accent-olive border-accent-olive' : 'text-accent-gold border-accent-gold';
  
  // Get initials for fallback
  const initials = university.name
    .split(' ')
    .filter(word => !['of', 'the', 'and', '&', 'at'].includes(word.toLowerCase()))
    .map(word => word[0])
    .join('')
    .toUpperCase()
    .slice(0, 3);

  return (
    <div 
        className={`group flex flex-col ${minimal ? 'w-full' : 'w-full max-w-[380px]'} ${className} cursor-pointer`}
        onClick={onClick}
    >
      {/* Image Container */}
      <div className="relative aspect-[16/10] overflow-hidden rounded-[32px] bg-slate-900 mb-6 flex items-center justify-center">
         {(!imgError && university.images && university.images.length > 0) ? (
           <img 
              src={university.images[0]} 
              alt={university.name} 
              className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110" 
              onError={() => setImgError(true)}
           />
         ) : (
           <div className="w-full h-full bg-slate-950 flex flex-col items-center justify-center p-8 transition-transform duration-700 group-hover:scale-105">
              <span className="font-serif italic text-6xl text-white/90 tracking-tighter select-none">
                {initials}
              </span>
              <div className="h-px w-12 bg-white/20 mt-4" />
           </div>
         )}
         
         {/* Match Score Badge */}
         <div className="absolute top-4 right-4 bg-white/10 backdrop-blur-xl px-4 py-2 rounded-full z-20 border border-white/20">
            <span className="text-white text-[10px] font-bold uppercase tracking-widest">
                {university.matchScore}% Match
            </span>
         </div>
      </div>

      {/* Info Section */}
      <div className="flex flex-col px-2">
         <div className="flex items-start justify-between gap-4 mb-2">
            <div className="flex items-center gap-4">
               <div className="w-8 h-8 rounded-xl overflow-hidden flex-shrink-0 border border-slate-50 shadow-sm bg-slate-950 p-1 flex items-center justify-center">
                  {!logoError && university.logo ? (
                     <img 
                        src={university.logo} 
                        alt="logo" 
                        className="w-full h-full object-contain" 
                        onError={() => setLogoError(true)}
                     />
                  ) : (
                     <span className="font-serif italic text-[10px] text-white/80 select-none">
                       {initials}
                     </span>
                  )}
               </div>
               <h3 className="text-slate-900 font-bold text-xl leading-tight tracking-tight line-clamp-2 break-words">
                  {university.name}
               </h3>
            </div>
         </div>
         
         <p className="text-slate-400 text-sm font-bold uppercase tracking-widest mb-4 truncate">
            {university.location}
         </p>

         <div className="flex items-center gap-3 text-slate-400 text-xs font-bold uppercase tracking-widest overflow-hidden">
            <span className="text-slate-900 shrink-0">{university.tuition}/yr</span>
            <span className="opacity-20 shrink-0">•</span>
            <div className="flex gap-2 truncate">
                {university.tags?.slice(0, 2).map((tag, idx) => (
                   <React.Fragment key={tag}>
                      <span className="truncate">{tag}</span>
                      {idx < 1 && <span className="opacity-20">•</span>}
                   </React.Fragment>
                ))}
            </div>
         </div>

         {/* Action buttons - always visible for better UX */}
         <div className="mt-6 flex flex-wrap gap-3 transition-all duration-300">
            {!isSaved ? (
                <button 
                    onClick={(e) => { e.stopPropagation(); onSave(university); }}
                    className="px-6 py-2.5 bg-slate-900 text-white text-xs font-bold rounded-full hover:bg-slate-800 transition-all shadow-lg shadow-slate-900/10"
                >
                    Save
                </button>
            ) : (
                <button 
                    className="px-6 py-2.5 bg-slate-50 text-slate-400 text-xs font-bold rounded-full cursor-default"
                    onClick={(e) => e.stopPropagation()}
                >
                    Saved
                </button>
            )}
            {university.website && (
                <a 
                    href={university.website}
                    target="_blank"
                    rel="noopener noreferrer"
                    onClick={(e) => e.stopPropagation()}
                    className="px-6 py-2.5 border border-slate-100 text-slate-900 text-xs font-bold rounded-full hover:bg-slate-50 transition-all flex items-center gap-2"
                >
                    Visit Site
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" className="w-3 h-3 opacity-30">
                        <path fillRule="evenodd" d="M4.25 5.5a.75.75 0 00-.75.75v8.5c0 .414.336.75.75.75h8.5a.75.75 0 00.75-.75v-4a.75.75 0 011.5 0v4A2.25 2.25 0 0112.75 17h-8.5A2.25 2.25 0 012 14.75v-8.5A2.25 2.25 0 014.25 4h5a.75.75 0 010 1.5h-5z" clipRule="evenodd" />
                        <path fillRule="evenodd" d="M6.194 12.753a.75.75 0 001.06.053L16.5 4.44v2.81a.75.75 0 001.5 0v-4.5a.75.75 0 00-.75-.75h-4.5a.75.75 0 000 1.5h2.553l-9.056 8.194a.75.75 0 00-.053 1.06z" clipRule="evenodd" />
                    </svg>
                </a>
            )}
            {!minimal && onDiscard && (
               <button 
                  onClick={(e) => { e.stopPropagation(); onDiscard(university.id); }}
                  className="px-6 py-2.5 border border-slate-100 text-slate-400 text-xs font-bold rounded-full hover:bg-slate-50 hover:text-slate-900 transition-all"
               >
                  Discard
               </button>
            )}
         </div>
      </div>
    </div>
  );
};

export default UniversityCard;
