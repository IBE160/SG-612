# Architecture

## Executive Summary

The ibe160 project is a minimalist, AI-enhanced web application for task management. This architecture document outlines the technical decisions to build a Python Flask application with TailwindCSS for the frontend, utilizing SQLite for data persistence, Flask session-based authentication, and integrating with the Google Gemini API via a backend proxy for intelligent task categorization. The application will be deployed on Render, focusing on a robust and maintainable solution for the MVP.

## Project Initialization

First implementation story should execute the manual setup for a Flask with TailwindCSS starter:

```bash
mkdir flask_tailwind_app
cd flask_tailwind_app
python -m venv venv
./venv/bin/pip install Flask Flask-SQLAlchemy
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

| Category                   | Decision                                                | Version  | Verification Date | Affects Epics | Rationale                                                                        |
| -------------------------- | ------------------------------------------------------- | -------- | ----------------- | ------------- | -------------------------------------------------------------------------------- |
| Language                   | Python                                                  | 3.14     | 2025-11-30        | All           | Latest stable version, ensures access to modern features and security updates.     |
| Backend Framework          | Flask                                                   | 3.1.2    | 2025-11-30        | All           | Minimalist, mature, and well-suited for REST APIs.                               |
| ORM                        | Flask-SQLAlchemy                                        | 3.1.2    | 2025-11-30        | 1, 3          | Integrates SQLAlchemy with Flask, simplifying database operations.               |
| Frontend Styling           | TailwindCSS                                             | 3.4.16   | 2025-11-30        | All           | Utility-first CSS framework for rapid UI development.                            |
| JS Runtime / Build Tooling | Node.js                                                 | 24.11.1  | 2025-11-30        | All           | Required for frontend asset compilation (TailwindCSS). Using LTS for stability.  |
| Data Persistence           | SQLite                                                  | 3.45     | (Bundled)         | 1, 2, 3       | Simple, file-based, serverless, and perfect for a single-user MVP.               |
| API Pattern                | REST API                                                | (N/A)    | (N/A)             | 2, 3          | Standard, well-understood pattern for web apps and a core strength of Flask.     |
| AI Application Integration | Direct Gemini API calls from backend (google-genai lib) | 1.52.0   | 2025-11-30        | 2             | Securely handles API keys on the backend with a robust fallback strategy.        |
| Authentication             | Flask Session-based authentication                      | (N/A)    | (N/A)             | 1             | Simple to implement and sufficient for securing a single-user application in MVP. |
| Deployment Target          | Render                                                  | (N/A)    | (N/A)             | All           | Beginner-friendly platform with a free tier and easy deployment from GitHub.     |

## Project Structure

```
/
|-- .env                    # Local environment variables (DO NOT COMMIT)
|-- .env.example            # Example environment variables
|-- .gitignore
|-- app.py                  # Main Flask application, routes, and API logic
|-- ai_service.py           # Module for Gemini API calls
|-- package.json
|-- postcss.config.js
|-- requirements.txt        # Python dependencies
|-- tailwind.config.js
|-- venv/                     # Virtual environment
|-- instance/
|   |-- tasks.db            # SQLite database file
|-- static/
|   |-- css/
|   |   |-- input.css       # TailwindCSS source file
|   |-- dist/
|       |-- output.css      # Compiled CSS
|-- templates/
|   |-- base.html           # Base layout template
|   |-- index.html          # Main dashboard view
|   |-- ... (other views)
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

| Technology          | Version | Role                            |
| ------------------- | ------- | ------------------------------- |
| Python              | 3.14    | Backend Language                |
| Flask               | 3.1.2   | Backend Framework               |
| Flask-SQLAlchemy    | 3.1.2   | ORM (Object-Relational Mapper)  |
| Node.js             | 24.11.1 | JS Runtime / Build Tooling      |
| TailwindCSS         | 3.4.16  | Frontend Styling                |
| SQLite              | 3.45    | Data Persistence                |
| Google Gemini API   | v1.52.0 | AI Integration                  |
| Render              | (N/A)   | Deployment Platform             |

