"""Clean Modern Editorial Landing Page matching live https://www.gradwyn.com/."""

from __future__ import annotations

import reflex as rx

from ..state import AppState
from .modals import global_modals
from .navbar import public_navbar


def _hero_preview_card() -> rx.Component:
    """Interactive editorial showcase card on the right side of the hero section."""
    return rx.el.div(
        # Top window bar
        rx.el.div(
            rx.el.div(
                rx.el.span(class_name="w-2.5 h-2.5 rounded-full bg-rose-400"),
                rx.el.span(class_name="w-2.5 h-2.5 rounded-full bg-amber-400"),
                rx.el.span(class_name="w-2.5 h-2.5 rounded-full bg-emerald-400"),
                class_name="flex items-center gap-1.5",
            ),
            rx.el.span(
                "Gradwyn AI Advisor · Gemini 3.8 Grounded",
                class_name="text-[11px] font-semibold text-slate-500",
            ),
            rx.el.span(
                "98% Match",
                class_name="text-[11px] font-bold px-2.5 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200",
            ),
            class_name="flex items-center justify-between pb-4 border-b border-slate-100",
        ),
        # Simulated AI conversation snippet
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "\"I have a 3.9 GPA in Computer Science and need full financial aid or a Mastercard Foundation Scholarship. Which universities fit me best?\"",
                    class_name="text-xs text-slate-700 italic",
                ),
                class_name="p-3.5 rounded-2xl bg-slate-50 border border-slate-200/80 mb-3",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon("sparkles", size=14, class_name="text-white"),
                        class_name="w-6 h-6 rounded-lg bg-slate-900 flex items-center justify-center shrink-0",
                    ),
                    rx.el.span(
                        "Gradwyn Advisor Analysis",
                        class_name="text-xs font-bold text-slate-900",
                    ),
                    class_name="flex items-center gap-2 mb-2",
                ),
                rx.el.p(
                    "Based on your academic record and full-need requirement, I have matched you with 6 institutions offering 100% demonstrated-need aid and full leadership fellowships:",
                    class_name="text-xs text-slate-600 leading-relaxed mb-3",
                ),
                # Mini university match cards
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.p("Massachusetts Institute of Technology", class_name="text-xs font-bold text-slate-900"),
                            rx.el.p("Cambridge, USA · 100% Need-Blind Aid", class_name="text-[11px] text-slate-500"),
                        ),
                        rx.el.span("98% Fit", class_name="text-[11px] font-bold px-2.5 py-1 rounded-full bg-slate-900 text-white"),
                        class_name="flex items-center justify-between p-3 rounded-xl bg-white border border-slate-200 shadow-xs",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.p("African Leadership University (ALU)", class_name="text-xs font-bold text-slate-900"),
                            rx.el.p("Mauritius & Rwanda · Mastercard Scholars", class_name="text-[11px] text-slate-500"),
                        ),
                        rx.el.span("97% Fit", class_name="text-[11px] font-bold px-2.5 py-1 rounded-full bg-slate-900 text-white"),
                        class_name="flex items-center justify-between p-3 rounded-xl bg-white border border-slate-200 shadow-xs",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.p("University of Toronto", class_name="text-xs font-bold text-slate-900"),
                            rx.el.p("Toronto, Canada · Lester B. Pearson Full Ride", class_name="text-[11px] text-slate-500"),
                        ),
                        rx.el.span("95% Fit", class_name="text-[11px] font-bold px-2.5 py-1 rounded-full bg-slate-900 text-white"),
                        class_name="flex items-center justify-between p-3 rounded-xl bg-white border border-slate-200 shadow-xs",
                    ),
                    class_name="space-y-2",
                ),
                class_name="p-4 rounded-2xl bg-slate-50/70 border border-slate-200/80",
            ),
            class_name="mt-4",
        ),
        # Quick interactive CTA bar inside card
        rx.el.div(
            rx.el.span(
                "14 Verified Global Scholarships · 45+ Mentor Specialties",
                class_name="text-[11px] font-medium text-slate-500",
            ),
            rx.el.button(
                "Try Live AI Advisor →",
                on_click=AppState.login_demo_student_advisor,
                class_name="text-xs font-bold text-slate-900 hover:underline cursor-pointer",
            ),
            class_name="flex items-center justify-between pt-4 mt-4 border-t border-slate-100",
        ),
        class_name="bg-white rounded-3xl p-6 sm:p-7 shadow-xl border border-slate-200/90",
    )


