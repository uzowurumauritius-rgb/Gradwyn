"""Mentor Onboarding (`/mentor-onboarding`) & Mentor Portal (`/mentor-dashboard`)."""

from __future__ import annotations

import reflex as rx

from ..state import AppState
from .modals import global_modals
from .navbar import brand_logo, yc_demo_switcher_bar


def mentor_onboarding_page() -> rx.Component:
    """4-Step Mentor Onboarding Wizard (`/mentor-onboarding`)."""
    return rx.el.div(
        yc_demo_switcher_bar(),
        global_modals(),
        rx.el.header(
            rx.el.div(
                brand_logo(),
                rx.el.a(
                    "Skip to Mentor Portal →",
                    href="/mentor-dashboard",
                    class_name="text-xs font-bold text-slate-700 hover:text-slate-900 underline",
                ),
                class_name="max-w-5xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between",
            ),
            class_name="bg-white border-b border-slate-200",
        ),
        rx.el.main(
            rx.el.div(
                rx.el.span(
                    f"MENTOR ONBOARDING · STEP {AppState.mentor_onboarding_step} OF 4",
                    class_name="text-xs font-bold uppercase tracking-widest text-slate-500",
                ),
                rx.el.h1(
                    "Join the Gradwyn Verified Mentor Network",
                    class_name="text-2xl sm:text-3xl font-bold text-slate-900 mt-1 mb-6",
                ),
                rx.el.div(
                    rx.cond(
                        AppState.mentor_onboarding_step == 1,
                        rx.el.div(
                            rx.el.label("Full Name & Title", class_name="block text-xs font-bold uppercase text-slate-500 mb-1.5"),
                            rx.el.input(
                                name="mentor_name",
                                default_value=AppState.mentor_name,
                                on_blur=AppState.set_mentor_name,
                                placeholder="e.g., Dr. Sarah Jenkins",
                                class_name="w-full px-4 py-3 rounded-2xl border border-slate-300 text-sm mb-4 focus:outline-none focus:ring-2 focus:ring-slate-900/10 focus:border-slate-900 transition-all",
                            ),
                            rx.el.label("University Affiliation", class_name="block text-xs font-bold uppercase text-slate-500 mb-1.5"),
                            rx.el.input(
                                name="mentor_university",
                                default_value=AppState.mentor_university,
                                on_blur=AppState.set_mentor_university,
                                placeholder="e.g., Stanford University",
                                class_name="w-full px-4 py-3 rounded-2xl border border-slate-300 text-sm focus:outline-none focus:ring-2 focus:ring-slate-900/10 focus:border-slate-900 transition-all",
                            ),
                        ),
                    ),
                    rx.cond(
                        AppState.mentor_onboarding_step == 2,
                        rx.el.div(
                            rx.el.label("Current Role / Fellowship", class_name="block text-xs font-bold uppercase text-slate-500 mb-1.5"),
                            rx.el.input(
                                name="mentor_role",
                                default_value=AppState.mentor_role,
                                on_blur=AppState.set_mentor_role,
                                placeholder="e.g., PhD Candidate & Admissions Fellow",
                                class_name="w-full px-4 py-3 rounded-2xl border border-slate-300 text-sm mb-4 focus:outline-none focus:ring-2 focus:ring-slate-900/10 focus:border-slate-900 transition-all",
                            ),
                            rx.el.label("City & Country", class_name="block text-xs font-bold uppercase text-slate-500 mb-1.5"),
                            rx.el.input(
                                name="mentor_location",
                                default_value=AppState.mentor_location,
                                on_blur=AppState.set_mentor_location,
                                placeholder="e.g., Stanford, USA",
                                class_name="w-full px-4 py-3 rounded-2xl border border-slate-300 text-sm focus:outline-none focus:ring-2 focus:ring-slate-900/10 focus:border-slate-900 transition-all",
                            ),
                        ),
                    ),
                    rx.cond(
                        AppState.mentor_onboarding_step == 3,
                        rx.el.div(
                            rx.el.label("Mentoring Bio", class_name="block text-xs font-bold uppercase text-slate-500 mb-1.5"),
                            rx.el.textarea(
                                name="mentor_bio",
                                default_value=AppState.mentor_bio,
                                on_blur=AppState.set_mentor_bio,
                                rows=4,
                                placeholder="Describe your research, mentorship background, and what students you help...",
                                class_name="w-full p-4 rounded-2xl border border-slate-300 text-sm mb-4 focus:outline-none focus:ring-2 focus:ring-slate-900/10 focus:border-slate-900 transition-all",
                            ),
                            rx.el.label("Specialties", class_name="block text-xs font-bold uppercase text-slate-500 mb-1.5"),
                            rx.el.div(
                                rx.foreach(
                                    AppState.mentor_specialties,
                                    lambda sp: rx.el.button(
                                        f"{sp} ×",
                                        type="button",
                                        on_click=AppState.remove_mentor_specialty(sp),
                                        class_name="px-3 py-1 rounded-full text-xs font-bold bg-slate-900 text-white cursor-pointer",
                                    ),
                                ),
                                class_name="flex flex-wrap gap-2 mb-3",
                            ),
                            rx.el.div(
                                rx.el.input(
                                    name="mentor_custom_specialty",
                                    on_blur=AppState.set_mentor_custom_specialty,
                                    placeholder="Add specialty (e.g., Rhodes Prep, STEM PhDs)...",
                                    class_name="w-full px-4 py-2 rounded-xl border border-slate-300 text-sm focus:outline-none focus:ring-2 focus:ring-slate-900/10 focus:border-slate-900 transition-all",
                                ),
                                rx.el.button(
                                    "Add",
                                    type="button",
                                    on_click=AppState.add_mentor_specialty,
                                    class_name="px-4 py-2 rounded-xl bg-slate-900 text-white text-xs font-bold cursor-pointer shrink-0",
                                ),
                                class_name="flex items-center gap-2",
                            ),
                        ),
                    ),
                    rx.cond(
                        AppState.mentor_onboarding_step == 4,
                        rx.el.div(
                            rx.el.label("LinkedIn / Booking Link", class_name="block text-xs font-bold uppercase text-slate-500 mb-1.5"),
                            rx.el.input(
                                name="mentor_linkedin",
                                default_value=AppState.mentor_linkedin,
                                on_blur=AppState.set_mentor_linkedin,
                                placeholder="https://linkedin.com/in/username or calendly link",
                                class_name="w-full px-4 py-3 rounded-2xl border border-slate-300 text-sm mb-4 focus:outline-none focus:ring-2 focus:ring-slate-900/10 focus:border-slate-900 transition-all",
                            ),
                            rx.el.p(
                                "Clicking 'Publish Mentor Profile' will make your card immediately visible to students in the Mentorship Network.",
                                class_name="text-xs text-slate-500",
                            ),
                        ),
                    ),
                    rx.el.div(
                        rx.cond(
                            AppState.mentor_onboarding_step > 1,
                            rx.el.button(
                                "← Back",
                                on_click=AppState.prev_mentor_step,
                                class_name="px-5 py-2.5 rounded-full text-sm font-semibold text-slate-600 hover:bg-slate-100 cursor-pointer",
                            ),
                            rx.el.div(),
                        ),
                        rx.el.button(
                            rx.cond(
                                AppState.mentor_onboarding_step < 4,
                                "Continue →",
                                "Publish Mentor Profile →",
                            ),
                            on_click=AppState.next_mentor_step,
                            class_name="px-6 py-2.5 rounded-full bg-slate-900 text-white text-sm font-semibold hover:bg-slate-800 cursor-pointer",
                        ),
                        class_name="flex items-center justify-between pt-6 mt-6 border-t border-slate-200",
                    ),
                    class_name="p-7 sm:p-9 rounded-3xl bg-white border border-slate-200 shadow-xs",
                ),
                class_name="max-w-xl mx-auto py-12 px-4 sm:px-6",
            ),
        ),
        class_name="min-h-screen bg-slate-50/50 text-slate-900 font-sans",
    )


