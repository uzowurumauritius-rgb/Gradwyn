
import { OnboardingQuestion, Mentor, University, Scholarship, Guide } from './types';

export const ONBOARDING_STEPS: OnboardingQuestion[] = [
  {
    id: 'name',
    question: "Welcome to Gradwyn. How should we address you?",
    type: 'text',
    placeholder: "Enter your full legal name"
  },
  {
    id: 'citizenship',
    question: "What is your country of citizenship?",
    subtext: "This determines visa requirements and international scholarship eligibility.",
    type: 'text',
    placeholder: "e.g. United States, India, Brazil, Nigeria"
  },
  {
    id: 'degreeLevel',
    question: "What academic distinction are you pursuing?",
    type: 'button-group',
    options: ["Bachelor's", "Master's", "PhD", "MBA", "JD", "MD"]
  },
  {
    id: 'fieldOfStudy',
    question: "In which field do you intend to specialize?",
    subtext: "It is acceptable if this is still a developing interest.",
    type: 'text',
    placeholder: "e.g. Economics, Art History, Bioengineering"
  },
  {
    id: 'preferredLocations',
    question: "Where in the world do you wish to study?",
    subtext: "Select as many as apply.",
    type: 'multiselect',
    options: [
        "USA - East Coast", 
        "USA - West Coast", 
        "USA - Midwest", 
        "USA - South",
        "Canada", 
        "UK - London", 
        "UK - Other",
        "Europe (EU)", 
        "Europe (Non-EU)",
        "Australia/NZ", 
        "Asia", 
        "Africa", 
        "South America",
        "Middle East",
        "Latin America (LATAM)",
        "Asia-Pacific (APAC)",
        "Europe, Middle East, & Africa (EMEA)",
        "Remote/Online"
    ]
  },
  {
    id: 'budgetRange',
    question: "What is your annual tuition investment range?",
    subtext: "This assists in curating viable options.",
    type: 'button-group',
    options: ["Under $15k", "$15k - $30k", "$30k - $50k", "$50k+", "Full Scholarship Required"]
  },
  {
    id: 'keyMetrics',
    question: "What elements define your ideal institution?",
    subtext: "Select your top 3 priorities.",
    type: 'multiselect',
    options: [
        "Academic Prestige",
        "Financial Aid & Value",
        "Campus Culture",
        "Safety & Location",
        "Career & Alumni Network",
        "Diversity & Inclusion",
        "Research Facilities",
        "Athletics"
    ]
  },
  {
    id: 'vibe',
    question: "What atmosphere suits you best?",
    subtext: "Select up to 3.",
    type: 'multiselect',
    options: [
      "Metropolitan", 
      "Historic College Town", 
      "Research Intensive", 
      "Socially Active", 
      "Athletic Focused", 
      "Intimate Community", 
      "Scenic / Outdoors",
      "Pre-Professional",
      "Liberal Arts",
      "Doesn't matter to me"
    ]
  },
  {
    id: 'priorities',
    question: "Any final specific requirements?",
    subtext: "e.g., Debate society, accessibility needs, specific internship programs...",
    type: 'text',
    placeholder: "Outline your must-haves..."
  }
];

