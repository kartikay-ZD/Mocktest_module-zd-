from sqlalchemy.orm import Session
import random
from typing import List

import models, schemas


def get_candidate(db: Session, candidate_id: int):
    return db.query(models.Candidate).filter(models.Candidate.id == candidate_id).first()


def get_candidates(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Candidate).offset(skip).limit(limit).all()


def create_candidate(db: Session, candidate: schemas.CandidateCreate):
    db_candidate = models.Candidate(name=candidate.name, email=candidate.email)
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    return db_candidate


def get_tech_stack(db: Session, stack_id: int):
    return db.query(models.TechStack).filter(models.TechStack.id == stack_id).first()

def get_tech_stack_by_name(db: Session, name: str):
    return db.query(models.TechStack).filter(models.TechStack.name == name).first()

def get_tech_stacks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.TechStack).offset(skip).limit(limit).all()

def create_tech_stack(db: Session, stack: schemas.TechStackCreate):
    db_stack = models.TechStack(name=stack.name)
    db.add(db_stack)
    db.commit()
    db.refresh(db_stack)
    return db_stack

def create_question(db: Session, question: schemas.QuestionCreate):
    db_question = models.Question(**question.dict())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

def get_questions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Question).offset(skip).limit(limit).all()


def get_mocks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Mock).offset(skip).limit(limit).all()

def get_mock(db: Session, mock_id: int):
    return db.query(models.Mock).filter(models.Mock.id == mock_id).first()


def create_mock_from_stacks(db: Session, mock_data: schemas.MockCreateFromStacks):
    # 1. Create the Mock object
    db_mock = models.Mock(name=mock_data.name, description=mock_data.description)
    db.add(db_mock)
    db.commit()
    
    # 2. Select questions
    # Strategy: Try to distribute questions evenly among selected stacks
    if not mock_data.tech_stack_ids:
        return db_mock

    questions_per_stack = mock_data.num_questions // len(mock_data.tech_stack_ids)
    remainder = mock_data.num_questions % len(mock_data.tech_stack_ids)

    selected_questions = []
    
    for i, stack_id in enumerate(mock_data.tech_stack_ids):
        limit = questions_per_stack + (1 if i < remainder else 0)
        
        # Fetch all questions for this stack (in a real app, might want to filter by difficulty)
        stack_questions = db.query(models.Question).filter(models.Question.tech_stack_id == stack_id).all()
        
        if stack_questions:
            # Randomly sample
            selected_questions.extend(random.sample(stack_questions, min(len(stack_questions), limit)))

    # 3. Associate questions with Mock
    db_mock.questions = selected_questions
    db.commit()
    db.refresh(db_mock)
    return db_mock

def create_mock_session(db: Session, session_data: schemas.MockSessionCreate):
    db_session = models.MockSession(
        candidate_id=session_data.candidate_id,
        mock_id=session_data.mock_id,
        status=models.MockStatusEnum.in_progress
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def submit_session(db: Session, session_id: int, answers: List[schemas.SessionAnswerCreate]):
    db_session = db.query(models.MockSession).filter(models.MockSession.id == session_id).first()
    if not db_session:
        return None
    
    for ans in answers:
        db_answer = models.SessionAnswer(mock_session_id=session_id, question_id=ans.question_id, candidate_answer=ans.candidate_answer)
        db.add(db_answer)
    
    db_session.status = models.MockStatusEnum.completed
    db.commit()
    db.refresh(db_session)
    return db_session