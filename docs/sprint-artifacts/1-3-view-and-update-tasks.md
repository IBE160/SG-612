# User Story: Story 1.3: View and Update Tasks

Status: ready-for-dev

As a user, I want to view the details of my tasks and update them, so that I can keep my task list accurate.

## Requirements Context

This story implements the "Read" and "Update" functionality for tasks as defined in the Product Brief's MVP Core Features and the "View Tasks Workflow" and "Update Task Workflow" in Epic 1 Technical Specification. It aligns with the REST API pattern outlined in the Architecture Document for `GET /api/tasks` and `PUT /api/tasks/<id>`. The UI interaction for viewing and editing tasks is detailed in the UX Design Specification's "Spacious & Focused List" design direction and the `Task Card` component.

## Acceptance Criteria

**Given** I am on the main dashboard
**When** I view my task list (a 'Spacious & Focused List' of `Task Card` components)
**Then** I can see the title, due date, label, and priority for each task. Each card shows a completion checkbox, task title, due date, and pill-shaped badges for label/priority. Edit/delete icons appear on hover.
**When** I click on a task to edit it
**Then** a modal appears with the task's details pre-filled.
**And** I can modify the title, notes, due date, label, and priority.
**When** I save my changes
**Then** the task is updated in the database and the dashboard reflects the changes.

## Tasks / Subtasks

*   **1. Frontend Implementation (View Tasks):**
    *   [ ] On dashboard load, fetch all tasks by calling `GET /api/tasks`.
    *   [ ] Implement the "Spacious & Focused List" layout using TailwindCSS.
    *   [ ] Create the `Task Card` component to display individual tasks.
    *   [ ] Each `Task Card` should display `title`, `due_date`, `label` (badge), and `priority` (badge).
    *   [ ] Implement hover effect to show edit and delete icons on the `Task Card`.
*   **2. Frontend Implementation (Update Tasks):**
    *   [ ] Clicking a `Task Card` opens an "Edit Task" modal.
    *   [ ] Pre-fill the modal form with the selected task's data.
    *   [ ] On form submission, send a `PUT /api/tasks/<id>` request with the updated data.
    *   [ ] On successful update, close the modal and refresh the task list on the dashboard.
*   **3. Backend API Endpoint:**
    *   [ ] Create `GET /api/tasks` endpoint in `app.py` to retrieve all tasks.
    *   [ ] Create `PUT /api/tasks/<id>` endpoint in `app.py` to update a specific task.
    *   [ ] Handle incoming JSON request body for task updates.
    *   [ ] Update the `Task` object in the database using `Flask-SQLAlchemy`.
    *   [ ] Return the updated task object.

## Dev Notes

### Constraints & Patterns:
- **API Pattern:** REST API for reading (`GET /api/tasks`) and updating (`PUT /api/tasks/<id>`) tasks. [Source: docs/fase-3-solutioning/architecture.md#API Pattern]
- **Data Model:** Use the existing `Task` SQLAlchemy model in `app.py`. [Source: docs/fase-3-solutioning/architecture.md#Data Models]
- **Frontend UI:** Implement the "Spacious & Focused List" layout and `Task Card` component using TailwindCSS as specified in the UX Design Spec.
- **Modal Behavior:** Use a standard modal for editing tasks.
- **Implementation:** Adhere to Python/Flask implementation patterns (naming, structure, etc.).

### Source Tree Components to Touch:
- `app.py`: For the `GET /api/tasks` and `PUT /api/tasks/<id>` endpoints.
- `templates/`: For the main dashboard to render the task list and for the "Edit Task" modal HTML.
- `static/css/input.css` and `static/dist/output.css`: For styling the `Task Card` and modal.

### Testing Standards Summary:
- **API/Integration Tests:** Cover `GET /api/tasks` and `PUT /api/tasks/<id>` endpoints.
- **E2E Tests:** Test the full user flow of viewing the task list, opening the edit modal, updating a task, and verifying the change on the dashboard.

## Project Structure Alignment

This story aligns with the established Flask project structure by extending `app.py` with new API endpoints, and adding/modifying HTML templates in `templates/` and CSS in `static/` to support the UI components.

### References

- [Source: docs/product-brief.md#MVP Scope]
- [Source: docs/fase-3-solutioning/architecture.md#API Pattern]
- [Source: docs/fase-3-solutioning/architecture.md#Data Models]
- [Source: docs/fase-3-solutioning/architecture.md#API Contracts]
- [Source: docs/fase-2-planning/ux-design-specification.md#Design Direction]
- [Source: docs/fase-2-planning/ux-design-specification.md#Component Library]
- [Source: docs/sprint-artifacts/tech-spec-epic-1.md#APIs and Interfaces]
- [Source: docs/sprint-artifacts/tech-spec-epic-1.md#Workflows and Sequencing]

## Dev Agent Record

### Context Reference
- [1-3-view-and-update-tasks.context.xml](1-3-view-and-update-tasks.context.xml)

### Agent Model Used

gemini-1.5-pro

### Debug Log References

### Completion Notes List

### File List