export const MOCK_MENTORS: Mentor[] = [
  {
    id: 'm1',
    name: "Dr. Sarah Chen",
    role: "Alumni & Research Lead",
    university: "Stanford University",
    image: "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=150&h=150",
    bio: "PhD in Computer Science. Happy to answer questions about research grants and finding lab placements at Stanford.",
    availability: "Mon, Wed 2pm-5pm EST",
    isAvailable: true,
    tags: ["STEM", "Research", "PhD"],
    email: "sarah.chen@alumni.stanford.edu",
    linkedin: "https://linkedin.com/in/sarahchen-demo"
  },
  {
    id: 'm2',
    name: "Marcus Johnson",
    role: "Senior Student Ambassador",
    university: "University of Manchester",
    image: "https://images.unsplash.com/photo-1566492031773-4f4e44671857?auto=format&fit=crop&w=150&h=150",
    bio: "Final year Engineering student. Ask me about finding housing, student societies, and the international student experience in the UK.",
    availability: "Fri 10am-1pm GMT",
    isAvailable: true,
    tags: ["Engineering", "Student Life", "International"],
    email: "marcus.j@student.manchester.ac.uk",
    linkedin: "https://linkedin.com/in/marcusj-demo"
  },
  {
    id: 'm3',
    name: "Elena Rodriguez",
    role: "Admissions Consultant",
    university: "Columbia University",
    image: "https://images.unsplash.com/photo-1580489944761-15a19d654956?auto=format&fit=crop&w=150&h=150",
    bio: "Former admissions officer. I can provide insights on essay writing and interview prep for Ivy League schools.",
    availability: "Tue, Thu 4pm-7pm EST",
    isAvailable: false,
    tags: ["Admissions", "Essay Review", "Liberal Arts"],
    email: "elena.rodriguez@columbia.edu",
    linkedin: "https://linkedin.com/in/elenar-demo"
  },
  {
    id: 'm4',
    name: "Akwasi Mensah",
    role: "Graduate Mentor",
    university: "University of Cape Town",
    image: "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?auto=format&fit=crop&w=150&h=150",
    bio: "Focusing on sustainable development. Reach out if you have questions about scholarships and living in Cape Town.",
    availability: "Sat 9am-12pm SAST",
    isAvailable: true,
    tags: ["Development", "Scholarships", "Africa"],
    email: "akwasi.mensah@uct.ac.za",
    linkedin: "https://linkedin.com/in/akwasim-demo"
  }
];

