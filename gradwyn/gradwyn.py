"""Main Reflex Application Entry Point for Gradwyn MVP."""

from __future__ import annotations

import reflex as rx

from .state import AppState
from .views.auth import auth_page
from .views.chat import chat_page
from .views.dashboard import dashboard_page
from .views.landing import landing_page
from .views.mentor_portal import mentor_dashboard_page, mentor_onboarding_page
from .views.onboarding import onboarding_page
from .views.university_portal import university_dashboard_page

app = rx.App(
    head_components=[
        rx.el.link(
            rel="preconnect",
            href="https://fonts.googleapis.com",
        ),
        rx.el.link(
            rel="preconnect",
            href="https://fonts.gstatic.com",
            cross_origin="",
        ),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Playfair+Display:ital,wght@0,600;0,700;1,400;1,600&display=swap",
            rel="stylesheet",
        ),
    ],
)

app.add_page(
    landing_page,
    route="/",
    title="Gradwyn | AI-Powered Global Higher Education, Scholarships & Mentorship",
    on_load=AppState.on_app_load,
)
app.add_page(
    auth_page,
    route="/login",
    title="Sign In | Gradwyn Ecosystem",
    on_load=AppState.on_app_load,
)
app.add_page(
    onboarding_page,
    route="/onboarding",
    title="Scholar Onboarding | Gradwyn",
    on_load=AppState.on_app_load,
)
app.add_page(
    chat_page,
    route="/chat",
    title="AI Admissions Advisor & University Match Deck | Gradwyn",
    on_load=AppState.on_app_load,
)
app.add_page(
    dashboard_page,
    route="/dashboard",
    title="Student Hub | Gradwyn",
    on_load=AppState.on_app_load,
)
app.add_page(
    mentor_onboarding_page,
    route="/mentor-onboarding",
    title="Mentor Onboarding | Gradwyn",
    on_load=AppState.on_app_load,
)
app.add_page(
    mentor_dashboard_page,
    route="/mentor-dashboard",
    title="Verified Alumni Mentor Portal | Gradwyn",
    on_load=AppState.on_app_load,
)
app.add_page(
    university_dashboard_page,
    route="/university-dashboard",
    title="Partner University Admissions Portal | Gradwyn",
    on_load=AppState.on_app_load,
)
