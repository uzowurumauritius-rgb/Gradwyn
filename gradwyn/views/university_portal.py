"""Partner University Admissions Portal (`/university-dashboard`)."""

from __future__ import annotations

from typing import Any

import reflex as rx

from ..state import AppState
from .modals import global_modals
from .navbar import brand_logo, yc_demo_switcher_bar


def _candidate_table_row(candidate: dict[str, Any]) -> rx.Component:
    """Render an applicant row in the University Admissions Portal."""
    status = candidate["status"]
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.el.p(candidate["studentName"], class_name="text-sm font-bold text-slate-900"),
                rx.el.p(f"{candidate['country']} · {candidate['studentEmail']}", class_name="text-xs text-slate-500"),
            ),
            class_name="px-5 py-4",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.p(candidate["targetName"], class_name="text-xs font-bold text-slate-900"),
                rx.el.p(candidate["program"], class_name="text-xs text-slate-500"),
            ),
            class_name="px-5 py-4",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.p(candidate["gpa"], class_name="text-xs font-bold text-slate-900"),
                rx.el.p(candidate["testScores"], class_name="text-[11px] text-slate-500"),
            ),
            class_name="px-5 py-4",
        ),
        rx.el.td(
            rx.el.span(
                f"{candidate['matchScore']}% Match",
                class_name="text-xs font-bold px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200",
            ),
            class_name="px-5 py-4",
        ),
        rx.el.td(
            rx.el.span(
                status,
                class_name=rx.cond(
                    status == "Accepted",
                    "text-xs font-bold px-3 py-1 rounded-full bg-emerald-100 text-emerald-800",
                    rx.cond(
                        status == "Rejected",
                        "text-xs font-bold px-3 py-1 rounded-full bg-rose-100 text-rose-800",
                        rx.cond(
                            status == "Under Review",
                            "text-xs font-bold px-3 py-1 rounded-full bg-amber-100 text-amber-900",
                            "text-xs font-bold px-3 py-1 rounded-full bg-slate-900 text-white",
                        ),
                    ),
                ),
            ),
            class_name="px-5 py-4",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    "Inspect Dossier",
                    on_click=AppState.open_candidate_modal(candidate),
                    class_name="px-3.5 py-1.5 rounded-full bg-slate-100 hover:bg-slate-200 text-xs font-bold text-slate-800 cursor-pointer",
                ),
                rx.el.button(
                    "✓ Admit",
                    on_click=AppState.update_candidate_status(candidate["id"], "Accepted"),
                    class_name="px-3 py-1.5 rounded-full bg-emerald-600 hover:bg-emerald-700 text-xs font-bold text-white cursor-pointer",
                ),
                rx.el.button(
                    "Reject",
                    on_click=AppState.update_candidate_status(candidate["id"], "Rejected"),
                    class_name="px-3 py-1.5 rounded-full bg-rose-50 hover:bg-rose-100 text-xs font-semibold text-rose-700 cursor-pointer",
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="px-5 py-4",
        ),
        class_name="border-b border-slate-100 hover:bg-slate-50/70 transition-colors",
    )