export const MOCK_SCHOLARSHIPS: Scholarship[] = [
    {
        id: 'sch1',
        name: 'Fulbright Foreign Student Program',
        provider: 'U.S. Department of State',
        amount: 'Full Tuition + Stipend',
        deadline: 'Oct 15, 2025',
        location: 'USA',
        tags: ['Global', 'Masters', 'PhD', 'Fully-funded'],
        description: 'Enables graduate students, young professionals and artists from abroad to study and conduct research in the United States.'
    },
    {
        id: 'sch2',
        name: 'Chevening Scholarship',
        provider: 'UK Government',
        amount: 'Full Funding',
        deadline: 'Nov 02, 2025',
        location: 'UK',
        tags: ['UK', 'Masters', 'Leadership', 'Fully-funded'],
        description: 'Chevening is the UK government’s international awards program aimed at developing global leaders.'
    },
    {
        id: 'sch-ba1',
        name: 'Ashinaga Africa Initiative',
        provider: 'Ashinaga Foundation',
        amount: 'Full Funding',
        deadline: 'Jan 20, 2026',
        location: 'Global',
        tags: ['Africa Specific', 'Bachelors', 'Fully-funded', 'Leadership'],
        description: 'An international leadership program that cultivates the next generation of leaders to contribute to the development of sub-Saharan Africa. Covers tuition, accommodation, and travel.'
    },
    {
        id: 'sch-ba2',
        name: 'Mastercard Foundation Scholars Program',
        provider: 'Mastercard Foundation',
        amount: 'Full Funding',
        deadline: 'Dec 01, 2025',
        location: 'USA, Canada, Africa',
        tags: ['Africa Specific', 'Bachelors', 'Masters', 'Fully-funded'],
        description: 'Provides talented young people from economically disadvantaged communities, particularly in Africa, with access to quality university education.'
    },
    {
        id: 'sch-ba3',
        name: 'Reach Oxford Scholarship',
        provider: 'University of Oxford',
        amount: 'Tuition + Living',
        deadline: 'Feb 15, 2026',
        location: 'UK',
        tags: ['UK', 'Bachelors', 'Fully-funded', 'Need-Based'],
        description: 'Offered to students from low-income countries who, for political or financial reasons, or because suitable educational facilities do not exist, cannot study for a degree in their own countries.'
    },
    {
        id: 'sch3',
        name: 'Rhodes Scholarship',
        provider: 'Rhodes Trust',
        amount: 'Full Tuition + Living',
        deadline: 'Oct 01, 2025',
        location: 'UK',
        tags: ['UK', 'Masters', 'PhD', 'Fully-funded'],
        description: 'The oldest (first awarded in 1902) and perhaps the most prestigious international scholarship program, enabling young people from around the world to study at the University of Oxford.'
    },
    {
        id: 'sch-ba4',
        name: 'York University International Entrance',
        provider: 'York University',
        amount: '$35,000/year',
        deadline: 'Jan 15, 2026',
        location: 'Canada',
        tags: ['Canada', 'Bachelors', 'Part-funded'],
        description: 'Scholarships for international applicants with excellent academic records admitted to undergraduate degree programs.'
    },
    {
        id: 'sch4',
        name: 'Gates Cambridge Scholarship',
        provider: 'Bill & Melinda Gates Foundation',
        amount: 'Full Cost',
        deadline: 'Dec 05, 2025',
        location: 'UK',
        tags: ['UK', 'PhD', 'Masters', 'Fully-funded'],
        description: 'Applicants must intend to undertake a full-time postgraduate degree at the University of Cambridge and show a commitment to improving the lives of others.'
    },
    {
        id: 'sch5',
        name: 'Erasmus Mundus Joint Masters',
        provider: 'European Union',
        amount: '€1,000/month + Travel',
        deadline: 'Jan 15, 2026',
        location: 'Europe',
        tags: ['Europe', 'Masters', 'Fully-funded'],
        description: 'High-level integrated study programs at master level. The program is designed and delivered by an international partnership of higher education institutions.'
    },
    {
        id: 'sch6',
        name: 'Knight-Hennessy Scholars',
        provider: 'Stanford University',
        amount: 'Full Funding',
        deadline: 'Oct 09, 2025',
        location: 'USA',
        tags: ['USA', 'Masters', 'PhD', 'Fully-funded'],
        description: 'Cultivates and supports a multidisciplinary and multicultural community of graduate students across Stanford University.'
    },
    {
        id: 'sch7',
        name: 'AAUW International Fellowships',
        provider: 'American Association of University Women',
        amount: '$18,000 - $30,000',
        deadline: 'Nov 15, 2025',
        location: 'USA',
        tags: ['USA', 'Women', 'Masters', 'PhD', 'Part-funded'],
        description: 'Support for women pursuing full-time graduate or postdoctoral study in the United States who are not U.S. citizens or permanent residents.'
    },
    {
        id: 'sch8',
        name: 'Schwarzman Scholars',
        provider: 'Blackstone',
        amount: 'Full Funding',
        deadline: 'Sep 19, 2025',
        location: 'Asia',
        tags: ['Asia', 'Masters', 'Fully-funded'],
        description: 'Designed to prepare the next generation of global leaders. Scholars pursue a one-year Master’s degree at Tsinghua University in Beijing.'
    },
    {
        id: 'sch9',
        name: 'Vanier Canada Graduate Scholarships',
        provider: 'Government of Canada',
        amount: '$50,000/year',
        deadline: 'Nov 01, 2025',
        location: 'Canada',
        tags: ['Canada', 'PhD', 'Research', 'Part-funded'],
        description: 'Attracts and retains world-class doctoral students and establishes Canada as a global center of excellence in research and higher learning.'
    },
    {
        id: 'sch10',
        name: 'Aga Khan Foundation ISP',
        provider: 'Aga Khan Foundation',
        amount: '50% Grant / 50% Loan',
        deadline: 'Mar 31, 2026',
        location: 'Global',
        tags: ['Global', 'Masters', 'PhD', 'Need-Based', 'Part-funded'],
        description: 'Provides a limited number of scholarships each year for postgraduate studies to outstanding students from select developing countries.'
    }
];

export const MOCK_GUIDES: Guide[] = [
    {
        id: 'g1',
        title: 'Mastering the Personal Statement',
        category: 'Essay Writing',
        readTime: '8 min read',
        image: 'https://images.unsplash.com/photo-1455390582262-044cdead277a?auto=format&fit=crop&w=400&q=80',
        description: 'Learn the narrative structures that captivate admissions officers and how to avoid common clichés.'
    },
    {
        id: 'g2',
        title: 'Cracking the Ivy League Interview',
        category: 'Interview Prep',
        readTime: '12 min read',
        image: 'https://images.unsplash.com/photo-1557804506-669a67965ba0?auto=format&fit=crop&w=400&q=80',
        description: 'Strategic frameworks for answering "Tell me about yourself" and "Why this school?" with impact.'
    },
    {
        id: 'g3',
        title: 'Demystifying Financial Aid Packages',
        category: 'Financial Planning',
        readTime: '10 min read',
        image: 'https://images.unsplash.com/photo-1554224155-6726b3ff858f?auto=format&fit=crop&w=400&q=80',
        description: 'A comprehensive guide to understanding FAFSA, CSS Profile, and negotiating your aid offer.'
    },
    {
        id: 'g4',
        title: 'The Art of the Recommendation Letter',
        category: 'Application Strategy',
        readTime: '6 min read',
        image: 'https://images.unsplash.com/photo-1586281380349-632531db7ed4?auto=format&fit=crop&w=400&q=80',
        description: 'Who to ask, when to ask, and how to prepare a "brag sheet" to ensure glowing references.'
    },
    {
        id: 'g5',
        title: 'GRE vs GMAT: Choosing Your Path',
        category: 'Standardized Testing',
        readTime: '7 min read',
        image: 'https://images.unsplash.com/photo-1434030216411-0b793f4b4173?auto=format&fit=crop&w=400&q=80',
        description: 'A comparative analysis of exam structures and how different graduate programs view them.'
    }
];

