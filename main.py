from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from fastapi.middleware.cors import CORSMiddleware

import models, schemas, crud
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configure CORS to allow requests from your React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Mock Test Module API is running"}

@app.post("/tech-stacks/", response_model=schemas.TechStack)
def create_tech_stack(stack: schemas.TechStackCreate, db: Session = Depends(get_db)):
    db_stack = crud.get_tech_stack_by_name(db, stack.name)
    if db_stack:
        raise HTTPException(status_code=409, detail="Tech stack with this name already exists")
    return crud.create_tech_stack(db=db, stack=stack) # This will now always create a new one

@app.get("/tech-stacks/", response_model=List[schemas.TechStack])
def read_tech_stacks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_tech_stacks(db, skip=skip, limit=limit)

@app.post("/questions/", response_model=schemas.Question)
def create_question(question: schemas.QuestionCreate, db: Session = Depends(get_db)):
    return crud.create_question(db=db, question=question)

@app.get("/questions/", response_model=List[schemas.Question])
def read_questions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_questions(db, skip=skip, limit=limit)

@app.post("/mocks/generate", response_model=schemas.Mock)
def generate_mock(mock_data: schemas.MockCreateFromStacks, db: Session = Depends(get_db)):
    return crud.create_mock_from_stacks(db=db, mock_data=mock_data)

@app.get("/mocks/{mock_id}", response_model=schemas.Mock)
def read_mock(mock_id: int, db: Session = Depends(get_db)):
    db_mock = crud.get_mock(db, mock_id=mock_id)
    if db_mock is None:
        raise HTTPException(status_code=404, detail="Mock not found")
    return db_mock

@app.post("/sessions/", response_model=schemas.MockSession)
def create_session(session: schemas.MockSessionCreate, db: Session = Depends(get_db)):
    return crud.create_mock_session(db=db, session_data=session)

@app.post("/sessions/{session_id}/submit", response_model=schemas.MockSession)
def submit_session(session_id: int, answers: List[schemas.SessionAnswerCreate], db: Session = Depends(get_db)):
    db_session = crud.submit_session(db=db, session_id=session_id, answers=answers)
    if db_session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return db_session