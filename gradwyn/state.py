"""Central Reflex Application State for Gradwyn MVP.

Manages:
- Multi-role Authentication (Student, Mentor, University) + 1-Click YC Demo Accounts
- SQLite / PostgreSQL Persistence via SQLModel (`UserAccount`, `MentorListing`, `ApplicationSubmission`, `FeedbackEntry`)
- 9-Step Student Onboarding & 4-Step Mentor Onboarding
- Gemini 3.8 Flash AI Advisor Chat + Google Search Grounding + Split-Screen University Match Deck
- Student Dashboard (Overview, Candidacy Tracker, Scholarships Hub, Mentorship Network, AI Prep Suite, Guides)
- 4-Step Interactive University & Scholarship Application Wizard
- Mentor Portal (Live Profile Editor & Availability Toggle synced to Student Mentorship Network)
- University Admissions Portal (Live Applicant Review, Dossier Modal, Accept / Reject / Filter)
"""

from __future__ import annotations

import hashlib
import json
import uuid
from datetime import datetime
from typing import Any

import reflex as rx
from sqlmodel import SQLModel, select

from .ai_service import (
    _fallback_advisor_response,
    _score_curated_universities,
    critique_essay_with_ai,
    evaluate_interview_answer,
    generate_advisor_response,
)
from .constants import (
    GLOBAL_UNIVERSITIES,
    GUIDES_DATA,
    INITIAL_CANDIDATE_APPLICATIONS,
    INITIAL_MENTORS,
    ONBOARDING_STEPS,
    SCHOLARSHIPS_DATA,
)
from .models import (
    ApplicationSubmission,
    CandidateAppItem,
    ChatMessageItem,
    ChecklistItem,
    FeedbackEntry,
    GuideItem,
    MentorItem,
    MentorListing,
    OnboardingStepItem,
    ScholarshipItem,
    StudentAppItem,
    UniversityItem,
    UserAccount,
)

INTERVIEW_QUESTIONS: list[str] = [
    "Tell us about a problem in your community that you took initiative to solve, and how it shaped your academic goals.",
    "Why is our institution the ideal environment for your degree, and how will you contribute to our campus community?",
    "Describe a time when a project or academic goal did not go as planned. How did you adapt?",
    "How will you use your education and scholarship funding to create measurable impact in your home country or region?",
    "What is an intellectual topic or research question outside your comfort zone that excites you right now?",
]


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


