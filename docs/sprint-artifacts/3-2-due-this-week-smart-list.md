# User Story: 3.2: "Due This Week" Smart List
Status: ready-for-dev

As a user, I want to easily access a "Due This Week" smart list from the dashboard, so that I can effectively plan and manage my upcoming tasks.

## Requirements Context

This story implements the "Due This Week" Smart List feature as part of Epic 3: "Smart Lists & Advanced Filtering." It directly addresses Functional Requirement FR13 from the Product Requirements Document (PRD): "The system can automatically generate 'Due This Week' smart lists." The UX Design Specification outlines this as a key interaction within the dashboard view, accessible from the sidebar. The technical implementation will leverage the existing `Task` data model and the `GET /api/tasks` endpoint with a `due_date_before=<calculated_date>` query parameter, where the date is 7 days from the current date. This is detailed in the Epic 3 Technical Specification and the overall Architecture Document. It's important to consider the potential complexity of date logic for filtering.

## Acceptance Criteria

1.  **Given** I am on the main dashboard, **when** I view the sidebar, **then** I see a "Due This Week" smart list option.
2.  **When** I click the "Due This Week" smart list, **then** the main task view is filtered to show only tasks with a due date within the next 7 days.

## Tasks / Subtasks

*   **1. Backend Implementation:**
    *   [ ] Modify existing `GET /api/tasks` Flask route in `app.py` to accept an optional `due_date_before` query parameter.
    *   [ ] Implement logic in `app.py` to calculate the date 7 days from the current date.
    *   [ ] Implement logic in `app.py` to filter tasks from the `Task` model where `due_date` is on or before the calculated date. (Source: `docs/fase-3-solutioning/architecture.md#Data-Models`)
*   **2. Frontend Implementation:**
    *   [ ] Add a "Due This Week" list item to the sidebar navigation in `templates/index.html` (or relevant template). (Source: `docs/fase-2-planning/ux-design-specification.md#Chosen-Design-Approach`)
    *   [ ] Implement a JavaScript click handler for the "Due This Week" sidebar option that calculates the date 7 days from now and sends an API request to `GET /api/tasks?due_date_before=<calculated_date>`. (Source: `docs/sprint-artifacts/tech-spec-epic-3.md#Workflows-and-Sequencing`)
    *   [ ] Update the main task list display based on the filtered response from the API.
*   **3. Testing:**
    *   [ ] **Unit Test**: Verify the date calculation logic (7 days from now) handles edge cases (month/year end, leap years) correctly.
    *   [ ] **Unit Test**: Verify the database query logic correctly filters tasks by `due_date_before`.
    *   [ ] **Integration Test**: Verify the `GET /api/tasks?due_date_before=<date>` endpoint returns only tasks due within the specified period.
    *   [ ] **E2E Test**: Using Playwright, simulate a user clicking the "Due This Week" smart list in the sidebar and verify that only tasks due within the next 7 days are displayed on the dashboard. (Source: `docs/sprint-artifacts/tech-spec-epic-3.md#Test-Strategy-Summary`)

## Dev Notes

*   **API Endpoint**: Extend the existing `GET /api/tasks` endpoint. Ensure proper handling of `due_date_before` query parameter. (Source: `docs/fase-3-solutioning/architecture.md#API-Contracts`, `docs/sprint-artifacts/tech-spec-epic-3.md#APIs-and-Interfaces`)
*   **Database Interaction**: Use Flask-SQLAlchemy to filter tasks based on the `due_date` column in the `Task` model. Consider adding a database index to the `due_date` column for performance if not already present. (Source: `docs/fase-3-solutioning/architecture.md#Data-Architecture`, `docs/sprint-artifacts/tech-spec-epic-3.md#Risks-Assumptions-Open-Questions`)
*   **Frontend UI**: The "Due This Week" smart list option should be integrated into the sidebar as per the UX Design. Ensure active state indication when selected. (Source: `docs/fase-2-planning/ux-design-specification.md#Chosen-Design-Approach`, `docs/fase-2-planning/ux-design-specification.md#Navigation-Patterns`)
*   **Testing**: Follow the test strategy outlined in the Epic 3 Tech Spec, focusing on unit tests for date calculation and query logic, integration tests for the API endpoint, and E2E tests for UI interaction. (Source: `docs/sprint-artifacts/tech-spec-epic-3.md#Test-Strategy-Summary`)
*   **Complex Date Logic**: Pay special attention to the "Complex Date Logic for 'Due This Week'" risk identified in the Epic 3 Tech Spec. Thorough unit testing of date calculations (e.g., across month/year boundaries, time zones) is critical.

### Learnings from Previous Story

**From Story 3-1-high-priority-smart-list (Status: ready-for-dev)**

- **Architectural Decision**: Consider adding a database index to filtering columns for performance. Apply this consideration to the `due_date` column as well.

## Change Log

| Version | Date                   | Change                                 | Author |
| :------ | :--------------------- | :------------------------------------- | :----- |
| 1.0     | mandag 1. desember 2025 | Initial draft of story document.       | BIP    |

## Project Structure Alignment

This story's implementation aligns with the existing project structure by modifying `app.py` for API endpoint handling and database interaction, and `templates/` for frontend display, as defined in the Architecture Document. Similar to Story 3.1, it primarily involves extending existing Flask routes and rendering logic. No new top-level services or significant structural changes are anticipated.

