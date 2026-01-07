# Mock Test Module

This project is a full-stack application designed to generate, administer, and manage technical assessment tests. The backend is built with FastAPI and the frontend with React.

## Table of Contents

- [Project Overview](#1-project-overview)
- Tech Stack
- Project Structure
- API Endpoints
- Database Schema
- Setup and Installation
  - Backend Setup
  - Frontend Setup
- How It Works
- Testing

## 1. Project Overview

The Mock Test Module allows for the dynamic creation of technical tests based on a predefined set of questions categorized by technology stacks. It provides an interface for candidates to take these tests and for their answers to be recorded.

- **Dynamic Test Generation**: Create tests by selecting technology stacks and the number of questions.
- **Test Administration**: A simple UI for candidates to take the generated tests.
- **Answer Submission**: Captures and stores candidate answers for review.

## 2. Tech Stack

-   **Backend**: Python 3.12, FastAPI, SQLAlchemy (ORM), Pydantic, SQLite.
-   **Frontend**: React 18, Vite, Axios.
-   **Testing**: Pytest, HTTPX.

## 3. Project Structure

```text
Mock_test_module/
├── frontend/            # React application
│   ├── src/
│   │   ├── components/
│   │   │   └── CreateMock.jsx
│   │   ├── App.jsx
│   │   └── TakeMockTest.jsx
│   └── ...
├── main.py              # FastAPI application & routes
├── crud.py              # Database CRUD operations
├── models.py            # SQLAlchemy database models
├── schemas.py           # Pydantic data validation schemas
├── database.py          # Database connection setup
├── seed.py              # Initial data seeding script
├── test_main.py         # Backend integration tests
└── requirements.txt     # Python dependencies
```

## 4. Backend API Endpoints

-   `GET /`: Health check for the API.
-   `POST /tech-stacks/`: Create a new technology stack.
-   `GET /tech-stacks/`: Retrieve a list of all tech stacks.
-   `POST /questions/`: Create a new question.
-   `GET /questions/`: Retrieve a list of all questions.
-   `POST /mocks/generate`: Generate a new mock test from selected tech stacks.
-   `GET /mocks/{mock_id}`: Retrieve a specific mock test by its ID.
-   `POST /sessions/`: Start a new test session for a candidate.
-   `POST /sessions/{session_id}/submit`: Submit answers for a session and mark it as complete.

## 5. Database Schema

-   **Candidate**: Stores candidate information (name, email, profile).
-   **TechStack**: Represents technology categories (e.g., "Python", "React").
-   **Question**: Stores individual questions, each linked to a `TechStack`.
-   **Mock**: A collection of questions that make up a single test.
-   **MockSession**: An instance of a candidate taking a specific `Mock`.
-   **SessionAnswer**: A candidate's answer to a question within a `MockSession`.

## 6. Setup and Installation

### Backend Setup

1.  **Create a Virtual Environment:**
    ```bash
    python -m venv .venv
    # On Windows
    .venv\Scripts\activate
    # On macOS/Linux
    source .venv/bin/activate
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Initialize Database & Seed Data:**
    This command creates the `sql_app.db` file and populates it with initial data.
    ```bash
    python seed.py
    ```

4.  **Run the Server:**
    ```bash
    uvicorn main:app --reload
    ```
    The API will be available at `http://127.0.0.1:8000`.
    Interactive documentation (Swagger UI) is at `http://127.0.0.1:8000/docs`.

### Frontend Setup

1.  **Navigate to Frontend Directory:**
    ```bash
    cd frontend
    ```

2.  **Install Dependencies:**
    ```bash
    npm install
    ```

3.  **Run the Development Server:**
    ```bash
    npm run dev
    ```
    The application will be available at `http://localhost:5173`.

## 7. How It Works

The application flow is straightforward:

1.  **Creation**: The user lands on the `CreateMock` page, selects tech stacks, and gives the test a name. Clicking "Generate" sends a `POST` request to `/mocks/generate`.
2.  **Initialization**: On a successful response, the frontend receives the new `mock_id`. The `App` component then renders the `TakeMockTest` component.
3.  **Taking the Test**: `TakeMockTest` fetches the mock details via `GET /mocks/{mock_id}` and creates a session via `POST /sessions/`. The questions are displayed for the candidate.
4.  **Submission**: After answering, the candidate clicks "Submit". The answers are sent to `POST /sessions/{session_id}/submit`, and the session is marked as `Completed`.

## 8. Testing

-   **Automated Backend Tests**: Run unit and integration tests for the API.
    ```bash
    pytest
    ```
    The tests use an isolated, temporary SQLite database to avoid interfering with development data.

-   **Manual API Testing**: Use the auto-generated Swagger UI to interact with each endpoint directly.
    -   Navigate to `http://127.0.0.1:8000/docs` while the backend server is running.