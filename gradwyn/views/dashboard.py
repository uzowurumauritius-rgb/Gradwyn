"""Comprehensive Student Hub Dashboard (`/dashboard`) for Gradwyn MVP.

Modules:
1. Overview (Metrics, Global University Search with Autocomplete, Saved Shortlist)
2. Candidacy Tracker (Real-time University & Scholarship Application Status synced with University Portal)
3. Scholarships Hub ("All Grants" vs "For You" AI Filter + 1-Click Grant Application)
4. Mentorship Network (Live Verified Alumni Mentors synced with Mentor Portal)
5. Interactive AI Prep Suite (Gemini Essay Critique Engine, Mock Interview Simulator, Readiness Checklist)
6. Editorial Admissions & Scholarship Guides (Full Article Reader Modal)
"""

from __future__ import annotations

from typing import Any

import reflex as rx

from ..state import AppState
from .chat import university_match_card
from .modals import global_modals
from .navbar import brand_logo, yc_demo_switcher_bar


def _sidebar_nav_button(tab_id: str, label: str, icon_name: str) -> rx.Component:
    is_active = AppState.dashboard_tab == tab_id
    return rx.el.button(
        rx.icon(icon_name, size=17),
        rx.el.span(label, class_name="text-sm font-semibold"),
        on_click=AppState.set_dashboard_tab(tab_id),
        class_name=rx.cond(
            is_active,
            "w-full flex items-center gap-3 px-4 py-3 rounded-2xl bg-slate-900 text-white shadow-xs transition-all cursor-pointer",
            "w-full flex items-center gap-3 px-4 py-3 rounded-2xl text-slate-600 hover:bg-slate-100 hover:text-slate-900 transition-all cursor-pointer",
        ),
    )


def _application_row_card(app: dict[str, Any]) -> rx.Component:
    """Render an application row in the Candidacy Tracker."""
    status = app["status"]
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    app["type"],
                    class_name="text-[10px] font-bold uppercase tracking-widest px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-700",
                ),
                rx.el.span(
                    f"Submitted: {app['submittedDate']}",
                    class_name="text-xs text-slate-400 ml-2",
                ),
            ),
            rx.el.h4(app["name"], class_name="text-base font-bold text-slate-900 mt-1"),
            rx.el.p(f"Track: {app['program']}", class_name="text-xs text-slate-500 mt-0.5"),
        ),
        rx.el.div(
            rx.el.span(
                status,
                class_name=rx.cond(
                    status == "Accepted",
                    "text-xs font-bold px-3.5 py-1.5 rounded-full bg-emerald-100 text-emerald-800 border border-emerald-200",
                    rx.cond(
                        status == "Rejected",
                        "text-xs font-bold px-3.5 py-1.5 rounded-full bg-rose-100 text-rose-800 border border-rose-200",
                        rx.cond(
                            status == "Under Review",
                            "text-xs font-bold px-3.5 py-1.5 rounded-full bg-amber-100 text-amber-900 border border-amber-200",
                            "text-xs font-bold px-3.5 py-1.5 rounded-full bg-slate-900 text-white",
                        ),
                    ),
                ),
            ),
            class_name="flex items-center gap-3",
        ),
        class_name="flex flex-wrap items-center justify-between gap-4 p-5 rounded-2xl bg-white border border-slate-200 shadow-2xs",
    )


