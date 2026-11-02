"""Interactive Modals for Gradwyn MVP.

Includes:
1. 4-Step University & Scholarship Application Wizard (`application_wizard_modal`)
2. Edit Student Profile + AI Re-Analysis Modal (`edit_profile_modal`)
3. Editorial Guide Reader Modal (`guide_reader_modal`)
4. Platform Feedback Modal (`feedback_modal`)
5. University Admissions Candidate Dossier Modal (`candidate_dossier_modal`)
"""

from __future__ import annotations

import reflex as rx

from ..state import AppState


def application_wizard_modal() -> rx.Component:
    """4-Step University & Scholarship Application Wizard."""
    return rx.cond(
        AppState.is_apply_modal_open,
        rx.el.div(
            rx.el.div(
                # Header
                rx.el.div(
                    rx.el.div(
                        rx.el.span(
                            AppState.apply_target_type,
                            class_name="text-[11px] font-bold uppercase tracking-widest px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-700 border border-slate-200",
                        ),
                        rx.el.h3(
                            AppState.apply_target_name,
                            class_name="text-xl font-bold text-slate-900 mt-1",
                        ),
                        rx.el.p(
                            f"Deadline: {AppState.apply_target_deadline} · Fee: {AppState.apply_target_fee}",
                            class_name="text-xs text-slate-500 mt-0.5",
                        ),
                    ),
                    rx.el.button(
                        rx.icon("x", size=18),
                        on_click=AppState.close_apply_modal,
                        class_name="p-2 rounded-full text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition-colors cursor-pointer",
                    ),
                    class_name="flex items-start justify-between pb-4 border-b border-slate-200",
                ),
                # Body: either Success state or 4-step form
                rx.cond(
                    AppState.apply_submitted_success,
                    rx.el.div(
                        rx.el.div(
                            rx.icon("circle-check-big", size=44, class_name="text-emerald-600"),
                            class_name="w-16 h-16 rounded-full bg-emerald-50 border border-emerald-200 flex items-center justify-center mx-auto mb-4",
                        ),
                        rx.el.h4(
                            "Application Submitted Successfully!",
                            class_name="text-2xl font-bold text-slate-900 text-center",
                        ),
                        rx.el.p(
                            "Your complete candidacy dossier has been transmitted to the admissions committee and added to your Candidacy Tracker.",
                            class_name="text-sm text-slate-600 text-center max-w-md mx-auto mt-2",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.span("Institution / Grant", class_name="text-xs text-slate-500"),
                                rx.el.span(AppState.apply_target_name, class_name="text-xs font-semibold text-slate-900"),
                                class_name="flex justify-between py-2 border-b border-slate-100",
                            ),
                            rx.el.div(
                                rx.el.span("Selected Track", class_name="text-xs text-slate-500"),
                                rx.el.span(AppState.apply_program, class_name="text-xs font-semibold text-slate-900"),
                                class_name="flex justify-between py-2 border-b border-slate-100",
                            ),
                            rx.el.div(
                                rx.el.span("Live Ecosystem Sync", class_name="text-xs text-slate-500"),
                                rx.el.span(
                                    "Visible in University Admissions Portal",
                                    class_name="text-xs font-semibold text-emerald-700",
                                ),
                                class_name="flex justify-between py-2",
                            ),
                            class_name="bg-slate-50 rounded-2xl p-4 border border-slate-200 mt-5 text-left",
                        ),
                        rx.el.div(
                            rx.el.button(
                                "Done & View Tracker",
                                on_click=AppState.close_apply_modal,
                                class_name="px-6 py-2.5 rounded-full bg-slate-900 text-white text-sm font-semibold hover:bg-slate-800 transition-colors cursor-pointer",
                            ),
                            rx.el.button(
                                "Inspect in University Portal →",
                                on_click=[AppState.close_apply_modal, AppState.login_demo_university],
                                class_name="px-5 py-2.5 rounded-full bg-slate-100 text-slate-800 text-sm font-semibold hover:bg-slate-200 transition-colors cursor-pointer",
                            ),
                            class_name="flex flex-wrap items-center justify-center gap-3 mt-6",
                        ),
                        class_name="py-6",
                    ),
                    rx.el.div(
                        # Step progress pills
                        rx.el.div(
                            rx.el.div(
                                rx.el.span("1. Profile & Track"),
                                class_name=rx.cond(
                                    AppState.apply_step >= 1,
                                    "text-xs font-semibold px-3 py-1 rounded-full bg-slate-900 text-white",
                                    "text-xs font-medium px-3 py-1 rounded-full bg-slate-100 text-slate-500",
                                ),
                            ),
                            rx.el.div(
                                rx.el.span("2. Personal Statement"),
                                class_name=rx.cond(
                                    AppState.apply_step >= 2,
                                    "text-xs font-semibold px-3 py-1 rounded-full bg-slate-900 text-white",
                                    "text-xs font-medium px-3 py-1 rounded-full bg-slate-100 text-slate-500",
                                ),
                            ),
                            rx.el.div(
                                rx.el.span("3. Documents"),
                                class_name=rx.cond(
                                    AppState.apply_step >= 3,
                                    "text-xs font-semibold px-3 py-1 rounded-full bg-slate-900 text-white",
                                    "text-xs font-medium px-3 py-1 rounded-full bg-slate-100 text-slate-500",
                                ),
                            ),
                            rx.el.div(
                                rx.el.span("4. Review & Submit"),
                                class_name=rx.cond(
                                    AppState.apply_step >= 4,
                                    "text-xs font-semibold px-3 py-1 rounded-full bg-slate-900 text-white",
                                    "text-xs font-medium px-3 py-1 rounded-full bg-slate-100 text-slate-500",
                                ),
                            ),
                            class_name="flex flex-wrap items-center gap-2 py-4",
                        ),
                        # Step 1: Academic Profile & Program
                        rx.cond(
                            AppState.apply_step == 1,
                            rx.el.div(
                                rx.el.label(
                                    "Intended Major / Fellowship Track",
                                    class_name="block text-xs font-bold uppercase tracking-wider text-slate-500 mb-1.5",
                                ),
                                rx.el.input(
                                    value=AppState.apply_program,
                                    on_change=AppState.set_apply_program,
                                    placeholder="e.g., BSc Computer Science & AI",
                                    class_name="w-full px-4 py-2.5 rounded-xl border border-slate-300 text-sm text-slate-900 focus:outline-none focus:border-slate-900 mb-4",
                                ),
                                rx.el.div(
                                    rx.el.div(
                                        rx.el.p("Applicant Name", class_name="text-xs text-slate-500"),
                                        rx.el.p(AppState.profile_name, class_name="text-sm font-semibold text-slate-900"),
                                        class_name="p-3 rounded-xl bg-slate-50 border border-slate-200",
                                    ),
                                    rx.el.div(
                                        rx.el.p("Country of Citizenship", class_name="text-xs text-slate-500"),
                                        rx.el.p(AppState.profile_country, class_name="text-sm font-semibold text-slate-900"),
                                        class_name="p-3 rounded-xl bg-slate-50 border border-slate-200",
                                    ),
                                    rx.el.div(
                                        rx.el.p("Verified GPA / Standing", class_name="text-xs text-slate-500"),
                                        rx.el.p(AppState.profile_gpa, class_name="text-sm font-semibold text-slate-900"),
                                        class_name="p-3 rounded-xl bg-slate-50 border border-slate-200",
                                    ),
                                    rx.el.div(
                                        rx.el.p("Test Scores", class_name="text-xs text-slate-500"),
                                        rx.el.p(AppState.profile_test_scores, class_name="text-sm font-semibold text-slate-900"),
                                        class_name="p-3 rounded-xl bg-slate-50 border border-slate-200",
                                    ),
                                    class_name="grid grid-cols-1 sm:grid-cols-2 gap-3",
                                ),
                                class_name="py-2",
                            ),
                        ),
                        # Step 2: Personal Statement + AI Polish
                        rx.cond(
                            AppState.apply_step == 2,
                            rx.el.div(
                                rx.el.div(
                                    rx.el.label(
                                        "Personal Statement / Motivation Essay",
                                        class_name="text-xs font-bold uppercase tracking-wider text-slate-500",
                                    ),
                                    rx.el.button(
                                        rx.icon("sparkles", size=14),
                                        rx.el.span("Enhance Opening with Gemini AI"),
                                        on_click=AppState.polish_apply_essay_with_ai,
                                        class_name="flex items-center gap-1.5 text-xs font-semibold px-3 py-1.5 rounded-full bg-slate-900 text-white hover:bg-slate-800 transition-colors cursor-pointer",
                                    ),
                                    class_name="flex items-center justify-between mb-2",
                                ),
                                rx.el.textarea(
                                    value=AppState.apply_essay,
                                    on_change=AppState.set_apply_essay,
                                    rows=6,
                                    class_name="w-full p-4 rounded-2xl border border-slate-300 text-sm text-slate-900 leading-relaxed focus:outline-none focus:border-slate-900",
                                ),
                                rx.el.p(
                                    "Tip: Gradwyn pre-fills your draft from your onboarding profile. Click 'Enhance Opening with Gemini AI' to craft a compelling hook.",
                                    class_name="text-xs text-slate-500 mt-2",
                                ),
                                class_name="py-2",
                            ),
                        ),
                        # Step 3: Supporting Documents
                        rx.cond(
                            AppState.apply_step == 3,
                            rx.el.div(
                                rx.el.p(
                                    "Select verified credentials from your Gradwyn Dossier Vault to attach:",
                                    class_name="text-sm text-slate-600 mb-3",
                                ),
                                rx.el.div(
                                    rx.el.button(
                                        rx.el.div(
                                            rx.icon("file-check", size=18, class_name="text-slate-900"),
                                            rx.el.div(
                                                rx.el.p("Official High School / University Transcripts.pdf", class_name="text-sm font-semibold text-slate-900 text-left"),
                                                rx.el.p("Verified GPA & Coursework Record", class_name="text-xs text-slate-500 text-left"),
                                            ),
                                            class_name="flex items-center gap-3",
                                        ),
                                        rx.el.span(
                                            rx.cond(AppState.apply_doc_transcript, "Attached ✓", "Attach"),
                                            class_name=rx.cond(
                                                AppState.apply_doc_transcript,
                                                "text-xs font-bold px-3 py-1 rounded-full bg-emerald-100 text-emerald-800",
                                                "text-xs font-medium px-3 py-1 rounded-full bg-slate-200 text-slate-700",
                                            ),
                                        ),
                                        on_click=AppState.toggle_apply_doc_transcript,
                                        class_name="w-full flex items-center justify-between p-3.5 rounded-2xl border border-slate-200 hover:border-slate-400 bg-white transition-all cursor-pointer",
                                    ),
                                    rx.el.button(
                                        rx.el.div(
                                            rx.icon("award", size=18, class_name="text-slate-900"),
                                            rx.el.div(
                                                rx.el.p("CV_Leadership_and_Impact_Portfolio.pdf", class_name="text-sm font-semibold text-slate-900 text-left"),
                                                rx.el.p("Extracurriculars, Honours & Community Leadership", class_name="text-xs text-slate-500 text-left"),
                                            ),
                                            class_name="flex items-center gap-3",
                                        ),
                                        rx.el.span(
                                            rx.cond(AppState.apply_doc_cv, "Attached ✓", "Attach"),
                                            class_name=rx.cond(
                                                AppState.apply_doc_cv,
                                                "text-xs font-bold px-3 py-1 rounded-full bg-emerald-100 text-emerald-800",
                                                "text-xs font-medium px-3 py-1 rounded-full bg-slate-200 text-slate-700",
                                            ),
                                        ),
                                        on_click=AppState.toggle_apply_doc_cv,
                                        class_name="w-full flex items-center justify-between p-3.5 rounded-2xl border border-slate-200 hover:border-slate-400 bg-white transition-all cursor-pointer",
                                    ),
                                    rx.el.button(
                                        rx.el.div(
                                            rx.icon("mail-check", size=18, class_name="text-slate-900"),
                                            rx.el.div(
                                                rx.el.p("2_Academic_Recommendation_Letters.pdf", class_name="text-sm font-semibold text-slate-900 text-left"),
                                                rx.el.p("FERPA-Waived Faculty Endorsements", class_name="text-xs text-slate-500 text-left"),
                                            ),
                                            class_name="flex items-center gap-3",
                                        ),
                                        rx.el.span(
                                            rx.cond(AppState.apply_doc_recommendation, "Attached ✓", "Attach"),
                                            class_name=rx.cond(
                                                AppState.apply_doc_recommendation,
                                                "text-xs font-bold px-3 py-1 rounded-full bg-emerald-100 text-emerald-800",
                                                "text-xs font-medium px-3 py-1 rounded-full bg-slate-200 text-slate-700",
                                            ),
                                        ),
                                        on_click=AppState.toggle_apply_doc_recommendation,
                                        class_name="w-full flex items-center justify-between p-3.5 rounded-2xl border border-slate-200 hover:border-slate-400 bg-white transition-all cursor-pointer",
                                    ),
                                    class_name="space-y-2.5",
                                ),
                                class_name="py-2",
                            ),
                        ),
                        # Step 4: Final Review
                        rx.cond(
                            AppState.apply_step == 4,
                            rx.el.div(
                                rx.el.div(
                                    rx.el.p("Target Institution / Grant", class_name="text-xs text-slate-500"),
                                    rx.el.p(AppState.apply_target_name, class_name="text-base font-bold text-slate-900"),
                                    rx.el.p(f"Track: {AppState.apply_program}", class_name="text-xs font-medium text-slate-600 mt-0.5"),
                                    rx.el.div(
                                        rx.el.p("Personal Statement Preview:", class_name="text-xs font-bold text-slate-500 uppercase mt-3 mb-1"),
                                        rx.el.p(AppState.apply_essay, class_name="text-xs text-slate-700 line-clamp-4 italic bg-white p-3 rounded-xl border border-slate-200"),
                                    ),
                                    class_name="p-4 rounded-2xl bg-slate-50 border border-slate-200",
                                ),
                                class_name="py-2",
                            ),
                        ),
                        # Footer Navigation
                        rx.el.div(
                            rx.cond(
                                AppState.apply_step > 1,
                                rx.el.button(
                                    "← Back",
                                    on_click=AppState.prev_apply_step,
                                    class_name="px-4 py-2 rounded-full text-sm font-medium text-slate-600 hover:bg-slate-100 transition-colors cursor-pointer",
                                ),
                                rx.el.div(),
                            ),
                            rx.cond(
                                AppState.apply_step < 4,
                                rx.el.button(
                                    "Continue →",
                                    on_click=AppState.next_apply_step,
                                    class_name="px-6 py-2.5 rounded-full bg-slate-900 text-white text-sm font-semibold hover:bg-slate-800 transition-colors cursor-pointer",
                                ),
                                rx.el.button(
                                    rx.icon("send", size=15),
                                    rx.el.span("Submit Official Application"),
                                    on_click=AppState.submit_application,
                                    class_name="flex items-center gap-2 px-6 py-2.5 rounded-full bg-emerald-600 hover:bg-emerald-700 text-white text-sm font-semibold shadow-sm transition-colors cursor-pointer",
                                ),
                            ),
                            class_name="flex items-center justify-between pt-4 mt-4 border-t border-slate-200",
                        ),
                    ),
                ),
                class_name="bg-white rounded-3xl max-w-xl w-full p-6 sm:p-8 shadow-2xl border border-slate-200 max-h-[90vh] overflow-y-auto",
            ),
            class_name="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4",
        ),
    )