def landing_page() -> rx.Component:
    """Main Landing Page view (`/`) matching https://www.gradwyn.com/."""
    return rx.el.div(
        public_navbar(),
        global_modals(),
        # Hero Section
        rx.el.section(
            rx.el.div(
                rx.el.div(
                    # Left Column: Editorial Headline & CTAs
                    rx.el.div(
                        rx.el.div(
                            rx.icon("sparkles", size=14, class_name="text-slate-900"),
                            rx.el.span(
                                "AI-Powered Admissions, Scholarships & Mentorship",
                                class_name="text-xs font-semibold text-slate-700",
                            ),
                            class_name="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-slate-100 border border-slate-200 mb-6",
                        ),
                        rx.el.h1(
                            "Your personal guide to ",
                            rx.el.span(
                                "global higher education.",
                                class_name="italic font-serif font-normal text-slate-800",
                            ),
                            class_name="text-4xl sm:text-6xl font-bold tracking-tight text-slate-900 leading-[1.08]",
                        ),
                        rx.el.p(
                            "Gradwyn pairs real-time AI admissions intelligence with verified scholarship matching, alumni mentorship, and direct partner university applications—democratizing access to world-class degrees.",
                            class_name="text-base sm:text-lg text-slate-600 leading-relaxed mt-6 max-w-xl",
                        ),
                        rx.el.div(
                            rx.el.a(
                                rx.el.span("Start Your Journey"),
                                rx.icon("arrow-right", size=17),
                                href="/onboarding",
                                class_name="inline-flex items-center justify-center gap-2 px-7 py-4 rounded-full bg-slate-900 hover:bg-slate-800 text-white text-sm font-semibold shadow-md transition-all",
                            ),
                            rx.el.button(
                                rx.icon("zap", size=16),
                                rx.el.span("1-Click Instant Demo"),
                                on_click=AppState.login_demo_student,
                                class_name="inline-flex items-center justify-center gap-2 px-6 py-4 rounded-full bg-white hover:bg-slate-50 text-slate-900 border border-slate-300 text-sm font-semibold transition-all cursor-pointer",
                            ),
                            class_name="flex flex-wrap items-center gap-3.5 mt-8",
                        ),
                        # Key metrics bar
                        rx.el.div(
                            rx.el.div(
                                rx.el.p("$2.4B+", class_name="text-2xl font-bold text-slate-900"),
                                rx.el.p("Global Grant Pool Indexed", class_name="text-xs text-slate-500"),
                            ),
                            rx.el.div(
                                rx.el.p("94%", class_name="text-2xl font-bold text-slate-900"),
                                rx.el.p("Match Precision Score", class_name="text-xs text-slate-500"),
                            ),
                            rx.el.div(
                                rx.el.p("3-Sided", class_name="text-2xl font-bold text-slate-900"),
                                rx.el.p("Student · Mentor · University", class_name="text-xs text-slate-500"),
                            ),
                            class_name="grid grid-cols-3 gap-4 pt-8 mt-8 border-t border-slate-200 max-w-lg",
                        ),
                    ),
                    # Right Column: Interactive Preview Card
                    _hero_preview_card(),
                    class_name="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center",
                ),
                class_name="max-w-7xl mx-auto px-4 sm:px-6 py-16 sm:py-24",
            ),
            class_name="bg-gradient-to-b from-slate-50/70 to-white border-b border-slate-200/70",
        ),
        # Section 2: How It Works
        rx.el.section(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "HOW GRADWYN WORKS",
                        class_name="text-xs font-bold uppercase tracking-widest text-slate-500",
                    ),
                    rx.el.h2(
                        "From academic profile to funded admission offer.",
                        class_name="text-3xl sm:text-4xl font-bold text-slate-900 mt-2",
                    ),
                    class_name="max-w-2xl mb-12",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.span("01", class_name="text-xs font-bold px-3 py-1 rounded-full bg-slate-900 text-white"),
                        rx.el.h3("9-Step Holistic Profiling", class_name="text-xl font-bold text-slate-900 mt-4"),
                        rx.el.p(
                            "Capture your GPA, standardized test scores, financial aid needs, leadership impact, and target regions in under 2 minutes.",
                            class_name="text-sm text-slate-600 leading-relaxed mt-2",
                        ),
                        class_name="p-7 rounded-3xl bg-slate-50 border border-slate-200/80",
                    ),
                    rx.el.div(
                        rx.el.span("02", class_name="text-xs font-bold px-3 py-1 rounded-full bg-slate-900 text-white"),
                        rx.el.h3("Grounded AI Matching & Prep", class_name="text-xl font-bold text-slate-900 mt-4"),
                        rx.el.p(
                            "Chat with our Gemini-powered Advisor grounded in real-time Google Search, polish your essays with AI critique, and practice mock interviews.",
                            class_name="text-sm text-slate-600 leading-relaxed mt-2",
                        ),
                        class_name="p-7 rounded-3xl bg-slate-50 border border-slate-200/80",
                    ),
                    rx.el.div(
                        rx.el.span("03", class_name="text-xs font-bold px-3 py-1 rounded-full bg-slate-900 text-white"),
                        rx.el.h3("Unified Application & Mentorship", class_name="text-xl font-bold text-slate-900 mt-4"),
                        rx.el.p(
                            "Submit verified dossiers directly to partner universities and global scholarships while connecting with alumni mentors at your dream schools.",
                            class_name="text-sm text-slate-600 leading-relaxed mt-2",
                        ),
                        class_name="p-7 rounded-3xl bg-slate-50 border border-slate-200/80",
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-3 gap-6",
                ),
                class_name="max-w-7xl mx-auto px-4 sm:px-6 py-20",
            ),
            id="how-it-works",
            class_name="bg-white border-b border-slate-200/70",
        ),
        # Section 3: Three-Sided Ecosystem
        rx.el.section(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "THE THREE-SIDED MARKETPLACE",
                        class_name="text-xs font-bold uppercase tracking-widest text-slate-500",
                    ),
                    rx.el.h2(
                        "One unified platform for Students, Mentors, and Universities.",
                        class_name="text-3xl sm:text-4xl font-bold text-slate-900 mt-2",
                    ),
                    rx.el.p(
                        "Explore any of the three live portals below with a single click.",
                        class_name="text-sm text-slate-600 mt-2",
                    ),
                    class_name="max-w-2xl mb-12",
                ),
                rx.el.div(
                    # Student Card
                    rx.el.div(
                        rx.el.div(
                            rx.icon("graduation-cap", size=22, class_name="text-slate-900"),
                            class_name="w-12 h-12 rounded-2xl bg-white border border-slate-200 flex items-center justify-center shadow-xs",
                        ),
                        rx.el.h3("For Prospective Students", class_name="text-xl font-bold text-slate-900 mt-5"),
                        rx.el.p(
                            "AI University Match Deck, 14+ full-funding scholarship matcher, AI Personal Statement Reviewer, Mock Interview Simulator, and Candidacy Tracker.",
                            class_name="text-sm text-slate-600 leading-relaxed mt-2 mb-6",
                        ),
                        rx.el.button(
                            "Open Student Dashboard →",
                            on_click=AppState.login_demo_student,
                            class_name="w-full py-3 rounded-full bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold transition-colors cursor-pointer",
                        ),
                        class_name="p-7 rounded-3xl bg-white border border-slate-200 shadow-sm flex flex-col justify-between",
                    ),
                    # Mentor Card
                    rx.el.div(
                        rx.el.div(
                            rx.icon("users", size=22, class_name="text-slate-900"),
                            class_name="w-12 h-12 rounded-2xl bg-white border border-slate-200 flex items-center justify-center shadow-xs",
                        ),
                        rx.el.h3("For Alumni & Scholars (Mentors)", class_name="text-xl font-bold text-slate-900 mt-5"),
                        rx.el.p(
                            "Publish your verified scholar profile, manage your mentoring specialties, toggle availability in real time, and guide the next generation of global talent.",
                            class_name="text-sm text-slate-600 leading-relaxed mt-2 mb-6",
                        ),
                        rx.el.button(
                            "Open Mentor Portal →",
                            on_click=AppState.login_demo_mentor,
                            class_name="w-full py-3 rounded-full bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold transition-colors cursor-pointer",
                        ),
                        class_name="p-7 rounded-3xl bg-white border border-slate-200 shadow-sm flex flex-col justify-between",
                    ),
                    # University Card
                    rx.el.div(
                        rx.el.div(
                            rx.icon("building-2", size=22, class_name="text-slate-900"),
                            class_name="w-12 h-12 rounded-2xl bg-white border border-slate-200 flex items-center justify-center shadow-xs",
                        ),
                        rx.el.h3("For Partner Universities", class_name="text-xl font-bold text-slate-900 mt-5"),
                        rx.el.p(
                            "Receive pre-vetted, high-match international applicant dossiers with verified transcripts, AI fit scores, and 1-click admissions status workflows.",
                            class_name="text-sm text-slate-600 leading-relaxed mt-2 mb-6",
                        ),
                        rx.el.button(
                            "Open University Portal →",
                            on_click=AppState.login_demo_university,
                            class_name="w-full py-3 rounded-full bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold transition-colors cursor-pointer",
                        ),
                        class_name="p-7 rounded-3xl bg-white border border-slate-200 shadow-sm flex flex-col justify-between",
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-3 gap-6",
                ),
                class_name="max-w-7xl mx-auto px-4 sm:px-6 py-20",
            ),
            id="ecosystem",
            class_name="bg-slate-50 border-b border-slate-200/70",
        ),
        # Footer
        rx.el.footer(
            rx.el.div(
                rx.el.div(
                    rx.el.span("© 2026 Gradwyn Inc. Built for global scholars.", class_name="text-xs text-slate-500"),
                    rx.el.div(
                        rx.el.a("Sign In", href="/login", class_name="text-xs font-medium text-slate-600 hover:text-slate-900"),
                        rx.el.a("Onboarding", href="/onboarding", class_name="text-xs font-medium text-slate-600 hover:text-slate-900"),
                        rx.el.button(
                            "Leave Feedback",
                            on_click=AppState.open_feedback_modal,
                            class_name="text-xs font-medium text-slate-600 hover:text-slate-900 cursor-pointer",
                        ),
                        class_name="flex items-center gap-6",
                    ),
                    class_name="max-w-7xl mx-auto px-4 sm:px-6 py-8 flex flex-wrap items-center justify-between gap-4",
                ),
                class_name="bg-white",
            ),
        ),
        class_name="min-h-screen bg-white text-slate-900 font-sans",
    )
