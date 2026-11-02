"""Database and TypedDict State Models for Gradwyn MVP."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional, TypedDict

import sqlmodel


# =====================================================================
# TypedDict Schemas for Reflex State & Foreach Type Inference
# =====================================================================


class SourceItem(TypedDict):
    title: str
    uri: str


class UniversityItem(TypedDict):
    name: str
    location: str
    rank: str
    matchScore: int
    acceptanceRate: str
    tuition: str
    programs: list[str]
    description: str
    website: str
    imageUrl: str
    applicationFee: str
    deadline: str
    scholarships: list[str]


class ScholarshipItem(TypedDict):
    id: str
    name: str
    provider: str
    amount: str
    deadline: str
    location: str
    eligibility: list[str]
    description: str
    website: str


class MentorItem(TypedDict):
    id: str
    name: str
    role: str
    university: str
    location: str
    bio: str
    specialties: list[str]
    imageUrl: str
    linkedin: str
    available: bool


class GuideItem(TypedDict):
    id: str
    title: str
    category: str
    readTime: str
    author: str
    authorRole: str
    imageUrl: str
    description: str
    content: str


class ChatMessageItem(TypedDict):
    id: str
    role: str
    content: str
    sources: list[SourceItem]


class StudentAppItem(TypedDict):
    id: str
    name: str
    type: str
    status: str
    deadline: str
    submittedDate: str
    program: str


class CandidateAppItem(TypedDict):
    id: str
    studentName: str
    studentEmail: str
    country: str
    targetName: str
    targetType: str
    program: str
    gpa: str
    testScores: str
    matchScore: int
    status: str
    submittedDate: str
    personalStatement: str
    documents: list[str]


class ChecklistItem(TypedDict):
    id: str
    label: str
    category: str
    done: bool


class OnboardingStepItem(TypedDict):
    id: str
    title: str
    subtitle: str
    type: str
    options: list[str]


# =====================================================================
# SQLModel Persistent Database Tables
# =====================================================================


class UserAccount(sqlmodel.SQLModel, table=True):
    """Persistent user account for Students, Mentors, and University Partners."""

    id: Optional[int] = sqlmodel.Field(default=None, primary_key=True)
    uid: str = sqlmodel.Field(index=True, unique=True)
    email: str = sqlmodel.Field(index=True)
    password_hash: str = ""
    display_name: str = ""
    role: str = "student"  # "student" | "mentor" | "university"
    onboarding_complete: bool = False
    partner_university_name: str = ""
    created_at: str = sqlmodel.Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


class MentorListing(sqlmodel.SQLModel, table=True):
    """Persistent mentor profile synced to the Student Mentorship Network."""

    id: Optional[int] = sqlmodel.Field(default=None, primary_key=True)
    mentor_uid: str = sqlmodel.Field(index=True, unique=True)
    name: str
    role: str
    university: str
    location: str
    bio: str
    specialties_json: str = "[]"
    image_url: str = ""
    linkedin: str = "https://www.linkedin.com"
    available: bool = True


class ApplicationSubmission(sqlmodel.SQLModel, table=True):
    """Persistent application dossier shared between Student Hub & University Portal."""

    id: Optional[int] = sqlmodel.Field(default=None, primary_key=True)
    app_uid: str = sqlmodel.Field(index=True, unique=True)
    student_uid: str = sqlmodel.Field(index=True)
    student_name: str
    student_email: str
    country: str
    target_name: str = sqlmodel.Field(index=True)
    target_type: str = "University"
    program: str
    gpa: str
    test_scores: str
    match_score: int = 94
    status: str = "Submitted"  # "Submitted" | "Under Review" | "Accepted" | "Rejected"
    submitted_date: str
    personal_statement: str
    documents_json: str = "[]"


class FeedbackEntry(sqlmodel.SQLModel, table=True):
    """User feedback entry."""

    id: Optional[int] = sqlmodel.Field(default=None, primary_key=True)
    user_uid: str = "anonymous"
    rating: int = 5
    category: str = "general"
    comment: str = ""
    created_at: str = sqlmodel.Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
