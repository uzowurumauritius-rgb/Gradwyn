"""Split-Screen AI Admissions Advisor & University Match Deck (`/chat`)."""

from __future__ import annotations

from typing import Any

import reflex as rx

from ..state import AppState
from .modals import global_modals
from .navbar import brand_logo, yc_demo_switcher_bar


def _chat_message_bubble(msg: dict[str, Any]) -> rx.Component:
    """Render an individual user or AI advisor message bubble."""
    is_user = msg["role"] == "user"
    return rx.el.div(
        rx.cond(
            is_user,
            rx.el.div(
                rx.el.p(
                    msg["content"],
                    class_name="text-sm leading-relaxed text-white",
                ),
                class_name="max-w-[85%] ml-auto bg-slate-900 text-white rounded-3xl rounded-br-sm px-5 py-3.5 shadow-xs",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon("sparkles", size=14, class_name="text-white"),
                        class_name="w-6 h-6 rounded-lg bg-slate-900 flex items-center justify-center shrink-0",
                    ),
                    rx.el.span(
                        "Gradwyn AI Advisor",
                        class_name="text-xs font-bold text-slate-900",
                    ),
                    rx.el.span(
                        "Gemini 3.8 Grounded",
                        class_name="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-slate-100 text-slate-600",
                    ),
                    class_name="flex items-center gap-2 mb-2",
                ),
                rx.el.div(
                    rx.markdown(msg["content"]),
                    class_name="prose prose-slate prose-sm max-w-none text-slate-700 leading-relaxed",
                ),
                class_name="max-w-[95%] bg-white border border-slate-200 rounded-3xl rounded-tl-sm p-5 shadow-xs",
            ),
        ),
        class_name="w-full",
    )


def university_match_card(uni: dict[str, Any]) -> rx.Component:
    """Editorial university recommendation card with Save, Discard, and 1-Click Apply."""
    is_saved = AppState.saved_university_names.contains(uni["name"])
    return rx.el.div(
        # Top campus photo banner with badges
        rx.el.div(
            rx.el.img(
                src=uni["imageUrl"],
                alt=uni["name"],
                class_name="w-full h-40 object-cover",
            ),
            rx.el.div(
                rx.el.span(
                    f"{uni['matchScore']}% Match",
                    class_name="text-xs font-bold px-3 py-1 rounded-full bg-emerald-500 text-white shadow-sm",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.icon("bookmark", size=15),
                        on_click=AppState.toggle_save_university(uni),
                        title="Save to Shortlist",
                        class_name=rx.cond(
                            is_saved,
                            "p-2 rounded-full bg-slate-900 text-white shadow-sm transition-colors cursor-pointer",
                            "p-2 rounded-full bg-white/90 hover:bg-white text-slate-700 shadow-sm transition-colors cursor-pointer",
                        ),
                    ),
                    rx.el.button(
                        rx.icon("x", size=15),
                        on_click=AppState.discard_university(uni["name"]),
                        title="Dismiss Recommendation",
                        class_name="p-2 rounded-full bg-white/90 hover:bg-rose-50 text-slate-600 hover:text-rose-600 shadow-sm transition-colors cursor-pointer",
                    ),
                    class_name="flex items-center gap-1.5",
                ),
                class_name="absolute top-3 inset-x-3 flex items-center justify-between",
            ),
            rx.el.div(
                rx.el.span(
                    uni["rank"],
                    class_name="text-[11px] font-bold px-2.5 py-0.5 rounded-full bg-slate-900/80 text-white backdrop-blur-xs",
                ),
                class_name="absolute bottom-3 left-3",
            ),
            class_name="relative w-full h-40 overflow-hidden bg-slate-100",
        ),
        # Card body
        rx.el.div(
            rx.el.h3(
                uni["name"],
                class_name="text-lg font-bold text-slate-900 leading-snug",
            ),
            rx.el.p(
                uni["location"],
                class_name="text-xs font-medium text-slate-500 mt-0.5",
            ),
            rx.el.p(
                uni["description"],
                class_name="text-xs text-slate-600 leading-relaxed mt-2.5 line-clamp-2",
            ),
            # Key metrics grid
            rx.el.div(
                rx.el.div(
                    rx.el.p("Acceptance", class_name="text-[10px] uppercase tracking-wider text-slate-400 font-bold"),
                    rx.el.p(uni["acceptanceRate"], class_name="text-xs font-bold text-slate-900"),
                    class_name="p-2.5 rounded-xl bg-slate-50 border border-slate-100",
                ),
                rx.el.div(
                    rx.el.p("Tuition / Aid", class_name="text-[10px] uppercase tracking-wider text-slate-400 font-bold"),
                    rx.el.p(uni["tuition"], class_name="text-xs font-bold text-slate-900 truncate"),
                    class_name="p-2.5 rounded-xl bg-slate-50 border border-slate-100",
                ),
                rx.el.div(
                    rx.el.p("Deadline", class_name="text-[10px] uppercase tracking-wider text-slate-400 font-bold"),
                    rx.el.p(uni["deadline"], class_name="text-xs font-bold text-slate-900"),
                    class_name="p-2.5 rounded-xl bg-slate-50 border border-slate-100",
                ),
                class_name="grid grid-cols-3 gap-2 my-3.5",
            ),
            # Action buttons
            rx.el.div(
                rx.el.button(
                    rx.icon("send", size=14),
                    rx.el.span("Apply Now"),
                    on_click=AppState.open_university_apply_modal(uni),
                    class_name="flex-1 flex items-center justify-center gap-1.5 py-2.5 px-4 rounded-full bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold transition-colors cursor-pointer",
                ),
                rx.el.a(
                    rx.el.span("Website"),
                    rx.icon("external-link", size=13),
                    href=uni["website"],
                    target="_blank",
                    class_name="flex items-center justify-center gap-1 py-2.5 px-4 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold transition-colors",
                ),
                class_name="flex items-center gap-2 pt-2 border-t border-slate-100",
            ),
            class_name="p-5",
        ),
        class_name="bg-white rounded-3xl border border-slate-200 shadow-xs hover:shadow-md transition-all overflow-hidden",
    )


