# User Story: 3.3: Manual Filtering and Sorting
Status: ready-for-dev

As a user, I want flexible manual filtering and sorting options for my tasks, so that I can easily customize my task view and maintain full control over my workload.

## Requirements Context

This story implements the manual filtering and sorting functionalities as part of Epic 3: "Smart Lists & Advanced Filtering." It directly addresses Functional Requirements FR14, FR15, and FR16 from the Product Requirements Document (PRD): "Users can filter tasks by a specific label," "Users can sort tasks by priority," and "Users can sort tasks by due date." The UX Design Specification outlines that these controls will be available in the main task view. The technical implementation will leverage the existing `Task` data model and extend the `GET /api/tasks` endpoint with `label`, `sort_by`, and `order` query parameters, as detailed in the Epic 3 Technical Specification and the overall Architecture Document. Open questions regarding filtering combinations and default sort order will need to be addressed during implementation.

## Acceptance Criteria

1.  **Given** I am viewing my tasks, **when** I select a label from a "Filter by Label" dropdown, **then** the task list is filtered to show only tasks with that label.
2.  **When** I choose to sort by priority, **then** the tasks are ordered from High to Low.
3.  **When** I choose to sort by due date, **then** the tasks are ordered with the soonest due date first.

## Tasks / Subtasks

*   **1. Backend Implementation:**
    *   [ ] Modify existing `GET /api/tasks` Flask route in `app.py` to accept optional `label`, `sort_by`, and `order` query parameters.
    *   [ ] Implement logic in `app.py` to filter tasks from the `Task` model by the `label` field. (Source: `docs/fase-3-solutioning/architecture.md#Data-Models`)
    *   [ ] Implement logic in `app.py` to sort tasks from the `Task` model by `priority` (High to Low by default) and `due_date` (soonest first by default), respecting the `order` parameter.
*   **2. Frontend Implementation:**
    *   [ ] Implement a "Filter by Label" dropdown in `templates/index.html` (or relevant template), populating options from available labels.
    *   [ ] Implement "Sort by" controls (e.g., dropdown or buttons) for `Priority` and `Due Date` in `templates/index.html`.
    *   [ ] Implement JavaScript event handlers for filter and sort controls that send API requests to `GET /api/tasks` with the appropriate `label`, `sort_by`, and `order` query parameters.
    *   [ ] Update the main task list display based on the filtered and sorted response from the API.
*   **3. Testing:**
    *   [ ] **Unit Test**: Verify the database query logic correctly filters tasks by label.
    *   [ ] **Unit Test**: Verify the database query logic correctly sorts tasks by priority (ASC/DESC).
    *   [ ] **Unit Test**: Verify the database query logic correctly sorts tasks by due date (ASC/DESC).
    *   [ ] **Integration Test**: Verify the `GET /api/tasks` endpoint returns tasks filtered by label and sorted by priority/due date.
    *   [ ] **E2E Test**: Using Playwright, simulate user interactions with filter and sort controls and verify that the task list updates correctly. (Source: `docs/sprint-artifacts/tech-spec-epic-3.md#Test-Strategy-Summary`)

## Dev Notes

*   **API Endpoint**: Extend the existing `GET /api/tasks` endpoint. Ensure proper handling of `label`, `sort_by`, and `order` query parameters. (Source: `docs/fase-3-solutioning/architecture.md#API-Contracts`, `docs/sprint-artifacts/tech-spec-epic-3.md#APIs-and-Interfaces`)
*   **Database Interaction**: Use Flask-SQLAlchemy to filter and sort tasks based on `label`, `priority`, and `due_date` columns. Consider adding database indexes to these columns for performance if not already present. (Source: `docs/fase-3-solutioning/architecture.md#Data-Architecture`, `docs/sprint-artifacts/tech-spec-epic-3.md#Risks-Assumptions-Open-Questions`)
*   **Frontend UI**: Implement intuitive controls for filtering by label and sorting by priority/due date, adhering to UX Design principles. (Source: `docs/fase-2-planning/ux-design-specification.md#Chosen-Design-Approach`, `docs/fase-2-planning/ux-design-specification.md#Search-Patterns`)
*   **Testing**: Follow the test strategy outlined in the Epic 3 Tech Spec, covering unit tests for filtering/sorting logic, integration tests for the API endpoint, and E2E tests for UI interaction. (Source: `docs/sprint-artifacts/tech-spec-epic-3.md#Test-Strategy-Summary`)
*   **Open Questions**: Consider the "Filtering Combinations" and "Default Sort Order" open questions from the Epic 3 Tech Spec during implementation and UI design.

### Learnings from Previous Story

**From Story 3-2-due-this-week-smart-list (Status: ready-for-dev)**

- **Architectural Decision**: Continue to consider adding database indexes to filtering columns (`label`, `priority`, `due_date`) for performance.
- **Warning**: "Complex Date Logic for 'Due This Week'" still applies to sorting by `due_date`. Ensure robust testing of date sorting.

## Change Log

| Version | Date                   | Change                                 | Author |
| :------ | :--------------------- | :------------------------------------- | :----- |
| 1.0     | mandag 1. desember 2025 | Initial draft of story document.       | BIP    |

## Project Structure Alignment

This story's implementation aligns with the existing project structure by further modifying `app.py` for API endpoint handling and database interaction, and `templates/` for frontend display, as defined in the Architecture Document. It extends the filtering capabilities built in previous stories. No new top-level services or significant structural changes are anticipated.