def mentor_dashboard_page() -> rx.Component:
    """Verified Alumni Mentor Portal (`/mentor-dashboard`)."""
    return rx.el.div(
        yc_demo_switcher_bar(),
        global_modals(),
        rx.el.header(
            rx.el.div(
                brand_logo(),
                rx.el.div(
                    rx.el.button(
                        "View Live in Student Hub →",
                        on_click=[AppState.set_dashboard_tab("mentors"), AppState.login_demo_student],
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
                # Top Mentor Banner
                rx.el.div(
                    rx.el.div(
                        rx.el.span(
                            "VERIFIED ALUMNI MENTOR PORTAL",
                            class_name="text-[11px] font-bold uppercase tracking-widest text-slate-400",
                        ),
                        rx.el.h1(
                            AppState.mentor_name,
                            class_name="text-2xl sm:text-3xl font-bold text-white mt-1",
                        ),
                        rx.el.p(
                            f"{AppState.mentor_role} · {AppState.mentor_university}",
                            class_name="text-xs sm:text-sm text-slate-300 mt-0.5",
                        ),
                    ),
                    rx.el.button(
                        rx.cond(
                            AppState.mentor_available,
                            "● Status: Available for Mentoring (Click to Pause)",
                            "○ Status: Paused / Booked (Click to Open)",
                        ),
                        on_click=AppState.toggle_mentor_availability,
                        class_name=rx.cond(
                            AppState.mentor_available,
                            "px-5 py-2.5 rounded-full text-xs font-bold bg-emerald-500 text-white shadow-xs cursor-pointer",
                            "px-5 py-2.5 rounded-full text-xs font-bold bg-white/15 text-slate-200 cursor-pointer",
                        ),
                    ),
                    class_name="p-6 sm:p-8 rounded-3xl bg-slate-900 text-white flex flex-wrap items-center justify-between gap-4 mb-8",
                ),
                # 2-Column Layout: Profile Editor + Live Card Preview
                rx.el.div(
                    # Left: Editor
                    rx.el.div(
                        rx.el.h2("Edit Public Mentor Listing", class_name="text-xl font-bold text-slate-900 mb-4"),
                        rx.el.div(
                            rx.el.div(
                                rx.el.label("Full Name", class_name="block text-xs font-bold text-slate-600 mb-1"),
                                rx.el.input(
                                    name="mentor_name",
                                    default_value=AppState.mentor_name,
                                    on_blur=AppState.set_mentor_name,
                                    class_name="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-sm focus:outline-none focus:ring-2 focus:ring-slate-900/10 focus:border-slate-900 transition-all",
                                ),
                            ),
                            rx.el.div(
                                rx.el.label("University", class_name="block text-xs font-bold text-slate-600 mb-1"),
                                rx.el.input(
                                    name="mentor_university",
                                    default_value=AppState.mentor_university,
                                    on_blur=AppState.set_mentor_university,
                                    class_name="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-sm focus:outline-none focus:ring-2 focus:ring-slate-900/10 focus:border-slate-900 transition-all",
                                ),
                            ),
                            rx.el.div(
                                rx.el.label("Academic Role / Fellowship", class_name="block text-xs font-bold text-slate-600 mb-1"),
                                rx.el.input(
                                    name="mentor_role",
                                    default_value=AppState.mentor_role,
                                    on_blur=AppState.set_mentor_role,
                                    class_name="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-sm focus:outline-none focus:ring-2 focus:ring-slate-900/10 focus:border-slate-900 transition-all",
                                ),
                            ),
                            rx.el.div(
                                rx.el.label("Location", class_name="block text-xs font-bold text-slate-600 mb-1"),
                                rx.el.input(
                                    name="mentor_location",
                                    default_value=AppState.mentor_location,
                                    on_blur=AppState.set_mentor_location,
                                    class_name="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-sm focus:outline-none focus:ring-2 focus:ring-slate-900/10 focus:border-slate-900 transition-all",
                                ),
                            ),
                            rx.el.div(
                                rx.el.label("Mentoring Bio", class_name="block text-xs font-bold text-slate-600 mb-1"),
                                rx.el.textarea(
                                    name="mentor_bio",
                                    default_value=AppState.mentor_bio,
                                    on_blur=AppState.set_mentor_bio,
                                    rows=3,
                                    class_name="w-full p-3.5 rounded-xl border border-slate-300 text-sm focus:outline-none focus:ring-2 focus:ring-slate-900/10 focus:border-slate-900 transition-all",
                                ),
                                class_name="sm:col-span-2",
                            ),
                            rx.el.div(
                                rx.el.label("LinkedIn / Calendly Booking URL", class_name="block text-xs font-bold text-slate-600 mb-1"),
                                rx.el.input(
                                    name="mentor_linkedin",
                                    default_value=AppState.mentor_linkedin,
                                    on_blur=AppState.set_mentor_linkedin,
                                    class_name="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 text-sm focus:outline-none focus:ring-2 focus:ring-slate-900/10 focus:border-slate-900 transition-all",
                                ),
                                class_name="sm:col-span-2",
                            ),
                            class_name="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-5",
                        ),
                        rx.el.button(
                            "Save & Sync to Student Mentorship Hub",
                            on_click=AppState.save_mentor_profile,
                            class_name="px-6 py-3 rounded-full bg-slate-900 hover:bg-slate-800 text-white text-xs font-bold shadow-xs cursor-pointer",
                        ),
                        class_name="p-6 sm:p-8 rounded-3xl bg-white border border-slate-200",
                    ),
                    # Right: Live Preview Card
                    rx.el.div(
                        rx.el.h2("Live Student View Preview", class_name="text-xl font-bold text-slate-900 mb-4"),
                        rx.el.div(
                            rx.el.div(
                                rx.el.div(
                                    rx.el.img(
                                        src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=400&q=80",
                                        alt=AppState.mentor_name,
                                        class_name="w-14 h-14 rounded-2xl object-cover border border-slate-200",
                                    ),
                                    rx.el.div(
                                        rx.el.h3(AppState.mentor_name, class_name="text-base font-bold text-slate-900"),
                                        rx.el.p(AppState.mentor_role, class_name="text-xs font-semibold text-slate-600"),
                                        rx.el.p(
                                            f"{AppState.mentor_university} · {AppState.mentor_location}",
                                            class_name="text-xs text-slate-400",
                                        ),
                                    ),
                                    class_name="flex items-center gap-3.5",
                                ),
                                rx.el.span(
                                    rx.cond(AppState.mentor_available, "Available", "Booked"),
                                    class_name=rx.cond(
                                        AppState.mentor_available,
                                        "text-[11px] font-bold px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200",
                                        "text-[11px] font-bold px-2.5 py-1 rounded-full bg-slate-100 text-slate-500",
                                    ),
                                ),
                                class_name="flex items-start justify-between mb-3",
                            ),
                            rx.el.p(AppState.mentor_bio, class_name="text-xs text-slate-600 leading-relaxed mb-4"),
                            rx.el.div(
                                rx.foreach(
                                    AppState.mentor_specialties,
                                    lambda sp: rx.el.span(
                                        sp,
                                        class_name="text-[11px] font-semibold px-2.5 py-1 rounded-full bg-slate-100 text-slate-700",
                                    ),
                                ),
                                class_name="flex flex-wrap gap-1.5 mb-4",
                            ),
                            rx.el.a(
                                "Connect & Request Session",
                                href=AppState.mentor_linkedin,
                                target="_blank",
                                class_name="block w-full text-center py-2.5 rounded-full bg-slate-900 text-white text-xs font-bold",
                            ),
                            class_name="p-6 rounded-3xl bg-white border border-slate-200 shadow-sm",
                        ),
                        class_name="flex flex-col",
                    ),
                    class_name="grid grid-cols-1 lg:grid-cols-2 gap-8",
                ),
                class_name="max-w-7xl mx-auto px-4 sm:px-6 py-8",
            ),
        ),
        class_name="min-h-screen bg-slate-50/50 text-slate-900 font-sans",
    )