def edit_profile_modal() -> rx.Component:
    """Modal allowing students to update their academic profile and trigger AI re-analysis."""
    return rx.cond(
        AppState.is_edit_profile_open,
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h3("Edit Academic Profile", class_name="text-xl font-bold text-slate-900"),
                        rx.el.p(
                            "Updating your profile automatically re-calibrates your AI university & scholarship matches.",
                            class_name="text-xs text-slate-500 mt-0.5",
                        ),
                    ),
                    rx.el.button(
                        rx.icon("x", size=18),
                        on_click=AppState.close_edit_profile_modal,
                        class_name="p-2 rounded-full text-slate-400 hover:text-slate-700 hover:bg-slate-100 cursor-pointer",
                    ),
                    class_name="flex items-start justify-between pb-4 border-b border-slate-200",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.label("Full Name", class_name="block text-xs font-bold text-slate-600 mb-1"),
                        rx.el.input(
                            value=AppState.profile_name,
                            on_change=AppState.set_profile_name,
                            class_name="w-full px-3.5 py-2 rounded-xl border border-slate-300 text-sm",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label("Country of Origin", class_name="block text-xs font-bold text-slate-600 mb-1"),
                        rx.el.input(
                            value=AppState.profile_country,
                            on_change=AppState.set_profile_country,
                            class_name="w-full px-3.5 py-2 rounded-xl border border-slate-300 text-sm",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label("GPA / Academic Standing", class_name="block text-xs font-bold text-slate-600 mb-1"),
                        rx.el.input(
                            value=AppState.profile_gpa,
                            on_change=AppState.set_profile_gpa,
                            class_name="w-full px-3.5 py-2 rounded-xl border border-slate-300 text-sm",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label("Standardized Test Scores", class_name="block text-xs font-bold text-slate-600 mb-1"),
                        rx.el.input(
                            value=AppState.profile_test_scores,
                            on_change=AppState.set_profile_test_scores,
                            class_name="w-full px-3.5 py-2 rounded-xl border border-slate-300 text-sm",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label("Annual Budget / Aid Requirement", class_name="block text-xs font-bold text-slate-600 mb-1"),
                        rx.el.input(
                            value=AppState.profile_budget,
                            on_change=AppState.set_profile_budget,
                            class_name="w-full px-3.5 py-2 rounded-xl border border-slate-300 text-sm",
                        ),
                        class_name="sm:col-span-2",
                    ),
                    rx.el.div(
                        rx.el.label("Extracurriculars & Leadership", class_name="block text-xs font-bold text-slate-600 mb-1"),
                        rx.el.textarea(
                            value=AppState.profile_extracurriculars,
                            on_change=AppState.set_profile_extracurriculars,
                            rows=3,
                            class_name="w-full p-3.5 rounded-xl border border-slate-300 text-sm",
                        ),
                        class_name="sm:col-span-2",
                    ),
                    rx.el.div(
                        rx.el.label("Career Aspirations", class_name="block text-xs font-bold text-slate-600 mb-1"),
                        rx.el.textarea(
                            value=AppState.profile_career_goals,
                            on_change=AppState.set_profile_career_goals,
                            rows=2,
                            class_name="w-full p-3.5 rounded-xl border border-slate-300 text-sm",
                        ),
                        class_name="sm:col-span-2",
                    ),
                    class_name="grid grid-cols-1 sm:grid-cols-2 gap-4 py-4",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancel",
                        on_click=AppState.close_edit_profile_modal,
                        class_name="px-4 py-2 rounded-full text-sm font-medium text-slate-600 hover:bg-slate-100 cursor-pointer",
                    ),
                    rx.el.button(
                        rx.icon("sparkles", size=15),
                        rx.el.span("Save & Re-Analyze with AI"),
                        on_click=AppState.save_edited_profile_and_reanalyze,
                        class_name="flex items-center gap-2 px-6 py-2.5 rounded-full bg-slate-900 text-white text-sm font-semibold hover:bg-slate-800 cursor-pointer",
                    ),
                    class_name="flex items-center justify-end gap-3 pt-4 border-t border-slate-200",
                ),
                class_name="bg-white rounded-3xl max-w-xl w-full p-6 sm:p-8 shadow-2xl border border-slate-200 max-h-[90vh] overflow-y-auto",
            ),
            class_name="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4",
        ),
    )


