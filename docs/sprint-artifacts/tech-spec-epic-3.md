# Epic Technical Specification: Smart lists & advanced filtering

Date: mandag 1. desember 2025
Author: BIP
Epic ID: 3
Status: Draft

---

## Overview

This technical specification details Epic 3: Smart Lists & Advanced Filtering, which focuses on enhancing task organization and user control within the ibe160 Smart To-Do AI application. This epic implements automated smart lists for "High Priority" and "Due This Week" tasks, alongside user-controlled filtering by label and sorting by priority or due date. The goal is to allow users to quickly focus on what is most important, thereby improving efficiency and the overall user experience as outlined in the Product Requirements Document.

## Objectives and Scope

**In-Scope:**
*   Automatic generation of "High Priority" smart lists.
*   Automatic generation of "Due This Week" smart lists.
*   Functionality to filter tasks by a specific label.
*   Functionality to sort tasks by priority.
*   Functionality to sort tasks by due date.

**Out-of-Scope:**
*   Gamified UI/UX features (Post-MVP).
*   Shared task lists (Post-MVP).
*   AI-Generated Sub-tasks (Post-MVP).
*   Simple Search (Post-MVP).
*   Export/Import functionality (Post-MVP).
*   Dark Mode (Post-MVP).

## System Architecture Alignment

Epic 3's implementation primarily involves the `app.py` for API routing and business logic related to filtering and sorting, as well as `templates/` for presenting the filtered and sorted task lists on the frontend. The `instance/tasks.db` will be central to querying and retrieving tasks based on criteria like priority, due date, and labels. The REST API pattern established in the architecture document will be used to expose endpoints for these filtering and sorting operations. This aligns with the overall Flask, SQLite, and TailwindCSS stack, ensuring efficient data handling and presentation.

## Detailed Design

## Detailed Design

### Services and Modules

*   **`app.py` (Main Flask Application)**:
    *   **Responsibilities**: Handles routing for `/api/tasks` with various query parameters for filtering and sorting tasks. Interacts with the database to retrieve and process tasks based on these parameters.
    *   **Inputs**: HTTP GET requests with optional query parameters (e.g., `priority`, `due_date`, `label`, `sort_by`).
    *   **Outputs**: JSON response containing filtered and/or sorted task data.
*   **Frontend Components (UI)**:
    *   **Responsibilities**: Renders the main task list. Provides UI elements for selecting smart lists (sidebar), filtering by label (dropdown), and sorting by priority/due date. Sends API requests with appropriate query parameters.
    *   **Inputs**: User interactions (clicks on smart lists, selections in dropdowns).
    *   **Outputs**: API requests to `GET /api/tasks` with query parameters.

### Data Models and Contracts

The `Task` model, as defined in the Architecture Document, is central to Epic 3. The `priority`, `label`, and `due_date` fields are directly leveraged for smart lists, filtering, and sorting.

**`Task` Model (Relevant Fields for Epic 3):**

| Column     | Type         | Constraints                         | Description                                       |
| :--------- | :----------- | :---------------------------------- | :------------------------------------------------ |
| `due_date` | `Date`       | Nullable                            | When the task is due.                             |
| `priority` | `String(20)` | Not Nullable, Default='Medium'      | Priority level (e.g., Low, Medium, High).         |
| `label`    | `String(50)` | Nullable                            | A category for the task (e.g., Work, Personal).   |

### APIs and Interfaces

**`GET /api/tasks`**

*   **Description**: Retrieves a list of tasks, with options for filtering and sorting.
*   **Method**: `GET`
*   **Query Parameters**:
    *   `priority`: (Optional) `String` - Filters tasks by priority (e.g., "High", "Medium", "Low").
    *   `due_date_before`: (Optional) `Date` - Filters tasks due before a specific date (e.g., for "Due This Week" smart list).
    *   `label`: (Optional) `String` - Filters tasks by a specific label (e.g., "Work", "Shopping").
    *   `sort_by`: (Optional) `String` - Sorts tasks by a field ("priority", "due_date").
    *   `order`: (Optional) `String` - Sort order ("asc", "desc"). Defaults to "desc" for priority, "asc" for due date.
*   **Response Body (JSON - Success)**:
    ```json
    {
      "data": [
        {
          "id": 1,
          "title": "Buy groceries",
          "notes": "Milk, eggs, bread",
          "due_date": "2025-12-05",
          "priority": "High",
          "label": "Shopping",
          "is_done": false,
          "created_at": "2025-12-01T10:00:00Z"
        },
        // ... more tasks
      ]
    }
    ```
*   **Response Body (JSON - Error)**: Standard error format `{"error": {"message": "...", "code": ...}}`.

### Workflows and Sequencing

**Task Listing and Interaction Flow:**

