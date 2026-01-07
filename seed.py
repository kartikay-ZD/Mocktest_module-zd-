from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas, crud

def seed_data():
    db = SessionLocal()
    
    print("Seeding data...")

    # Tech Stacks
    if not db.query(models.TechStack).first():
        python_stack = crud.create_tech_stack(db, schemas.TechStackCreate(name="Python"))
        react_stack = crud.create_tech_stack(db, schemas.TechStackCreate(name="React"))
        sql_stack = crud.create_tech_stack(db, schemas.TechStackCreate(name="SQL"))

        # Questions
        questions = [
            {"text": "What is a decorator?", "topic": "Core", "stack_id": python_stack.id},
            {"text": "Explain list comprehension.", "topic": "Core", "stack_id": python_stack.id},
            {"text": "What is the Virtual DOM?", "topic": "Core", "stack_id": react_stack.id},
            {"text": "Explain useEffect hook.", "topic": "Hooks", "stack_id": react_stack.id},
            {"text": "What is a JOIN?", "topic": "Core", "stack_id": sql_stack.id},
        ]

        for q in questions:
            crud.create_question(db, schemas.QuestionCreate(
                question_text=q["text"],
                topic=q["topic"],
                ideal_answer="Answer...",
                tech_stack_id=q["stack_id"]
            ))
        print("Tech stacks and questions seeded.")

    # Candidate
    if not db.query(models.Candidate).first():
        crud.create_candidate(db, schemas.CandidateCreate(name="Test Candidate", email="test@example.com"))
        print("Test candidate seeded.")

    print("Seeding complete.")
    db.close()

if __name__ == "__main__":
    models.Base.metadata.create_all(bind=engine)
    seed_data()