// Reliable high-quality architectural images
export const UNI_IMAGES = [
    "https://images.unsplash.com/photo-1562774053-701939374585?q=80&w=800&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1592280771884-4284b19273f2?q=80&w=800&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?q=80&w=800&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1541339907198-e08756dedf3f?q=80&w=800&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?q=80&w=800&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1564981797816-1043664bf78d?q=80&w=800&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1580659446629-284e3dd498d7?q=80&w=800&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1622396090064-2c895861e3f4?q=80&w=800&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1576764698177-20604ec432c9?q=80&w=800&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1590579491624-f98f36d4c763?q=80&w=800&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1617634667039-8e4cb277ab46?q=80&w=800&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1590082870347-b23722c05d3f?q=80&w=800&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1568792923760-d70635a89fdc?q=80&w=800&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1525921429624-479b6a26d84d?q=80&w=800&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1462536943532-57a629f6cc60?q=80&w=800&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1565514020176-8002c77e7cfa?q=80&w=800&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1504042535685-d1a5a072f324?q=80&w=800&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1558452020-f06610f5c724?q=80&w=800&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1492538368677-f6e0afe31dcc?q=80&w=800&auto=format&fit=crop",
    "https://images.unsplash.com/photo-1560526860-42eb5f78b3d5?q=80&w=800&auto=format&fit=crop"
];

export const MOCK_DATABASE_UNIVERSITIES: University[] = [
  {
    id: 'd1',
    name: "Massachusetts Institute of Technology",
    location: "Cambridge, MA, USA",
    matchScore: 98,
    tuition: "$57,000/yr",
    description: "World-renowned for STEM. Intense research focus with a collaborative, albeit stressful, culture.",
    website: "https://www.mit.edu",
    tags: ["Top Ranked", "Research", "Urban"],
    logo: "https://upload.wikimedia.org/wikipedia/commons/0/0c/MIT_logo.svg", 
    images: [UNI_IMAGES[5], UNI_IMAGES[2]]
  },
  {
    id: 'd2',
    name: "University of Oxford",
    location: "Oxford, UK",
    matchScore: 95,
    tuition: "£30,000/yr (Intl)",
    description: "Historic collegiate university. Unique tutorial system offering personalized academic attention.",
    website: "https://www.ox.ac.uk",
    tags: ["Historic", "Prestige", "Collegiate"],
    logo: "https://upload.wikimedia.org/wikipedia/commons/f/ff/Oxford_University_Coat_Of_Arms.svg",
    images: [UNI_IMAGES[6], UNI_IMAGES[1]]
  },
  {
    id: 'd3',
    name: "University of Toronto",
    location: "Toronto, Canada",
    matchScore: 90,
    tuition: "$45,000 CAD/yr",
    description: "Major research hub in a diverse global city. Large class sizes but incredible networking opportunities.",
    website: "https://www.utoronto.ca",
    tags: ["Diverse", "Urban", "Research"],
    logo: "https://upload.wikimedia.org/wikipedia/en/0/04/Utoronto_coat.svg",
    images: [UNI_IMAGES[7], UNI_IMAGES[3]]
  },
  {
    id: 'd4',
    name: "University of Cape Town",
    location: "Cape Town, South Africa",
    matchScore: 88,
    tuition: "$15,000/yr",
    description: "Top university in Africa. Stunning campus setting and strong focus on development studies.",
    website: "https://www.uct.ac.za",
    tags: ["Scenic", "Development", "Africa"],
    logo: "https://upload.wikimedia.org/wikipedia/en/7/7c/University_of_Cape_Town_logo.svg",
    images: [UNI_IMAGES[8], UNI_IMAGES[4]]
  },
  {
    id: 'alu-rw',
    name: "African Leadership University - Rwanda",
    location: "Kigali, Rwanda",
    matchScore: 89,
    tuition: "$3,000/yr",
    description: "A mission-driven university nurturing the next generation of African leaders. Innovative, student-led project-based learning model in the heart of Kigali.",
    website: "https://www.alueducation.com",
    tags: ["Leadership", "Innovation", "Africa"],
    logo: "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/African_Leadership_University_logo.png/640px-African_Leadership_University_logo.png",
    images: ["https://images.unsplash.com/photo-1523240795612-9a054b0db644?q=80&w=800&auto=format&fit=crop", UNI_IMAGES[0]]
  },
  {
    id: 'alu-mu',
    name: "African Leadership University - Mauritius",
    location: "Pamplemousses, Mauritius",
    matchScore: 87,
    tuition: "$3,000/yr",
    description: "Located in the beautiful island nation, focusing on ethical leadership and entrepreneurial thinking in a diverse pan-African environment.",
    website: "https://www.alueducation.com",
    tags: ["Entrepreneurship", "Diversity", "Island Campus"],
    logo: "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/African_Leadership_University_logo.png/640px-African_Leadership_University_logo.png",
    images: ["https://images.unsplash.com/photo-1596462502278-27bfdd403348?q=80&w=800&auto=format&fit=crop", UNI_IMAGES[1]]
  }
];