1.  **User Action**: User navigates to the main dashboard.
2.  **System Response**: Frontend sends `GET /api/tasks` to retrieve all active tasks.
3.  **User Action**: User clicks on "High Priority" smart list in the sidebar.
4.  **Frontend**:
    *   Sends `GET /api/tasks?priority=High` to the backend.
    *   Updates the UI to highlight "High Priority" in the sidebar and displays only high-priority tasks.
5.  **User Action**: User clicks on "Due This Week" smart list in the sidebar.
6.  **Frontend**:
    *   Calculates the date 7 days from now.
    *   Sends `GET /api/tasks?due_date_before=<calculated_date>` to the backend.
    *   Updates the UI to highlight "Due This Week" in the sidebar and displays tasks due within the week.
7.  **User Action**: User selects "Work" from a "Filter by Label" dropdown.
8.  **Frontend**:
    *   Sends `GET /api/tasks?label=Work` to the backend.
    *   Updates the UI to reflect the "Work" filter.
9.  **User Action**: User selects "Priority" from a "Sort by" dropdown, then "Descending" from "Order".
10. **Frontend**:
    *   Sends `GET /api/tasks?sort_by=priority&order=desc` to the backend.
    *   Updates the UI to display tasks sorted by priority descending.
11. **Backend (`app.py`)**: Processes the `GET /api/tasks` request, queries the SQLite database using Flask-SQLAlchemy with the provided filters and sorting parameters, and returns the results.
12. **Frontend**: Receives the JSON response and re-renders the task list accordingly.

## Non-Functional Requirements

### Performance

*   **UI Responsiveness**: The UI for filtering and sorting tasks should update within 0.5-1 second of user interaction to provide immediate feedback.
*   **API Response Time**: API calls to `GET /api/tasks` with filtering and sorting parameters must complete within 1-2 seconds, even with a moderate number of tasks (e.g., 50-100). This aligns with the overall performance NFRs from the PRD and Architecture.

### Security

*   **Data Protection**: User task data (including labels and priorities) stored in SQLite and accessed through filtering/sorting APIs will continue to be protected from unauthorized access. This aligns with the security architecture and PRD NFRs.
*   **Access Control**: Ensure that filter and sort operations respect user authentication and only expose tasks owned by the authenticated user.

### Reliability/Availability

*   **Database Integrity**: The SQLite database must maintain data integrity for task attributes (`priority`, `label`, `due_date`) used in filtering and sorting.
*   **Graceful Degradation**: If the database is unavailable, the application should display an appropriate error message and prevent task manipulation, rather than crashing.
*   **Client-Side Resilience**: Frontend filtering and sorting logic, if any (though primarily backend-driven in this design), should be robust against malformed data.

### Observability

*   **Logging**: Backend logs (structured JSON logging as per Architecture) will record queries made to the `/api/tasks` endpoint, including filter and sort parameters, to aid in debugging and performance analysis.
*   **Error Monitoring**: Any errors occurring during database queries or API processing related to filtering and sorting will be logged with appropriate detail.

## Dependencies and Integrations

*   **Python (3.14) / Flask (3.1.2)**:
    *   **Description**: Backend framework and language for handling API requests for filtering and sorting tasks.
    *   **Integration Point**: Core logic within `app.py` for database queries and API routing.
*   **Flask-SQLAlchemy (3.1.2)**:
    *   **Description**: ORM for interacting with the SQLite database to perform filtered and sorted queries efficiently.
    *   **Integration Point**: Database operations within `app.py`.
*   **SQLite (3.45)**:
    *   **Description**: Local, file-based database storing task data, which is directly queried for smart list generation, filtering, and sorting.
    *   **Integration Point**: Data persistence layer, accessed via Flask-SQLAlchemy.
*   **Frontend (HTML Templates / TailwindCSS 3.4.16)**:
    *   **Description**: User interface for displaying tasks and providing controls for filtering and sorting.
    *   **Integration Point**: Communicates with the Flask backend via REST API (`GET /api/tasks`).
*   **Node.js (24.11.1)**:
    *   **Description**: Used for frontend asset compilation (e.g., TailwindCSS). Not a direct runtime dependency for the filtering/sorting logic itself, but part of the overall development stack.

## Acceptance Criteria (Authoritative)

**Story 3.1: "High Priority" Smart List**
1.  **Given** I am on the main dashboard, **when** I view the sidebar, **then** I see a "High Priority" smart list option.
2.  **When** I click the "High Priority" smart list, **then** the main task view is filtered to show only tasks with a "High" priority.

**Story 3.2: "Due This Week" Smart List**
3.  **Given** I am on the main dashboard, **when** I view the sidebar, **then** I see a "Due This Week" smart list option.
4.  **When** I click the "Due This Week" smart list, **then** the main task view is filtered to show only tasks with a due date within the next 7 days.