### References

## Dev Agent Record

### Context Reference
- docs/sprint-artifacts/3-2-due-this-week-smart-list.context.xml

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List

## Requirements Context

This story implements the "Due This Week" Smart List feature as part of Epic 3: "Smart Lists & Advanced Filtering." It directly addresses Functional Requirement FR13 from the Product Requirements Document (PRD): "The system can automatically generate 'Due This Week' smart lists." The UX Design Specification outlines this as a key interaction within the dashboard view, accessible from the sidebar. The technical implementation will leverage the existing `Task` data model and the `GET /api/tasks` endpoint with a `due_date_before=<calculated_date>` query parameter, where the date is 7 days from the current date. This is detailed in the Epic 3 Technical Specification and the overall Architecture Document. It's important to consider the potential complexity of date logic for filtering.

## Acceptance Criteria

1.  **Given** I am on the main dashboard, **when** I view the sidebar, **then** I see a "Due This Week" smart list option.
2.  **When** I click the "Due This Week" smart list, **then** the main task view is filtered to show only tasks with a due date within the next 7 days.

## Tasks / Subtasks

*   **1. Backend Implementation:**
    *   [ ] Modify existing `GET /api/tasks` Flask route in `app.py` to accept an optional `due_date_before` query parameter.
    *   [ ] Implement logic in `app.py` to calculate the date 7 days from the current date.
    *   [ ] Implement logic in `app.py` to filter tasks from the `Task` model where `due_date` is on or before the calculated date. (Source: `docs/fase-3-solutioning/architecture.md#Data-Models`)
*   **2. Frontend Implementation:**
    *   [ ] Add a "Due This Week" list item to the sidebar navigation in `templates/index.html` (or relevant template). (Source: `docs/fase-2-planning/ux-design-specification.md#Chosen-Design-Approach`)
    *   [ ] Implement a JavaScript click handler for the "Due This Week" sidebar option that calculates the date 7 days from now and sends an API request to `GET /api/tasks?due_date_before=<calculated_date>`. (Source: `docs/sprint-artifacts/tech-spec-epic-3.md#Workflows-and-Sequencing`)
    *   [ ] Update the main task list display based on the filtered response from the API.
*   **3. Testing:**
    *   [ ] **Unit Test**: Verify the date calculation logic (7 days from now) handles edge cases (month/year end, leap years) correctly.
    *   [ ] **Unit Test**: Verify the database query logic correctly filters tasks by `due_date_before`.
    *   [ ] **Integration Test**: Verify the `GET /api/tasks?due_date_before=<date>` endpoint returns only tasks due within the specified period.
    *   [ ] **E2E Test**: Using Playwright, simulate a user clicking the "Due This Week" smart list in the sidebar and verify that only tasks due within the next 7 days are displayed on the dashboard. (Source: `docs/sprint-artifacts/tech-spec-epic-3.md#Test-Strategy-Summary`)

## Dev Notes

*   **API Endpoint**: Extend the existing `GET /api/tasks` endpoint. Ensure proper handling of `due_date_before` query parameter. (Source: `docs/fase-3-solutioning/architecture.md#API-Contracts`, `docs/sprint-artifacts/tech-spec-epic-3.md#APIs-and-Interfaces`)
*   **Database Interaction**: Use Flask-SQLAlchemy to filter tasks based on the `due_date` column in the `Task` model. Consider adding a database index to the `due_date` column for performance if not already present. (Source: `docs/fase-3-solutioning/architecture.md#Data-Architecture`, `docs/sprint-artifacts/tech-spec-epic-3.md#Risks-Assumptions-Open-Questions`)
*   **Frontend UI**: The "Due This Week" smart list option should be integrated into the sidebar as per the UX Design. Ensure active state indication when selected. (Source: `docs/fase-2-planning/ux-design-specification.md#Chosen-Design-Approach`, `docs/fase-2-planning/ux-design-specification.md#Navigation-Patterns`)
*   **Testing**: Follow the test strategy outlined in the Epic 3 Tech Spec, focusing on unit tests for date calculation and query logic, integration tests for the API endpoint, and E2E tests for UI interaction. (Source: `docs/sprint-artifacts/tech-spec-epic-3.md#Test-Strategy-Summary`)
*   **Complex Date Logic**: Pay special attention to the "Complex Date Logic for 'Due This Week'" risk identified in the Epic 3 Tech Spec. Thorough unit testing of date calculations (e.g., across month/year boundaries, time zones) is critical.

### Learnings from Previous Story

**From Story 3-1-high-priority-smart-list (Status: ready-for-dev)**

- **Architectural Decision**: Consider adding a database index to filtering columns for performance. Apply this consideration to the `due_date` column as well.

## Change Log

| Version | Date                   | Change                                 | Author |
| :------ | :--------------------- | :------------------------------------- | :----- |
| 1.0     | mandag 1. desember 2025 | Initial draft of story document.       | BIP    |

## Project Structure Alignment

This story's implementation aligns with the existing project structure by modifying `app.py` for API endpoint handling and database interaction, and `templates/` for frontend display, as defined in the Architecture Document. Similar to Story 3.1, it primarily involves extending existing Flask routes and rendering logic. No new top-level services or significant structural changes are anticipated.

### References

## Dev Agent Record

### Context Reference

### Agent Model Used

### Debug Log References

### Completion Notes List

### File List