class AppState(rx.State):
    """Unified full-stack state for the Gradwyn platform."""

    # ------------------------------------------------------------------
    # Navigation & Global UI State
    # ------------------------------------------------------------------
    is_authenticated: bool = False
    user_id: str = ""
    user_email: str = ""
    user_name: str = ""
    user_role: str = "student"  # "student" | "mentor" | "university"
    toast_message: str = ""

    # ------------------------------------------------------------------
    # Auth Form State
    # ------------------------------------------------------------------
    auth_mode: str = "login"  # "login" | "signup"
    auth_role_tab: str = "student"  # "student" | "mentor" | "university"
    auth_name_input: str = ""
    auth_email_input: str = ""
    auth_password_input: str = ""
    auth_university_input: str = "African Leadership University (ALU) - Mauritius"
    auth_error: str = ""

    # ------------------------------------------------------------------
    # Student Profile & 9-Step Onboarding State
    # ------------------------------------------------------------------
    onboarding_step: int = 0
    profile_name: str = ""
    profile_country: str = ""
    profile_education_level: str = "High School Senior"
    profile_target_degree: str = "Bachelor's (BSc/BA)"
    profile_academic_interests: list[str] = ["Computer Science & AI", "Business & Finance"]
    profile_gpa: str = ""
    profile_test_scores: str = ""
    profile_preferred_locations: list[str] = ["North America (US & Canada)", "Europe & UK", "Africa (ALU, UCT, Ashesi)"]
    profile_budget: str = "Need Full Financial Aid / Scholarship"
    profile_extracurriculars: str = ""
    profile_career_goals: str = ""
    custom_interest_input: str = ""

    # ------------------------------------------------------------------
    # AI Chat & University Recommendation State
    # ------------------------------------------------------------------
    chat_messages: list[ChatMessageItem] = []
    chat_input: str = ""
    is_ai_loading: bool = False
    previous_interaction_id: str = ""
    recommended_universities: list[UniversityItem] = []
    saved_universities: list[UniversityItem] = []
    discarded_university_names: list[str] = []

    # ------------------------------------------------------------------
    # Student Dashboard Navigation & Search State
    # ------------------------------------------------------------------
    dashboard_tab: str = "overview"  # "overview" | "candidacy" | "scholarships" | "mentors" | "prep" | "guides"
    uni_search_query: str = ""
    scholarship_filter: str = "all"  # "all" | "for_you"
    scholarship_search_query: str = ""
    mentor_search_query: str = ""
    mentor_only_available: bool = False

    # ------------------------------------------------------------------
    # Applications & Candidacy State
    # ------------------------------------------------------------------
    student_applications: list[StudentAppItem] = []
    # 4-Step Application Wizard Modal
    is_apply_modal_open: bool = False
    apply_step: int = 1
    apply_target_name: str = ""
    apply_target_type: str = "University"  # "University" | "Scholarship"
    apply_target_location: str = ""
    apply_target_deadline: str = ""
    apply_target_fee: str = ""
    apply_program: str = "BSc Computer Science & AI"
    apply_essay: str = ""
    apply_doc_transcript: bool = True
    apply_doc_cv: bool = True
    apply_doc_recommendation: bool = True
    apply_submitted_success: bool = False

    # ------------------------------------------------------------------
    # Prep Suite (AI Essay Reviewer, AI Mock Interview, Checklist)
    # ------------------------------------------------------------------
    prep_active_tool: str = "essay"  # "essay" | "interview" | "checklist"
    prep_essay_target: str = "Massachusetts Institute of Technology (MIT)"
    prep_essay_draft: str = (
        "Growing up in Lagos and studying in Mauritius, I saw firsthand how access to reliable educational tools transforms trajectories. "
        "When power outages disrupted our school's computer lab, I built an offline-first peer learning platform on Raspberry Pi servers that served 180 students across three schools. "
        "Leading a team of four student developers taught me that technical elegance only matters when paired with deep human empathy. "
        "I am applying to study Computer Science and Artificial Intelligence so I can research low-resource machine learning systems and scale educational access across emerging markets."
    )
    prep_essay_result: dict[str, Any] = {}
    prep_essay_strengths: list[str] = []
    prep_essay_improvements: list[str] = []
    is_prep_essay_loading: bool = False

    prep_interview_question: str = INTERVIEW_QUESTIONS[0]
    prep_interview_answer: str = (
        "In my junior year, I noticed that over 150 students at neighboring schools had no access to coding mentorship. "
        "I organized a weekend peer-coding initiative using refurbished laptops and offline Python environments. "
        "Within two semesters, 45 students built working community projects and three won regional STEM awards. "
        "This experience solidified my goal to study Computer Science and build scalable learning technology."
    )
    prep_interview_result: dict[str, Any] = {}
    is_prep_interview_loading: bool = False

    checklist_items: list[ChecklistItem] = [
        {"id": "transcript", "label": "Official High School / Undergraduate Transcripts Evaluated", "category": "Academic", "done": True},
        {"id": "tests", "label": "Standardized Test Scores (SAT / ACT / GRE / IELTS / TOEFL)", "category": "Testing", "done": True},
        {"id": "essay", "label": "Personal Statement & Supplemental Why-Us Essays Critiqued", "category": "Essays", "done": True},
        {"id": "recs", "label": "2 Academic Recommendation Letters Requested & Waived FERPA", "category": "Recommendations", "done": False},
        {"id": "css", "label": "CSS Profile / ISFAA / Mastercard Foundation Financial Aid Dossier", "category": "Financial Aid", "done": False},
        {"id": "portfolio", "label": "Extracurricular Impact Resume & GitHub / Leadership Portfolio", "category": "Activities", "done": True},
    ]

    # ------------------------------------------------------------------
    # Modals State (Edit Profile, Guide Reader, Feedback)
    # ------------------------------------------------------------------
    is_edit_profile_open: bool = False
    is_guide_modal_open: bool = False
    active_guide: GuideItem = {
        "id": "",
        "title": "",
        "category": "",
        "readTime": "",
        "author": "",
        "authorRole": "",
        "imageUrl": "",
        "description": "",
        "content": "",
    }
    is_feedback_modal_open: bool = False
    feedback_rating: int = 5
    feedback_category: str = "general"
    feedback_comment: str = ""
    feedback_submitted: bool = False

    # ------------------------------------------------------------------
    # Mentor Portal & Mentorship Network State
    # ------------------------------------------------------------------
    mentors_list: list[MentorItem] = []
    mentor_onboarding_step: int = 1
    mentor_name: str = "Dr. Sarah Jenkins"
    mentor_role: str = "PhD Candidate & Admissions Fellow"
    mentor_university: str = "Stanford University"
    mentor_location: str = "Stanford, USA"
    mentor_bio: str = "Helping international students navigate CS & AI admissions, Knight-Hennessy fellowships, and research statements."
    mentor_specialties: list[str] = ["Computer Science & AI", "Knight-Hennessy Prep", "Statement of Purpose"]
    mentor_linkedin: str = "https://www.linkedin.com"
    mentor_available: bool = True
    mentor_custom_specialty: str = ""

    # ------------------------------------------------------------------
    # University Admissions Portal State
    # ------------------------------------------------------------------
    partner_university_name: str = "All Partner Institutions"
    uni_portal_filter_status: str = "All"  # "All" | "Submitted" | "Under Review" | "Accepted" | "Rejected"
    uni_portal_search: str = ""
    all_candidate_applications: list[CandidateAppItem] = []
    is_candidate_modal_open: bool = False
    selected_candidate: CandidateAppItem = {
        "id": "",
        "studentName": "",
        "studentEmail": "",
        "country": "",
        "targetName": "",
        "targetType": "University",
        "program": "",
        "gpa": "",
        "testScores": "",
        "matchScore": 95,
        "status": "Submitted",
        "submittedDate": "",
        "personalStatement": "",
        "documents": [],
    }

    # ==================================================================
    # Database Initialization & Sync Helpers
    # ==================================================================
    def _ensure_db_initialized(self) -> None:
        """Create SQLModel tables and seed initial mentors and applications if empty."""
        try:
            from sqlmodel import create_engine
            db_url = rx.config.get_config().db_url or "sqlite:///gradwyn.db"
            engine = create_engine(db_url)
            SQLModel.metadata.create_all(engine)
        except Exception:
            pass

        with rx.session() as session:
            # Seed mentors if empty
            existing_mentors = session.exec(select(MentorListing)).all()
            if not existing_mentors:
                for m in INITIAL_MENTORS:
                    session.add(
                        MentorListing(
                            mentor_uid=m["id"],
                            name=m["name"],
                            role=m["role"],
                            university=m["university"],
                            location=m["location"],
                            bio=m["bio"],
                            specialties_json=json.dumps(m["specialties"]),
                            image_url=m["imageUrl"],
                            linkedin=m["linkedin"],
                            available=bool(m["available"]),
                        )
                    )
                session.commit()

            # Seed initial candidate applications if empty
            existing_apps = session.exec(select(ApplicationSubmission)).all()
            if not existing_apps:
                for app in INITIAL_CANDIDATE_APPLICATIONS:
                    session.add(
                        ApplicationSubmission(
                            app_uid=app["id"],
                            student_uid="demo-seed",
                            student_name=app["studentName"],
                            student_email=app["studentEmail"],
                            country=app["country"],
                            target_name=app["targetName"],
                            target_type=app["targetType"],
                            program=app["program"],
                            gpa=app["gpa"],
                            test_scores=app["testScores"],
                            match_score=int(app["matchScore"]),
                            status=app["status"],
                            submitted_date=app["submittedDate"],
                            personal_statement=app["personalStatement"],
                            documents_json=json.dumps(app["documents"]),
                        )
                    )
                session.commit()

        self._refresh_from_db()

    def _refresh_from_db(self) -> None:
        """Sync in-memory lists from SQLModel database tables."""
        with rx.session() as session:
            db_mentors = session.exec(select(MentorListing)).all()
            self.mentors_list = [
                {
                    "id": m.mentor_uid,
                    "name": m.name,
                    "role": m.role,
                    "university": m.university,
                    "location": m.location,
                    "bio": m.bio,
                    "specialties": json.loads(m.specialties_json or "[]"),
                    "imageUrl": m.image_url,
                    "linkedin": m.linkedin,
                    "available": m.available,
                }
                for m in db_mentors
            ]

            db_apps = session.exec(select(ApplicationSubmission)).all()
            self.all_candidate_applications = [
                {
                    "id": a.app_uid,
                    "studentName": a.student_name,
                    "studentEmail": a.student_email,
                    "country": a.country,
                    "targetName": a.target_name,
                    "targetType": a.target_type,
                    "program": a.program,
                    "gpa": a.gpa,
                    "testScores": a.test_scores,
                    "matchScore": a.match_score,
                    "status": a.status,
                    "submittedDate": a.submitted_date,
                    "personalStatement": a.personal_statement,
                    "documents": json.loads(a.documents_json or "[]"),
                }
                for a in reversed(db_apps)
            ]

    def on_app_load(self) -> None:
        """Lifecycle hook run when any page loads."""
        self._ensure_db_initialized()
        if not self.recommended_universities:
            self.recommended_universities = _score_curated_universities(self._get_profile_dict())
        if not self.saved_universities:
            self.saved_universities = self.recommended_universities[:3]
        if not self.student_applications and self.all_candidate_applications:
            self.student_applications = [
                {
                    "id": a["id"],
                    "name": a["targetName"],
                    "type": a["targetType"],
                    "status": a["status"],
                    "deadline": "Jan 15, 2027",
                    "submittedDate": a["submittedDate"],
                    "program": a["program"],
                }
                for a in self.all_candidate_applications[:3]
            ]
        if not self.chat_messages:
            initial = _fallback_advisor_response(
                self._get_profile_dict(),
                "Hi! I just completed my onboarding profile. Please analyze my profile and recommend the best universities and scholarships for me.",
            )
            self.chat_messages = [
                {
                    "id": "welcome-msg",
                    "role": "assistant",
                    "content": initial["text"],
                    "sources": initial.get("sources", []),
                }
            ]
            if initial.get("universities"):
                self.recommended_universities = initial["universities"]

    def _get_profile_dict(self) -> dict[str, Any]:
        return {
            "name": self.profile_name.strip() or "Scholar",
            "country": self.profile_country.strip() or "Nigeria / Emerging Markets",
            "educationLevel": self.profile_education_level or "High School Senior",
            "targetDegree": self.profile_target_degree or "Bachelor's (BSc/BA)",
            "academicInterests": self.profile_academic_interests or ["Computer Science & AI", "Business & Finance"],
            "gpa": self.profile_gpa.strip() or "3.8/4.0",
            "testScores": self.profile_test_scores.strip() or "SAT 1500 / Test-Optional",
            "preferredLocations": self.profile_preferred_locations or ["North America (US & Canada)", "Europe & UK", "Africa (ALU, UCT, Ashesi)"],
            "budget": self.profile_budget or "Need Full Financial Aid / Scholarship",
            "extracurriculars": self.profile_extracurriculars.strip() or "Student leader, community initiative founder",
            "careerGoals": self.profile_career_goals.strip() or "Build impactful technology for emerging economies",
        }

    # ==================================================================
    # Computed Vars (`@rx.var`)
    # ==================================================================
    @rx.var
    def current_onboarding_step_data(self) -> OnboardingStepItem:
        idx = max(0, min(len(ONBOARDING_STEPS) - 1, self.onboarding_step))
        return ONBOARDING_STEPS[idx]

    @rx.var
    def onboarding_progress_pct(self) -> int:
        return int(((self.onboarding_step + 1) / len(ONBOARDING_STEPS)) * 100)

    @rx.var
    def onboarding_step_number(self) -> int:
        return self.onboarding_step + 1

    @rx.var
    def total_onboarding_steps(self) -> int:
        return len(ONBOARDING_STEPS)

    @rx.var
    def current_onboarding_options(self) -> list[str]:
        step = self.current_onboarding_step_data
        return step.get("options", [])

    @rx.var
    def visible_recommended_universities(self) -> list[UniversityItem]:
        discarded = set(self.discarded_university_names)
        return [u for u in self.recommended_universities if u.get("name") not in discarded]

    @rx.var
    def saved_university_names(self) -> list[str]:
        return [u.get("name", "") for u in self.saved_universities]

    @rx.var
    def searched_global_universities(self) -> list[UniversityItem]:
        q = self.uni_search_query.strip().lower()
        if not q:
            return []
        results: list[UniversityItem] = []
        for u in GLOBAL_UNIVERSITIES:
            if (
                q in u["name"].lower()
                or q in u["location"].lower()
                or any(q in p.lower() for p in u["programs"])
            ):
                results.append(u)
        return results[:6]

    @rx.var
    def filtered_scholarships(self) -> list[ScholarshipItem]:
        q = self.scholarship_search_query.strip().lower()
        items = list(SCHOLARSHIPS_DATA)

        if self.scholarship_filter == "for_you":
            # Filter/prioritize based on student profile
            locations_str = " ".join(self.profile_preferred_locations).lower()
            degree_str = self.profile_target_degree.lower()
            filtered: list[ScholarshipItem] = []
            for s in items:
                loc = s["location"].lower()
                elig = " ".join(s["eligibility"]).lower()
                if (
                    "global" in loc
                    or ("africa" in locations_str and ("africa" in loc or "rwanda" in loc or "mauritius" in loc or "african" in elig))
                    or ("north america" in locations_str and ("usa" in loc or "canada" in loc))
                    or ("europe" in locations_str and ("uk" in loc or "europe" in loc or "switzerland" in loc))
                    or ("master" in degree_str and ("master" in elig or "graduate" in elig))
                    or ("bachelor" in degree_str and ("undergraduate" in elig or "high school" in elig or "international" in elig))
                ):
                    filtered.append(s)
            items = filtered if filtered else items[:8]

        if q:
            items = [
                s
                for s in items
                if q in s["name"].lower()
                or q in s["provider"].lower()
                or q in s["location"].lower()
                or q in s["description"].lower()
            ]
        return items

    @rx.var
    def filtered_mentors(self) -> list[MentorItem]:
        q = self.mentor_search_query.strip().lower()
        items = list(self.mentors_list) if self.mentors_list else list(INITIAL_MENTORS)
        if self.mentor_only_available:
            items = [m for m in items if m.get("available", True)]
        if q:
            items = [
                m
                for m in items
                if q in m["name"].lower()
                or q in m["university"].lower()
                or q in m["role"].lower()
                or any(q in sp.lower() for sp in m.get("specialties", []))
            ]
        return items

    @rx.var
    def all_guides(self) -> list[GuideItem]:
        return GUIDES_DATA

    @rx.var
    def interview_question_options(self) -> list[str]:
        return INTERVIEW_QUESTIONS

    @rx.var
    def checklist_completed_count(self) -> int:
        return sum(1 for item in self.checklist_items if item.get("done"))

    @rx.var
    def saved_universities_count(self) -> int:
        return len(self.saved_universities)

    @rx.var
    def active_applications_count(self) -> int:
        return len(self.student_applications)

    @rx.var
    def matched_scholarships_count(self) -> int:
        return len(self.filtered_scholarships)

    @rx.var
    def filtered_university_applications(self) -> list[CandidateAppItem]:
        apps = list(self.all_candidate_applications)
        if (
            self.partner_university_name
            and self.partner_university_name != "All Partner Institutions"
        ):
            apps = [
                a
                for a in apps
                if self.partner_university_name.lower() in a["targetName"].lower()
                or a["targetName"].lower() in self.partner_university_name.lower()
            ]
        if self.uni_portal_filter_status != "All":
            apps = [a for a in apps if a["status"] == self.uni_portal_filter_status]
        q = self.uni_portal_search.strip().lower()
        if q:
            apps = [
                a
                for a in apps
                if q in a["studentName"].lower()
                or q in a["country"].lower()
                or q in a["program"].lower()
                or q in a["targetName"].lower()
            ]
        return apps

    @rx.var
    def uni_portal_total_count(self) -> int:
        return len(self.all_candidate_applications)

    @rx.var
    def uni_portal_accepted_count(self) -> int:
        return sum(1 for a in self.all_candidate_applications if a.get("status") == "Accepted")

    @rx.var
    def uni_portal_review_count(self) -> int:
        return sum(
            1
            for a in self.all_candidate_applications
            if a.get("status") in ("Submitted", "Under Review")
        )

    @rx.var
    def partner_university_options(self) -> list[str]:
        return [
            "All Partner Institutions",
            "African Leadership University (ALU) - Mauritius",
            "African Leadership University (ALU) - Rwanda",
            "Massachusetts Institute of Technology (MIT)",
            "University of Oxford",
            "Stanford University",
            "University of Toronto",
            "ETH Zurich",
        ]

    # ==================================================================
    # Authentication & 1-Click YC Demo Logins
    # ==================================================================
    def set_auth_mode(self, mode: str) -> None:
        self.auth_mode = mode
        self.auth_error = ""

    def set_auth_role_tab(self, role: str) -> None:
        self.auth_role_tab = role
        self.auth_error = ""

    def set_auth_name_input(self, val: str) -> None:
        self.auth_name_input = val

    def set_auth_email_input(self, val: str) -> None:
        self.auth_email_input = val

    def set_auth_password_input(self, val: str) -> None:
        self.auth_password_input = val

    def set_auth_university_input(self, val: str) -> None:
        self.auth_university_input = val

    def login_demo_student(self):
        """1-Click YC Demo Login as a high-achieving Student."""
        self._ensure_db_initialized()
        self.is_authenticated = True
        self.user_id = "demo-student-yc"
        self.user_email = "amara.okafor@gradwyn.com"
        self.user_name = "Amara Okafor"
        self.user_role = "student"
        self.profile_name = "Amara Okafor"
        self.profile_country = "Nigeria / Mauritius"
        self.profile_education_level = "High School Senior"
        self.profile_target_degree = "Bachelor's (BSc/BA)"
        self.profile_academic_interests = ["Computer Science & AI", "Business & Finance"]
        self.profile_gpa = "3.9/4.0 (First Class / A*AA)"
        self.profile_test_scores = "SAT 1510, IELTS 8.0"
        self.profile_preferred_locations = ["North America (US & Canada)", "Europe & UK", "Africa (ALU, UCT, Ashesi)"]
        self.profile_budget = "Need Full Financial Aid / Scholarship"
        self.profile_extracurriculars = "Founded a youth coding academy for 180 students; National Robotics Finalist; Student Council President."
        self.profile_career_goals = "Build scalable AI infrastructure for education and financial inclusion across emerging markets."
        self.on_app_load()
        return rx.redirect("/dashboard")

    def login_demo_student_advisor(self):
        """1-Click YC Demo Launch directly into the AI Advisor + Match Deck."""
        self._ensure_db_initialized()
        self.is_authenticated = True
        self.user_id = "demo-student-yc"
        self.user_email = "amara.okafor@gradwyn.com"
        self.user_name = "Amara Okafor"
        self.user_role = "student"
        self.profile_name = "Amara Okafor"
        self.profile_country = "Nigeria / Mauritius"
        self.profile_education_level = "High School Senior"
        self.profile_target_degree = "Bachelor's (BSc/BA)"
        self.profile_academic_interests = ["Computer Science & AI", "Business & Finance"]
        self.profile_gpa = "3.9/4.0 (First Class / A*AA)"
        self.profile_test_scores = "SAT 1510, IELTS 8.0"
        self.profile_preferred_locations = ["North America (US & Canada)", "Europe & UK", "Africa (ALU, UCT, Ashesi)"]
        self.profile_budget = "Need Full Financial Aid / Scholarship"
        self.profile_extracurriculars = "Founded a youth coding academy for 180 students; National Robotics Finalist; Student Council President."
        self.profile_career_goals = "Build scalable AI infrastructure for education and financial inclusion across emerging markets."
        self.on_app_load()
        return rx.redirect("/chat")

    def login_demo_mentor(self):
        """1-Click YC Demo Login as a Verified Alumni Mentor."""
        self._ensure_db_initialized()
        self.is_authenticated = True
        self.user_id = "mentor-1"
        self.user_email = "sarah.jenkins@stanford.edu"
        self.user_name = "Dr. Sarah Jenkins"
        self.user_role = "mentor"
        return rx.redirect("/mentor-dashboard")

    def login_demo_university(self):
        """1-Click YC Demo Login as a Partner University Admissions Officer."""
        self._ensure_db_initialized()
        self.is_authenticated = True
        self.user_id = "uni-partner-yc"
        self.user_email = "admissions@alueducation.com"
        self.user_name = "ALU & Global Partner Admissions"
        self.user_role = "university"
        self.partner_university_name = "All Partner Institutions"
        return rx.redirect("/university-dashboard")

    def handle_auth_form_submit(self, form_data: dict[str, Any]):
        """Handle submit from uncontrolled auth form."""
        if form_data.get("email"):
            self.auth_email_input = str(form_data["email"]).strip().lower()
        if form_data.get("password"):
            self.auth_password_input = str(form_data["password"]).strip()
        if form_data.get("name"):
            self.auth_name_input = str(form_data["name"]).strip()
        if form_data.get("university"):
            self.auth_university_input = str(form_data["university"]).strip()
        return self.handle_auth_submit()

    def handle_auth_key_down(self, key: str, info: dict | None = None):
        """Handle Enter key in authentication form."""
        if key == "Enter":
            return self.handle_auth_submit()

    def handle_auth_submit(self):
        """Handle standard Email/Password Sign In or Sign Up."""
        self._ensure_db_initialized()
        email = self.auth_email_input.strip().lower()
        password = self.auth_password_input.strip()
        name = self.auth_name_input.strip() or (email.split("@")[0].title() if email else "Scholar")

        if not email or "@" not in email:
            self.auth_error = "Please enter a valid email address."
            return
        if len(password) < 4:
            self.auth_error = "Please enter a password (at least 4 characters)."
            return

        self.auth_error = ""
        role = self.auth_role_tab

        with rx.session() as session:
            existing = session.exec(select(UserAccount).where(UserAccount.email == email)).first()

            if self.auth_mode == "signup":
                if existing:
                    self.auth_error = "An account with this email already exists. Please sign in."
                    return
                uid = f"user-{uuid.uuid4().hex[:8]}"
                new_user = UserAccount(
                    uid=uid,
                    email=email,
                    password_hash=_hash_password(password),
                    display_name=name,
                    role=role,
                    onboarding_complete=(role == "university"),
                    partner_university_name=self.auth_university_input if role == "university" else "",
                )
                session.add(new_user)
                session.commit()
                self.user_id = uid
                self.user_email = email
                self.user_name = name
                self.user_role = role
                self.is_authenticated = True

                if role == "student":
                    self.profile_name = name
                    self.onboarding_step = 0
                    return rx.redirect("/onboarding")
                elif role == "mentor":
                    self.mentor_name = name
                    self.mentor_onboarding_step = 1
                    return rx.redirect("/mentor-onboarding")
                else:
                    self.partner_university_name = self.auth_university_input or "All Partner Institutions"
                    return rx.redirect("/university-dashboard")

            else:
                # Login mode
                if existing:
                    if existing.password_hash != _hash_password(password):
                        self.auth_error = "Incorrect password. Or use a 1-Click YC Demo Login below."
                        return
                    self.user_id = existing.uid
                    self.user_email = existing.email
                    self.user_name = existing.display_name
                    self.user_role = existing.role
                    self.is_authenticated = True
                    role = existing.role
                else:
                    # Auto-provision account on first login for frictionless evaluation
                    uid = f"user-{uuid.uuid4().hex[:8]}"
                    new_user = UserAccount(
                        uid=uid,
                        email=email,
                        password_hash=_hash_password(password),
                        display_name=name,
                        role=role,
                        onboarding_complete=True,
                        partner_university_name=self.auth_university_input if role == "university" else "",
                    )
                    session.add(new_user)
                    session.commit()
                    self.user_id = uid
                    self.user_email = email
                    self.user_name = name
                    self.user_role = role
                    self.is_authenticated = True

                self.on_app_load()
                if role == "student":
                    return rx.redirect("/dashboard")
                elif role == "mentor":
                    return rx.redirect("/mentor-dashboard")
                else:
                    return rx.redirect("/university-dashboard")

    def logout(self):
        self.is_authenticated = False
        self.user_id = ""
        self.user_email = ""
        self.auth_error = ""
        return rx.redirect("/")

    # ==================================================================
    # 9-Step Student Onboarding Handlers
    # ==================================================================
    def set_profile_name(self, val: str) -> None:
        self.profile_name = val

    def set_profile_country(self, val: str) -> None:
        self.profile_country = val

    def set_profile_education_level(self, val: str) -> None:
        self.profile_education_level = val

    def set_profile_target_degree(self, val: str) -> None:
        self.profile_target_degree = val

    def toggle_academic_interest(self, interest: str) -> None:
        if interest in self.profile_academic_interests:
            if len(self.profile_academic_interests) > 1:
                self.profile_academic_interests = [
                    i for i in self.profile_academic_interests if i != interest
                ]
        else:
            self.profile_academic_interests = self.profile_academic_interests + [interest]

    def set_custom_interest_input(self, val: str) -> None:
        self.custom_interest_input = val

    def add_custom_interest(self) -> None:
        val = self.custom_interest_input.strip()
        if val and val not in self.profile_academic_interests:
            self.profile_academic_interests = self.profile_academic_interests + [val]
        self.custom_interest_input = ""

    def set_profile_gpa(self, val: str) -> None:
        self.profile_gpa = val

    def set_profile_test_scores(self, val: str) -> None:
        self.profile_test_scores = val

    def toggle_preferred_location(self, loc: str) -> None:
        if loc in self.profile_preferred_locations:
            if len(self.profile_preferred_locations) > 1:
                self.profile_preferred_locations = [
                    l for l in self.profile_preferred_locations if l != loc
                ]
        else:
            self.profile_preferred_locations = self.profile_preferred_locations + [loc]

    def set_profile_budget(self, val: str) -> None:
        self.profile_budget = val

    def set_profile_extracurriculars(self, val: str) -> None:
        self.profile_extracurriculars = val

    def set_profile_career_goals(self, val: str) -> None:
        self.profile_career_goals = val

    def handle_onboarding_form_submit(self, form_data: dict[str, Any]):
        """Save submitted form fields from current onboarding step and advance."""
        if "profile_name" in form_data and str(form_data["profile_name"]).strip():
            self.profile_name = str(form_data["profile_name"]).strip()
        if "profile_country" in form_data and str(form_data["profile_country"]).strip():
            self.profile_country = str(form_data["profile_country"]).strip()
        if "profile_gpa" in form_data and str(form_data["profile_gpa"]).strip():
            self.profile_gpa = str(form_data["profile_gpa"]).strip()
        if "profile_test_scores" in form_data and str(form_data["profile_test_scores"]).strip():
            self.profile_test_scores = str(form_data["profile_test_scores"]).strip()
        if "profile_extracurriculars" in form_data and str(form_data["profile_extracurriculars"]).strip():
            self.profile_extracurriculars = str(form_data["profile_extracurriculars"]).strip()
        if "profile_career_goals" in form_data and str(form_data["profile_career_goals"]).strip():
            self.profile_career_goals = str(form_data["profile_career_goals"]).strip()
        if "custom_interest_input" in form_data:
            c_val = str(form_data["custom_interest_input"]).strip()
            if c_val and c_val not in self.profile_academic_interests:
                self.profile_academic_interests = self.profile_academic_interests + [c_val]
        return self.next_onboarding_step()

    def handle_custom_interest_form_submit(self, form_data: dict[str, Any]):
        """Add custom interest from native form submission."""
        val = str(form_data.get("custom_interest", form_data.get("custom_interest_input", ""))).strip()
        if val and val not in self.profile_academic_interests:
            self.profile_academic_interests = self.profile_academic_interests + [val]

    def handle_prep_essay_form_submit(self, form_data: dict[str, Any]):
        """Analyze essay from uncontrolled form."""
        if "essay_target" in form_data and str(form_data["essay_target"]).strip():
            self.prep_essay_target = str(form_data["essay_target"]).strip()
        if "essay_draft" in form_data and str(form_data["essay_draft"]).strip():
            self.prep_essay_draft = str(form_data["essay_draft"]).strip()
        return self.run_prep_essay_critique()

    def handle_prep_interview_form_submit(self, form_data: dict[str, Any]):
        """Evaluate mock interview from uncontrolled form."""
        if "interview_answer" in form_data and str(form_data["interview_answer"]).strip():
            self.prep_interview_answer = str(form_data["interview_answer"]).strip()
        return self.run_prep_interview_evaluation()

    def handle_profile_edit_form_submit(self, form_data: dict[str, Any]):
        """Save edited profile from modal form."""
        if "profile_name" in form_data and str(form_data["profile_name"]).strip():
            self.profile_name = str(form_data["profile_name"]).strip()
        if "profile_country" in form_data and str(form_data["profile_country"]).strip():
            self.profile_country = str(form_data["profile_country"]).strip()
        if "profile_gpa" in form_data and str(form_data["profile_gpa"]).strip():
            self.profile_gpa = str(form_data["profile_gpa"]).strip()
        if "profile_test_scores" in form_data and str(form_data["profile_test_scores"]).strip():
            self.profile_test_scores = str(form_data["profile_test_scores"]).strip()
        if "profile_budget" in form_data and str(form_data["profile_budget"]).strip():
            self.profile_budget = str(form_data["profile_budget"]).strip()
        if "profile_extracurriculars" in form_data and str(form_data["profile_extracurriculars"]).strip():
            self.profile_extracurriculars = str(form_data["profile_extracurriculars"]).strip()
        if "profile_career_goals" in form_data and str(form_data["profile_career_goals"]).strip():
            self.profile_career_goals = str(form_data["profile_career_goals"]).strip()
        return self.save_edited_profile_and_reanalyze()

    def handle_onboarding_key_down(self, key: str, info: dict | None = None):
        """Advance onboarding step on Enter."""
        if key == "Enter":
            return self.next_onboarding_step()

    def handle_custom_interest_key_down(self, key: str, info: dict | None = None):
        """Add custom interest on Enter."""
        if key == "Enter":
            return self.add_custom_interest()

    def next_onboarding_step(self):
        if self.onboarding_step < len(ONBOARDING_STEPS) - 1:
            self.onboarding_step += 1
            return
        # Final step completed -> run AI analysis and route to /chat
        return self.complete_student_onboarding()

    def prev_onboarding_step(self) -> None:
        if self.onboarding_step > 0:
            self.onboarding_step -= 1

    def complete_student_onboarding(self):
        self._ensure_db_initialized()
        profile = self._get_profile_dict()
        self.user_name = self.profile_name
        self.is_authenticated = True
        self.user_role = "student"

        result = generate_advisor_response(
            profile,
            "Hi! I just finished my onboarding profile. Please analyze my profile and recommend the best universities and scholarships for me.",
        )
        self.chat_messages = [
            {
                "id": f"msg-{uuid.uuid4().hex[:6]}",
                "role": "assistant",
                "content": result["text"],
                "sources": result.get("sources", []),
            }
        ]
        if result.get("universities"):
            self.recommended_universities = result["universities"]
            self.saved_universities = result["universities"][:3]
        self.previous_interaction_id = result.get("interaction_id", "")
        return rx.redirect("/chat")

    # ==================================================================
    # AI Chat & University Match Deck Handlers
    # ==================================================================
    def set_chat_input(self, val: str) -> None:
        self.chat_input = val

    def send_quick_prompt(self, prompt_text: str):
        self.chat_input = prompt_text
        return self.send_chat_message()

    def handle_chat_form_submit(self, form_data: dict[str, Any]):
        """Send chat message from native form submit."""
        msg = str(form_data.get("message", "")).strip()
        if not msg or self.is_ai_loading:
            return
        self.chat_input = msg
        return self.send_chat_message()

    def handle_chat_key_down(self, key: str, info: dict | None = None):
        """Send chat message on Enter key."""
        if key == "Enter":
            return self.send_chat_message()

    def send_chat_message(self):
        msg = self.chat_input.strip()
        if not msg or self.is_ai_loading:
            return
        self.chat_input = ""
        user_msg = {
            "id": f"user-{uuid.uuid4().hex[:6]}",
            "role": "user",
            "content": msg,
            "sources": [],
        }
        self.chat_messages = self.chat_messages + [user_msg]
        self.is_ai_loading = True
        yield

        result = generate_advisor_response(
            self._get_profile_dict(),
            msg,
            self.previous_interaction_id,
        )
        ai_msg = {
            "id": f"ai-{uuid.uuid4().hex[:6]}",
            "role": "assistant",
            "content": result["text"],
            "sources": result.get("sources", []),
        }
        self.chat_messages = self.chat_messages + [ai_msg]
        if result.get("universities"):
            self.recommended_universities = result["universities"]
            self.discarded_university_names = []
        if result.get("interaction_id"):
            self.previous_interaction_id = result["interaction_id"]
        self.is_ai_loading = False

    def toggle_save_university(self, uni: dict[str, Any]) -> None:
        name = uni.get("name", "")
        existing_names = [u.get("name") for u in self.saved_universities]
        if name in existing_names:
            self.saved_universities = [
                u for u in self.saved_universities if u.get("name") != name
            ]
        else:
            self.saved_universities = [uni] + self.saved_universities

    def discard_university(self, uni_name: str) -> None:
        if uni_name not in self.discarded_university_names:
            self.discarded_university_names = self.discarded_university_names + [uni_name]

    def reset_discarded_universities(self) -> None:
        self.discarded_university_names = []

    # ==================================================================
    # Student Dashboard Navigation & Search
    # ==================================================================
    def set_dashboard_tab(self, tab: str) -> None:
        self.dashboard_tab = tab

    def set_uni_search_query(self, val: str) -> None:
        self.uni_search_query = val

    def select_searched_university(self, uni: dict[str, Any]) -> None:
        self.toggle_save_university(uni)
        self.uni_search_query = ""

    def set_scholarship_filter(self, f: str) -> None:
        self.scholarship_filter = f

    def set_scholarship_search_query(self, val: str) -> None:
        self.scholarship_search_query = val

    def set_mentor_search_query(self, val: str) -> None:
        self.mentor_search_query = val

    def toggle_mentor_only_available(self) -> None:
        self.mentor_only_available = not self.mentor_only_available

    # ==================================================================
    # 4-Step Application Wizard Modal
    # ==================================================================
    def open_university_apply_modal(self, uni: dict[str, Any]) -> None:
        self.apply_target_name = uni.get("name", "Partner University")
        self.apply_target_type = "University"
        self.apply_target_location = uni.get("location", "Global Campus")
        self.apply_target_deadline = uni.get("deadline", "Jan 15, 2027")
        self.apply_target_fee = uni.get("applicationFee", "$75 (Fee Waiver Available)")
        programs = uni.get("programs", ["Computer Science & AI"])
        self.apply_program = programs[0] if programs else "Computer Science & AI"
        self.apply_essay = (
            f"I am applying to {self.apply_target_name} to pursue my {self.profile_target_degree} in {self.apply_program}. "
            f"{self.profile_extracurriculars} My goal is to {self.profile_career_goals.lower()}"
        )
        self.apply_step = 1
        self.apply_submitted_success = False
        self.is_apply_modal_open = True

    def open_scholarship_apply_modal(self, sch: dict[str, Any]) -> None:
        self.apply_target_name = sch.get("name", "Global Scholarship")
        self.apply_target_type = "Scholarship"
        self.apply_target_location = sch.get("location", "Global")
        self.apply_target_deadline = sch.get("deadline", "Nov 15, 2026")
        self.apply_target_fee = "Free ($0 Grant Application)"
        self.apply_program = f"{sch.get('provider', 'Foundation')} Fellowship"
        self.apply_essay = (
            f"As a scholar from {self.profile_country} with a {self.profile_gpa} academic standing, "
            f"I am applying for the {self.apply_target_name} to fund my studies in {', '.join(self.profile_academic_interests[:2])}. "
            f"{self.profile_extracurriculars} Upon graduation, I will {self.profile_career_goals.lower()}"
        )
        self.apply_step = 1
        self.apply_submitted_success = False
        self.is_apply_modal_open = True

    def close_apply_modal(self) -> None:
        self.is_apply_modal_open = False
        self.apply_submitted_success = False

    def set_apply_program(self, val: str) -> None:
        self.apply_program = val

    def set_apply_essay(self, val: str) -> None:
        self.apply_essay = val

    def polish_apply_essay_with_ai(self) -> None:
        """Enhance the student's application essay draft using AI critique."""
        critique = critique_essay_with_ai(
            self.apply_essay,
            self.apply_target_name,
            self.profile_target_degree,
            self.profile_name,
        )
        opening = critique.get("rewrittenOpening", "")
        if opening and opening not in self.apply_essay:
            self.apply_essay = f"{opening}\n\n{self.apply_essay}"

    def toggle_apply_doc_transcript(self) -> None:
        self.apply_doc_transcript = not self.apply_doc_transcript

    def toggle_apply_doc_cv(self) -> None:
        self.apply_doc_cv = not self.apply_doc_cv

    def toggle_apply_doc_recommendation(self) -> None:
        self.apply_doc_recommendation = not self.apply_doc_recommendation

    def next_apply_step(self) -> None:
        if self.apply_step < 4:
            self.apply_step += 1

    def prev_apply_step(self) -> None:
        if self.apply_step > 1:
            self.apply_step -= 1

    def submit_application(self) -> None:
        """Persist application to SQLModel DB and update both Student & University Portals."""
        self._ensure_db_initialized()
        app_id = f"app-{uuid.uuid4().hex[:8]}"
        today_str = datetime.now().strftime("%b %d, %Y")
        docs: list[str] = []
        if self.apply_doc_transcript:
            docs.append("Official Academic Transcripts.pdf")
        if self.apply_doc_cv:
            docs.append("CV_Leadership_Portfolio.pdf")
        if self.apply_doc_recommendation:
            docs.append("2_Academic_Recommendations.pdf")

        with rx.session() as session:
            new_sub = ApplicationSubmission(
                app_uid=app_id,
                student_uid=self.user_id or "demo-student-yc",
                student_name=self.profile_name,
                student_email=self.user_email or "amara.okafor@gradwyn.com",
                country=self.profile_country,
                target_name=self.apply_target_name,
                target_type=self.apply_target_type,
                program=self.apply_program,
                gpa=self.profile_gpa,
                test_scores=self.profile_test_scores,
                match_score=96,
                status="Submitted",
                submitted_date=today_str,
                personal_statement=self.apply_essay,
                documents_json=json.dumps(docs),
            )
            session.add(new_sub)
            session.commit()

        self._refresh_from_db()
        self.student_applications = [
            {
                "id": app_id,
                "name": self.apply_target_name,
                "type": self.apply_target_type,
                "status": "Submitted",
                "deadline": self.apply_target_deadline,
                "submittedDate": today_str,
                "program": self.apply_program,
            }
        ] + self.student_applications
        self.apply_submitted_success = True

    # ==================================================================
    # Prep Suite Handlers (AI Essay Critique, Mock Interview, Checklist)
    # ==================================================================
    def set_prep_active_tool(self, tool: str) -> None:
        self.prep_active_tool = tool

    def set_prep_essay_target(self, val: str) -> None:
        self.prep_essay_target = val

    def set_prep_essay_draft(self, val: str) -> None:
        self.prep_essay_draft = val

    def run_prep_essay_critique(self):
        self.is_prep_essay_loading = True
        yield
        res = critique_essay_with_ai(
            self.prep_essay_draft,
            self.prep_essay_target,
            self.profile_target_degree,
            self.profile_name,
        )
        self.prep_essay_result = res
        self.prep_essay_strengths = res.get("strengths", [])
        self.prep_essay_improvements = res.get("improvements", [])
        self.is_prep_essay_loading = False

    def set_prep_interview_question(self, q: str) -> None:
        self.prep_interview_question = q
        self.prep_interview_result = {}

    def set_prep_interview_answer(self, val: str) -> None:
        self.prep_interview_answer = val

    def run_prep_interview_evaluation(self):
        self.is_prep_interview_loading = True
        yield
        res = evaluate_interview_answer(
            self.prep_interview_question,
            self.prep_interview_answer,
            self.prep_essay_target,
        )
        self.prep_interview_result = res
        self.is_prep_interview_loading = False

    def toggle_checklist_item(self, item_id: str) -> None:
        updated: list[dict[str, Any]] = []
        for item in self.checklist_items:
            if item["id"] == item_id:
                updated.append({**item, "done": not item["done"]})
            else:
                updated.append(item)
        self.checklist_items = updated

    # ==================================================================
    # Modals: Edit Profile, Guide Reader, Feedback
    # ==================================================================
    def open_edit_profile_modal(self) -> None:
        self.is_edit_profile_open = True

    def close_edit_profile_modal(self) -> None:
        self.is_edit_profile_open = False

    def save_edited_profile_and_reanalyze(self):
        self.is_edit_profile_open = False
        profile = self._get_profile_dict()
        result = generate_advisor_response(
            profile,
            "I just updated my student profile. Please re-analyze my profile and refresh my university recommendations.",
        )
        self.chat_messages = self.chat_messages + [
            {
                "id": f"reanalyze-{uuid.uuid4().hex[:6]}",
                "role": "assistant",
                "content": result["text"],
                "sources": result.get("sources", []),
            }
        ]
        if result.get("universities"):
            self.recommended_universities = result["universities"]
            self.discarded_university_names = []

    def open_guide_reader(self, guide: dict[str, Any]) -> None:
        self.active_guide = guide
        self.is_guide_modal_open = True

    def close_guide_reader(self) -> None:
        self.is_guide_modal_open = False

    def open_feedback_modal(self) -> None:
        self.feedback_submitted = False
        self.is_feedback_modal_open = True

    def close_feedback_modal(self) -> None:
        self.is_feedback_modal_open = False

    def set_feedback_rating(self, r: int) -> None:
        self.feedback_rating = r

    def set_feedback_category(self, cat: str) -> None:
        self.feedback_category = cat

    def set_feedback_comment(self, val: str) -> None:
        self.feedback_comment = val

    def submit_feedback(self) -> None:
        self._ensure_db_initialized()
        with rx.session() as session:
            session.add(
                FeedbackEntry(
                    user_uid=self.user_id or "anonymous",
                    rating=self.feedback_rating,
                    category=self.feedback_category,
                    comment=self.feedback_comment.strip(),
                )
            )
            session.commit()
        self.feedback_comment = ""
        self.feedback_submitted = True

    # ==================================================================
    # Mentor Onboarding & Mentor Portal Handlers
    # ==================================================================
    def set_mentor_name(self, val: str) -> None:
        self.mentor_name = val

    def set_mentor_role(self, val: str) -> None:
        self.mentor_role = val

    def set_mentor_university(self, val: str) -> None:
        self.mentor_university = val

    def set_mentor_location(self, val: str) -> None:
        self.mentor_location = val

    def set_mentor_bio(self, val: str) -> None:
        self.mentor_bio = val

    def set_mentor_linkedin(self, val: str) -> None:
        self.mentor_linkedin = val

    def set_mentor_custom_specialty(self, val: str) -> None:
        self.mentor_custom_specialty = val

    def add_mentor_specialty(self) -> None:
        sp = self.mentor_custom_specialty.strip()
        if sp and sp not in self.mentor_specialties:
            self.mentor_specialties = self.mentor_specialties + [sp]
        self.mentor_custom_specialty = ""

    def remove_mentor_specialty(self, sp: str) -> None:
        if len(self.mentor_specialties) > 1:
            self.mentor_specialties = [s for s in self.mentor_specialties if s != sp]

    def toggle_mentor_availability(self) -> None:
        self.mentor_available = not self.mentor_available
        self.save_mentor_profile()

    def handle_mentor_onboarding_key_down(self, key: str, info: dict | None = None):
        """Advance mentor onboarding step on Enter."""
        if key == "Enter":
            return self.next_mentor_step()

    def next_mentor_step(self):
        if self.mentor_onboarding_step < 4:
            self.mentor_onboarding_step += 1
            return
        self.save_mentor_profile()
        return rx.redirect("/mentor-dashboard")

    def prev_mentor_step(self) -> None:
        if self.mentor_onboarding_step > 1:
            self.mentor_onboarding_step -= 1

    def save_mentor_profile(self) -> None:
        """Upsert mentor profile into `MentorListing` table so Students see it immediately."""
        self._ensure_db_initialized()
        uid = self.user_id if self.user_id.startswith("mentor") else "mentor-1"
        with rx.session() as session:
            existing = session.exec(
                select(MentorListing).where(MentorListing.mentor_uid == uid)
            ).first()
            if existing:
                existing.name = self.mentor_name
                existing.role = self.mentor_role
                existing.university = self.mentor_university
                existing.location = self.mentor_location
                existing.bio = self.mentor_bio
                existing.specialties_json = json.dumps(self.mentor_specialties)
                existing.linkedin = self.mentor_linkedin
                existing.available = self.mentor_available
                session.add(existing)
            else:
                session.add(
                    MentorListing(
                        mentor_uid=uid,
                        name=self.mentor_name,
                        role=self.mentor_role,
                        university=self.mentor_university,
                        location=self.mentor_location,
                        bio=self.mentor_bio,
                        specialties_json=json.dumps(self.mentor_specialties),
                        image_url="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=400&q=80",
                        linkedin=self.mentor_linkedin,
                        available=self.mentor_available,
                    )
                )
            session.commit()
        self._refresh_from_db()

    # ==================================================================
    # University Admissions Portal Handlers
    # ==================================================================
    def set_partner_university_name(self, val: str) -> None:
        self.partner_university_name = val

    def set_uni_portal_filter_status(self, status: str) -> None:
        self.uni_portal_filter_status = status

    def set_uni_portal_search(self, val: str) -> None:
        self.uni_portal_search = val

    def open_candidate_modal(self, candidate: dict[str, Any]) -> None:
        self.selected_candidate = candidate
        self.is_candidate_modal_open = True

    def close_candidate_modal(self) -> None:
        self.is_candidate_modal_open = False

    def update_candidate_status(self, app_id: str, new_status: str) -> None:
        """Update an applicant's admission decision in SQLModel DB & sync Student Tracker."""
        self._ensure_db_initialized()
        with rx.session() as session:
            sub = session.exec(
                select(ApplicationSubmission).where(ApplicationSubmission.app_uid == app_id)
            ).first()
            if sub:
                sub.status = new_status
                session.add(sub)
                session.commit()

        self._refresh_from_db()
        # Also update student_applications if present
        updated_student_apps: list[dict[str, Any]] = []
        for s_app in self.student_applications:
            if s_app.get("id") == app_id:
                updated_student_apps.append({**s_app, "status": new_status})
            else:
                updated_student_apps.append(s_app)
        self.student_applications = updated_student_apps

        if self.selected_candidate and self.selected_candidate.get("id") == app_id:
            self.selected_candidate = {**self.selected_candidate, "status": new_status}
