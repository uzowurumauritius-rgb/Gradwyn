"""Authentication Page (`/login`) with Multi-Role Sign In/Up & 1-Click YC Demo Access."""

from __future__ import annotations

import reflex as rx

from ..state import AppState
from .modals import global_modals
from .navbar import public_navbar


def auth_page() -> rx.Component:
    """Clean editorial login & registration page."""
    return rx.el.div(
        public_navbar(),
        global_modals(),
        rx.el.main(
            rx.el.div(
                # Left card: Standard Sign In / Sign Up
                rx.el.div(
                    rx.el.div(
                        rx.el.h1(
                            rx.cond(
                                AppState.auth_mode == "login",
                                "Welcome back to Gradwyn",
                                "Create your Gradwyn account",
                            ),
                            class_name="text-2xl sm:text-3xl font-bold text-slate-900",
                        ),
                        rx.el.p(
                            "Select your portal role below to sign in or register.",
                            class_name="text-sm text-slate-500 mt-1",
                        ),
                        class_name="mb-6",
                    ),
                    # Role Selector Tabs (Student / Mentor / University)
                    rx.el.div(
                        rx.el.button(
                            rx.icon("graduation-cap", size=15),
                            rx.el.span("Student"),
                            on_click=AppState.set_auth_role_tab("student"),
                            class_name=rx.cond(
                                AppState.auth_role_tab == "student",
                                "flex-1 flex items-center justify-center gap-1.5 py-2.5 rounded-full text-xs font-bold bg-slate-900 text-white shadow-xs cursor-pointer",
                                "flex-1 flex items-center justify-center gap-1.5 py-2.5 rounded-full text-xs font-semibold text-slate-600 hover:text-slate-900 cursor-pointer",
                            ),
                        ),
                        rx.el.button(
                            rx.icon("users", size=15),
                            rx.el.span("Mentor"),
                            on_click=AppState.set_auth_role_tab("mentor"),
                            class_name=rx.cond(
                                AppState.auth_role_tab == "mentor",
                                "flex-1 flex items-center justify-center gap-1.5 py-2.5 rounded-full text-xs font-bold bg-slate-900 text-white shadow-xs cursor-pointer",
                                "flex-1 flex items-center justify-center gap-1.5 py-2.5 rounded-full text-xs font-semibold text-slate-600 hover:text-slate-900 cursor-pointer",
                            ),
                        ),
                        rx.el.button(
                            rx.icon("building-2", size=15),
                            rx.el.span("University"),
                            on_click=AppState.set_auth_role_tab("university"),
                            class_name=rx.cond(
                                AppState.auth_role_tab == "university",
                                "flex-1 flex items-center justify-center gap-1.5 py-2.5 rounded-full text-xs font-bold bg-slate-900 text-white shadow-xs cursor-pointer",
                                "flex-1 flex items-center justify-center gap-1.5 py-2.5 rounded-full text-xs font-semibold text-slate-600 hover:text-slate-900 cursor-pointer",
                            ),
                        ),
                        class_name="flex items-center p-1 rounded-full bg-slate-100 border border-slate-200 mb-6",
                    ),
                    # Error alert if any
                    rx.cond(
                        AppState.auth_error != "",
                        rx.el.div(
                            rx.icon("circle-alert", size=16, class_name="text-rose-600 shrink-0"),
                            rx.el.span(AppState.auth_error, class_name="text-xs font-medium text-rose-700"),
                            class_name="flex items-center gap-2 p-3 rounded-xl bg-rose-50 border border-rose-200 mb-4",
                        ),
                    ),
                    # Form fields
                    rx.el.div(
                        rx.cond(
                            AppState.auth_mode == "signup",
                            rx.el.div(
                                rx.el.label(
                                    "Full Name",
                                    class_name="block text-xs font-bold uppercase tracking-wider text-slate-500 mb-1",
                                ),
                                rx.debounce_input(
                                    rx.el.input(
                                        value=AppState.auth_name_input,
                                        on_change=AppState.set_auth_name_input,
                                        on_key_down=AppState.handle_auth_key_down,
                                        placeholder="e.g., Amara Okafor",
                                        class_name="w-full px-4 py-2.5 rounded-xl border border-slate-300 text-sm focus:outline-none focus:ring-2 focus:ring-slate-900/10 focus:border-slate-900 transition-all",
                                    ),
                                    debounce_timeout=150,
                                ),
                            ),
                        ),
                        rx.cond(
                            AppState.auth_role_tab == "university",
                            rx.el.div(
                                rx.el.label(
                                    "Partner Institution",
                                    class_name="block text-xs font-bold uppercase tracking-wider text-slate-500 mb-1",
                                ),
                                rx.debounce_input(
                                    rx.el.input(
                                        value=AppState.auth_university_input,
                                        on_change=AppState.set_auth_university_input,
                                        on_key_down=AppState.handle_auth_key_down,
                                        placeholder="e.g., African Leadership University (ALU)",
                                        class_name="w-full px-4 py-2.5 rounded-xl border border-slate-300 text-sm focus:outline-none focus:ring-2 focus:ring-slate-900/10 focus:border-slate-900 transition-all",
                                    ),
                                    debounce_timeout=150,
                                ),
                            ),
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Email Address",
                                class_name="block text-xs font-bold uppercase tracking-wider text-slate-500 mb-1",
                            ),
                            rx.debounce_input(
                                rx.el.input(
                                    type="email",
                                    value=AppState.auth_email_input,
                                    on_change=AppState.set_auth_email_input,
                                    on_key_down=AppState.handle_auth_key_down,
                                    placeholder="you@university.edu",
                                    class_name="w-full px-4 py-2.5 rounded-xl border border-slate-300 text-sm focus:outline-none focus:ring-2 focus:ring-slate-900/10 focus:border-slate-900 transition-all",
                                ),
                                debounce_timeout=150,
                            ),
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Password",
                                class_name="block text-xs font-bold uppercase tracking-wider text-slate-500 mb-1",
                            ),
                            rx.debounce_input(
                                rx.el.input(
                                    type="password",
                                    value=AppState.auth_password_input,
                                    on_change=AppState.set_auth_password_input,
                                    on_key_down=AppState.handle_auth_key_down,
                                    placeholder="••••••••",
                                    class_name="w-full px-4 py-2.5 rounded-xl border border-slate-300 text-sm focus:outline-none focus:ring-2 focus:ring-slate-900/10 focus:border-slate-900 transition-all",
                                ),
                                debounce_timeout=150,
                            ),
                        ),
                        rx.el.button(
                            rx.cond(
                                AppState.auth_mode == "login",
                                "Sign In to Portal →",
                                "Create Account & Continue →",
                            ),
                            on_click=AppState.handle_auth_submit,
                            class_name="w-full py-3 rounded-full bg-slate-900 hover:bg-slate-800 text-white text-sm font-semibold shadow-sm transition-colors cursor-pointer mt-2",
                        ),
                        class_name="space-y-4",
                    ),
                    # Toggle Sign In / Sign Up
                    rx.el.div(
                        rx.cond(
                            AppState.auth_mode == "login",
                            rx.el.p(
                                "New to Gradwyn? ",
                                rx.el.button(
                                    "Create a free account",
                                    on_click=AppState.set_auth_mode("signup"),
                                    class_name="font-bold text-slate-900 hover:underline cursor-pointer",
                                ),
                                class_name="text-xs text-slate-600 text-center",
                            ),
                            rx.el.p(
                                "Already have an account? ",
                                rx.el.button(
                                    "Sign in here",
                                    on_click=AppState.set_auth_mode("login"),
                                    class_name="font-bold text-slate-900 hover:underline cursor-pointer",
                                ),
                                class_name="text-xs text-slate-600 text-center",
                            ),
                        ),
                        class_name="mt-6 pt-5 border-t border-slate-200",
                    ),
                    class_name="bg-white rounded-3xl p-7 sm:p-8 border border-slate-200 shadow-sm",
                ),
                # Right card: 1-Click Instant Demo Access for YC Reviewers
                rx.el.div(
                    rx.el.span(
                        "INSTANT DEMO SANDBOX",
                        class_name="text-[11px] font-bold uppercase tracking-widest px-3 py-1 rounded-full bg-emerald-50 text-emerald-800 border border-emerald-200",
                    ),
                    rx.el.h2(
                        "Explore every portal in 1 click.",
                        class_name="text-2xl font-bold text-slate-900 mt-3",
                    ),
                    rx.el.p(
                        "Pre-loaded with a realistic student profile, AI university recommendations, 14 global scholarships, alumni mentors, and live admissions applications.",
                        class_name="text-sm text-slate-600 leading-relaxed mt-2 mb-6",
                    ),
                    rx.el.div(
                        rx.el.button(
                            rx.el.div(
                                rx.icon("sparkles", size=18, class_name="text-slate-900"),
                                rx.el.div(
                                    rx.el.p("Launch AI Admissions Advisor & Match Deck", class_name="text-sm font-bold text-slate-900 text-left"),
                                    rx.el.p("Split-screen Gemini 3.8 chat + interactive university cards", class_name="text-xs text-slate-500 text-left"),
                                ),
                                class_name="flex items-center gap-3",
                            ),
                            rx.icon("arrow-right", size=16, class_name="text-slate-400"),
                            on_click=AppState.login_demo_student_advisor,
                            class_name="w-full flex items-center justify-between p-4 rounded-2xl bg-white hover:bg-slate-50 border border-slate-200 hover:border-slate-400 transition-all cursor-pointer",
                        ),
                        rx.el.button(
                            rx.el.div(
                                rx.icon("layout-dashboard", size=18, class_name="text-slate-900"),
                                rx.el.div(
                                    rx.el.p("Launch Student Hub (Amara Okafor)", class_name="text-sm font-bold text-slate-900 text-left"),
                                    rx.el.p("Overview, Scholarships, Mentors, AI Essay & Interview Prep", class_name="text-xs text-slate-500 text-left"),
                                ),
                                class_name="flex items-center gap-3",
                            ),
                            rx.icon("arrow-right", size=16, class_name="text-slate-400"),
                            on_click=AppState.login_demo_student,
                            class_name="w-full flex items-center justify-between p-4 rounded-2xl bg-white hover:bg-slate-50 border border-slate-200 hover:border-slate-400 transition-all cursor-pointer",
                        ),
                        rx.el.button(
                            rx.el.div(
                                rx.icon("users", size=18, class_name="text-slate-900"),
                                rx.el.div(
                                    rx.el.p("Launch Verified Mentor Portal (Dr. Sarah Jenkins)", class_name="text-sm font-bold text-slate-900 text-left"),
                                    rx.el.p("Manage mentor availability & specialties synced to students", class_name="text-xs text-slate-500 text-left"),
                                ),
                                class_name="flex items-center gap-3",
                            ),
                            rx.icon("arrow-right", size=16, class_name="text-slate-400"),
                            on_click=AppState.login_demo_mentor,
                            class_name="w-full flex items-center justify-between p-4 rounded-2xl bg-white hover:bg-slate-50 border border-slate-200 hover:border-slate-400 transition-all cursor-pointer",
                        ),
                        rx.el.button(
                            rx.el.div(
                                rx.icon("building-2", size=18, class_name="text-slate-900"),
                                rx.el.div(
                                    rx.el.p("Launch Partner University Admissions Portal", class_name="text-sm font-bold text-slate-900 text-left"),
                                    rx.el.p("Review candidate dossiers, essays & issue admission decisions", class_name="text-xs text-slate-500 text-left"),
                                ),
                                class_name="flex items-center gap-3",
                            ),
                            rx.icon("arrow-right", size=16, class_name="text-slate-400"),
                            on_click=AppState.login_demo_university,
                            class_name="w-full flex items-center justify-between p-4 rounded-2xl bg-white hover:bg-slate-50 border border-slate-200 hover:border-slate-400 transition-all cursor-pointer",
                        ),
                        class_name="space-y-3",
                    ),
                    class_name="bg-slate-50 rounded-3xl p-7 sm:p-8 border border-slate-200 flex flex-col justify-center",
                ),
                class_name="max-w-5xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-8 items-stretch",
            ),
            class_name="py-12 sm:py-20 px-4 sm:px-6",
        ),
        class_name="min-h-screen bg-white text-slate-900 font-sans",
    )
