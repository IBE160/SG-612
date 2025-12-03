# Epic Technical Specification: {{epic_title}}

Date: {{date}}
Author: {{user_name}}
Epic ID: {{epic_id}}
Status: Draft

---

## Overview

This epic, "Foundational Setup & Core Task Management," lays the groundwork for the Smart To-Do AI application. It focuses on establishing the essential technical infrastructure and implementing the core Create, Read, Update, and Delete (CRUD) functionality for tasks. This forms the backbone of the application, enabling users to manage their to-do items before the introduction of more advanced AI features.

## Objectives and Scope

*In-Scope:*
*   Setting up the Flask project structure, including the virtual environment, dependencies, and database.
*   Defining the `Task` data model.
*   Implementing the UI and API for creating, viewing, updating, and deleting tasks.
*   Implementing the ability to mark tasks as complete.
*Out-of-Scope:*
*   Any AI-powered features, including "Magic Fill".
*   Smart lists and advanced filtering.
*   User authentication.

## System Architecture Alignment

This epic directly implements the foundational components outlined in the architecture document. It will create the main `app.py`, the `Task` model in `instance/tasks.db` as defined by the SQLAlchemy ORM, and the basic HTML templates in the `templates/` directory styled with TailwindCSS. The API endpoints for `/api/tasks` (POST, GET, PUT, DELETE) will be created as specified in the REST API pattern.

## Detailed Design

### Services and Modules

*   **`app.py`**: The main Flask application entry point. It will handle routing for both the web interface and the REST API, and will contain the core business logic for task management.
*   **`instance/tasks.db`**: The SQLite database file where all task data will be stored.
*   **`templates/` directory**: Will contain all user-facing HTML files, including a `base.html` for layout and `index.html` for the main task view.
*   **`static/` directory**: Will house all compiled CSS and any other static assets.

### Data Models and Contracts

The core data model for this epic is the `Task` model, as defined in the architecture.

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

### APIs and Interfaces

This epic will establish the foundational REST API for task management.

*   `POST /api/tasks`: Creates a new task.
    *   **Request Body**: `{ "title": "...", "notes": "...", "due_date": "..." }`
    *   **Success Response**: `201 Created` with `{ "data": { ...task object... } }`
*   `GET /api/tasks`: Retrieves a list of all tasks.
    *   **Success Response**: `200 OK` with `{ "data": [ ...task objects... ] }`
*   `PUT /api/tasks/<id>`: Updates an existing task (including marking as complete).
    *   **Request Body**: `{ "title": "...", "notes": "...", "due_date": "...", "is_done": ... }`
    *   **Success Response**: `200 OK` with `{ "data": { ...task object... } }`
*   `DELETE /api/tasks/<id>`: Deletes a task.
    *   **Success Response**: `204 No Content`

### Workflows and Sequencing

1.  **Create Task Workflow**: User clicks "Add Task" button -> A UI modal appears -> User fills the form and submits -> Frontend sends a `POST` request to `/api/tasks` -> On success, the modal closes and the task list UI is updated.
2.  **View Tasks Workflow**: On initial application load -> Frontend sends a `GET` request to `/api/tasks` -> The list of tasks is rendered in the main view.
3.  **Update Task Workflow**: User clicks an "Edit" affordance on a task -> A UI modal appears pre-filled with task data -> User modifies the form and submits -> Frontend sends a `PUT` request to `/api/tasks/<id>` -> On success, the modal closes and the task list UI is updated.
4.  **Delete Task Workflow**: User clicks a "Delete" affordance on a task -> A confirmation dialog appears -> On confirmation, frontend sends a `DELETE` request to `/api/tasks/<id>` -> On success, the task is removed from the UI.
5.  **Complete Task Workflow**: User clicks the checkbox on a task -> Frontend sends a `PUT` request to `/api/tasks/<id>` with `is_done: true` -> The UI updates to visually reflect the completed state (e.g., strikethrough).

## Non-Functional Requirements

### Performance

*   **API Response Time**: All CRUD API endpoints (`/api/tasks`) must respond in under 500ms under normal load.
*   **Initial Page Load**: The main dashboard page (`index.html` with task data) should render in under 2 seconds.

### Security

*   **Data Validation**: All incoming API data must be validated on the backend to ensure type and format correctness before being processed.
*   **Output Encoding**: All dynamic data rendered in HTML templates must be properly escaped to prevent Cross-Site Scripting (XSS) attacks.

### Reliability/Availability

*   **Database Integrity**: The application must handle database sessions correctly to prevent data corruption. Standard transaction management (commit/rollback) should be used for all database writes.

### Observability

