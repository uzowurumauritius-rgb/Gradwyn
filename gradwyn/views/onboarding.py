"""9-Step Student Onboarding Wizard (`/onboarding`) for Gradwyn."""

from __future__ import annotations

import reflex as rx

from ..state import AppState
from .modals import global_modals
from .navbar import public_navbar


def _step_0_name() -> rx.Component:
    return rx.el.div(
        rx.el.label(
            "Your Full Name",
            class_name="block text-xs font-bold uppercase tracking-wider text-slate-500 mb-2",
        ),
        rx.el.input(
            value=AppState.profile_name,
            on_change=AppState.set_profile_name,
            placeholder="e.g., Amara Okafor",
            class_name="w-full px-4 py-3.5 rounded-2xl border border-slate-300 text-base text-slate-900 focus:outline-none focus:border-slate-900",
        ),
    )


def _step_1_country() -> rx.Component:
    return rx.el.div(
        rx.el.label(
            "Country of Citizenship / Residence",
            class_name="block text-xs font-bold uppercase tracking-wider text-slate-500 mb-2",
        ),
        rx.el.input(
            value=AppState.profile_country,
            on_change=AppState.set_profile_country,
            placeholder="e.g., Nigeria, Mauritius, Kenya, India...",
            class_name="w-full px-4 py-3.5 rounded-2xl border border-slate-300 text-base text-slate-900 focus:outline-none focus:border-slate-900",
        ),
    )


def _step_2_education_level() -> rx.Component:
    return rx.el.div(
        rx.foreach(
            AppState.current_onboarding_options,
            lambda opt: rx.el.button(
                rx.el.span(opt, class_name="text-sm font-semibold"),
                rx.cond(
                    AppState.profile_education_level == opt,
                    rx.icon("circle-check", size=18),
                    rx.icon("circle", size=18, class_name="text-slate-300"),
                ),
                on_click=AppState.set_profile_education_level(opt),
                class_name=rx.cond(
                    AppState.profile_education_level == opt,
                    "w-full flex items-center justify-between p-4 rounded-2xl bg-slate-900 text-white font-semibold shadow-xs transition-all cursor-pointer",
                    "w-full flex items-center justify-between p-4 rounded-2xl bg-white hover:bg-slate-50 text-slate-800 border border-slate-200 transition-all cursor-pointer",
                ),
            ),
        ),
        class_name="grid grid-cols-1 sm:grid-cols-2 gap-3",
    )


def _step_3_target_degree() -> rx.Component:
    return rx.el.div(
        rx.foreach(
            AppState.current_onboarding_options,
            lambda opt: rx.el.button(
                rx.el.span(opt, class_name="text-sm font-semibold"),
                rx.cond(
                    AppState.profile_target_degree == opt,
                    rx.icon("circle-check", size=18),
                    rx.icon("circle", size=18, class_name="text-slate-300"),
                ),
                on_click=AppState.set_profile_target_degree(opt),
                class_name=rx.cond(
                    AppState.profile_target_degree == opt,
                    "w-full flex items-center justify-between p-4 rounded-2xl bg-slate-900 text-white font-semibold shadow-xs transition-all cursor-pointer",
                    "w-full flex items-center justify-between p-4 rounded-2xl bg-white hover:bg-slate-50 text-slate-800 border border-slate-200 transition-all cursor-pointer",
                ),
            ),
        ),
        class_name="grid grid-cols-1 sm:grid-cols-2 gap-3",
    )


def _step_4_academic_interests() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.foreach(
                AppState.current_onboarding_options,
                lambda opt: rx.el.button(
                    opt,
                    on_click=AppState.toggle_academic_interest(opt),
                    class_name=rx.cond(
                        AppState.profile_academic_interests.contains(opt),
                        "px-4 py-2.5 rounded-full text-xs font-bold bg-slate-900 text-white shadow-xs transition-all cursor-pointer",
                        "px-4 py-2.5 rounded-full text-xs font-semibold bg-slate-100 hover:bg-slate-200 text-slate-700 transition-all cursor-pointer",
                    ),
                ),
            ),
            class_name="flex flex-wrap gap-2.5 mb-5",
        ),
        rx.el.div(
            rx.el.input(
                value=AppState.custom_interest_input,
                on_change=AppState.set_custom_interest_input,
                placeholder="Add another major or interest (e.g., Robotics, Climate Tech)...",
                class_name="flex-1 px-4 py-2.5 rounded-xl border border-slate-300 text-sm focus:outline-none focus:border-slate-900",
            ),
            rx.el.button(
                "Add +",
                on_click=AppState.add_custom_interest,
                class_name="px-4 py-2.5 rounded-xl bg-slate-900 text-white text-xs font-bold hover:bg-slate-800 cursor-pointer",
            ),
            class_name="flex items-center gap-2",
        ),
    )


