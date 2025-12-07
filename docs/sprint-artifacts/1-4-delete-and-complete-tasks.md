# User Story: Story 1.4: Delete and Complete Tasks

Status: review

As a user, I want to delete tasks I no longer need and mark tasks as complete, so that I can manage my task list effectively.

## Requirements Context

This story implements the "Delete" and "Update" (for completion) functionality for tasks as defined in the Product Brief's MVP Core Features and the Epic 1 Technical Specification. It aligns with the REST API pattern outlined in the Architecture Document for `DELETE /api/tasks/<id>` and `PUT /api/tasks/<id>` (for `is_done` status). The UI interaction for deleting and completing tasks is handled via the `Task Card` component.

## Acceptance Criteria

**Given** I am on the main dashboard
**When** I click a "Delete" button (an icon that appears on `Task Card` hover) on a task
**Then** I am prompted for confirmation.
**And** upon confirmation, the task is permanently removed from the database.
**When** I check a checkbox on a task
**Then** the task is marked as complete (`is_done` = true).
**And** the completed task is visually distinguished from active tasks (e.g., strikethrough, grayed out). When a task is marked complete, the title text receives a strikethrough effect and a muted color.

## Tasks / Subtasks

*   **1. Frontend Implementation (Delete Tasks):**
    *   [x] Implement a confirmation dialog when the delete icon on a `Task Card` is clicked.
    *   [x] On confirmation, send a `DELETE /api/tasks/<id>` request to the backend.
    *   [x] On successful deletion, remove the task from the dashboard UI.
*   **2. Frontend Implementation (Complete Tasks):**
    *   [x] Implement the checkbox on the `Task Card`.
    *   [x] On checkbox click, send a `PUT /api/tasks/<id>` request with `is_done: true`.
    *   [x] On successful update, apply visual distinction (strikethrough, muted color) to the completed task on the UI.
*   **3. Backend API Endpoint:**
    *   [x] Create `DELETE /api/tasks/<id>` endpoint in `app.py`.
    *   [x] Delete the `Task` object from the database using `Flask-SQLAlchemy`.
    *   [x] Return `204 No Content` on successful deletion.
    *   [x] Modify `PUT /api/tasks/<id>` endpoint to handle `is_done` field updates.

## Dev Notes

### Constraints & Patterns:
- **API Pattern:** REST API for deleting (`DELETE /api/tasks/<id>`) and updating (`PUT /api/tasks/<id>`) task status. [Source: docs/fase-3-solutioning/architecture.md#API Pattern]
- **Data Model:** Use the existing `Task` SQLAlchemy model in `app.py`. Update `is_done` field. [Source: docs/fase-3-solutioning/architecture.md#Data Models]
- **Frontend UI:** `Task Card` component will handle delete icon and completion checkbox. Visual distinction for completed tasks.
- **Confirmation Pattern:** Implement a confirmation dialog for destructive actions (deletion).
- **Implementation:** Adhere to Python/Flask implementation patterns.

### Source Tree Components to Touch:
- `app.py`: For the `DELETE /api/tasks/<id>` and `PUT /api/tasks/<id>` endpoints.
- `templates/`: For updating the `Task Card` rendering to show delete icon on hover, checkbox, and visual distinction for completed tasks.
- `static/css/input.css` and `static/dist/output.css`: For styling the delete icon, checkbox, and completed task visual.

### Testing Standards Summary:
- **API/Integration Tests:** Cover `DELETE /api/tasks/<id>` and `PUT /api/tasks/<id>` (for `is_done`) endpoints.
- **E2E Tests:** Test the full user flow of deleting a task with confirmation, marking a task as complete, and verifying visual changes.

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
- [1-4-delete-and-complete-tasks.context.xml](1-4-delete-and-complete-tasks.context.xml)

### Agent Model Used

gemini-1.5-pro

### File List
- app.py
- templates/index.html

### Debug Log References

### Completion Notes
- Implemented `DELETE /api/tasks/<id>` endpoint in `app.py` to delete tasks from the database.
- Modified `PUT /api/tasks/<id>` in `app.py` to handle `is_done` field updates for task completion.
- Modified `templates/index.html` to include JavaScript logic for:
    - Confirmation dialog and API call for task deletion.
    - Checkbox interaction to toggle `is_done` status via `PUT` request.
    - Visual distinction for completed tasks (strikethrough/muted color).

## Change Log

| Version | Date       | Change                                                                 | Author |
| :------ | :--------- | :--------------------------------------------------------------------- | :----- |
| 1.1     | 2025-12-07 | Implemented delete and complete functionalities for tasks.             | BIP    |