*   **Structured Logging**: The Flask application should implement structured (JSON format) logging for all API requests, recording the endpoint, status code, and response time. This aligns with the consistency pattern defined in the architecture.

## Dependencies and Integrations

### Frontend / Build
*   **`tailwindcss`**: `^4.1.17` - For utility-first CSS styling.
*   **`postcss`**: `^8.5.6` - For transforming CSS with plugins.
*   **`autoprefixer`**: `^10.4.22` - For adding vendor prefixes to CSS.

### Backend (from Architecture Document)
*Note: `requirements.txt` was not found at the project root.*
*   **`Flask`**: The core backend framework.
*   **`Flask-SQLAlchemy`**: ORM for database interaction.

### Testing
*   **`@playwright/test`**: `1.57.0` - For end-to-end testing.
*   **`@faker-js/faker`**: `8.4.1` - For generating test data.

## Acceptance Criteria (Authoritative)

1.  The project structure must be created as defined in the architecture document.
2.  A SQLite database file (`tasks.db`) must be created within the `instance/` directory.
3.  The `Task` model must be defined in SQLAlchemy with all specified fields (`id`, `title`, `notes`, `due_date`, `priority`, `label`, `is_done`, `created_at`).
4.  A user can create a new task via the UI, which calls `POST /api/tasks` and receives a `201 Created` response.
5.  A user can view all tasks, which are fetched from `GET /api/tasks` and rendered on the main dashboard.
6.  A user can update a task's details via the UI, which calls `PUT /api/tasks/<id>`.
7.  A user can delete a task via the UI (with confirmation), which calls `DELETE /api/tasks/<id>`.
8.  A user can mark a task as complete via a checkbox, which calls `PUT /api/tasks/<id>` with `is_done: true`.
9.  Completed tasks are visually distinguished in the UI with a strikethrough and muted color.
10. The "Add Task" modal can be dismissed with the Escape key or by clicking the modal backdrop.

## Traceability Mapping

| AC # | Spec Section(s)                                   | Component(s)/API(s)                                 | Test Idea                                    |
| :--- | :------------------------------------------------ | :-------------------------------------------------- | :------------------------------------------- |
| 1-3  | Detailed Design > Data Models                     | Project structure, `instance/tasks.db`, SQLAlchemy Model | Unit test for `Task` model definition.       |
| 4    | Detailed Design > APIs > `POST /api/tasks`        | `app.py`, "Add Task" Modal UI                       | API test for task creation, E2E test for UI flow. |
| 5    | Detailed Design > APIs > `GET /api/tasks`         | `app.py`, Main dashboard UI (Task Card list)        | API test for fetching tasks, E2E test for list display. |
| 6    | Detailed Design > APIs > `PUT /api/tasks/<id>`    | `app.py`, "Edit Task" Modal UI                      | API test for task update, E2E test for UI flow. |
| 7    | Detailed Design > APIs > `DELETE /api/tasks/<id>` | `app.py`, Task Card UI                              | API test for task deletion, E2E test for UI flow. |
| 8-9  | Detailed Design > APIs > `PUT /api/tasks/<id>`    | `app.py`, Task Card UI                              | API test for completion status, E2E test for visual change. |
| 10   | UX Design Spec > Modal Patterns                   | "Add Task" Modal UI                                 | E2E test for modal dismissal behavior.       |

## Risks, Assumptions, Open Questions

*   **Risk**: The `requirements.txt` file is missing. This could lead to incorrect or incompatible versions of backend dependencies being installed.
    *   **Mitigation**: The first development task should be to create a `requirements.txt` file with `Flask` and `Flask-SQLAlchemy` and their versions as specified in the architecture document.
*   **Assumption**: The frontend will be a simple vanilla JavaScript implementation making direct API calls, without a complex framework like React or Vue.
*   **Question**: What is the specific UI/UX for displaying API error states? While the architecture mentions error states, the detailed design for how they appear to the user (e.g., toast message content and style) for this epic needs clarification.

## Test Strategy Summary

The test strategy will follow the pyramid defined in the system architecture:
*   **Unit Tests**: Focus on the SQLAlchemy `Task` model definition to ensure all fields, types, and constraints are correct.
*   **API/Integration Tests**: This will be the primary focus for this epic. Tests will cover all CRUD operations on the `/api/tasks` endpoint, including creating tasks, validating responses, updating, deleting, and checking completion status. These will be written using `pytest`.
*   **E2E Tests**: A single, critical path E2E test will be created to cover the primary user flow: 1) Click "Add Task", 2) Fill out and save the form, 3) Verify the new task appears in the list, 4) Mark the task as complete, 5) Verify the completed visual state. This will be implemented using Playwright.