def _overview_tab() -> rx.Component:
    """Tab 1: Student Overview, Global University Search & Saved Shortlist."""
    return rx.el.div(
        # Welcome Banner
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    f"SCHOLAR DOSSIER · {AppState.profile_country}",
                    class_name="text-[11px] font-bold uppercase tracking-widest text-slate-400",
                ),
                rx.el.h1(
                    f"Welcome back, {AppState.profile_name}",
                    class_name="text-2xl sm:text-3xl font-bold text-white mt-1",
                ),
                rx.el.p(
                    f"{AppState.profile_target_degree} Candidate · GPA: {AppState.profile_gpa} · {AppState.profile_budget}",
                    class_name="text-xs sm:text-sm text-slate-300 mt-1",
                ),
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("user-pen", size=15),
                    rx.el.span("Edit Profile"),
                    on_click=AppState.open_edit_profile_modal,
                    class_name="flex items-center gap-1.5 px-4 py-2.5 rounded-full bg-white/10 hover:bg-white/20 text-white text-xs font-semibold transition-colors cursor-pointer",
                ),
                rx.el.a(
                    rx.icon("sparkles", size=15),
                    rx.el.span("Ask AI Advisor"),
                    href="/chat",
                    class_name="flex items-center gap-1.5 px-5 py-2.5 rounded-full bg-white text-slate-900 hover:bg-slate-100 text-xs font-bold shadow-xs transition-colors",
                ),
                class_name="flex flex-wrap items-center gap-2.5",
            ),
            class_name="p-6 sm:p-8 rounded-3xl bg-slate-900 text-white flex flex-wrap items-center justify-between gap-4 mb-6",
        ),
        # 4 Key Readiness Metrics
        rx.el.div(
            rx.el.div(
                rx.el.p("Saved Universities", class_name="text-xs font-medium text-slate-500"),
                rx.el.p(AppState.saved_universities_count, class_name="text-3xl font-bold text-slate-900 mt-1"),
                rx.el.p("Shortlisted for 2026/27", class_name="text-[11px] text-emerald-600 font-semibold mt-1"),
                class_name="p-5 rounded-3xl bg-white border border-slate-200",
            ),
            rx.el.div(
                rx.el.p("Active Applications", class_name="text-xs font-medium text-slate-500"),
                rx.el.p(AppState.active_applications_count, class_name="text-3xl font-bold text-slate-900 mt-1"),
                rx.el.button(
                    "View Candidacy Tracker →",
                    on_click=AppState.set_dashboard_tab("candidacy"),
                    class_name="text-[11px] text-slate-700 font-bold hover:underline mt-1 cursor-pointer",
                ),
                class_name="p-5 rounded-3xl bg-white border border-slate-200",
            ),
            rx.el.div(
                rx.el.p("Matched Grants", class_name="text-xs font-medium text-slate-500"),
                rx.el.p("14", class_name="text-3xl font-bold text-slate-900 mt-1"),
                rx.el.button(
                    "Explore Scholarships →",
                    on_click=AppState.set_dashboard_tab("scholarships"),
                    class_name="text-[11px] text-slate-700 font-bold hover:underline mt-1 cursor-pointer",
                ),
                class_name="p-5 rounded-3xl bg-white border border-slate-200",
            ),
            rx.el.div(
                rx.el.p("Admissions Readiness", class_name="text-xs font-medium text-slate-500"),
                rx.el.p("94%", class_name="text-3xl font-bold text-slate-900 mt-1"),
                rx.el.button(
                    "Open AI Prep Suite →",
                    on_click=AppState.set_dashboard_tab("prep"),
                    class_name="text-[11px] text-emerald-700 font-bold hover:underline mt-1 cursor-pointer",
                ),
                class_name="p-5 rounded-3xl bg-white border border-slate-200",
            ),
            class_name="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8",
        ),
        # Global University Search Bar with Autocomplete
        rx.el.div(
            rx.el.div(
                rx.icon("search", size=18, class_name="text-slate-400 shrink-0"),
                rx.debounce_input(
                    rx.el.input(
                        on_change=AppState.set_uni_search_query,
                        placeholder="Search global universities by name, country, or major (e.g., MIT, ALU Mauritius, Oxford, Toronto)...",
                        class_name="w-full text-sm text-slate-900 focus:outline-none bg-transparent",
                    ),
                    debounce_timeout=250,
                ),
                class_name="flex items-center gap-3 px-5 py-3.5 rounded-2xl bg-white border border-slate-300 shadow-2xs",
            ),
            rx.cond(
                AppState.searched_global_universities.length() > 0,
                rx.el.div(
                    rx.foreach(
                        AppState.searched_global_universities,
                        lambda u: rx.el.div(
                            rx.el.div(
                                rx.el.p(u["name"], class_name="text-sm font-bold text-slate-900"),
                                rx.el.p(
                                    f"{u['location']} · {u['rank']} · Acceptance: {u['acceptanceRate']}",
                                    class_name="text-xs text-slate-500",
                                ),
                            ),
                            rx.el.div(
                                rx.el.button(
                                    "Save to Shortlist",
                                    on_click=AppState.select_searched_university(u),
                                    class_name="px-3.5 py-1.5 rounded-full bg-slate-100 hover:bg-slate-200 text-xs font-semibold text-slate-800 cursor-pointer",
                                ),
                                rx.el.button(
                                    "Apply Now",
                                    on_click=AppState.open_university_apply_modal(u),
                                    class_name="px-3.5 py-1.5 rounded-full bg-slate-900 hover:bg-slate-800 text-xs font-bold text-white cursor-pointer",
                                ),
                                class_name="flex items-center gap-2",
                            ),
                            class_name="flex flex-wrap items-center justify-between gap-2 p-3.5 hover:bg-slate-50 rounded-xl border-b border-slate-100 last:border-none",
                        ),
                    ),
                    class_name="mt-2 p-2 rounded-2xl bg-white border border-slate-200 shadow-lg",
                ),
            ),
            class_name="mb-8",
        ),
        # Saved Universities Grid
        rx.el.div(
            rx.el.div(
                rx.el.h2("Your Saved Universities Shortlist", class_name="text-xl font-bold text-slate-900"),
                rx.el.a(
                    "Discover More with AI Advisor →",
                    href="/chat",
                    class_name="text-xs font-bold text-slate-700 hover:text-slate-900 underline",
                ),
                class_name="flex items-center justify-between mb-4",
            ),
            rx.el.div(
                rx.foreach(AppState.saved_universities, university_match_card),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5",
            ),
            class_name="mb-10",
        ),
        # Recent Applications Snapshot
        rx.el.div(
            rx.el.div(
                rx.el.h2("Recent Candidacy Submissions", class_name="text-xl font-bold text-slate-900"),
                rx.el.button(
                    "View All →",
                    on_click=AppState.set_dashboard_tab("candidacy"),
                    class_name="text-xs font-bold text-slate-700 hover:text-slate-900 underline cursor-pointer",
                ),
                class_name="flex items-center justify-between mb-4",
            ),
            rx.el.div(
                rx.foreach(AppState.student_applications, _application_row_card),
                class_name="space-y-3",
            ),
        ),
    )


