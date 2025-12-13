# User Story: Story 1.1: Project Foundation & Database Setup

As a developer, I want to set up the initial Flask project structure, database model, and dependencies, so that I have a foundation for building the application.

## Requirements Context

This story is foundational to Epic 1: "Foundational Setup & Core Task Management". It directly addresses the initial project setup, database schema definition, and dependency management as detailed in the Architecture Document (`docs/fase-3-solutioning/architecture.md`) and elaborated in the Epic Tech Spec for Epic 1 (`docs/sprint-artifacts/tech-spec-epic-1.md`). The PRD implicitly requires this setup to support all subsequent functional requirements. The UX Design Specification's reliance on a Flask/TailwindCSS frontend also necessitates this setup.

## Acceptance Criteria

1.  **AC1**: The project structure adheres to the layout specified in the Architecture Document, including `app.py`, `instance/`, `static/`, `templates/`.
2.  **AC2**: A Python virtual environment is initialized, and `Flask`, `Flask-SQLAlchemy` are installed and listed in `requirements.txt`.
3.  **AC3**: Frontend build tools (`npm`, `tailwindcss`, `postcss`, `autoprefixer`) are installed, and `tailwind.config.js` is initialized and configured with the specified theme extensions (primary color, font family, border-radius).
4.  **AC4**: The `Task` SQLAlchemy model is defined with `id`, `title`, `notes`, `due_date`, `priority`, `label`, `is_done`, and `created_at` fields, as detailed in the Architecture Document.
5.  **AC5**: An empty `tasks.db` SQLite database file can be created within the `instance/` directory using the application's setup logic.
6.  **AC6**: The `.gitignore` file is updated to correctly ignore generated files and directories such as `venv/`, `__pycache__/`, `instance/*.db`, `node_modules/`, and `static/dist/`.

## Tasks / Subtasks

*   **1. Project Initialization:**
    *   [ ] Initialize Python virtual environment.
    *   [ ] Install Python dependencies: `Flask==3.1.2`, `Flask-SQLAlchemy==3.1.1`.
    *   [ ] Create `requirements.txt` based on installed Python packages.
    *   [ ] Initialize Node.js project (`npm init -y`).
    *   [ ] Install Node.js dev dependencies: `tailwindcss@^3.4.16`, `postcss@^8.5.6`, `autoprefixer@^10.4.22`.
    *   [ ] Initialize Tailwind CSS (`npx tailwindcss init -p`).
*   **2. Project Structure Creation:**
    *   [ ] Create core directories: `instance/`, `static/`, `static/css/`, `static/dist/`, `templates/`.
    *   [ ] Create an empty `app.py` file.
    *   [ ] Create `static/css/input.css` with `@tailwind base; @tailwind components; @tailwind utilities;`.
*   **3. Configuration Files Setup:**
    *   [ ] Configure `tailwind.config.js` to match the UX design specification for `primary` color (`#607AFB`), `display` font family (`Sora`), and `borderRadius` values.
    *   [ ] Update `.gitignore` to include `venv/`, `__pycache__/`, `instance/*.db`, `node_modules/`, `static/dist/`, `.env`, `.env.local`.
*   **4. Database Model Definition:**
    *   [ ] Define the `Task` SQLAlchemy model in `app.py` (or a dedicated `models.py` file if preferred, ensuring proper import into `app.py`).
    *   [ ] Add basic Flask-SQLAlchemy initialization and database creation (`db.create_all()`) logic to `app.py` for setup.
*   **5. Verification & Testing:**
    *   [ ] **Unit Test**: Verify `Task` model fields and types.
    *   [ ] **Manual Test**: Run the Flask app's initialization script to confirm `tasks.db` is created and the directory structure is correct.
    *   [ ] **Manual Test**: Verify TailwindCSS compilation works by running `npm run build:css` (or equivalent) and checking `static/dist/output.css`.

## Dev Notes

- Relevant architecture patterns and constraints
- Source tree components to touch
- Testing standards summary

## Project Structure Alignment

This story is responsible for establishing the core project structure as defined in `docs/fase-3-solutioning/architecture.md`. Key elements include:
*   **Python Virtual Environment**: Creation of `venv/` and installation of core Python dependencies.
*   **Main Flask Application**: `app.py` as the entry point for the Flask application.
*   **Database**: Initialization of `instance/tasks.db` for SQLite.
*   **Frontend Assets**: Setting up `static/` (with `input.css` and `dist/output.css`) and `templates/` directories.
*   **Configuration Files**: `requirements.txt` (to be created), `package.json`, `tailwind.config.js`, `postcss.config.js`.

This story ensures strict adherence to the planned directory layout and naming conventions from the architecture.

### References

- Cite all technical details with source paths and sections, e.g. [Source: docs/<file>.md#Section]

## Dev Agent Record

### Context Reference

<!-- Path(s) to story context XML will be added here by context workflow -->

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List