### References

## Dev Agent Record

### Context Reference
- docs/sprint-artifacts/3-3-manual-filtering-and-sorting.context.xml

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List

## Requirements Context

This story implements the manual filtering and sorting functionalities as part of Epic 3: "Smart Lists & Advanced Filtering." It directly addresses Functional Requirements FR14, FR15, and FR16 from the Product Requirements Document (PRD): "Users can filter tasks by a specific label," "Users can sort tasks by priority," and "Users can sort tasks by due date." The UX Design Specification outlines that these controls will be available in the main task view. The technical implementation will leverage the existing `Task` data model and extend the `GET /api/tasks` endpoint with `label`, `sort_by`, and `order` query parameters, as detailed in the Epic 3 Technical Specification and the overall Architecture Document. Open questions regarding filtering combinations and default sort order will need to be addressed during implementation.

## Acceptance Criteria

1.  **Given** I am viewing my tasks, **when** I select a label from a "Filter by Label" dropdown, **then** the task list is filtered to show only tasks with that label.
2.  **When** I choose to sort by priority, **then** the tasks are ordered from High to Low.
3.  **When** I choose to sort by due date, **then** the tasks are ordered with the soonest due date first.

## Tasks / Subtasks

*   **1. Backend Implementation:**
    *   [ ] Modify existing `GET /api/tasks` Flask route in `app.py` to accept optional `label`, `sort_by`, and `order` query parameters.
    *   [ ] Implement logic in `app.py` to filter tasks from the `Task` model by the `label` field. (Source: `docs/fase-3-solutioning/architecture.md#Data-Models`)
    *   [ ] Implement logic in `app.py` to sort tasks from the `Task` model by `priority` (High to Low by default) and `due_date` (soonest first by default), respecting the `order` parameter.
*   **2. Frontend Implementation:**
    *   [ ] Implement a "Filter by Label" dropdown in `templates/index.html` (or relevant template), populating options from available labels.
    *   [ ] Implement "Sort by" controls (e.g., dropdown or buttons) for `Priority` and `Due Date` in `templates/index.html`.
    *   [ ] Implement JavaScript event handlers for filter and sort controls that send API requests to `GET /api/tasks` with the appropriate `label`, `sort_by`, and `order` query parameters.
    *   [ ] Update the main task list display based on the filtered and sorted response from the API.
*   **3. Testing:**
    *   [ ] **Unit Test**: Verify the database query logic correctly filters tasks by label.
    *   [ ] **Unit Test**: Verify the database query logic correctly sorts tasks by priority (ASC/DESC).
    *   [ ] **Unit Test**: Verify the database query logic correctly sorts tasks by due date (ASC/DESC).
    *   [ ] **Integration Test**: Verify the `GET /api/tasks` endpoint returns tasks filtered by label and sorted by priority/due date.
    *   [ ] **E2E Test**: Using Playwright, simulate user interactions with filter and sort controls and verify that the task list updates correctly. (Source: `docs/sprint-artifacts/tech-spec-epic-3.md#Test-Strategy-Summary`)

## Dev Notes

*   **API Endpoint**: Extend the existing `GET /api/tasks` endpoint. Ensure proper handling of `label`, `sort_by`, and `order` query parameters. (Source: `docs/fase-3-solutioning/architecture.md#API-Contracts`, `docs/sprint-artifacts/tech-spec-epic-3.md#APIs-and-Interfaces`)
*   **Database Interaction**: Use Flask-SQLAlchemy to filter and sort tasks based on `label`, `priority`, and `due_date` columns. Consider adding database indexes to these columns for performance if not already present. (Source: `docs/fase-3-solutioning/architecture.md#Data-Architecture`, `docs/sprint-artifacts/tech-spec-epic-3.md#Risks-Assumptions-Open-Questions`)
*   **Frontend UI**: Implement intuitive controls for filtering by label and sorting by priority/due date, adhering to UX Design principles. (Source: `docs/fase-2-planning/ux-design-specification.md#Chosen-Design-Approach`, `docs/fase-2-planning/ux-design-specification.md#Search-Patterns`)
*   **Testing**: Follow the test strategy outlined in the Epic 3 Tech Spec, covering unit tests for filtering/sorting logic, integration tests for the API endpoint, and E2E tests for UI interaction. (Source: `docs/sprint-artifacts/tech-spec-epic-3.md#Test-Strategy-Summary`)
*   **Open Questions**: Consider the "Filtering Combinations" and "Default Sort Order" open questions from the Epic 3 Tech Spec during implementation and UI design.

### Learnings from Previous Story

**From Story 3-2-due-this-week-smart-list (Status: ready-for-dev)**

- **Architectural Decision**: Continue to consider adding database indexes to filtering columns (`label`, `priority`, `due_date`) for performance.
- **Warning**: "Complex Date Logic for 'Due This Week'" still applies to sorting by `due_date`. Ensure robust testing of date sorting.

## Change Log

| Version | Date                   | Change                                 | Author |
| :------ | :--------------------- | :------------------------------------- | :----- |
| 1.0     | mandag 1. desember 2025 | Initial draft of story document.       | BIP    |

## Project Structure Alignment

This story's implementation aligns with the existing project structure by further modifying `app.py` for API endpoint handling and database interaction, and `templates/` for frontend display, as defined in the Architecture Document. It extends the filtering capabilities built in previous stories. No new top-level services or significant structural changes are anticipated.

### References

## Dev Agent Record

### Context Reference

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List