def _step_5_academics() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.label(
                "Current GPA / Academic Standing",
                class_name="block text-xs font-bold uppercase tracking-wider text-slate-500 mb-1.5",
            ),
            rx.el.input(
                value=AppState.profile_gpa,
                on_change=AppState.set_profile_gpa,
                placeholder="e.g., 3.9/4.0, A*AA, IB 40/45, or First Class",
                class_name="w-full px-4 py-3 rounded-2xl border border-slate-300 text-sm focus:outline-none focus:border-slate-900",
            ),
        ),
        rx.el.div(
            rx.el.label(
                "Standardized Test Scores (Optional)",
                class_name="block text-xs font-bold uppercase tracking-wider text-slate-500 mb-1.5",
            ),
            rx.el.input(
                value=AppState.profile_test_scores,
                on_change=AppState.set_profile_test_scores,
                placeholder="e.g., SAT 1510, GRE 328, IELTS 8.0, or Test-Optional",
                class_name="w-full px-4 py-3 rounded-2xl border border-slate-300 text-sm focus:outline-none focus:border-slate-900",
            ),
        ),
        class_name="space-y-4",
    )


def _step_6_locations() -> rx.Component:
    return rx.el.div(
        rx.foreach(
            AppState.current_onboarding_options,
            lambda loc: rx.el.button(
                rx.el.span(loc, class_name="text-sm font-semibold"),
                rx.cond(
                    AppState.profile_preferred_locations.contains(loc),
                    rx.icon("check", size=18),
                    rx.icon("plus", size=18, class_name="text-slate-400"),
                ),
                on_click=AppState.toggle_preferred_location(loc),
                class_name=rx.cond(
                    AppState.profile_preferred_locations.contains(loc),
                    "w-full flex items-center justify-between p-4 rounded-2xl bg-slate-900 text-white font-semibold shadow-xs transition-all cursor-pointer",
                    "w-full flex items-center justify-between p-4 rounded-2xl bg-white hover:bg-slate-50 text-slate-800 border border-slate-200 transition-all cursor-pointer",
                ),
            ),
        ),
        class_name="grid grid-cols-1 sm:grid-cols-2 gap-3",
    )


def _step_7_budget() -> rx.Component:
    return rx.el.div(
        rx.foreach(
            AppState.current_onboarding_options,
            lambda opt: rx.el.button(
                rx.el.span(opt, class_name="text-sm font-semibold"),
                rx.cond(
                    AppState.profile_budget == opt,
                    rx.icon("circle-check", size=18),
                    rx.icon("circle", size=18, class_name="text-slate-300"),
                ),
                on_click=AppState.set_profile_budget(opt),
                class_name=rx.cond(
                    AppState.profile_budget == opt,
                    "w-full flex items-center justify-between p-4 rounded-2xl bg-slate-900 text-white font-semibold shadow-xs transition-all cursor-pointer",
                    "w-full flex items-center justify-between p-4 rounded-2xl bg-white hover:bg-slate-50 text-slate-800 border border-slate-200 transition-all cursor-pointer",
                ),
            ),
        ),
        class_name="space-y-2.5",
    )