### Integration Points

-   Frontend (HTML templates) <-> Backend (`app.py` REST API) for all task management and AI suggestion requests.
-   Backend (`ai_service.py`) <-> Google Gemini API for AI-powered suggestions.

## Novel Pattern Designs

### Pattern: AI-Suggestion Flow (Magic Fill)

-   **Purpose**: To streamline task creation by using AI to automatically suggest a `label` and `priority` based on the user's task `title`. This reduces manual effort and encourages consistent task categorization.
-   **Affects Epics**: Epic 2.
-   **Components**:
    -   **Frontend**: A "Suggest" button or similar trigger next to the task title input field.
    -   **Backend API**: A new Flask route at `POST /api/suggest`.
    -   **AI Service**: The `ai_service.py` module containing the logic to call the Gemini API.
    -   **Fallback**: A simple, rule-based mechanism within `ai_service.py` to provide suggestions if the AI call fails.

#### Data Flow and Implementation Guide

1.  **Trigger (Frontend)**: The user types a task title (e.g., "Write weekly report for sales team") and clicks the "Suggest" button. The frontend disables the button and shows a loading indicator.
2.  **API Request (Frontend)**: The frontend sends a `POST` request to `/api/suggest` with a JSON body: `{ "title": "Write weekly report for sales team" }`.
3.  **Request Handling (Backend)**: The `/api/suggest` route in `app.py` receives the request. It calls the `get_ai_suggestions()` function from `ai_service.py`, passing the title.
4.  **AI Service Logic (`ai_service.py`)**:
    -   The `get_ai_suggestions(title)` function constructs a precise prompt for the Gemini API.
        -   **Prompt Example**: `Given the task title, suggest a priority (Low, Medium, High) and a relevant category label. Return ONLY a JSON object with "priority" and "label" keys. Task Title: "{title}"`
    -   It then attempts to call the Gemini API.
5.  **Response Handling (`ai_service.py`)**:
    -   **On AI Success**: If the API returns a valid JSON object (e.g., `{ "priority": "High", "label": "Reporting" }`), the service returns this dictionary to the backend route.
    -   **On AI Failure (Fallback)**: If the API call fails (error, timeout, empty response, malformed JSON), the function executes the **Rule-based Fallback** and returns its output.
6.  **API Response (Backend)**: The `app.py` route receives the dictionary from the AI service and returns it to the frontend as a JSON response with a 200 status code.
7.  **Display (Frontend)**: The frontend receives the JSON response. It re-enables the "Suggest" button, hides the loading indicator, and populates the "Priority" and "Label" input fields with the suggested values.

#### Edge Cases and Fallback Mechanism

-   **Goal**: To ensure the feature is resilient and provides a baseline level of utility even if the AI service is unavailable.
-   **Fallback Trigger**: The fallback is triggered by any of these conditions in `ai_service.py`:
    -   The Gemini API returns a non-200 status code.
    -   The API response is empty or not valid JSON.
    -   The API response is missing the `priority` or `label` keys.
    -   The request to the Gemini API times out (e.g., after 5 seconds).
-   **Rule-based Fallback Logic**: A simple keyword-based system.
    -   If "report", "review", or "meeting" is in the title -> `priority: "Medium"`, `label: "Planning"`
    -   If "fix", "bug", "issue", or "error" is in the title -> `priority: "High"`, `label: "Engineering"`
    -   If "create", "design", or "develop" is in the title -> `priority: "Medium"`, `label: "Development"`
    -   **Default**: If no keywords match -> `priority: "Low"`, `label: "General"`
-   **Frontend Behavior on Error**: If the `/api/suggest` endpoint itself returns an error (e.g., 500), the frontend should briefly show an error message (e.g., "Suggestion failed") and re-enable the suggestion button. It should not block the user from manually filling in the fields.