def guide_reader_modal() -> rx.Component:
    """Full editorial article reader modal for Admissions Guides."""
    return rx.cond(
        AppState.is_guide_modal_open,
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.span(
                            AppState.active_guide["category"],
                            class_name="text-xs font-bold uppercase tracking-widest px-3 py-1 rounded-full bg-slate-100 text-slate-800",
                        ),
                        rx.el.span(
                            AppState.active_guide["readTime"],
                            class_name="text-xs text-slate-500 ml-2",
                        ),
                    ),
                    rx.el.button(
                        rx.icon("x", size=18),
                        on_click=AppState.close_guide_reader,
                        class_name="p-2 rounded-full text-slate-400 hover:text-slate-700 hover:bg-slate-100 cursor-pointer",
                    ),
                    class_name="flex items-center justify-between pb-4 border-b border-slate-200",
                ),
                rx.el.h2(
                    AppState.active_guide["title"],
                    class_name="text-2xl sm:text-3xl font-bold text-slate-900 mt-4 leading-tight",
                ),
                rx.el.p(
                    f"By {AppState.active_guide['author']} — {AppState.active_guide['authorRole']}",
                    class_name="text-xs font-medium text-slate-500 mt-1 mb-5",
                ),
                rx.el.div(
                    rx.markdown(AppState.active_guide["content"]),
                    class_name="prose prose-slate max-w-none text-sm text-slate-700 leading-relaxed space-y-3",
                ),
                rx.el.div(
                    rx.el.button(
                        "Close Guide",
                        on_click=AppState.close_guide_reader,
                        class_name="px-6 py-2.5 rounded-full bg-slate-900 text-white text-sm font-semibold hover:bg-slate-800 cursor-pointer",
                    ),
                    class_name="flex justify-end pt-6 mt-6 border-t border-slate-200",
                ),
                class_name="bg-white rounded-3xl max-w-2xl w-full p-6 sm:p-8 shadow-2xl border border-slate-200 max-h-[88vh] overflow-y-auto",
            ),
            class_name="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4",
        ),
    )


