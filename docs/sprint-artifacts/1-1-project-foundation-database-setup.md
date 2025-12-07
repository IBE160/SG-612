# User Story: Story 1.1: Project Foundation & Database Setup

Status: review

## Dev Agent Record

### Context Reference
- [1-1-project-foundation-database-setup.context.xml](1-1-project-foundation-database-setup.context.xml)

### Debug Log References

### Completion Notes
- Updated `Flask-SQLAlchemy` dependency from `3.1.2` to `3.1.1` due to version unavailability, as per user's instruction.

### File List
- tests/test_app.py

## Change Log

| Version | Date       | Change                                                                 | Author |
| :------ | :--------- | :--------------------------------------------------------------------- | :----- |
| 1.1     | 2025-12-07 | Corrected `Flask-SQLAlchemy` version to `3.1.1` due to installation issue. | BIP    |

As a developer, I want to set up the initial Flask project structure, database model, and dependencies, so that I have a foundation for building the application.

## Requirements Context

This story is foundational to Epic 1: "Foundational Setup & Core Task Management". It directly addresses the initial project setup, database schema definition, and dependency management as detailed in the Architecture Document (`docs/fase-3-solutioning/architecture.md`) and elaborated in the Epic Tech Spec for Epic 1 (`docs/sprint-artifacts/tech-spec-epic-1.md`). The PRD implicitly requires this setup to support all subsequent functional requirements. The UX Design Specification's reliance on a Flask/TailwindCSS frontend also necessitates this setup.

## Project Structure Alignment

This story is responsible for establishing the core project structure as defined in `docs/fase-3-solutioning/architecture.md`. Key elements include:
*   **Python Virtual Environment**: Creation of `venv/` and installation of core Python dependencies.
*   **Main Flask Application**: `app.py` as the entry point for the Flask application.
*   **Database**: Initialization of `instance/tasks.db` for SQLite.
*   **Frontend Assets**: Setting up `static/` (with `input.css` and `dist/output.css`) and `templates/` directories.
*   **Configuration Files**: `requirements.txt` (to be created), `package.json`, `tailwind.config.js`, `postcss.config.js`.

This story ensures strict adherence to the planned directory layout and naming conventions from the architecture.

## Acceptance Criteria

1.  **AC1**: The project structure adheres to the layout specified in the Architecture Document, including `app.py`, `instance/`, `static/`, `templates/`.
2.  **AC2**: A Python virtual environment is initialized, and `Flask`, `Flask-SQLAlchemy` are installed and listed in `requirements.txt`.
3.  **AC3**: Frontend build tools (`npm`, `tailwindcss`, `postcss`, `autoprefixer`) are installed, and `tailwind.config.js` is initialized and configured with the specified theme extensions (primary color, font family, border-radius).
4.  **AC4**: The `Task` SQLAlchemy model is defined with `id`, `title`, `notes`, `due_date`, `priority`, `label`, `is_done`, and `created_at` fields, as detailed in the Architecture Document.
5.  **AC5**: An empty `tasks.db` SQLite database file can be created within the `instance/` directory using the application's setup logic.
6.  **AC6**: The `.gitignore` file is updated to correctly ignore generated files and directories such as `venv/`, `__pycache__/`, `instance/*.db`, `node_modules/`, and `static/dist/`.

## Tasks / Subtasks

*   **1. Project Initialization:**
    *   [x] Initialize Python virtual environment.
    *   [x] Install Python dependencies: `Flask==3.1.2`, `Flask-SQLAlchemy==3.1.1`.
    *   [x] Create `requirements.txt` based on installed Python packages.
    *   [x] Initialize Node.js project (`npm init -y`).
    *   [x] Install Node.js dev dependencies: `tailwindcss@^3.4.16`, `postcss@^8.5.6`, `autoprefixer@^10.4.22`.
    *   [x] Initialize Tailwind CSS (`npx tailwindcss init -p`).
*   **2. Project Structure Creation:**
    *   [x] Create core directories: `instance/`, `static/`, `static/css/`, `static/dist/`, `templates/`.
    *   [x] Create an empty `app.py` file.
    *   [x] Create `static/css/input.css` with `@tailwind base; @tailwind components; @tailwind utilities;`.
*   **3. Configuration Files Setup:**
    *   [x] Configure `tailwind.config.js` to match the UX design specification for `primary` color (`#607AFB`), `display` font family (`Sora`), and `borderRadius` values.
    *   [x] Update `.gitignore` to include `venv/`, `__pycache__/`, `instance/*.db`, `node_modules/`, and `static/dist/`, `.env`, `.env.local`.
*   **4. Database Model Definition:**
    *   [x] Define the `Task` SQLAlchemy model in `app.py` (or a dedicated `models.py` file if preferred, ensuring proper import into `app.py`).
    *   [x] Add basic Flask-SQLAlchemy initialization and database creation (`db.create_all()`) logic to `app.py` for setup.
*   **5. Verification & Testing:**
    *   [x] **Unit Test**: Verify `Task` model fields and types.
    *   [x] **Manual Test**: Run the Flask app's initialization script to confirm `tasks.db` is created and the directory structure is correct.
    *   [ ] **Manual Test**: Verify TailwindCSS compilation works by running `npm run build:css` (or equivalent) and checking `static/dist/output.css`.

### Completion Notes
- Updated `Flask-SQLAlchemy` dependency from `3.1.2` to `3.1.1` due to version unavailability, as per user's instruction.
- Created `tests/test_app.py` and implemented unit tests for `Task` model fields and types. All tests passed.
- **Note:** `Manual Test: Verify TailwindCSS compilation` is currently blocked due to `tailwindcss` executable not being recognized in the environment. Manual creation of config files was performed..
