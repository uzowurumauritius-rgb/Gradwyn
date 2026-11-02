
export interface AuthUser {
  id: string;
  email: string;
  emailVerified: boolean;
  name: string;
  image?: string;
  createdAt: Date;
  updatedAt: Date;
  type: 'applicant' | 'mentor' | 'university';
}

export type ApplicationStatus = 'draft' | 'submitted' | 'under_review' | 'accepted' | 'rejected';

export interface Application {
  id: string;
  type: 'university' | 'scholarship';
  university?: University;
  scholarship?: Scholarship;
  status: ApplicationStatus;
  submittedDate?: Date;
  lastUpdated: Date;
  progress: number; // 0-100
  currentStep: number; // 1-4
  formData: {
    personal?: {
      fullName?: string;
      email?: string;
      phone?: string;
      address?: string;
    };
    academic?: {
      gpa?: string;
      major?: string;
    };
    essay?: string;
  };
}

export interface UserProfile {
  // Identity
  id: string;
  email: string;
  name: string;
  photoUrl?: string;
  
  // Demographics & Background
  citizenship: string;
  
  // Research Preferences
  degreeLevel: string;
  fieldOfStudy: string;
  budgetRange: string;
  preferredLocations: string[];
  keyMetrics: string[];
  vibe: string[];
  priorities: string;
  
  // State
  savedSchools: University[];
  discardedSchools: string[]; 
}

export interface MentorProfile {
  id: string;
  name: string;
  photoUrl: string;
  university: string;
  major: string; // Functions as "Role" or "Field"
  bio: string;
  email: string;
  linkedin: string;
  isAvailable: boolean;
  studentsGuided: number;
  tags: string[];
}

export interface UniversityProfile {
  id: string; 
  name: string;
  email: string;
  website: string;
  logoUrl?: string;
  location: string;
  description: string;
  programs: string[];
}

export interface OnboardingQuestion {
  id: keyof UserProfile;
  question: string;
  subtext?: string;
  type: 'text' | 'select' | 'multiselect' | 'button-group';
  options?: string[];
  placeholder?: string;
}

export interface GroundingSource {
  title: string;
  uri: string;
  placeAnswerSources?: { reviewSnippets: { snippet: string }[] }
}

export interface University {
  id: string;
  name: string;
  location: string;
  matchScore: number;
  tuition: string;
  description: string;
  website: string;
  tags: string[];
  logo?: string; // URL
  images?: string[]; // Array of URLs
  acceptanceRate?: string;
  ranking?: string;
  studentBody?: string;
  programs?: string[];
}

export interface Mentor {
  id: string;
  name: string;
  role: string;
  university: string;
  image: string;
  bio: string;
  availability: string;
  isAvailable: boolean; // Added for filtering
  tags: string[];
  email: string;
  linkedin: string;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'model';
  text: string;
  timestamp: Date;
  sources?: GroundingSource[];
  isThinking?: boolean;
  recommendations?: University[];
}

export interface ChatState {
  messages: ChatMessage[];
  isLoading: boolean;
}

export interface Scholarship {
  id: string;
  name: string;
  provider: string;
  amount: string;
  deadline: string;
  location?: string;
  tags: string[];
  description: string;
}

export interface Guide {
  id: string;
  title: string;
  category: string;
  readTime: string;
  image: string;
  description: string;
}
