# Architecture

## Executive Summary

The ibe160 project is a minimalist, AI-enhanced web application for task management. This architecture document outlines the technical decisions to build a Python Flask application with TailwindCSS for the frontend, utilizing SQLite for data persistence, Flask session-based authentication, and integrating with the Google Gemini API via a backend proxy for intelligent task categorization. The application will be deployed on Render, focusing on a robust and maintainable solution for the MVP.

## Project Initialization

First implementation story should execute the manual setup for a Flask with TailwindCSS starter:

```bash
mkdir flask_tailwind_app
cd flask_tailwind_app
python -m venv venv
./venv/bin/pip install Flask
npm init -y
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

This establishes the base architecture with these decisions:
- Language: Python (Flask)
- Styling solution: TailwindCSS
- Build tooling: npm scripts for TailwindCSS compilation
- Project structure: Standard Flask application layout

## Decision Summary

| Category                   | Decision                                                | Version  | Affects Epics | Rationale                                                                        |
| -------------------------- | ------------------------------------------------------- | -------- | ------------- | -------------------------------------------------------------------------------- |
| Data Persistence           | SQLite                                                  | (N/A)    | 1, 2, 3       | Simple, file-based, serverless, and perfect for a single-user MVP.               |
| API Pattern                | REST API                                                | (N/A)    | 2, 3          | Standard, well-understood pattern for web apps and a core strength of Flask.     |
| AI Application Integration | Direct Gemini API calls from backend (google-genai lib) | 1.52.0   | 2             | Securely handles API keys on the backend with a robust fallback strategy.        |
| Authentication             | Flask Session-based authentication                      | (N/A)    | 1             | Simple to implement and sufficient for securing a single-user application in MVP. |
| Deployment Target          | Render                                                  | (NA)    | All           | Beginner-friendly platform with a free tier and easy deployment from GitHub.     |

## Project Structure

```
/
|-- app.py                  # Main Flask application, routes, and API logic
|-- ai_service.py           # Module for Gemini API calls
|-- .gitignore
|-- package.json
|-- tailwind.config.js
|-- postcss.config.js
|-- requirements.txt        # Python dependencies
|-- venv/                     # Virtual environment
|-- static/
|   |-- src/
|   |   |-- input.css       # TailwindCSS input
|   |-- dist/
|       |-- output.css      # Compiled CSS
|-- templates/
|   |-- base.html           # Base layout template
|   |-- index.html          # Main dashboard view
|   |-- ... (other views)
|-- instance/
|   |-- tasks.db            # SQLite database file
|-- tests/                    # Tests for the application
    |-- test_api.py
    |-- test_app.py
```

## Epic to Architecture Mapping

| Epic ID | Epic Name                         | Architectural Components                               |
| ------- | --------------------------------- | ------------------------------------------------------ |
| 1       | Foundational Setup & Core Task Mgmt | `app.py`, `templates/`, `instance/tasks.db`            |
| 2       | AI-Powered Task Intelligence      | `ai_service.py`, `app.py` (API proxy)                  |
| 3       | Smart Lists & Advanced Filtering  | `app.py`, `templates/`, `instance/tasks.db`            |

## Technology Stack Details

### Core Technologies

-   **Backend Framework:** Flask
-   **Database:** SQLite
-   **Frontend Styling:** TailwindCSS
-   **AI Integration:** Google Gemini API (`google-genai` Python library, v1.52.0)
-   **Deployment Platform:** Render

### Integration Points

-   Frontend (HTML templates) <-> Backend (`app.py` REST API) for all task management and AI suggestion requests.
-   Backend (`ai_service.py`) <-> Google Gemini API for AI-powered suggestions.

## Novel Pattern Designs

-   Pattern Name: AI-Suggestion Flow (Magic Fill)
-   Purpose: Streamline task categorization/prioritization with AI, reduce manual effort.
-   Components: Frontend Task Modal, Flask Backend API (`/suggest`), Google Gemini API, Rule-based Fallback.
-   Data Flow: User -> Frontend -> Backend (`/suggest`) -> `ai_service.py` -> Gemini API (or Fallback) -> `ai_service.py` -> Backend -> Frontend.
-   Affects Epics: Epic 2.

## Implementation Patterns

These patterns ensure consistent implementation across all AI agents:

-   Naming: Snake_case for Python/DB, Kebab-case for CSS, Plural Kebab-case for API.
-   Structure: Flask standard with `ai_service.py`, `templates/`, `static/`, `tests/`.
-   Format: JSON for API, ISO 8601 for dates/times.
-   Communication: RESTful HTTP (FE-BE), Python function calls (BE-AI).
-   Location: `instance/tasks.db`, `static/dist/`.

## Consistency Rules

### Naming Conventions

-   Database Tables & Columns: Snake_case.
-   Python Variables/Functions: Snake_case.
-   Frontend CSS Classes: Kebab-case (Tailwind default).
-   API Endpoints: Plural, kebab-case.

### Code Organization

-   Python Project: `app.py` as main, `ai_service.py` for AI logic. Separate `templates/` and `static/`.
-   Tests: `tests/` directory with `test_*.py` files.

### Error Handling

-   Standard Flask error handlers with JSON responses for API errors.

### Logging Strategy

-   Basic console logging via Python's built-in `logging` module.

## Data Architecture

-   **Database:** SQLite (`instance/tasks.db`).
-   **Models:** `Task` model (id, title, notes, due_date, label, priority, is_done, created_at) using SQLAlchemy.

## API Contracts

-   **Type:** RESTful JSON API.
-   **Success Response:** `{ "data": ... }`.
-   **Error Response:** `{ "error": { "message": "...", "code": ... } }`.
-   **Endpoints:** e.g., `POST /api/tasks`, `GET /api/tasks`, `PUT /api/tasks/<id>`, `DELETE /api/tasks/<id>`, `POST /api/suggest` (for AI).

## Security Architecture

-   **Authentication:** Flask Session-based.
-   **API Key Management:** Google Gemini API key is securely handled on the backend and not exposed client-side.
-   **Data Protection:** User task data stored in SQLite is protected from unauthorized access.

## Performance Considerations

-   Load key UI within 1-2 seconds.
-   CRUD operations complete within 1-2 seconds.
-   AI suggestions returned within 1-2 seconds.
-   Strategies: Optimized database queries, efficient Flask rendering, efficient API calls to Gemini.

## Deployment Architecture

-   **Platform:** Render.
-   **Method:** Continuous deployment from GitHub repository.

## Development Environment

### Prerequisites

-   Python 3.x
-   Node.js (for npm)

### Setup Commands

```bash
mkdir flask_tailwind_app
cd flask_tailwind_app
python -m venv venv
./venv/bin/pip install Flask
npm init -y
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

## Architecture Decision Records (ADRs)

-   **Data Persistence:** SQLite for simplicity and MVP scope.
-   **API Pattern:** REST API for standard web communication.
-   **AI Integration:** Secure backend proxy for Google Gemini API calls.
-   **Authentication:** Flask Session-based for basic user management.
-   **Deployment Target:** Render for easy and cost-effective deployment.

---

_Generated by BMAD Decision Architecture Workflow v1.0_
_Date: søndag 30. november 2025_
_For: BIP_