def _candidacy_tab() -> rx.Component:
    """Tab 2: Full Candidacy & Applications Tracker."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h1("Candidacy & Applications Tracker", class_name="text-2xl font-bold text-slate-900"),
                rx.el.p(
                    "Track your university and scholarship applications in real time. Decisions issued by Partner Universities appear here immediately.",
                    class_name="text-sm text-slate-600 mt-1",
                ),
            ),
            rx.el.button(
                "Inspect in University Portal →",
                on_click=AppState.login_demo_university,
                class_name="px-4 py-2.5 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-bold transition-colors cursor-pointer",
            ),
            class_name="flex flex-wrap items-center justify-between gap-4 mb-6",
        ),
        rx.el.div(
            rx.foreach(AppState.student_applications, _application_row_card),
            class_name="space-y-3",
        ),
    )


def _scholarship_card(sch: dict[str, Any]) -> rx.Component:
    """Render a Scholarship grant card."""
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                sch["location"],
                class_name="text-[11px] font-bold px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-700",
            ),
            rx.el.span(
                f"Deadline: {sch['deadline']}",
                class_name="text-xs font-semibold text-slate-500",
            ),
            class_name="flex items-center justify-between mb-3",
        ),
        rx.el.h3(sch["name"], class_name="text-lg font-bold text-slate-900 leading-snug"),
        rx.el.p(sch["provider"], class_name="text-xs font-semibold text-slate-500 mt-0.5"),
        rx.el.div(
            rx.icon("banknote", size=15, class_name="text-emerald-700 shrink-0"),
            rx.el.span(sch["amount"], class_name="text-xs font-bold text-emerald-800"),
            class_name="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-50 border border-emerald-200 mt-3",
        ),
        rx.el.p(
            sch["description"],
            class_name="text-xs text-slate-600 leading-relaxed mt-3 mb-4",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("send", size=14),
                rx.el.span("Apply for Grant"),
                on_click=AppState.open_scholarship_apply_modal(sch),
                class_name="flex-1 flex items-center justify-center gap-1.5 py-2.5 px-4 rounded-full bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold transition-colors cursor-pointer",
            ),
            rx.el.a(
                rx.el.span("Official Site"),
                rx.icon("external-link", size=13),
                href=sch["website"],
                target="_blank",
                class_name="flex items-center justify-center gap-1 py-2.5 px-4 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold transition-colors",
            ),
            class_name="flex items-center gap-2 pt-3 border-t border-slate-100",
        ),
        class_name="p-6 rounded-3xl bg-white border border-slate-200 shadow-2xs flex flex-col justify-between",
    )


def _scholarships_tab() -> rx.Component:
    """Tab 3: Global Scholarships Hub with 'All Grants' vs 'For You' AI matching."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h1("Global Scholarships & Fellowships Hub", class_name="text-2xl font-bold text-slate-900"),
                rx.el.p(
                    "Verified full-tuition and merit grants across North America, Europe, Africa, and Asia.",
                    class_name="text-sm text-slate-600 mt-1",
                ),
            ),
            # Filter pills: All Grants vs For You
            rx.el.div(
                rx.el.button(
                    "All Grants (14)",
                    on_click=AppState.set_scholarship_filter("all"),
                    class_name=rx.cond(
                        AppState.scholarship_filter == "all",
                        "px-4 py-2 rounded-full text-xs font-bold bg-slate-900 text-white cursor-pointer",
                        "px-4 py-2 rounded-full text-xs font-semibold bg-slate-100 text-slate-700 hover:bg-slate-200 cursor-pointer",
                    ),
                ),
                rx.el.button(
                    "✨ For You (AI Matched)",
                    on_click=AppState.set_scholarship_filter("for_you"),
                    class_name=rx.cond(
                        AppState.scholarship_filter == "for_you",
                        "px-4 py-2 rounded-full text-xs font-bold bg-slate-900 text-white cursor-pointer",
                        "px-4 py-2 rounded-full text-xs font-semibold bg-slate-100 text-slate-700 hover:bg-slate-200 cursor-pointer",
                    ),
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="flex flex-wrap items-center justify-between gap-4 mb-6",
        ),
        # Search bar
        rx.el.div(
            rx.icon("search", size=17, class_name="text-slate-400 shrink-0"),
            rx.debounce_input(
                rx.el.input(
                    on_change=AppState.set_scholarship_search_query,
                    placeholder="Filter scholarships by name, foundation, or region (e.g., Mastercard, Gates, Rhodes, Canada)...",
                    class_name="w-full text-sm text-slate-900 focus:outline-none bg-transparent",
                ),
                debounce_timeout=250,
            ),
            class_name="flex items-center gap-3 px-4 py-3 rounded-2xl bg-white border border-slate-300 mb-6",
        ),
        rx.el.div(
            rx.foreach(AppState.filtered_scholarships, _scholarship_card),
            class_name="grid grid-cols-1 md:grid-cols-2 gap-5",
        ),
    )


