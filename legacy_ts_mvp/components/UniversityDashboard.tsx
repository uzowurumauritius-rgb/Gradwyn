
import React, { useState, useEffect } from 'react';
import { UniversityProfile, Application } from '../types';
import { db, handleFirestoreError, OperationType } from '../firebase';
import { collection, query, where, getDocs, updateDoc, doc } from 'firebase/firestore';

interface UniversityDashboardProps {
  profile: UniversityProfile;
  onLogout: () => void;
}

const UniversityDashboard: React.FC<UniversityDashboardProps> = ({ profile, onLogout }) => {
  const [applications, setApplications] = useState<Application[]>([]);
  const [activeTab, setActiveTab] = useState<'pending' | 'reviewing' | 'decided'>('pending');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchApplications = async () => {
      setIsLoading(true);
      try {
        // In a real app, we'd query applications where university.id === profile.id
        // For this demo, we'll fetch all 'submitted' applications and filter
        const q = query(collection(db, 'applications'), where('status', '!=', 'draft'));
        const querySnapshot = await getDocs(q);
        const apps = querySnapshot.docs.map(doc => ({ id: doc.id, ...doc.data() } as Application));
        
        // Filter those that belong to this university
        const universityApps = apps.filter(app => app.university?.id === profile.id || app.university?.name === profile.name);
        setApplications(universityApps);
      } catch (error) {
        handleFirestoreError(error, OperationType.LIST, 'applications');
      } finally {
        setIsLoading(false);
      }
    };

    fetchApplications();
  }, [profile.id, profile.name]);

  const handleUpdateStatus = async (appId: string, newStatus: Application['status']) => {
    try {
      await updateDoc(doc(db, 'applications', appId), {
        status: newStatus,
        lastUpdated: new Date()
      });
      setApplications(prev => prev.map(app => 
        app.id === appId ? { ...app, status: newStatus } : app
      ));
    } catch (error) {
      handleFirestoreError(error, OperationType.UPDATE, `applications/${appId}`);
    }
  };

  const filteredApps = applications.filter(app => {
    if (activeTab === 'pending') return app.status === 'submitted';
    if (activeTab === 'reviewing') return app.status === 'under_review';
    if (activeTab === 'decided') return ['accepted', 'rejected'].includes(app.status);
    return true;
  });

  return (
    <div className="min-h-screen bg-slate-50 font-sans">
        <nav className="bg-white border-b border-slate-200 px-8 py-4 flex justify-between items-center sticky top-0 z-30">
            <div className="flex items-center gap-4">
               <div className="w-10 h-10 bg-slate-900 flex items-center justify-center text-white font-serif font-bold text-xl shadow-lg rounded-lg">
                   {profile.name?.[0] || 'U'}
               </div>
               <div>
                  <h1 className="text-xl font-bold text-slate-900 font-serif leading-none">{profile.name}</h1>
                  <p className="text-[10px] text-brand-600 font-bold uppercase tracking-widest mt-1">Admissions Portal</p>
               </div>
            </div>
            <div className="flex items-center gap-6">
                <button onClick={onLogout} className="text-xs font-bold uppercase tracking-widest text-slate-400 hover:text-slate-900 transition-colors">Sign Out</button>
            </div>
        </nav>

        <main className="max-w-6xl mx-auto p-6 md:p-12">
            <div className="mb-12">
                <h2 className="text-4xl font-serif font-bold text-slate-900 mb-2">Admissions Overview</h2>
                <p className="text-slate-500 font-medium">Review and process student applications for the upcoming semester.</p>
            </div>

            {/* Statistics Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
                {[
                    { label: 'Total Received', value: applications.length, color: 'slate-900' },
                    { label: 'Pending Review', value: applications.filter(a => a.status === 'submitted').length, color: 'blue-600' },
                    { label: 'Under Review', value: applications.filter(a => a.status === 'under_review').length, color: 'orange-500' },
                    { label: 'Decisioned', value: applications.filter(a => ['accepted', 'rejected'].includes(a.status)).length, color: 'green-600' },
                ].map((stat, idx) => (
                    <div key={idx} className="bg-white p-6 border border-slate-200 shadow-sm hover:shadow-md transition-shadow">
                        <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-2">{stat.label}</p>
                        <p className={`text-4xl font-serif font-bold text-${stat.color}`}>{stat.value}</p>
                    </div>
                ))}
            </div>

            {/* Applications List Section */}
            <div className="bg-white border border-slate-200 shadow-sm">
                <div className="border-b border-slate-200 px-8 flex">
                    {(['pending', 'reviewing', 'decided'] as const).map(tab => (
                        <button
                            key={tab}
                            onClick={() => setActiveTab(tab)}
                            className={`px-6 py-4 text-xs font-bold uppercase tracking-widest transition-all relative
                                ${activeTab === tab ? 'text-slate-900' : 'text-slate-400 hover:text-slate-600'}`}
                        >
                            {tab}
                            {activeTab === tab && <div className="absolute bottom-0 left-0 w-full h-1 bg-slate-900"></div>}
                        </button>
                    ))}
                </div>

                <div className="p-0">
                    {isLoading ? (
                        <div className="p-20 text-center text-slate-400">Loading applications...</div>
                    ) : filteredApps.length === 0 ? (
                        <div className="p-20 text-center">
                            <p className="text-slate-400 font-medium italic">No applications in this category.</p>
                        </div>
                    ) : (
                        <div className="overflow-x-auto">
                            <table className="w-full text-left">
                                <thead className="bg-slate-50 border-b border-slate-200">
                                    <tr>
                                        <th className="px-8 py-4 text-[10px] font-bold text-slate-400 uppercase tracking-widest">Candidate</th>
                                        <th className="px-8 py-4 text-[10px] font-bold text-slate-400 uppercase tracking-widest">Major</th>
                                        <th className="px-8 py-4 text-[10px] font-bold text-slate-400 uppercase tracking-widest">GPA</th>
                                        <th className="px-8 py-4 text-[10px] font-bold text-slate-400 uppercase tracking-widest">Status</th>
                                        <th className="px-8 py-4 text-[10px] font-bold text-slate-400 uppercase tracking-widest text-right">Actions</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-slate-100">
                                    {filteredApps.map(app => (
                                        <tr key={app.id} className="hover:bg-slate-50/50 transition-colors group">
                                            <td className="px-8 py-5">
                                                <div className="font-bold text-slate-900">{app.formData.personal?.fullName || "Anonymous"}</div>
                                                <div className="text-xs text-slate-400 lowercase italic">{app.formData.personal?.email}</div>
                                            </td>
                                            <td className="px-8 py-5">
                                                <div className="text-sm font-medium text-slate-600">{app.formData.academic?.major || "Undecided"}</div>
                                            </td>
                                            <td className="px-8 py-5">
                                                <div className="text-sm font-mono font-bold text-slate-400">{app.formData.academic?.gpa || "N/A"}</div>
                                            </td>
                                            <td className="px-8 py-5">
                                                <span className={`px-2 py-1 text-[10px] font-bold uppercase tracking-widest border ${
                                                    app.status === 'accepted' ? 'bg-green-50 text-green-700 border-green-100' :
                                                    app.status === 'rejected' ? 'bg-red-50 text-red-700 border-red-100' :
                                                    'bg-blue-50 text-blue-700 border-blue-100'
                                                }`}>
                                                    {app.status.replace('_', ' ')}
                                                </span>
                                            </td>
                                            <td className="px-8 py-5 text-right space-x-3 opacity-0 group-hover:opacity-100 transition-opacity">
                                                {app.status === 'submitted' && (
                                                    <button 
                                                        onClick={() => handleUpdateStatus(app.id, 'under_review')}
                                                        className="text-[10px] font-bold uppercase tracking-widest text-blue-600 hover:underline"
                                                    >
                                                        Review
                                                    </button>
                                                )}
                                                {app.status === 'under_review' && (
                                                    <>
                                                        <button 
                                                            onClick={() => handleUpdateStatus(app.id, 'accepted')}
                                                            className="text-[10px] font-bold uppercase tracking-widest text-green-600 hover:underline"
                                                        >
                                                            Accept
                                                        </button>
                                                        <button 
                                                            onClick={() => handleUpdateStatus(app.id, 'rejected')}
                                                            className="text-[10px] font-bold uppercase tracking-widest text-red-600 hover:underline"
                                                        >
                                                            Reject
                                                        </button>
                                                    </>
                                                )}
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </div>
            </div>
        </main>
    </div>
  );
};

export default UniversityDashboard;