## Implementation Patterns

These patterns ensure consistent implementation across all AI agents:

-   Naming: Snake_case for Python/DB, Kebab-case for CSS, Plural Kebab-case for API.
-   Structure: Flask standard with `ai_service.py`, `templates/`, `static/`, `tests/`.
-   Format: JSON for API, ISO 8601 for dates/times.
-   Communication: RESTful HTTP (FE-BE), Python function calls (BE-AI).
-   Location: `instance/tasks.db`, `static/dist/`.

## Lifecycle Patterns

### Application States

-   **Loading State**: When the application is fetching data (e.g., initial task list, AI suggestions), a visual indicator must be displayed.
    -   **UI Example**: A subtle pulsing skeleton screen or a spinner overlay on the relevant UI container. The rest of the UI should be disabled to prevent interactions.
-   **Empty State**: When a list or data set is empty (e.g., no tasks), a helpful message and a call-to-action must be displayed.
    -   **UI Example**: "No tasks yet. Add one to get started!" with a prominent "Add Task" button.
-   **Error State**: When an API call or an internal operation fails, a non-intrusive notification should be displayed.
    -   **UI Example**: A temporary toast notification at the top of the screen (e.g., "Error: Could not save task."). The UI should revert to its previous state gracefully.

## Consistency Patterns

### Logging

-   **Purpose**: To ensure logs are structured, consistent, and machine-readable.
-   **Library**: Python's built-in `logging` module.
-   **Format**: All logs should be in JSON format.
    -   `{ "timestamp": "YYYY-MM-DDTHH:MM:SSZ", "level": "INFO", "message": "User logged in", "details": { "user_id": 123 } }`
-   **Levels**:
    -   `INFO`: For significant application events (e.g., user login, startup).
    -   `WARNING`: For non-critical issues or potential problems (e.g., AI fallback triggered).
    -   `ERROR`: For application errors and exceptions. Include stack traces.

### User-Facing Errors

-   **Purpose**: To provide clear, non-technical, and helpful error messages to the user.
-   **Format**: Use simple language and avoid technical jargon.
-   **Examples**:
    -   **Instead of**: "500 Internal Server Error"
    -   **Use**: "Something went wrong on our end. Please try again in a moment."
    -   **Instead of**: "Failed to fetch"
    -   **Use**: "Could not connect to the server. Please check your internet connection."

## Data Architecture

-   **Database:** SQLite (`instance/tasks.db`).
-   **ORM:** Flask-SQLAlchemy will be used to manage the database schema and interactions.

### Data Models

#### `Task` Model
This model represents a single to-do item in the application.

| Column       | Type             | Constraints              | Description                                  |
| ------------ | ---------------- | ------------------------ | -------------------------------------------- |
| `id`         | `Integer`        | Primary Key, Autoincrement | Unique identifier for the task.              |
| `title`      | `String(200)`    | Not Nullable             | The main description of the task.            |
| `notes`      | `Text`           | Nullable                 | Additional details about the task.           |
| `due_date`   | `Date`           | Nullable                 | When the task is due.                        |
| `priority`   | `String(20)`     | Not Nullable, Default='Medium' | Priority level (e.g., Low, Medium, High).   |
| `label`      | `String(50)`     | Nullable                 | A category for the task (e.g., Work, Personal).|
| `is_done`    | `Boolean`        | Not Nullable, Default=False    | Whether the task has been completed.         |
| `created_at` | `DateTime`       | Not Nullable, Default=now()  | Timestamp when the task was created.         |

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

-   Python 3.14+
-   Node.js 24.11.1+ (LTS)

### Setup Commands

```bash
mkdir flask_tailwind_app
cd flask_tailwind_app
python -m venv venv
./venv/bin/pip install Flask Flask-SQLAlchemy
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