def feedback_modal() -> rx.Component:
    """User feedback modal persisted to SQLModel."""
    return rx.cond(
        AppState.is_feedback_modal_open,
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h3("Share Product Feedback", class_name="text-lg font-bold text-slate-900"),
                    rx.el.button(
                        rx.icon("x", size=18),
                        on_click=AppState.close_feedback_modal,
                        class_name="p-1.5 rounded-full text-slate-400 hover:text-slate-700 hover:bg-slate-100 cursor-pointer",
                    ),
                    class_name="flex items-center justify-between pb-3 border-b border-slate-200",
                ),
                rx.cond(
                    AppState.feedback_submitted,
                    rx.el.div(
                        rx.icon("heart-handshake", size=36, class_name="text-emerald-600 mx-auto mb-2"),
                        rx.el.p("Thank you! Your feedback has been recorded.", class_name="text-base font-bold text-slate-900 text-center"),
                        rx.el.button(
                            "Close",
                            on_click=AppState.close_feedback_modal,
                            class_name="mt-4 px-5 py-2 rounded-full bg-slate-900 text-white text-xs font-semibold mx-auto block cursor-pointer",
                        ),
                        class_name="py-6 text-center",
                    ),
                    rx.el.div(
                        rx.el.p("How would you rate your experience with Gradwyn?", class_name="text-xs font-bold uppercase text-slate-500 mt-4 mb-2"),
                        rx.el.div(
                            rx.foreach(
                                [1, 2, 3, 4, 5],
                                lambda r: rx.el.button(
                                    f"{r} ★",
                                    on_click=AppState.set_feedback_rating(r),
                                    class_name=rx.cond(
                                        AppState.feedback_rating == r,
                                        "px-3.5 py-1.5 rounded-full text-xs font-bold bg-slate-900 text-white cursor-pointer",
                                        "px-3.5 py-1.5 rounded-full text-xs font-semibold bg-slate-100 text-slate-700 hover:bg-slate-200 cursor-pointer",
                                    ),
                                ),
                            ),
                            class_name="flex items-center gap-2 mb-4",
                        ),
                        rx.el.textarea(
                            value=AppState.feedback_comment,
                            on_change=AppState.set_feedback_comment,
                            placeholder="Tell us what you love or what we should build next...",
                            rows=3,
                            class_name="w-full p-3 rounded-xl border border-slate-300 text-sm mb-4",
                        ),
                        rx.el.div(
                            rx.el.button(
                                "Submit Feedback",
                                on_click=AppState.submit_feedback,
                                class_name="w-full py-2.5 rounded-full bg-slate-900 text-white text-sm font-semibold hover:bg-slate-800 cursor-pointer",
                            ),
                        ),
                    ),
                ),
                class_name="bg-white rounded-3xl max-w-md w-full p-6 shadow-2xl border border-slate-200",
            ),
            class_name="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4",
        ),
    )


