
import React, { useState } from 'react';
import { UserProfile } from '../types';
import { motion as m, AnimatePresence } from 'motion/react';
import { AlertTriangle, Trash2, X } from 'lucide-react';

interface EditProfileModalProps {
  isOpen: boolean;
  onClose: () => void;
  profile: UserProfile;
  onSave: (newProfile: UserProfile) => void;
  onDeleteAccount: () => void;
}

const EditProfileModal: React.FC<EditProfileModalProps> = ({ isOpen, onClose, profile, onSave, onDeleteAccount }) => {
  const [formData, setFormData] = useState<UserProfile>(profile);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  if (!isOpen) return null;

  const handleSave = () => {
    onSave(formData);
    onClose();
  };

  return (
    <>
      <div className="fixed inset-0 z-[100] flex items-center justify-center p-2 sm:p-4 bg-slate-900/40 backdrop-blur-md">
        <div className="bg-white rounded-[2rem] shadow-2xl w-full max-w-2xl max-h-[95vh] sm:max-h-[90vh] overflow-y-auto flex flex-col animate-fade-in border border-slate-100 relative">
          <div className="p-5 sm:p-8 border-b border-slate-50 flex justify-between items-center sticky top-0 bg-white/80 backdrop-blur-md z-10">
            <h2 className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight">Edit Preferences</h2>
            <button onClick={onClose} className="p-2 text-slate-400 hover:text-slate-900 hover:bg-slate-50 rounded-full transition-all">
              <X className="w-5 h-5" />
            </button>
          </div>

          <div className="p-5 sm:p-8 space-y-8 sm:space-y-10">
            <div>
              <label className="block text-[10px] sm:text-xs font-bold text-slate-400 uppercase tracking-widest mb-2 sm:mb-3">Field of Study</label>
              <input 
                type="text" 
                value={formData.fieldOfStudy} 
                onChange={(e) => setFormData({...formData, fieldOfStudy: e.target.value})}
                className="w-full px-4 py-3 sm:p-4 rounded-xl sm:rounded-2xl border border-slate-100 focus:border-slate-900 outline-none bg-slate-50 text-slate-900 font-bold transition-all text-sm sm:text-base"
              />
            </div>

            <div>
              <label className="block text-[10px] sm:text-xs font-bold text-slate-400 uppercase tracking-widest mb-2 sm:mb-3">Budget</label>
              <select 
                value={formData.budgetRange}
                onChange={(e) => setFormData({...formData, budgetRange: e.target.value})}
                className="w-full px-4 py-3 sm:p-4 rounded-xl sm:rounded-2xl border border-slate-100 focus:border-slate-900 outline-none bg-slate-50 text-slate-900 font-bold transition-all appearance-none text-sm sm:text-base"
              >
                {["Under $15k", "$15k - $30k", "$30k - $50k", "$50k+", "Full Scholarship Required"].map(opt => (
                  <option key={opt} value={opt}>{opt}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-[10px] sm:text-xs font-bold text-slate-400 uppercase tracking-widest mb-2 sm:mb-3">Preferred Locations</label>
              <div className="grid grid-cols-2 sm:flex sm:flex-wrap gap-2">
                {[
                  "USA - East", "USA - West", "USA - Midwest", "USA - South",
                  "Canada", "UK - London", "UK - Other", "Europe (EU)", "Europe (Non-EU)",
                  "Australia/NZ", "Asia", "Africa", "South America", "Middle East",
                  "LATAM", "APAC", "EMEA", "Remote/Online"
                ].map(loc => (
                  <button
                    key={loc}
                    onClick={() => {
                      const exists = formData.preferredLocations.includes(loc);
                      setFormData({
                        ...formData,
                        preferredLocations: exists 
                          ? formData.preferredLocations.filter(l => l !== loc)
                          : [...formData.preferredLocations, loc]
                      })
                    }}
                    className={`px-3 py-2 rounded-full text-[10px] sm:text-xs font-bold transition-all border block w-full sm:w-auto truncate
                      ${formData.preferredLocations.includes(loc)
                        ? 'bg-slate-900 text-white border-slate-900 shadow-lg shadow-slate-900/10'
                        : 'bg-white text-slate-500 border-slate-100 hover:border-slate-300 hover:text-slate-900'}`}
                  >
                    {loc}
                  </button>
                ))}
              </div>
            </div>
            
            <div>
               <label className="block text-[10px] sm:text-xs font-bold text-slate-400 uppercase tracking-widest mb-2 sm:mb-3">Key Priorities (Select 3)</label>
               <div className="grid grid-cols-1 sm:flex sm:flex-wrap gap-2">
                   {[
                      "Prestige",
                      "Financial Aid",
                      "Campus Culture",
                      "Location Safety",
                      "Career & Alumni",
                      "Diversity",
                      "Research",
                      "Athletics"
                   ].map(metric => (
                       <button
                        key={metric}
                        onClick={() => {
                          const exists = formData.keyMetrics.includes(metric);
                          if (!exists && formData.keyMetrics.length >= 3) return;
                          setFormData({
                            ...formData,
                            keyMetrics: exists 
                              ? formData.keyMetrics.filter(m => m !== metric)
                              : [...formData.keyMetrics, metric]
                          })
                        }}
                        className={`px-3 py-2 rounded-full text-[10px] sm:text-xs font-bold transition-all border text-center sm:text-left
                          ${formData.keyMetrics.includes(metric)
                            ? 'bg-slate-900 text-white border-slate-900 shadow-lg shadow-slate-900/10'
                            : 'bg-white text-slate-500 border-slate-100 hover:border-slate-300 hover:text-slate-900'}`}
                      >
                        {metric}
                      </button>
                   ))}
               </div>
            </div>

            <div>
              <label className="block text-[10px] sm:text-xs font-bold text-slate-400 uppercase tracking-widest mb-2 sm:mb-3">Specific Requirements</label>
              <textarea 
                value={formData.priorities || ''} 
                onChange={(e) => setFormData({...formData, priorities: e.target.value})}
                placeholder="E.g. Need a debate team..."
                className="w-full px-4 py-3 rounded-xl sm:rounded-2xl border border-slate-100 focus:border-slate-900 outline-none min-h-[100px] sm:min-h-[120px] bg-slate-50 text-slate-900 font-bold transition-all text-sm sm:text-base"
              />
            </div>

            {/* Danger Zone */}
            <div className="pt-10 border-t border-slate-100">
               <div className="bg-red-50 rounded-3xl p-6 sm:p-8 border border-red-100">
                  <div className="flex items-center gap-3 mb-4">
                     <AlertTriangle className="text-red-500 w-5 h-5" />
                     <h3 className="text-lg font-bold text-red-900">Danger Zone</h3>
                  </div>
                  <p className="text-sm text-red-600/80 mb-6 font-medium">
                    Once you delete your account, there is no going back. All your research, saved schools, and application progress will be permanently removed.
                  </p>
                  <button 
                    onClick={() => setShowDeleteConfirm(true)}
                    className="flex items-center gap-2 px-6 py-3 bg-red-600 text-white rounded-full font-bold hover:bg-red-700 transition-all shadow-lg shadow-red-200 text-sm"
                  >
                    <Trash2 size={16} />
                    Delete Account & Data
                  </button>
               </div>
            </div>
          </div>

          <div className="p-5 sm:p-8 border-t border-slate-50 flex flex-col sm:flex-row justify-end gap-3 sm:gap-4 sticky bottom-0 bg-white/80 backdrop-blur-md">
            <button onClick={onClose} className="px-6 py-2 sm:py-3 text-slate-400 font-bold hover:text-slate-900 transition-all text-sm sm:text-base order-2 sm:order-1">Cancel</button>
            <button onClick={handleSave} className="px-6 py-3 sm:px-8 sm:py-3 bg-slate-900 text-white rounded-full font-bold hover:bg-slate-800 transition-all shadow-xl shadow-slate-900/10 text-sm sm:text-base order-1 sm:order-2">Update & Re-Analyze</button>
          </div>
        </div>
      </div>

      {/* Delete Confirmation Modal */}
      <AnimatePresence>
        {showDeleteConfirm && (
          <div className="fixed inset-0 z-[110] flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm">
            <m.div 
              initial={{ opacity: 0, scale: 0.95, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: 20 }}
              className="bg-white rounded-[2.5rem] shadow-2xl w-full max-w-md overflow-hidden flex flex-col border border-slate-100"
            >
              <div className="p-8 text-center">
                <div className="w-20 h-20 bg-red-50 text-red-600 rounded-full flex items-center justify-center mx-auto mb-6">
                  <AlertTriangle size={40} />
                </div>
                <h3 className="text-2xl font-bold text-slate-900 mb-2">Are you sure?</h3>
                <p className="text-slate-500 mb-8 font-medium">
                  This action is permanent and cannot be undone. You will lose all your data and access to Gradwyn.
                </p>
                
                <div className="grid grid-cols-2 gap-4">
                  <button 
                    onClick={() => setShowDeleteConfirm(false)}
                    className="px-6 py-4 border border-slate-200 text-slate-600 rounded-full font-bold hover:bg-slate-50 transition-all"
                  >
                    No, Keep it
                  </button>
                  <button 
                    onClick={() => {
                       onDeleteAccount();
                       setShowDeleteConfirm(false);
                    }}
                    className="px-6 py-4 bg-red-600 text-white rounded-full font-bold hover:bg-red-700 transition-all shadow-xl shadow-red-200 flex items-center justify-center gap-2"
                  >
                    <Trash2 size={18} />
                    Yes, Delete
                  </button>
                </div>
              </div>
            </m.div>
          </div>
        )}
      </AnimatePresence>
    </>
  );
};

export default EditProfileModal;