def _step_8_holistic() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.label(
                "Extracurriculars, Leadership & Awards",
                class_name="block text-xs font-bold uppercase tracking-wider text-slate-500 mb-1.5",
            ),
            rx.el.textarea(
                value=AppState.profile_extracurriculars,
                on_change=AppState.set_profile_extracurriculars,
                rows=3,
                placeholder="e.g., Founded school coding club, National Debate winner, community volunteering...",
                class_name="w-full p-4 rounded-2xl border border-slate-300 text-sm focus:outline-none focus:border-slate-900",
            ),
        ),
        rx.el.div(
            rx.el.label(
                "Long-Term Career Aspirations",
                class_name="block text-xs font-bold uppercase tracking-wider text-slate-500 mb-1.5",
            ),
            rx.el.textarea(
                value=AppState.profile_career_goals,
                on_change=AppState.set_profile_career_goals,
                rows=3,
                placeholder="e.g., Lead AI research and build financial/educational infrastructure in emerging markets...",
                class_name="w-full p-4 rounded-2xl border border-slate-300 text-sm focus:outline-none focus:border-slate-900",
            ),
        ),
        class_name="space-y-4",
    )


def onboarding_page() -> rx.Component:
    """9-Step Student Onboarding Wizard (`/onboarding`)."""
    return rx.el.div(
        public_navbar(),
        global_modals(),
        rx.el.main(
            rx.el.div(
                # Top progress header
                rx.el.div(
                    rx.el.div(
                        rx.el.span(
                            f"STEP {AppState.onboarding_step_number} OF {AppState.total_onboarding_steps}",
                            class_name="text-xs font-bold uppercase tracking-widest text-slate-500",
                        ),
                        rx.el.button(
                            "Skip to Instant AI Analysis →",
                            on_click=AppState.complete_student_onboarding,
                            class_name="text-xs font-bold text-slate-700 hover:text-slate-900 underline cursor-pointer",
                        ),
                        class_name="flex items-center justify-between mb-2",
                    ),
                    rx.el.div(
                        rx.el.div(
                            style={"width": f"{AppState.onboarding_progress_pct}%"},
                            class_name="h-2 rounded-full bg-slate-900 transition-all duration-300",
                        ),
                        class_name="w-full h-2 rounded-full bg-slate-200 overflow-hidden",
                    ),
                    class_name="mb-8",
                ),
                # Main card
                rx.el.div(
                    rx.el.h1(
                        AppState.current_onboarding_step_data["title"],
                        class_name="text-2xl sm:text-3xl font-bold text-slate-900",
                    ),
                    rx.el.p(
                        AppState.current_onboarding_step_data["subtitle"],
                        class_name="text-sm text-slate-600 mt-1.5 mb-6",
                    ),
                    # Dynamic step body
                    rx.cond(AppState.onboarding_step == 0, _step_0_name()),
                    rx.cond(AppState.onboarding_step == 1, _step_1_country()),
                    rx.cond(AppState.onboarding_step == 2, _step_2_education_level()),
                    rx.cond(AppState.onboarding_step == 3, _step_3_target_degree()),
                    rx.cond(AppState.onboarding_step == 4, _step_4_academic_interests()),
                    rx.cond(AppState.onboarding_step == 5, _step_5_academics()),
                    rx.cond(AppState.onboarding_step == 6, _step_6_locations()),
                    rx.cond(AppState.onboarding_step == 7, _step_7_budget()),
                    rx.cond(AppState.onboarding_step == 8, _step_8_holistic()),
                    # Footer controls
                    rx.el.div(
                        rx.cond(
                            AppState.onboarding_step > 0,
                            rx.el.button(
                                "← Previous",
                                on_click=AppState.prev_onboarding_step,
                                class_name="px-5 py-2.5 rounded-full text-sm font-semibold text-slate-600 hover:bg-slate-100 transition-colors cursor-pointer",
                            ),
                            rx.el.div(),
                        ),
                        rx.el.button(
                            rx.cond(
                                AppState.onboarding_step < 8,
                                "Continue →",
                                "✨ Complete & Launch AI Advisor",
                            ),
                            on_click=AppState.next_onboarding_step,
                            class_name="px-7 py-3 rounded-full bg-slate-900 hover:bg-slate-800 text-white text-sm font-semibold shadow-sm transition-all cursor-pointer",
                        ),
                        class_name="flex items-center justify-between pt-6 mt-8 border-t border-slate-200",
                    ),
                    class_name="bg-white rounded-3xl p-7 sm:p-10 border border-slate-200 shadow-sm",
                ),
                class_name="max-w-2xl mx-auto",
            ),
            class_name="py-10 sm:py-16 px-4 sm:px-6",
        ),
        class_name="min-h-screen bg-slate-50/60 text-slate-900 font-sans",
    )