def university_dashboard_page() -> rx.Component:
    """Partner University Admissions Portal (`/university-dashboard`)."""
    return rx.el.div(
        yc_demo_switcher_bar(),
        global_modals(),
        rx.el.header(
            rx.el.div(
                brand_logo(),
                rx.el.div(
                    rx.el.button(
                        "Switch to Student Hub →",
                        on_click=AppState.login_demo_student,
                        class_name="px-4 py-2 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-bold cursor-pointer",
                    ),
                    rx.el.button(
                        rx.icon("log-out", size=15),
                        on_click=AppState.logout,
                        class_name="p-2 rounded-full text-slate-500 hover:text-slate-900 hover:bg-slate-100 cursor-pointer",
                    ),
                    class_name="flex items-center gap-2",
                ),
                class_name="max-w-7xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between",
            ),
            class_name="bg-white border-b border-slate-200",
        ),
        rx.el.main(
            rx.el.div(
                # Top University Partner Header
                rx.el.div(
                    rx.el.div(
                        rx.el.span(
                            "PARTNER UNIVERSITY ADMISSIONS PORTAL",
                            class_name="text-[11px] font-bold uppercase tracking-widest text-slate-400",
                        ),
                        rx.el.h1(
                            AppState.partner_university_name,
                            class_name="text-2xl sm:text-3xl font-bold text-white mt-1",
                        ),
                        rx.el.p(
                            "Review pre-vetted international candidate dossiers, AI fit scores, and issue real-time admission decisions.",
                            class_name="text-xs sm:text-sm text-slate-300 mt-1",
                        ),
                    ),
                    rx.el.div(
                        rx.el.select(
                            rx.foreach(
                                AppState.partner_university_options,
                                lambda opt: rx.el.option(opt, value=opt),
                            ),
                            value=AppState.partner_university_name,
                            on_change=AppState.set_partner_university_name,
                            class_name="px-4 py-2.5 rounded-full bg-white text-slate-900 text-xs font-bold focus:outline-none cursor-pointer",
                        ),
                    ),
                    class_name="p-6 sm:p-8 rounded-3xl bg-slate-900 text-white flex flex-wrap items-center justify-between gap-4 mb-6",
                ),
                # Funnel Metrics
                rx.el.div(
                    rx.el.div(
                        rx.el.p("Total Dossiers Received", class_name="text-xs font-medium text-slate-500"),
                        rx.el.p(AppState.uni_portal_total_count, class_name="text-3xl font-bold text-slate-900 mt-1"),
                        class_name="p-5 rounded-3xl bg-white border border-slate-200",
                    ),
                    rx.el.div(
                        rx.el.p("Awaiting Committee Review", class_name="text-xs font-medium text-slate-500"),
                        rx.el.p(AppState.uni_portal_review_count, class_name="text-3xl font-bold text-amber-700 mt-1"),
                        class_name="p-5 rounded-3xl bg-white border border-slate-200",
                    ),
                    rx.el.div(
                        rx.el.p("Admitted Scholars", class_name="text-xs font-medium text-slate-500"),
                        rx.el.p(AppState.uni_portal_accepted_count, class_name="text-3xl font-bold text-emerald-700 mt-1"),
                        class_name="p-5 rounded-3xl bg-white border border-slate-200",
                    ),
                    class_name="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6",
                ),
                # Filter & Search Bar
                rx.el.div(
                    rx.el.div(
                        rx.foreach(
                            ["All", "Submitted", "Under Review", "Accepted", "Rejected"],
                            lambda st: rx.el.button(
                                st,
                                on_click=AppState.set_uni_portal_filter_status(st),
                                class_name=rx.cond(
                                    AppState.uni_portal_filter_status == st,
                                    "px-4 py-2 rounded-full text-xs font-bold bg-slate-900 text-white cursor-pointer",
                                    "px-4 py-2 rounded-full text-xs font-semibold bg-white border border-slate-200 text-slate-600 hover:bg-slate-100 cursor-pointer",
                                ),
                            ),
                        ),
                        class_name="flex flex-wrap items-center gap-2",
                    ),
                    rx.el.div(
                        rx.icon("search", size=16, class_name="text-slate-400 shrink-0"),
                        rx.debounce_input(
                            rx.el.input(
                                on_change=AppState.set_uni_portal_search,
                                placeholder="Search by applicant name, country, or program...",
                                class_name="text-xs text-slate-900 focus:outline-none bg-transparent w-64",
                            ),
                            debounce_timeout=250,
                        ),
                        class_name="flex items-center gap-2 px-4 py-2 rounded-full bg-white border border-slate-300",
                    ),
                    class_name="flex flex-wrap items-center justify-between gap-4 mb-6",
                ),
                # Candidates Table
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th("Candidate", class_name="text-left text-[11px] font-bold uppercase tracking-wider text-slate-400 px-5 py-3.5"),
                                rx.el.th("Target Institution & Track", class_name="text-left text-[11px] font-bold uppercase tracking-wider text-slate-400 px-5 py-3.5"),
                                rx.el.th("Academic Standing", class_name="text-left text-[11px] font-bold uppercase tracking-wider text-slate-400 px-5 py-3.5"),
                                rx.el.th("AI Fit Score", class_name="text-left text-[11px] font-bold uppercase tracking-wider text-slate-400 px-5 py-3.5"),
                                rx.el.th("Decision Status", class_name="text-left text-[11px] font-bold uppercase tracking-wider text-slate-400 px-5 py-3.5"),
                                rx.el.th("Committee Actions", class_name="text-left text-[11px] font-bold uppercase tracking-wider text-slate-400 px-5 py-3.5"),
                                class_name="border-b border-slate-200 bg-slate-50/80",
                            ),
                        ),
                        rx.el.tbody(
                            rx.foreach(
                                AppState.filtered_university_applications,
                                _candidate_table_row,
                            ),
                        ),
                        class_name="w-full border-collapse",
                    ),
                    class_name="bg-white rounded-3xl border border-slate-200 shadow-xs overflow-x-auto",
                ),
                class_name="max-w-7xl mx-auto px-4 sm:px-6 py-8",
            ),
        ),
        class_name="min-h-screen bg-slate-50/50 text-slate-900 font-sans",
    )