def candidate_dossier_modal() -> rx.Component:
    """University Admissions Officer modal to inspect a student's application and issue a decision."""
    return rx.cond(
        AppState.is_candidate_modal_open,
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.span(
                            f"AI Fit Score: {AppState.selected_candidate['matchScore']}%",
                            class_name="text-xs font-bold px-2.5 py-0.5 rounded-full bg-emerald-100 text-emerald-800",
                        ),
                        rx.el.h3(
                            AppState.selected_candidate["studentName"],
                            class_name="text-2xl font-bold text-slate-900 mt-1",
                        ),
                        rx.el.p(
                            f"{AppState.selected_candidate['country']} · {AppState.selected_candidate['studentEmail']}",
                            class_name="text-xs text-slate-500",
                        ),
                    ),
                    rx.el.button(
                        rx.icon("x", size=18),
                        on_click=AppState.close_candidate_modal,
                        class_name="p-2 rounded-full text-slate-400 hover:text-slate-700 hover:bg-slate-100 cursor-pointer",
                    ),
                    class_name="flex items-start justify-between pb-4 border-b border-slate-200",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.p("Target Institution", class_name="text-xs text-slate-500"),
                        rx.el.p(AppState.selected_candidate["targetName"], class_name="text-sm font-bold text-slate-900"),
                        class_name="p-3 rounded-xl bg-slate-50 border border-slate-200",
                    ),
                    rx.el.div(
                        rx.el.p("Applied Program", class_name="text-xs text-slate-500"),
                        rx.el.p(AppState.selected_candidate["program"], class_name="text-sm font-bold text-slate-900"),
                        class_name="p-3 rounded-xl bg-slate-50 border border-slate-200",
                    ),
                    rx.el.div(
                        rx.el.p("Verified GPA", class_name="text-xs text-slate-500"),
                        rx.el.p(AppState.selected_candidate["gpa"], class_name="text-sm font-bold text-slate-900"),
                        class_name="p-3 rounded-xl bg-slate-50 border border-slate-200",
                    ),
                    rx.el.div(
                        rx.el.p("Standardized Tests", class_name="text-xs text-slate-500"),
                        rx.el.p(AppState.selected_candidate["testScores"], class_name="text-sm font-bold text-slate-900"),
                        class_name="p-3 rounded-xl bg-slate-50 border border-slate-200",
                    ),
                    class_name="grid grid-cols-1 sm:grid-cols-2 gap-3 my-4",
                ),
                rx.el.div(
                    rx.el.p("Personal Statement / Admissions Essay", class_name="text-xs font-bold uppercase tracking-wider text-slate-500 mb-1.5"),
                    rx.el.p(
                        AppState.selected_candidate["personalStatement"],
                        class_name="text-sm text-slate-700 leading-relaxed bg-slate-50 p-4 rounded-2xl border border-slate-200",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.span("Current Decision Status: ", class_name="text-xs text-slate-500"),
                        rx.el.span(
                            AppState.selected_candidate["status"],
                            class_name="text-xs font-bold text-slate-900",
                        ),
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Mark Under Review",
                            on_click=AppState.update_candidate_status(
                                AppState.selected_candidate["id"], "Under Review"
                            ),
                            class_name="px-4 py-2 rounded-full text-xs font-semibold bg-amber-100 text-amber-900 hover:bg-amber-200 transition-colors cursor-pointer",
                        ),
                        rx.el.button(
                            "Reject Candidate",
                            on_click=AppState.update_candidate_status(
                                AppState.selected_candidate["id"], "Rejected"
                            ),
                            class_name="px-4 py-2 rounded-full text-xs font-semibold bg-rose-100 text-rose-800 hover:bg-rose-200 transition-colors cursor-pointer",
                        ),
                        rx.el.button(
                            "✓ Admit Candidate",
                            on_click=AppState.update_candidate_status(
                                AppState.selected_candidate["id"], "Accepted"
                            ),
                            class_name="px-5 py-2 rounded-full text-xs font-bold bg-emerald-600 text-white hover:bg-emerald-700 transition-colors cursor-pointer",
                        ),
                        class_name="flex flex-wrap items-center gap-2",
                    ),
                    class_name="flex flex-wrap items-center justify-between gap-3 pt-4 border-t border-slate-200",
                ),
                class_name="bg-white rounded-3xl max-w-2xl w-full p-6 sm:p-8 shadow-2xl border border-slate-200 max-h-[90vh] overflow-y-auto",
            ),
            class_name="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4",
        ),
    )


def global_modals() -> rx.Component:
    """Bundle all global modals so they can be mounted on any page."""
    return rx.fragment(
        application_wizard_modal(),
        edit_profile_modal(),
        guide_reader_modal(),
        feedback_modal(),
        candidate_dossier_modal(),
    )