def _mentor_card(mentor: dict[str, Any]) -> rx.Component:
    """Render a Verified Mentor card in the Student Mentorship Network."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.img(
                    src=mentor["imageUrl"],
                    alt=mentor["name"],
                    class_name="w-14 h-14 rounded-2xl object-cover border border-slate-200",
                ),
                rx.el.div(
                    rx.el.h3(mentor["name"], class_name="text-base font-bold text-slate-900"),
                    rx.el.p(mentor["role"], class_name="text-xs font-semibold text-slate-600"),
                    rx.el.p(
                        f"{mentor['university']} · {mentor['location']}",
                        class_name="text-xs text-slate-400",
                    ),
                ),
                class_name="flex items-center gap-3.5",
            ),
            rx.el.span(
                rx.cond(mentor["available"], "Available", "Booked"),
                class_name=rx.cond(
                    mentor["available"],
                    "text-[11px] font-bold px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200",
                    "text-[11px] font-bold px-2.5 py-1 rounded-full bg-slate-100 text-slate-500",
                ),
            ),
            class_name="flex items-start justify-between gap-2 mb-3",
        ),
        rx.el.p(mentor["bio"], class_name="text-xs text-slate-600 leading-relaxed mb-4"),
        rx.el.div(
            rx.foreach(
                mentor["specialties"],
                lambda sp: rx.el.span(
                    sp,
                    class_name="text-[11px] font-semibold px-2.5 py-1 rounded-full bg-slate-100 text-slate-700",
                ),
            ),
            class_name="flex flex-wrap gap-1.5 mb-4",
        ),
        rx.el.div(
            rx.el.a(
                rx.icon("message-square-more", size=14),
                rx.el.span("Connect & Request Session"),
                href=mentor["linkedin"],
                target="_blank",
                class_name="w-full flex items-center justify-center gap-2 py-2.5 rounded-full bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold transition-colors",
            ),
            class_name="pt-3 border-t border-slate-100",
        ),
        class_name="p-6 rounded-3xl bg-white border border-slate-200 shadow-2xs flex flex-col justify-between",
    )


def _mentors_tab() -> rx.Component:
    """Tab 4: Verified Alumni & Scholar Mentorship Network."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h1("Verified Alumni & Scholar Mentorship Network", class_name="text-2xl font-bold text-slate-900"),
                rx.el.p(
                    "Connect with current Rhodes, Mastercard, and PhD scholars at Stanford, Oxford, MIT, and ALU. Synced live with the Mentor Portal.",
                    class_name="text-sm text-slate-600 mt-1",
                ),
            ),
            rx.el.button(
                "Switch to Mentor Portal →",
                on_click=AppState.login_demo_mentor,
                class_name="px-4 py-2 rounded-full bg-slate-100 hover:bg-slate-200 text-xs font-bold text-slate-800 cursor-pointer",
            ),
            class_name="flex flex-wrap items-center justify-between gap-4 mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("search", size=17, class_name="text-slate-400 shrink-0"),
                rx.debounce_input(
                    rx.el.input(
                        on_change=AppState.set_mentor_search_query,
                        placeholder="Search mentors by university, specialty, or name (e.g., Stanford, Oxford, ALU, Rhodes)...",
                        class_name="w-full text-sm text-slate-900 focus:outline-none bg-transparent",
                    ),
                    debounce_timeout=250,
                ),
                class_name="flex-1 flex items-center gap-3 px-4 py-2.5 rounded-2xl bg-white border border-slate-300",
            ),
            rx.el.button(
                rx.cond(
                    AppState.mentor_only_available,
                    "✓ Showing Available Now",
                    "Filter: Available Now",
                ),
                on_click=AppState.toggle_mentor_only_available,
                class_name=rx.cond(
                    AppState.mentor_only_available,
                    "px-4 py-2.5 rounded-2xl text-xs font-bold bg-slate-900 text-white cursor-pointer",
                    "px-4 py-2.5 rounded-2xl text-xs font-semibold bg-white border border-slate-300 text-slate-700 hover:bg-slate-50 cursor-pointer",
                ),
            ),
            class_name="flex flex-wrap items-center gap-3 mb-6",
        ),
        rx.el.div(
            rx.foreach(AppState.filtered_mentors, _mentor_card),
            class_name="grid grid-cols-1 md:grid-cols-2 gap-5",
        ),
    )