export const AUTOCOMPLETE_UNIVERSITIES: University[] = [
    ...MOCK_DATABASE_UNIVERSITIES,
    { id: 's1', name: 'Harvard University', location: 'Cambridge, MA', matchScore: 96, tuition: '$57,000/yr', description: 'The oldest institution of higher learning in the US.', website: 'https://harvard.edu', tags: ['Ivy League', 'Historic', 'Research'], logo: 'https://upload.wikimedia.org/wikipedia/en/2/29/Harvard_shield_wreath.svg', images: ["https://images.unsplash.com/photo-1559136555-9303baea8ebd?q=80&w=800&auto=format&fit=crop", UNI_IMAGES[1]] },
    { id: 's2', name: 'Stanford University', location: 'Stanford, CA', matchScore: 97, tuition: '$56,000/yr', description: 'Known for entrepreneurial spirit and computer science.', website: 'https://stanford.edu', tags: ['Tech', 'Entrepreneurship'], logo: 'https://upload.wikimedia.org/wikipedia/commons/b/b5/Seal_of_Stanford_University.svg', images: ["https://images.unsplash.com/photo-1604871000636-074fa5117945?q=80&w=800&auto=format&fit=crop", UNI_IMAGES[3]] },
    { id: 's3', name: 'ETH Zurich', location: 'Zurich, Switzerland', matchScore: 92, tuition: '$1,500/yr', description: 'Leading STEM university in Europe.', website: 'https://ethz.ch', tags: ['STEM', 'Europe', 'Low Tuition'], logo: 'https://upload.wikimedia.org/wikipedia/commons/9/99/ETH_Z%C3%BCrich_Logo_black.svg', images: ["https://images.unsplash.com/photo-1522008629172-055a56fe00ef?q=80&w=800&auto=format&fit=crop", UNI_IMAGES[0]] },
    { id: 's4', name: 'National University of Singapore', location: 'Singapore', matchScore: 91, tuition: '$30,000/yr', description: 'Comprehensive research university in Asia.', website: 'https://nus.edu.sg', tags: ['Asia', 'Research', 'Global'], logo: 'https://upload.wikimedia.org/wikipedia/en/b/b9/NUS_coat_of_arms.svg', images: ["https://images.unsplash.com/photo-1552914873-986293458947?q=80&w=800&auto=format&fit=crop", UNI_IMAGES[2]] },
    { id: 's5', name: 'Yale University', location: 'New Haven, CT', matchScore: 94, tuition: '$60,000/yr', description: 'Known for drama, music, and secret societies.', website: 'https://yale.edu', tags: ['Ivy League', 'Arts', 'Historic'], logo: 'https://upload.wikimedia.org/wikipedia/commons/0/07/Yale_University_Shield_1.svg', images: ["https://images.unsplash.com/photo-1582642984008-46d16528b855?q=80&w=800&auto=format&fit=crop", UNI_IMAGES[4]] }
];
