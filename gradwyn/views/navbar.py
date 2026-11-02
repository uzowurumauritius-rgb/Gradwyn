"""Shared Top Navigation Bar & Instant Role Switcher for Gradwyn."""

from __future__ import annotations

import reflex as rx

from ..state import AppState


def brand_logo() -> rx.Component:
    """Gradwyn editorial logo with graduation cap badge."""
    return rx.el.a(
        rx.el.div(
            rx.icon("graduation-cap", size=20, class_name="text-white"),
            class_name="w-9 h-9 rounded-xl bg-slate-900 flex items-center justify-center shadow-sm",
        ),
        rx.el.span(
            "Gradwyn",
            class_name="text-xl font-bold tracking-tight text-slate-900",
        ),
        rx.el.span(
            "BETA",
            class_name="text-[10px] font-bold uppercase tracking-widest px-2 py-0.5 rounded-full bg-slate-100 text-slate-600 border border-slate-200",
        ),
        href="/",
        class_name="flex items-center gap-2.5 hover:opacity-90 transition-opacity",
    )


def yc_demo_switcher_bar() -> rx.Component:
    """Refined top banner allowing 1-click switching across the 4 ecosystem portals."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    "YC EVALUATOR QUICK SWITCH",
                    class_name="text-[10px] font-bold tracking-widest uppercase px-2.5 py-0.5 rounded-full bg-emerald-500/15 text-emerald-300 border border-emerald-500/30",
                ),
                rx.el.span(
                    "Test 3-sided marketplace:",
                    class_name="text-xs text-slate-300 font-medium hidden md:inline",
                ),
                class_name="flex items-center gap-2",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("sparkles", size=13, class_name="text-emerald-400"),
                    rx.el.span("AI Advisor"),
                    on_click=AppState.login_demo_student_advisor,
                    class_name="flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-white/10 hover:bg-white/20 text-white transition-all cursor-pointer",
                ),
                rx.el.button(
                    rx.icon("layout-dashboard", size=13),
                    rx.el.span("Student Hub"),
                    on_click=AppState.login_demo_student,
                    class_name="flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-white/10 hover:bg-white/20 text-white transition-all cursor-pointer",
                ),
                rx.el.button(
                    rx.icon("users", size=13),
                    rx.el.span("Mentor Portal"),
                    on_click=AppState.login_demo_mentor,
                    class_name="flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-white/10 hover:bg-white/20 text-white transition-all cursor-pointer",
                ),
                rx.el.button(
                    rx.icon("building-2", size=13),
                    rx.el.span("University Admissions"),
                    on_click=AppState.login_demo_university,
                    class_name="flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-white/10 hover:bg-white/20 text-white transition-all cursor-pointer",
                ),
                class_name="flex items-center gap-1.5 flex-wrap",
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 py-2 flex flex-wrap items-center justify-between gap-2",
        ),
        class_name="w-full bg-slate-950 text-white border-b border-slate-800 z-50",
    )


def onboarding_navbar() -> rx.Component:
    """Minimal, focused, distraction-free header for the onboarding wizard."""
    return rx.el.header(
        rx.el.div(
            brand_logo(),
            rx.el.div(
                rx.el.span(
                    "STUDENT ONBOARDING",
                    class_name="hidden sm:inline-block text-[11px] font-bold tracking-widest uppercase text-slate-500 bg-slate-100 px-3 py-1 rounded-full border border-slate-200",
                ),
                rx.el.button(
                    rx.icon("sparkles", size=13, class_name="text-slate-900"),
                    rx.el.span("Quick Fill Demo Profile"),
                    on_click=AppState.login_demo_student_advisor,
                    title="Load sample profile and see AI recommendations immediately",
                    class_name="flex items-center gap-1.5 px-3.5 py-1.5 rounded-full text-xs font-semibold bg-slate-100 hover:bg-slate-200 text-slate-800 transition-colors cursor-pointer",
                ),
                rx.el.a(
                    "Exit",
                    href="/",
                    class_name="text-xs font-semibold text-slate-500 hover:text-slate-900 transition-colors px-2 py-1",
                ),
                class_name="flex items-center gap-3",
            ),
            class_name="max-w-5xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between",
        ),
        class_name="w-full bg-white/95 backdrop-blur-md border-b border-slate-200/80 sticky top-0 z-40",
    )


def public_navbar() -> rx.Component:
    """Clean editorial navbar for Landing, Auth, and Onboarding pages."""
    return rx.el.header(
        yc_demo_switcher_bar(),
        rx.el.div(
            rx.el.div(
                brand_logo(),
                rx.el.nav(
                    rx.el.a(
                        "How It Works",
                        href="/#how-it-works",
                        class_name="text-sm font-medium text-slate-600 hover:text-slate-900 transition-colors",
                    ),
                    rx.el.a(
                        "Ecosystem",
                        href="/#ecosystem",
                        class_name="text-sm font-medium text-slate-600 hover:text-slate-900 transition-colors",
                    ),
                    rx.el.button(
                        "AI Advisor",
                        on_click=AppState.login_demo_student_advisor,
                        class_name="text-sm font-medium text-slate-600 hover:text-slate-900 transition-colors cursor-pointer",
                    ),
                    rx.el.button(
                        "Feedback",
                        on_click=AppState.open_feedback_modal,
                        class_name="text-sm font-medium text-slate-600 hover:text-slate-900 transition-colors cursor-pointer",
                    ),
                    class_name="hidden md:flex items-center gap-7",
                ),
                rx.el.div(
                    rx.el.a(
                        "Sign In",
                        href="/login",
                        class_name="text-sm font-semibold text-slate-700 hover:text-slate-900 px-4 py-2 rounded-full transition-colors",
                    ),
                    rx.el.a(
                        rx.el.span("Get Started"),
                        rx.icon("arrow-right", size=15),
                        href="/onboarding",
                        class_name="flex items-center gap-1.5 bg-slate-900 hover:bg-slate-800 text-white text-sm font-semibold px-5 py-2.5 rounded-full shadow-sm transition-all",
                    ),
                    class_name="flex items-center gap-2",
                ),
                class_name="max-w-7xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between",
            ),
            class_name="w-full bg-white/90 backdrop-blur-md border-b border-slate-200/80",
        ),
        class_name="sticky top-0 z-40 w-full",
    )