def _prep_suite_tab() -> rx.Component:
    """Tab 5: Interactive AI Prep Suite (Essay Critique, Mock Interview, Readiness Checklist)."""
    return rx.el.div(
        rx.el.div(
            rx.el.h1("AI Application & Interview Prep Suite", class_name="text-2xl font-bold text-slate-900"),
            rx.el.p(
                "Sharpen your Personal Statement, practice real admissions interviews with Gemini AI, and track your dossier readiness.",
                class_name="text-sm text-slate-600 mt-1",
            ),
            class_name="mb-6",
        ),
        # Sub-navigation pills
        rx.el.div(
            rx.el.button(
                rx.icon("file-pen-line", size=15),
                rx.el.span("1. AI Essay Critique Engine"),
                on_click=AppState.set_prep_active_tool("essay"),
                class_name=rx.cond(
                    AppState.prep_active_tool == "essay",
                    "flex items-center gap-2 px-5 py-2.5 rounded-full text-xs font-bold bg-slate-900 text-white shadow-xs cursor-pointer",
                    "flex items-center gap-2 px-5 py-2.5 rounded-full text-xs font-semibold bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 cursor-pointer",
                ),
            ),
            rx.el.button(
                rx.icon("mic", size=15),
                rx.el.span("2. AI Mock Interview Simulator"),
                on_click=AppState.set_prep_active_tool("interview"),
                class_name=rx.cond(
                    AppState.prep_active_tool == "interview",
                    "flex items-center gap-2 px-5 py-2.5 rounded-full text-xs font-bold bg-slate-900 text-white shadow-xs cursor-pointer",
                    "flex items-center gap-2 px-5 py-2.5 rounded-full text-xs font-semibold bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 cursor-pointer",
                ),
            ),
            rx.el.button(
                rx.icon("list-checks", size=15),
                rx.el.span(f"3. Dossier Checklist ({AppState.checklist_completed_count}/6)"),
                on_click=AppState.set_prep_active_tool("checklist"),
                class_name=rx.cond(
                    AppState.prep_active_tool == "checklist",
                    "flex items-center gap-2 px-5 py-2.5 rounded-full text-xs font-bold bg-slate-900 text-white shadow-xs cursor-pointer",
                    "flex items-center gap-2 px-5 py-2.5 rounded-full text-xs font-semibold bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 cursor-pointer",
                ),
            ),
            class_name="flex flex-wrap items-center gap-2.5 mb-6",
        ),
        # Tool 1: AI Essay Critique
        rx.cond(
            AppState.prep_active_tool == "essay",
            rx.el.div(
                rx.form(
                    rx.el.label(
                        "Target University or Scholarship",
                        html_for="prep_essay_target",
                        class_name="block text-xs font-bold uppercase tracking-wider text-slate-500 mb-1.5",
                    ),
                    rx.el.input(
                        id="prep_essay_target",
                        name="essay_target",
                        default_value=AppState.prep_essay_target,
                        placeholder="e.g., Massachusetts Institute of Technology (MIT)",
                        class_name="w-full px-4 py-2.5 rounded-xl border border-slate-300 text-sm mb-4 focus:outline-none focus:ring-2 focus:ring-slate-900/10 focus:border-slate-900 transition-all",
                    ),
                    rx.el.label(
                        "Personal Statement / Motivation Essay Draft",
                        html_for="prep_essay_draft",
                        class_name="block text-xs font-bold uppercase tracking-wider text-slate-500 mb-1.5",
                    ),
                    rx.el.textarea(
                        id="prep_essay_draft",
                        name="essay_draft",
                        default_value=AppState.prep_essay_draft,
                        rows=7,
                        placeholder="Paste your essay draft here...",
                        class_name="w-full p-4 rounded-2xl border border-slate-300 text-sm leading-relaxed mb-4 focus:outline-none focus:ring-2 focus:ring-slate-900/10 focus:border-slate-900 transition-all",
                    ),
                    rx.el.button(
                        rx.icon("sparkles", size=16),
                        rx.el.span(
                            rx.cond(
                                AppState.is_prep_essay_loading,
                                "Evaluating Essay with Gemini 3.8...",
                                "Run AI Admissions Reader Critique",
                            )
                        ),
                        type="submit",
                        class_name="flex items-center gap-2 px-6 py-3 rounded-full bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold shadow-xs cursor-pointer",
                    ),
                    on_submit=AppState.handle_prep_essay_form_submit,
                    class_name="p-6 rounded-3xl bg-white border border-slate-200 mb-6",
                ),
                rx.cond(
                    AppState.prep_essay_result.contains("overallScore"),
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                rx.el.p("Overall Score", class_name="text-xs text-slate-500"),
                                rx.el.p(f"{AppState.prep_essay_result['overallScore']}/100", class_name="text-2xl font-bold text-slate-900"),
                                class_name="p-4 rounded-2xl bg-slate-50 border border-slate-200",
                            ),
                            rx.el.div(
                                rx.el.p("Opening Hook", class_name="text-xs text-slate-500"),
                                rx.el.p(f"{AppState.prep_essay_result['hookScore']}/100", class_name="text-2xl font-bold text-slate-900"),
                                class_name="p-4 rounded-2xl bg-slate-50 border border-slate-200",
                            ),
                            rx.el.div(
                                rx.el.p("Leadership Impact", class_name="text-xs text-slate-500"),
                                rx.el.p(f"{AppState.prep_essay_result['impactScore']}/100", class_name="text-2xl font-bold text-slate-900"),
                                class_name="p-4 rounded-2xl bg-slate-50 border border-slate-200",
                            ),
                            rx.el.div(
                                rx.el.p("Institutional Fit", class_name="text-xs text-slate-500"),
                                rx.el.p(f"{AppState.prep_essay_result['fitScore']}/100", class_name="text-2xl font-bold text-slate-900"),
                                class_name="p-4 rounded-2xl bg-slate-50 border border-slate-200",
                            ),
                            class_name="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-5",
                        ),
                        rx.el.p(
                            AppState.prep_essay_result["summary"],
                            class_name="text-sm text-slate-700 leading-relaxed mb-4",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "AI-Suggested Stronger Opening Paragraph:",
                                class_name="text-xs font-bold uppercase tracking-wider text-emerald-800 mb-1.5",
                            ),
                            rx.el.p(
                                AppState.prep_essay_result["rewrittenOpening"],
                                class_name="text-sm text-slate-800 italic bg-emerald-50/70 p-4 rounded-2xl border border-emerald-200",
                            ),
                        ),
                        class_name="p-6 rounded-3xl bg-white border border-slate-200",
                    ),
                ),
            ),
        ),
        # Tool 2: AI Mock Interview Simulator
        rx.cond(
            AppState.prep_active_tool == "interview",
            rx.el.div(
                rx.form(
                    rx.el.p(
                        "Select an Admissions / Scholarship Interview Question:",
                        class_name="text-xs font-bold uppercase tracking-wider text-slate-500 mb-2",
                    ),
                    rx.el.div(
                        rx.foreach(
                            AppState.interview_question_options,
                            lambda q: rx.el.button(
                                q,
                                type="button",
                                on_click=AppState.set_prep_interview_question(q),
                                class_name=rx.cond(
                                    AppState.prep_interview_question == q,
                                    "w-full text-left p-3.5 rounded-2xl text-xs font-bold bg-slate-900 text-white cursor-pointer",
                                    "w-full text-left p-3.5 rounded-2xl text-xs font-medium bg-slate-50 hover:bg-slate-100 text-slate-700 border border-slate-200 cursor-pointer",
                                ),
                            ),
                        ),
                        class_name="space-y-2 mb-5",
                    ),
                    rx.el.label(
                        "Your Spoken / Written Interview Response",
                        html_for="prep_interview_answer",
                        class_name="block text-xs font-bold uppercase tracking-wider text-slate-500 mb-1.5",
                    ),
                    rx.el.textarea(
                        id="prep_interview_answer",
                        name="interview_answer",
                        default_value=AppState.prep_interview_answer,
                        rows=5,
                        placeholder="Type or dictate your mock interview response...",
                        class_name="w-full p-4 rounded-2xl border border-slate-300 text-sm leading-relaxed mb-4 focus:outline-none focus:ring-2 focus:ring-slate-900/10 focus:border-slate-900 transition-all",
                    ),
                    rx.el.button(
                        rx.icon("sparkles", size=16),
                        rx.el.span(
                            rx.cond(
                                AppState.is_prep_interview_loading,
                                "Scoring Response...",
                                "Evaluate Interview Response",
                            )
                        ),
                        type="submit",
                        class_name="flex items-center gap-2 px-6 py-3 rounded-full bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold cursor-pointer",
                    ),
                    on_submit=AppState.handle_prep_interview_form_submit,
                    class_name="p-6 rounded-3xl bg-white border border-slate-200 mb-6",
                ),
                rx.cond(
                    AppState.prep_interview_result.contains("score"),
                    rx.el.div(
                        rx.el.div(
                            rx.el.span(
                                f"Interviewer Score: {AppState.prep_interview_result['score']}/100",
                                class_name="text-xs font-bold px-3 py-1 rounded-full bg-slate-900 text-white",
                            ),
                            rx.el.span(
                                AppState.prep_interview_result["clarity"],
                                class_name="text-xs font-bold px-3 py-1 rounded-full bg-emerald-100 text-emerald-800",
                            ),
                            class_name="flex items-center gap-2 mb-3",
                        ),
                        rx.el.p(
                            AppState.prep_interview_result["feedback"],
                            class_name="text-sm text-slate-700 leading-relaxed mb-4",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Model STAR Response:",
                                class_name="text-xs font-bold uppercase tracking-wider text-slate-500 mb-1",
                            ),
                            rx.el.p(
                                AppState.prep_interview_result["sampleAnswer"],
                                class_name="text-xs text-slate-700 italic bg-slate-50 p-4 rounded-2xl border border-slate-200",
                            ),
                        ),
                        class_name="p-6 rounded-3xl bg-white border border-slate-200",
                    ),
                ),
            ),
        ),
        # Tool 3: Admissions Dossier Checklist
        rx.cond(
            AppState.prep_active_tool == "checklist",
            rx.el.div(
                rx.foreach(
                    AppState.checklist_items,
                    lambda item: rx.el.button(
                        rx.el.div(
                            rx.cond(
                                item["done"],
                                rx.icon("circle-check-big", size=20, class_name="text-emerald-600"),
                                rx.icon("circle", size=20, class_name="text-slate-300"),
                            ),
                            rx.el.div(
                                rx.el.p(item["label"], class_name="text-sm font-bold text-slate-900 text-left"),
                                rx.el.p(item["category"], class_name="text-xs text-slate-500 text-left"),
                            ),
                            class_name="flex items-center gap-3",
                        ),
                        rx.el.span(
                            rx.cond(item["done"], "Completed", "Pending"),
                            class_name=rx.cond(
                                item["done"],
                                "text-xs font-bold px-3 py-1 rounded-full bg-emerald-100 text-emerald-800",
                                "text-xs font-semibold px-3 py-1 rounded-full bg-slate-100 text-slate-600",
                            ),
                        ),
                        on_click=AppState.toggle_checklist_item(item["id"]),
                        class_name="w-full flex items-center justify-between p-4 rounded-2xl bg-white border border-slate-200 hover:border-slate-400 transition-all cursor-pointer",
                    ),
                ),
                class_name="space-y-3",
            ),
        ),
    )


