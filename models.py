import enum
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Enum, Text, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class MockStatusEnum(str, enum.Enum):
    scheduled = "Scheduled"
    in_progress = "In Progress"
    completed = "Completed"

class CorrectnessEnum(str, enum.Enum):
    correct = "Correct"
    incorrect = "Incorrect"
    partial = "Partial"

# Association table for Mock <-> Question (Many-to-Many)
mock_questions = Table('mock_questions', Base.metadata,
    Column('mock_id', Integer, ForeignKey('mocks.id')),
    Column('question_id', Integer, ForeignKey('questions.id'))
)

class TechStack(Base):
    __tablename__ = "tech_stacks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    
    questions = relationship("Question", back_populates="tech_stack")

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(Text, nullable=False)
    topic = Column(String)
    ideal_answer = Column(Text)
    tech_stack_id = Column(Integer, ForeignKey("tech_stacks.id"))

    tech_stack = relationship("TechStack", back_populates="questions")

class Mock(Base):
    __tablename__ = "mocks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    questions = relationship("Question", secondary=mock_questions)
    sessions = relationship("MockSession", back_populates="mock")

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    profile_exp = Column(String, nullable=True)
    passing_year = Column(Integer, nullable=True)
    graduation_details = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    sessions = relationship("MockSession", back_populates="candidate")

class MockSession(Base):
    __tablename__ = "mock_sessions"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    mock_id = Column(Integer, ForeignKey("mocks.id"))
    session_date = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(Enum(MockStatusEnum), default=MockStatusEnum.scheduled)
    overall_result = Column(String, nullable=True)
    soft_skills_feedback = Column(Text, nullable=True)
    coding_feedback = Column(Text, nullable=True)

    candidate = relationship("Candidate", back_populates="sessions")
    mock = relationship("Mock", back_populates="sessions")
    answers = relationship("SessionAnswer", back_populates="session")

class SessionAnswer(Base):
    __tablename__ = "session_answers"

    id = Column(Integer, primary_key=True, index=True)
    mock_session_id = Column(Integer, ForeignKey("mock_sessions.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    candidate_answer = Column(Text)
    correctness = Column(Enum(CorrectnessEnum), nullable=True)

    session = relationship("MockSession", back_populates="answers")
    question = relationship("Question")