**Story 3.3: Manual Filtering and Sorting**
5.  **Given** I am viewing my tasks, **when** I select a label from a "Filter by Label" dropdown, **then** the task list is filtered to show only tasks with that label.
6.  **When** I choose to sort by priority, **then** the tasks are ordered from High to Low.
7.  **When** I choose to sort by due date, **then** the tasks are ordered with the soonest due date first.

## Traceability Mapping

| Acceptance Criteria (AC) | Spec Section(s)                   | Component(s)/API(s) | Test Idea                                                                 |
| :----------------------- | :-------------------------------- | :------------------ | :------------------------------------------------------------------------ |
| AC 1, 2 (Story 3.1)      | 4.1.4 Workflows & Sequencing      | Frontend, `app.py` (`GET /api/tasks?priority=High`) | E2E Test: User clicks 'High Priority' list, verifies filtered results       |
| AC 3, 4 (Story 3.2)      | 4.1.4 Workflows & Sequencing      | Frontend, `app.py` (`GET /api/tasks?due_date_before=...`) | E2E Test: User clicks 'Due This Week' list, verifies filtered results       |
| AC 5, 6, 7 (Story 3.3)   | 4.1.4 Workflows & Sequencing      | Frontend, `app.py` (`GET /api/tasks?label=...&sort_by=...`) | E2E Test: User uses filter/sort controls, verifies filtered/sorted results |
| FR12                     | 4.1.1 Services & Modules          | `app.py`            | Integration Test: Backend query for high priority tasks                   |
| FR13                     | 4.1.1 Services & Modules          | `app.py`            | Integration Test: Backend query for tasks due this week                   |
| FR14                     | 4.1.1 Services & Modules          | `app.py`            | Integration Test: Backend query for tasks by label                        |
| FR15                     | 4.1.1 Services & Modules          | `app.py`            | Integration Test: Backend query for tasks sorted by priority              |
| FR16                     | 4.1.1 Services & Modules          | `app.py`            | Integration Test: Backend query for tasks sorted by due date              |

## Risks, Assumptions, Open Questions

### Risks

*   **Risk: Performance Degradation with Large Task Lists (ASR-02 Performance)**: As the number of tasks grows, filtering and sorting queries might become slow, impacting the 1-2 second UI responsiveness NFR.
    *   **Mitigation**: Implement database indexing on `priority`, `label`, and `due_date` columns. Monitor query performance.
*   **Risk: Complex Date Logic for "Due This Week"**: Incorrect calculation of "Due This Week" range, especially across month/year boundaries or time zones, could lead to inaccurate smart list display.
    *   **Mitigation**: Thorough unit and integration testing of date calculation logic. Use a robust date/time library if Python's `datetime` proves insufficient for complex scenarios.

### Assumptions

*   **Frontend Controls**: It is assumed that the frontend will provide intuitive and clear controls for filtering and sorting, as detailed in the UX Design Specification.
*   **API Parameter Validity**: The backend assumes valid input for API query parameters (e.g., `priority` values are "High", "Medium", "Low"; `order` values are "asc", "desc"). Invalid inputs will be handled gracefully but are assumed to be rare from a well-behaved frontend.

### Open Questions

*   **Filtering Combinations**: How many filter/sort combinations should the UI support simultaneously (e.g., filter by label AND priority, then sort by due date)? (Medium Priority Concern)
*   **Default Sort Order**: What should be the default sort order for the main task list when no specific sort is applied? (Low Priority Concern)

## Test Strategy Summary

The testing strategy for Epic 3 will ensure the accuracy and performance of smart lists, filtering, and sorting functionalities.

*   **Unit Tests (50%)**: Will cover the core logic for database queries related to filtering by priority, label, and due date, as well as sorting algorithms. This includes rigorous testing of date calculation for "Due This Week".
    *   **Tools**: `pytest`
*   **Integration/API Tests (35%)**: Crucial for validating the `GET /api/tasks` endpoint with various combinations of query parameters (filters and sorts). These tests will verify that the backend correctly processes requests, interacts with the SQLite database, and returns accurate results.
    *   **Tools**: `pytest`, `httpx` (or Flask test client)
*   **End-to-End (E2E) Tests (15%)**: Will validate critical user journeys involving the UI controls for smart lists, filtering, and sorting. This includes verifying that the UI correctly reflects the filtered/sorted task lists and that interactions are smooth.
    *   **Tools**: Playwright
*   **Performance Testing**: API load testing for the `GET /api/tasks` endpoint using `k6` will ensure that filtering and sorting operations meet the 1-2 second response time NFR under load.
*   **Accessibility Testing**: E2E tests will include checks to ensure that filtering and sorting controls (e.g., dropdowns, smart list links) are keyboard navigable and provide appropriate ARIA attributes.
