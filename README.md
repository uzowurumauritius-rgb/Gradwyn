# Gradwyn — AI-Powered Global Higher Education, Scholarships & Mentorship Ecosystem

> **Y Combinator Ready Full-Stack MVP** · Built in **100% Python Reflex (`reflex==0.10.1`) + FastAPI + SQLModel + Google Gemini (`google-genai`)**
> Live Brand Reference: [https://www.gradwyn.com/](https://www.gradwyn.com/)

Gradwyn is a three-sided global higher-education marketplace connecting **Prospective International Students**, **Verified Alumni & Fellowship Mentors**, and **Partner Universities**.

---

## ✨ What Was Rebuilt & Upgraded From the Deprecated AI Studio Prototype

1. **100% Python Full-Stack Architecture (Reflex + FastAPI + SQLModel)**:
   - Replaced the broken client-side Firebase/Vite prototype (which failed due to missing `firebase-applet-config.json` and exposed client-side API keys) with a unified, server-stateful Python Reflex architecture.
2. **Real-Time Three-Sided Marketplace Sync (SQLite / PostgreSQL via SQLModel)**:
   - **Student → University Live Sync**: When a student completes the **4-Step Application Wizard** for a university or scholarship, the dossier (`ApplicationSubmission`) is persisted to the database and immediately appears in the **Partner University Admissions Portal**, where admissions officers can inspect the student's GPA, test scores, and Personal Statement and click **Admit / Under Review / Reject**—updating the student's **Candidacy Tracker** in real time.
   - **Mentor → Student Live Sync**: When an alumni mentor completes **Mentor Onboarding** or toggles their availability in the **Mentor Portal** (`MentorListing`), their card updates immediately inside the Student **Mentorship Network**.
3. **Gemini 3.8 Flash + Google Search Grounding (`google-genai` SDK)**:
   - Uses `client.interactions.create(model="gemini-3.8-flash", tools=[{"type": "google_search"}])` on the backend (`gradwyn/ai_service.py`).
   - Includes a **Zero-Failure Profile-Aware Fallback Engine** so live YC partner demos work instantaneously even if `GEMINI_API_KEY` is unset or rate-limited.
4. **Complete Feature Suite (No "Coming Soon" Placeholders)**:
   - **Interactive AI Prep Suite**:
     - **AI Personal Statement & Essay Critique Engine** (Overall, Hook, Impact & Fit scores + rewritten opening paragraph).
     - **AI Mock Interview Simulator** (5 real admissions/scholarship questions + STAR method scoring & model answer).
     - **Interactive Admissions & Financial Aid Dossier Checklist**.
   - **Global Scholarships Hub**: 14 curated full-funding and merit grants (Mastercard Foundation, Lester B. Pearson, Reach Oxford, Rhodes, Knight-Hennessy, Gates Cambridge, Fulbright, Chevening, Erasmus Mundus, ETH ESOP, Ashinaga, etc.) with **"All Grants"** vs **"For You (AI Matched)"** filtering.
   - **Full Editorial Admissions Guides**: 5 complete, multi-section playbooks with a full-screen article reader modal.
   - **1-Click YC Ecosystem Demo Switcher**: Top bar on every page allowing reviewers to switch between **AI Advisor**, **Student Hub**, **Mentor Portal**, and **University Admissions Portal** in one click.

---

## 🗂️ Project Structure

```text
Gradwyn MVP/
├── rxconfig.py                  # Reflex + TailwindV3 + Database configuration
├── requirements.txt             # Python dependencies (reflex, google-genai, sqlmodel)
├── Dockerfile                   # Production container definition
├── docker-compose.yml           # 1-command VPS / Docker deployment
├── .env.example                 # Environment variable template
├── gradwyn/
│   ├── __init__.py
│   ├── gradwyn.py               # Main app entry point & 8 route definitions
│   ├── models.py                # TypedDict schemas & SQLModel database tables
│   ├── constants.py             # Curated universities, 14 scholarships, mentors, 5 guides
│   ├── ai_service.py            # Gemini 3.8 Flash Interactions API + fallback engine
│   ├── state.py                 # Unified AppState (Auth, Onboarding, Chat, Hub, Portals)
│   └── views/
│       ├── navbar.py            # Brand header & 1-Click YC Ecosystem Demo Switcher
│       ├── modals.py            # 4-Step Application Wizard, Edit Profile, Guide & Dossier modals
│       ├── landing.py           # Editorial Landing Page (gradwyn.com aesthetic)
│       ├── auth.py              # Multi-role Sign In/Up + 1-Click YC Demo Sandbox
│       ├── onboarding.py        # 9-Step Student Onboarding Wizard
│       ├── chat.py              # Split-screen AI Advisor Chat + University Match Deck
│       ├── dashboard.py         # 6-Tab Student Hub (Overview, Tracker, Grants, Mentors, Prep, Guides)
│       ├── mentor_portal.py     # 4-Step Mentor Onboarding + Live Mentor Portal
│       └── university_portal.py # Partner University Admissions Portal & Dossier Reviewer
└── legacy_ts_mvp/               # Archived deprecated TypeScript/Vite AI Studio prototype
```

---

## 🚀 Quickstart (Local Development)

```bash
# 1. Activate the virtual environment
source .venv/bin/activate

# 2. (Optional) Configure your Gemini API key
cp .env.example .env
# Edit .env and set GEMINI_API_KEY="your-key"

# 3. Run the full-stack Reflex server
reflex run
```

- **Frontend UI**: `http://localhost:3000`
- **FastAPI Backend**: `http://localhost:8000`

---

## 🐳 Production Deployment (Hostinger KVM VPS / Docker)

```bash
docker compose up -d --build
```
