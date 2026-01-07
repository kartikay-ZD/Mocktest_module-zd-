# Mock Test Module - Requirements Document

## 1. Introduction
The Mock Test Module is a specialized component designed to be integrated into a larger candidate portal. It enables users (candidates) to dynamically generate and take technical mock assessments based on selected technology stacks. The system automates the assembly of questions and tracks user responses for review.

## 2. Scope
The module encompasses the backend API for managing questions and sessions, and the frontend user interface for configuring and taking tests. User management (authentication/authorization) is assumed to be handled by the parent portal.

## 3. Functional Requirements

### 3.1. Question Bank Management
*   **FR-01 Tech Stack Management**: The system shall maintain a list of supported Technology Stacks (e.g., Python, React, SQL, DevOps).
*   **FR-02 Question Storage**: The system shall store a repository of questions, each linked to a specific Tech Stack.
*   **FR-03 Question Attributes**: Each question shall contain:
    *   Question Text
    *   Topic/Category (e.g., "Hooks" for React)
    *   Ideal Answer (for grading reference)

### 3.2. Mock Test Generation
*   **FR-04 Custom Configuration**: Candidates shall be able to initiate a new mock test by specifying:
    *   A name for the test session.
    *   One or more Tech Stacks to include.
    *   The total number of questions desired.
*   **FR-05 Dynamic Assembly**: The system shall automatically generate a unique test by randomly selecting questions from the database that match the selected Tech Stacks.
*   **FR-06 Distribution**: The system should attempt to distribute questions evenly across the selected stacks.

### 3.3. Test Execution (Session)
*   **FR-07 Session Tracking**: The system shall create a unique `MockSession` for every attempt, tracking the start time and status (Scheduled, In Progress, Completed).
*   **FR-08 Test Interface**: The user interface shall display the questions associated with the generated mock.
*   **FR-09 Response Capture**: The system shall allow the candidate to input text-based answers for each question.

### 3.4. Submission & Completion
*   **FR-10 Submission**: The candidate shall be able to submit the test once finished.
*   **FR-11 Status Update**: Upon submission, the session status shall update to "Completed".
*   **FR-12 Data Persistence**: All candidate answers must be persisted in the database linked to the specific session and question.

## 4. Non-Functional Requirements
*   **NFR-01 Integration**: The frontend component must be built as a React module compatible with the existing portal architecture.
*   **NFR-02 API Design**: The backend must expose a RESTful API using JSON for data exchange.
*   **NFR-03 Database Abstraction**: The system shall use an ORM (SQLAlchemy) to ensure database independence (currently SQLite, scalable to PostgreSQL).
*   **NFR-04 Performance**: Test generation should occur in real-time (< 2 seconds).

## 5. Data Model

The following entities define the core data structure:

| Entity | Description |
| :--- | :--- |
| **Candidate** | Represents the user taking the test. |
| **TechStack** | Categories of technologies (e.g., Python, Java). |
| **Question** | Individual assessment items linked to a TechStack. |
| **Mock** | A generated test template containing a specific list of Questions. |
| **MockSession** | A specific instance of a Candidate taking a Mock. Tracks status and results. |
| **SessionAnswer** | The specific answer provided by a Candidate for a Question within a Session. |

## 6. API Specification

### Tech Stacks & Questions
*   `GET /tech-stacks/`: Retrieve list of available technologies.
*   `POST /tech-stacks/`: Add a new technology.
*   `GET /questions/`: Retrieve all questions.
*   `POST /questions/`: Add a new question to the bank.

### Mock Management
*   `POST /mocks/generate`: Generate a new Mock based on selected stacks and question count.
*   `GET /mocks/{mock_id}`: Retrieve details and questions for a specific Mock.

### Sessions
*   `POST /sessions/`: Start a new test session for a candidate.
*   `POST /sessions/{session_id}/submit`: Submit answers and complete the session.

## 7. Future Enhancements (Roadmap)
*   **Timer**: Enforce a time limit for the test session.
*   **Auto-Grading**: Implement keyword matching or AI-based grading for initial scoring.
*   **Review Dashboard**: An admin view to grade answers and provide feedback.
*   **Difficulty Levels**: Allow users to select difficulty (Easy, Medium, Hard) during generation.
