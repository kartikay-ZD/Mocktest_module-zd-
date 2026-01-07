import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool # Important for SQLite in-memory or temp files
import tempfile
from database import Base
from main import app, get_db
import os

# Use a temporary file for the database for each test
@pytest.fixture(name="db_url")
def db_url_fixture():
    # Create a unique temporary file for the database for each test
    with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as tmp:
        yield f"sqlite:///{tmp.name}"
        # Ensure the file is deleted after the test
        try:
            os.unlink(tmp.name)
        except PermissionError as e:
            print(f"Warning: Could not remove temporary test_db.db file '{tmp.name}': {e}")

@pytest.fixture(name="test_engine")
def test_engine_fixture(db_url):
    # Create an engine for the temporary database
    engine = create_engine(
        db_url,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool # Use StaticPool for SQLite temp files to prevent connection issues
    )
    # Create all tables in the temporary database
    Base.metadata.create_all(bind=engine)
    yield engine
    # Drop all tables and dispose the engine after the test
    Base.metadata.drop_all(bind=engine)
    engine.dispose()

@pytest.fixture(name="test_session")
def test_session_fixture(test_engine):
    # Create a session factory for the test engine
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    # Get a session
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(name="client")
def client_fixture(test_session):
    # Override the get_db dependency in the FastAPI app to use our test session
    app.dependency_overrides[get_db] = lambda: test_session
    # Yield the TestClient
    with TestClient(app) as c:
        yield c
    # Clean up the dependency override after the test
    app.dependency_overrides.pop(get_db)

# Now, all your tests can simply request the 'client' fixture
# and it will automatically provide an isolated test environment.

def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Mock Test Module API is running"}

def test_create_tech_stack(client):
    response = client.post("/tech-stacks/", json={"name": "FastAPI"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "FastAPI"
    assert "id" in data

def test_get_tech_stacks(client):
    # Create one first
    client.post("/tech-stacks/", json={"name": "React"})
    response = client.get("/tech-stacks/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "React"

def test_generate_mock(client):
    # 1. Create some tech stacks
    response_python = client.post("/tech-stacks/", json={"name": "Python"})
    assert response_python.status_code == 200
    python_stack_id = response_python.json()["id"]

    response_react = client.post("/tech-stacks/", json={"name": "React"})
    assert response_react.status_code == 200
    react_stack_id = response_react.json()["id"]

    # 2. Create some questions for these tech stacks
    client.post("/questions/", json={
        "question_text": "What is a decorator?", "topic": "Core", "ideal_answer": "...", "tech_stack_id": python_stack_id
    })
    client.post("/questions/", json={
        "question_text": "Explain list comprehension.", "topic": "Core", "ideal_answer": "...", "tech_stack_id": python_stack_id
    })
    client.post("/questions/", json={
        "question_text": "What is the Virtual DOM?", "topic": "Core", "ideal_answer": "...", "tech_stack_id": react_stack_id
    })

    # 3. Generate a mock test
    mock_payload = {
        "name": "Test Generated Mock",
        "tech_stack_ids": [python_stack_id, react_stack_id],
        "num_questions": 2
    }
    response = client.post("/mocks/generate", json=mock_payload)
    assert response.status_code == 200
    mock_data = response.json()
    assert mock_data["name"] == "Test Generated Mock"
    assert "id" in mock_data
    assert len(mock_data["questions"]) == 2 # Expecting 2 questions
    # Further checks could ensure distribution, but that's more complex for a basic test

def test_generate_mock():
    # 1. Create some tech stacks
    response_python = client.post("/tech-stacks/", json={"name": "Python"})
    assert response_python.status_code == 200
    python_stack_id = response_python.json()["id"]

    response_react = client.post("/tech-stacks/", json={"name": "React"})
    assert response_react.status_code == 200
    react_stack_id = response_react.json()["id"]

    # 2. Create some questions for these tech stacks
    client.post("/questions/", json={
        "question_text": "What is a decorator?", "topic": "Core", "ideal_answer": "...", "tech_stack_id": python_stack_id
    })
    client.post("/questions/", json={
        "question_text": "Explain list comprehension.", "topic": "Core", "ideal_answer": "...", "tech_stack_id": python_stack_id
    })
    client.post("/questions/", json={
        "question_text": "What is the Virtual DOM?", "topic": "Core", "ideal_answer": "...", "tech_stack_id": react_stack_id
    })

    # 3. Generate a mock test
    mock_payload = {
        "name": "Test Generated Mock",
        "tech_stack_ids": [python_stack_id, react_stack_id],
        "num_questions": 2
    }
    response = client.post("/mocks/generate", json=mock_payload)
    assert response.status_code == 200
    mock_data = response.json()
    assert mock_data["name"] == "Test Generated Mock"
    assert "id" in mock_data
    assert len(mock_data["questions"]) == 2 # Expecting 2 questions
    # Further checks could ensure distribution, but that's more complex for a basic test