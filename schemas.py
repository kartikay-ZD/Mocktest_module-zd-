from __future__ import annotations

import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr

from models import CorrectnessEnum, MockStatusEnum


# Pydantic models (or "schemas") are used for data validation and serialization.

# --- Question Schemas ---
class QuestionBase(BaseModel):
    question_text: str
    topic: Optional[str] = None
    ideal_answer: Optional[str] = None
    tech_stack_id: int

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    id: int

    class Config:
        from_attributes = True


# --- TechStack Schemas ---
class TechStackBase(BaseModel):
    name: str

class TechStackCreate(TechStackBase):
    pass

class TechStack(TechStackBase):
    id: int
    questions: List[Question] = []

    class Config:
        from_attributes = True


# --- Mock Schemas ---
class MockBase(BaseModel):
    name: str
    description: Optional[str] = None

class MockCreate(MockBase):
    """Schema for creating a Mock with a specific list of questions."""
    question_ids: List[int]

class MockCreateFromStacks(BaseModel):
    """Schema for creating a Mock by selecting tech stacks."""
    name: str
    description: Optional[str] = None
    tech_stack_ids: List[int]
    # We can add more config here, e.g., number of questions per stack
    num_questions: Optional[int] = 10

class Mock(MockBase):
    id: int
    created_at: datetime.datetime
    questions: List[Question] = []

    class Config:
        from_attributes = True


# --- Candidate Schemas ---
class CandidateBase(BaseModel):
    name: str
    email: EmailStr
    profile_exp: Optional[str] = None
    passing_year: Optional[int] = None
    graduation_details: Optional[str] = None

class CandidateCreate(CandidateBase):
    pass

class Candidate(CandidateBase):
    id: int
    created_at: datetime.datetime

    class Config:
        from_attributes = True


# --- SessionAnswer Schemas ---
class SessionAnswerBase(BaseModel):
    question_id: int
    candidate_answer: Optional[str] = None

class SessionAnswerCreate(SessionAnswerBase):
    pass

class SessionAnswer(SessionAnswerBase):
    id: int
    correctness: Optional[CorrectnessEnum] = None
    mock_session_id: int

    class Config:
        from_attributes = True


# --- MockSession Schemas ---
class MockSessionBase(BaseModel):
    candidate_id: int
    mock_id: int

class MockSessionCreate(MockSessionBase):
    pass

class MockSession(MockSessionBase):
    id: int
    session_date: datetime.datetime
    status: MockStatusEnum
    overall_result: Optional[str] = None
    soft_skills_feedback: Optional[str] = None
    coding_feedback: Optional[str] = None
    answers: List[SessionAnswer] = []
    candidate: Candidate
    mock: Mock

    class Config:
        from_attributes = True