def _guide_card(guide: dict[str, Any]) -> rx.Component:
    """Render an Editorial Guide Card with a working 'Read Full Guide' modal trigger."""
    return rx.el.div(
        rx.el.div(
            rx.el.img(
                src=guide["imageUrl"],
                alt=guide["title"],
                class_name="w-full h-44 object-cover",
            ),
            rx.el.span(
                guide["category"],
                class_name="absolute top-3 left-3 text-[11px] font-bold px-3 py-1 rounded-full bg-slate-900/85 text-white backdrop-blur-xs",
            ),
            class_name="relative w-full h-44 overflow-hidden bg-slate-100",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.span(guide["readTime"], class_name="text-xs font-semibold text-slate-400"),
                rx.el.span(f"By {guide['author']}", class_name="text-xs font-medium text-slate-500"),
                class_name="flex items-center justify-between mb-2",
            ),
            rx.el.h3(guide["title"], class_name="text-lg font-bold text-slate-900 leading-snug"),
            rx.el.p(guide["description"], class_name="text-xs text-slate-600 leading-relaxed mt-2 mb-4"),
            rx.el.button(
                rx.el.span("Read Full Guide"),
                rx.icon("book-open", size=14),
                on_click=AppState.open_guide_reader(guide),
                class_name="w-full flex items-center justify-center gap-2 py-2.5 rounded-full bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold transition-colors cursor-pointer",
            ),
            class_name="p-5",
        ),
        class_name="bg-white rounded-3xl border border-slate-200 overflow-hidden shadow-2xs flex flex-col justify-between",
    )