def chat_page() -> rx.Component:
    """Split-screen AI Admissions Advisor & University Match Deck (`/chat`)."""
    return rx.el.div(
        yc_demo_switcher_bar(),
        global_modals(),
        # Top App Header
        rx.el.header(
            rx.el.div(
                brand_logo(),
                rx.el.div(
                    rx.el.button(
                        rx.icon("user-pen", size=15),
                        rx.el.span("Edit Profile"),
                        on_click=AppState.open_edit_profile_modal,
                        class_name="flex items-center gap-1.5 px-3.5 py-2 rounded-full text-xs font-semibold bg-slate-100 hover:bg-slate-200 text-slate-700 transition-colors cursor-pointer",
                    ),
                    rx.el.a(
                        rx.icon("bookmark-check", size=15),
                        rx.el.span(f"Shortlist ({AppState.saved_universities_count})"),
                        href="/dashboard",
                        class_name="flex items-center gap-1.5 px-3.5 py-2 rounded-full text-xs font-semibold bg-slate-100 hover:bg-slate-200 text-slate-700 transition-colors",
                    ),
                    rx.el.a(
                        rx.icon("layout-dashboard", size=15),
                        rx.el.span("Go to Student Hub →"),
                        href="/dashboard",
                        class_name="flex items-center gap-1.5 px-4 py-2 rounded-full text-xs font-bold bg-slate-900 hover:bg-slate-800 text-white shadow-xs transition-colors",
                    ),
                    class_name="flex items-center gap-2",
                ),
                class_name="max-w-7xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between",
            ),
            class_name="bg-white border-b border-slate-200 sticky top-0 z-30",
        ),
        # Split-screen workspace
        rx.el.main(
            rx.el.div(
                # Left Column: AI Chat Advisor
                rx.el.div(
                    # Profile context bar
                    rx.el.div(
                        rx.el.div(
                            rx.el.p(
                                f"Advising: {AppState.profile_name} ({AppState.profile_country})",
                                class_name="text-xs font-bold text-slate-900",
                            ),
                            rx.el.p(
                                f"{AppState.profile_target_degree} · GPA: {AppState.profile_gpa} · {AppState.profile_budget}",
                                class_name="text-[11px] text-slate-500",
                            ),
                        ),
                        rx.el.button(
                            "Re-Calibrate",
                            on_click=AppState.open_edit_profile_modal,
                            class_name="text-xs font-bold text-slate-900 hover:underline cursor-pointer",
                        ),
                        class_name="flex items-center justify-between px-5 py-3 bg-slate-50 border-b border-slate-200",
                    ),
                    # Messages list
                    rx.el.div(
                        rx.foreach(AppState.chat_messages, _chat_message_bubble),
                        rx.cond(
                            AppState.is_ai_loading,
                            rx.el.div(
                                rx.icon("loader-circle", size=16, class_name="animate-spin text-slate-700"),
                                rx.el.span(
                                    "Gradwyn AI is researching live admissions & scholarship data...",
                                    class_name="text-xs font-medium text-slate-600",
                                ),
                                class_name="flex items-center gap-2.5 p-4 rounded-2xl bg-white border border-slate-200 w-fit",
                            ),
                        ),
                        class_name="flex-1 p-5 space-y-4 overflow-y-auto max-h-[58vh]",
                    ),
                    # Quick prompt chips
                    rx.el.div(
                        rx.el.button(
                            rx.icon("circle-dollar-sign", size=13, class_name="text-emerald-600"),
                            rx.el.span("Full-ride scholarships for my profile"),
                            on_click=AppState.send_quick_prompt(
                                "Which full-ride scholarships and financial aid grants fit my profile best?"
                            ),
                            class_name="flex items-center gap-1.5 text-xs font-semibold px-3.5 py-1.5 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-700 transition-colors cursor-pointer",
                        ),
                        rx.el.button(
                            rx.icon("globe", size=13, class_name="text-indigo-600"),
                            rx.el.span("Compare US Ivies vs ALU Mauritius"),
                            on_click=AppState.send_quick_prompt(
                                "Compare full-need US universities like MIT/Stanford with African Leadership University (ALU) in Mauritius and Rwanda."
                            ),
                            class_name="flex items-center gap-1.5 text-xs font-semibold px-3.5 py-1.5 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-700 transition-colors cursor-pointer",
                        ),
                        rx.el.button(
                            rx.icon("pen-tool", size=13, class_name="text-purple-600"),
                            rx.el.span("Personal Statement Strategy"),
                            on_click=AppState.send_quick_prompt(
                                "How should I structure my Personal Statement to highlight my leadership and secure financial aid?"
                            ),
                            class_name="flex items-center gap-1.5 text-xs font-semibold px-3.5 py-1.5 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-700 transition-colors cursor-pointer",
                        ),
                        class_name="px-5 py-2.5 flex flex-wrap gap-2 border-t border-slate-100 bg-white",
                    ),
                    # Chat input bar
                    rx.el.div(
                        rx.debounce_input(
                            rx.el.input(
                                value=AppState.chat_input,
                                on_change=AppState.set_chat_input,
                                on_key_down=AppState.handle_chat_key_down,
                                placeholder="Ask about universities, acceptance rates, scholarships, or essay strategy (Press Enter to send)...",
                                class_name="w-full px-5 py-3 rounded-full border border-slate-300 text-sm focus:outline-none focus:ring-2 focus:ring-slate-900/10 focus:border-slate-900 transition-all",
                            ),
                            debounce_timeout=150,
                        ),
                        rx.el.button(
                            rx.icon("send", size=16),
                            rx.el.span("Ask AI"),
                            on_click=AppState.send_chat_message,
                            class_name="flex items-center gap-1.5 px-5 py-3 rounded-full bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold transition-colors cursor-pointer shrink-0",
                        ),
                        class_name="p-4 bg-white border-t border-slate-200 flex items-center gap-2",
                    ),
                    class_name="lg:col-span-5 bg-slate-50/50 rounded-3xl border border-slate-200 flex flex-col overflow-hidden shadow-xs",
                ),
                # Right Column: Curated University Match Deck
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.h2(
                                "University Match Deck",
                                class_name="text-xl font-bold text-slate-900",
                            ),
                            rx.el.p(
                                "Personalized to your GPA, major, and financial aid profile. Save your favorites or apply in 1 click.",
                                class_name="text-xs text-slate-500 mt-0.5",
                            ),
                        ),
                        rx.cond(
                            AppState.discarded_university_names.length() > 0,
                            rx.el.button(
                                "Restore Dismissed",
                                on_click=AppState.reset_discarded_universities,
                                class_name="text-xs font-semibold text-slate-600 hover:text-slate-900 underline cursor-pointer",
                            ),
                        ),
                        class_name="flex items-center justify-between mb-4",
                    ),
                    rx.el.div(
                        rx.foreach(
                            AppState.visible_recommended_universities,
                            university_match_card,
                        ),
                        class_name="grid grid-cols-1 md:grid-cols-2 gap-4 overflow-y-auto max-h-[75vh] pr-1",
                    ),
                    class_name="lg:col-span-7 flex flex-col",
                ),
                class_name="max-w-7xl mx-auto px-4 sm:px-6 py-6 grid grid-cols-1 lg:grid-cols-12 gap-6",
            ),
        ),
        class_name="min-h-screen bg-slate-50/40 text-slate-900 font-sans",
    )