def _guides_tab() -> rx.Component:
    """Tab 6: Editorial Admissions & Scholarship Guides."""
    return rx.el.div(
        rx.el.div(
            rx.el.h1("Admissions & Financial Aid Playbooks", class_name="text-2xl font-bold text-slate-900"),
            rx.el.p(
                "Step-by-step blueprints written by former admissions readers and global fellowship recipients.",
                class_name="text-sm text-slate-600 mt-1",
            ),
            class_name="mb-6",
        ),
        rx.el.div(
            rx.foreach(AppState.all_guides, _guide_card),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5",
        ),
    )


def dashboard_page() -> rx.Component:
    """Main Student Hub View (`/dashboard`)."""
    return rx.el.div(
        yc_demo_switcher_bar(),
        global_modals(),
        # Top Header
        rx.el.header(
            rx.el.div(
                brand_logo(),
                rx.el.div(
                    rx.el.a(
                        rx.icon("sparkles", size=15),
                        rx.el.span("AI Advisor & Match Deck"),
                        href="/chat",
                        class_name="flex items-center gap-1.5 px-4 py-2 rounded-full bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold transition-colors",
                    ),
                    rx.el.button(
                        rx.icon("message-square-heart", size=15),
                        rx.el.span("Feedback"),
                        on_click=AppState.open_feedback_modal,
                        class_name="flex items-center gap-1.5 px-3.5 py-2 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold transition-colors cursor-pointer",
                    ),
                    rx.el.button(
                        rx.icon("log-out", size=15),
                        on_click=AppState.logout,
                        title="Sign Out",
                        class_name="p-2 rounded-full text-slate-500 hover:text-slate-900 hover:bg-slate-100 transition-colors cursor-pointer",
                    ),
                    class_name="flex items-center gap-2",
                ),
                class_name="max-w-7xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between",
            ),
            class_name="bg-white border-b border-slate-200 sticky top-0 z-30",
        ),
        # Main Dashboard Layout (Left Sidebar + Right Content Area)
        rx.el.div(
            # Left Sidebar Navigation
            rx.el.aside(
                rx.el.div(
                    _sidebar_nav_button("overview", "Overview & Shortlist", "layout-dashboard"),
                    _sidebar_nav_button("candidacy", "Candidacy Tracker", "folder-check"),
                    _sidebar_nav_button("scholarships", "Scholarships Hub", "award"),
                    _sidebar_nav_button("mentors", "Mentorship Network", "users"),
                    _sidebar_nav_button("prep", "AI Prep Suite", "sparkles"),
                    _sidebar_nav_button("guides", "Admissions Guides", "book-open"),
                    class_name="space-y-1.5",
                ),
                rx.el.div(
                    rx.el.p("Need tailored advice?", class_name="text-xs font-bold text-slate-900"),
                    rx.el.p(
                        "Launch the split-screen Gemini 3.8 Advisor to compare universities in real time.",
                        class_name="text-[11px] text-slate-500 mt-1 mb-3",
                    ),
                    rx.el.a(
                        "Open AI Chat →",
                        href="/chat",
                        class_name="block text-center py-2 rounded-full bg-slate-900 text-white text-xs font-bold hover:bg-slate-800",
                    ),
                    class_name="p-4 rounded-2xl bg-slate-100 border border-slate-200 mt-8",
                ),
                class_name="w-full lg:w-64 shrink-0",
            ),
            # Right Content Area
            rx.el.main(
                rx.cond(AppState.dashboard_tab == "overview", _overview_tab()),
                rx.cond(AppState.dashboard_tab == "candidacy", _candidacy_tab()),
                rx.cond(AppState.dashboard_tab == "scholarships", _scholarships_tab()),
                rx.cond(AppState.dashboard_tab == "mentors", _mentors_tab()),
                rx.cond(AppState.dashboard_tab == "prep", _prep_suite_tab()),
                rx.cond(AppState.dashboard_tab == "guides", _guides_tab()),
                class_name="flex-1 min-w-0",
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 py-8 flex flex-col lg:flex-row gap-8",
        ),
        class_name="min-h-screen bg-slate-50/50 text-slate-900 font-sans",
    )
