# Epic Technical Specification: AI-Powered Task Intelligence

Date: mandag 1. desember 2025
Author: BIP
Epic ID: 2
Status: Draft

---

## Overview

This technical specification details Epic 2: AI-Powered Task Intelligence, focusing on integrating the Google Gemini AI into the Smart To-Do AI application. This epic is a core component of the product's unique selling proposition, leveraging AI for intelligent task categorization and prioritization to reduce manual effort for users. The overall objective is to enhance the user experience by making task management more intuitive and efficient, aligning with the minimalist design philosophy.

## Objectives and Scope

**In-Scope:**
*   Integration with the Google Gemini API to analyze task descriptions and suggest appropriate Labels (e.g., School, Work, Home, Health, Finance, Shopping, Other) and Priority levels (Low, Medium, High).
*   Implementation of user control mechanisms to review, accept, or override any AI suggestions before saving a task.
*   Development of the "Magic Fill" feature to trigger AI-powered suggestions during task creation and editing.
*   Implementation of a robust rule-based fallback mechanism for label and priority suggestions if the AI service is unavailable or exceeds quota.

**Out-of-Scope:**
*   Gamified UI/UX features (Post-MVP).
*   Shared task lists (Post-MVP).
*   AI-generated sub-tasks (Post-MVP).
*   Simple Search (Post-MVP).
*   Export/Import functionality (Post-MVP).
*   Dark Mode (Post-MVP).
*   Hyper-personalized AI assistance (Future Vision).
*   Automated project decomposition (Future Vision).
*   Universal Inbox integration (Future Vision).

## System Architecture Alignment

The AI-Powered Task Intelligence epic aligns directly with the established architecture. The `ai_service.py` module will handle direct Gemini API calls from the backend, ensuring secure API key management. A new Flask route `POST /api/suggest` will serve as the integration point between the frontend and the AI service. A robust rule-based fallback mechanism is defined within `ai_service.py` to ensure application resilience. The frontend will integrate the "Magic Fill" pattern to trigger and display AI suggestions.

## Detailed Design

### Services and Modules

*   **`app.py` (Main Flask Application)**:
    *   **Responsibilities**: Handles routing for `/api/suggest`, acts as a proxy between the frontend and the `ai_service` module.
    *   **Inputs**: JSON payload from frontend (`{"title": "..."}`).
    *   **Outputs**: JSON response from `ai_service` (`{"priority": "...", "label": "..."}`).
*   **`ai_service.py` (AI Service Module)**:
    *   **Responsibilities**:
        *   Constructs prompts for the Google Gemini API.
        *   Makes secure calls to the Gemini API using the `google-genai` library.
        *   Parses Gemini API responses.
        *   Implements the rule-based fallback mechanism if the Gemini API call fails or returns an invalid response.
        *   Manages the Gemini API key securely (not exposed to frontend).
    *   **Inputs**: Task title string.
    *   **Outputs**: Dictionary containing `priority` and `label` (e.g., `{"priority": "High", "label": "Work"}`).
*   **Frontend Components (UI)**:
    *   **Responsibilities**: Provides the "Magic Fill" button in task creation/editing modals. Displays loading indicators. Populates the `label` and `priority` fields with AI suggestions or fallback suggestions.
    *   **Inputs**: User input for task title; AI/fallback suggestions.
    *   **Outputs**: API requests to `POST /api/suggest`.

### Data Models and Contracts

The `Task` model in the SQLite database is extended to include `priority` and `label` fields, which are directly influenced by Epic 2's AI suggestions:

**`Task` Model (Relevant Fields for Epic 2):**

| Column   | Type          | Constraints                       | Description                                       |
| :------- | :------------ | :-------------------------------- | :------------------------------------------------ |
| `priority` | `String(20)`  | Not Nullable, Default='Medium'    | Priority level (e.g., Low, Medium, High).         |
| `label`    | `String(50)`  | Nullable                          | A category for the task (e.g., Work, Personal).   |

The AI service (`ai_service.py`) returns a dictionary with `priority` and `label` keys, which directly map to these model fields.

### APIs and Interfaces

**`POST /api/suggest`**

*   **Description**: Frontend endpoint to request AI-powered label and priority suggestions for a task title.
*   **Method**: `POST`
*   **Request Body (JSON)**:
    ```json
    {
      "title": "String" // The task title for which suggestions are requested
    }
    ```
*   **Response Body (JSON - Success)**:
    ```json
    {
      "priority": "String", // Suggested priority (e.g., "Low", "Medium", "High")
      "label": "String"    // Suggested label (e.g., "Work", "Shopping", "Home")
    }
    ```
*   **Response Body (JSON - Error)**: Standard error format `{"error": {"message": "...", "code": ...}}`. In case of AI service failure, the fallback mechanism will still return a success response with rule-based suggestions.
*   **Behavior**: This endpoint proxies the request to `ai_service.py` and returns its output. It includes a loading indicator on the frontend during the request.

### Workflows and Sequencing

**AI-Suggestion Flow ("Magic Fill"):**

1.  **User Action**: User types a task title into the `Title` field within the task creation or editing modal.
2.  **User Action**: User clicks the "Magic Fill" button.
3.  **Frontend**:
    *   Displays a subtle loading indicator on the "Magic Fill" button.
    *   Sends a `POST` request to `/api/suggest` with the task title in the request body.
4.  **Backend (`app.py`)**:
    *   Receives the `POST /api/suggest` request.
    *   Extracts the `title` from the request body.
    *   Calls the `get_ai_suggestions(title)` function in `ai_service.py`.
5.  **AI Service (`ai_service.py`)**:
    *   Constructs a suitable prompt for the Google Gemini API based on the provided `title`.
    *   Attempts to call the Gemini API.
    *   **If Gemini API call succeeds**: Parses the JSON response to extract `priority` and `label`.
    *   **If Gemini API call fails (error, timeout, malformed response)**: Triggers the **Rule-Based Fallback Mechanism**:
        *   Analyzes keywords in the `title` (e.g., "report", "bug", "fix").
        *   Suggests a `priority` and `label` based on matched keywords.
        *   If no keywords match, defaults to `priority: "Low"` and `label: "General"`.
    *   Returns the suggested `priority` and `label` to `app.py`.
6.  **Backend (`app.py`)**: Returns the `priority` and `label` received from `ai_service.py` as a JSON response to the frontend.
7.  **Frontend**:
    *   Hides the loading indicator.
    *   Populates the `Priority` and `Label` fields in the task modal with the received suggestions.
    *   The user can then review, accept, or override these suggestions before saving the task.

## Non-Functional Requirements

### Performance

*   **AI Suggestion Response Time**: AI suggestion responses from the Gemini API, proxied through the backend, must be returned and displayed within 1-2 seconds to ensure a fluid user experience. This includes the time taken for the backend to call the Gemini API and for the frontend to update the UI.
*   **API Load Testing**: Key endpoints related to AI suggestions (`/api/suggest`) will be load-tested using `k6` to ensure they meet the 1-2 second response time SLA under a simulated load.
*   **Frontend Audits**: Automated Lighthouse audits will monitor frontend performance metrics (LCP, FCP) for the task modal interaction with AI suggestions.

### Security

*   **API Key Protection**: The Google Gemini API key will be securely handled on the backend within `ai_service.py` and will *never* be exposed client-side. All AI API calls will be proxied through the Flask backend. (ASR-01)
*   **Testing**: SAST (`bandit`) will be integrated into CI to scan for vulnerabilities. Dependency scanning (`pip-audit`) will identify known vulnerabilities in libraries. E2E tests using Playwright will validate that unauthenticated users cannot access AI suggestion endpoints.
*   **Data Protection**: User task data (including labels and priorities) stored in SQLite will be protected from unauthorized access.

### Reliability

*   **AI Service Fallback**: The application must provide a robust rule-based fallback mechanism within `ai_service.py` if the Google Gemini AI service is unavailable (e.g., due to API errors, timeouts, or malformed responses). This ensures core functionality is not blocked by external dependency failure. (ASR-03)
*   **Testing**: Integration tests will use `pytest-mock` to simulate failed responses from the Gemini API within `ai_service.py`, verifying that the rule-based fallback is triggered correctly and the UI communicates this appropriately. E2E tests using Playwright will validate the frontend behavior during fallback scenarios.

### Observability

*   **Logging**: The Flask application will implement structured JSON logging to record significant events, including calls to the Gemini API and instances where the rule-based fallback mechanism is triggered. This provides a consistent data source for debugging and monitoring.
*   **Metrics (Future)**: While not in the immediate MVP, future enhancements should include instrumentation with Prometheus metrics to expose a `/metrics` endpoint. This would allow for more precise monitoring of API latency, error rates, and Gemini API usage during performance and reliability testing.

## Dependencies and Integrations

*   **Google Gemini API (v1.52.0)**:
    *   **Description**: External AI service providing intelligent suggestions for task labels and priorities.
    *   **Integration Point**: Backend (`ai_service.py`). Calls are proxied through the backend to ensure secure API key management.
    *   **Credential**: `GEMINI_API_KEY` (stored as a GitHub Action secret and local environment variable).
*   **Python (3.14) / Flask (3.1.2)**:
    *   **Description**: Backend framework and language for handling API requests and business logic.
    *   **Dependency**: `google-genai` Python library for interacting with the Gemini API.
*   **Frontend (HTML Templates / TailwindCSS 3.4.16)**:
    *   **Description**: User interface for creating/editing tasks and triggering AI suggestions.
    *   **Integration Point**: Communicates with the Flask backend via REST API (`POST /api/suggest`).
*   **SQLite (3.45)**:
    *   **Description**: Local, file-based database for storing task data, including `priority` and `label` fields which are populated by AI suggestions.
*   **Node.js (24.11.1)**:
    *   **Description**: Used for frontend asset compilation (e.g., TailwindCSS). Not a runtime dependency for the core AI suggestion flow, but part of the overall development stack.

## Acceptance Criteria (Authoritative)

**Story 2.1: Gemini API Integration**
1.  **Given** a task description, **when** the backend service is called, **then** it successfully sends the description to the Gemini API.
2.  **And** the backend service securely manages the API key.
3.  **And** the backend can receive and parse a JSON response from the API containing `label` and `priority`.

**Story 2.2: "Magic Fill" AI Suggestions**
4.  **Given** the user is in the "Add Task" or "Edit Task" modal, **when** they click the "Magic Fill" button, **then** the task description is sent to the backend AI service.
5.  **And** a subtle loading indicator appears on the button until the `label` and `priority` fields are populated.
6.  **And** the `label` and `priority` fields in the form are populated with the suggestions returned by the AI.
7.  **And** the user can then accept or edit these suggestions before saving.

**Story 2.3: Rule-Based Fallback Mechanism**
8.  **Given** the AI service call fails, **when** a user requests AI suggestions, **then** the fallback mechanism is triggered.
9.  **And** the fallback uses keyword matching to suggest a label (e.g., "buy" -> "Shopping").
10. **And** if no keyword matches, the fallback suggests "Other" for the label and "Low" for the priority.
11. **And** the UI subtly indicates that the suggestions are from the fallback system (e.g., a toast notification saying "AI unavailable, used fallback suggestions").

## Traceability Mapping

| Acceptance Criteria (AC) | Spec Section(s)                                    | Component(s)/API(s)        | Test Idea                                                 |
| :----------------------- | :------------------------------------------------- | :------------------------- | :-------------------------------------------------------- |
| AC 1, 2, 3 (Story 2.1)   | 4.1.1 Services & Modules, 4.1.3 APIs & Interfaces  | `ai_service.py`, Gemini API | Unit/Integration Test: `ai_service.py` directly, mocking Gemini API |
| AC 4, 5, 6, 7 (Story 2.2)  | 4.1.4 Workflows & Sequencing, UX Design Spec       | Frontend, `app.py` (`/api/suggest`) | E2E Test: User clicks Magic Fill, fields populate, user can edit |
| AC 8, 9, 10, 11 (Story 2.3) | 4.1.4 Workflows & Sequencing, NFR (Reliability) | `ai_service.py`, Frontend  | Integration Test: Mock Gemini API failure, verify fallback suggestions and UI message |
| FR6                      | 4.1.1 Services & Modules                           | `ai_service.py`, Gemini API | Integration Test: Successful call to Gemini API           |
| FR7, FR8                 | 4.1.1 Services & Modules, 4.1.3 APIs & Interfaces  | `ai_service.py`, `app.py`   | E2E Test: Verify suggested label/priority from AI         |
| FR9, FR10                | 4.1.4 Workflows & Sequencing                       | Frontend                   | E2E Test: User can accept/override suggestions            |
| FR11                     | 4.1.4 Workflows & Sequencing, NFR (Reliability) | `ai_service.py`, Frontend  | E2E Test: AI unavailable, verify fallback mechanism       |

## Risks, Assumptions, Open Questions

### Risks, Assumptions, Open Questions

*   **Risk: Compromised Gemini API Key (ASR-01 Security)**: If the Gemini API key is exposed, it could lead to unauthorized use and significant cost.
    *   **Mitigation**: Secure backend handling (`ai_service.py`) and storage as environment variables (`GEMINI_API_KEY`). Regular rotation of API keys.
*   **Risk: Slow AI Suggestion Response Time (ASR-02 Performance)**: A slow response from the core "Magic Fill" feature would lead to a poor user experience, undermining the product's value proposition.
    *   **Mitigation**: Performance testing with `k6` to ensure 1-2 second response times. Implementation of loading indicators on the frontend.
*   **Risk: Gemini AI Service Unavailability (ASR-03 Reliability)**: The core functionality could be blocked by the failure of the external Gemini API.
    *   **Mitigation**: Robust rule-based fallback mechanism in `ai_service.py` to provide suggestions even if the AI is down.
*   **Assumption: Mocking External Dependencies**: Tests will rely on mocking the `ai_service.py` module's downstream dependencies (e.g., Gemini API calls) to simulate various scenarios and failures.
*   **Question: Error Injection Mechanism**: Currently, there is no dedicated mechanism for forcing failure modes in `ai_service.py` during testing, which could simplify testing of fallback scenarios. (Medium Priority Concern C-01)
*   **Question: Observability for Performance NFRs**: Without dedicated observability tooling (e.g., Prometheus metrics), validating performance NFRs (e.g., 1-2 second response time) under load remains challenging. (Medium Priority Concern C-02)

## Test Strategy Summary

### Test Strategy Summary

The testing strategy for Epic 2 will adhere to the project's overall test pyramid, with a strong emphasis on integration and E2E testing to cover the AI suggestion flow.

*   **Unit Tests (50%)**: Will cover the isolated business logic within `ai_service.py`, including the rule-based fallback logic (keyword matching, default suggestions).
    *   **Tools**: `pytest`
*   **Integration/API Tests (35%)**: Crucial for validating the `POST /api/suggest` endpoint, ensuring correct communication between the frontend, `app.py`, and `ai_service.py`. These tests will mock the external Gemini API to simulate success, failure, and latency scenarios to thoroughly test the fallback mechanism.
    *   **Tools**: `pytest`, `pytest-mock`
*   **End-to-End (E2E) Tests (15%)**: Will validate the critical user journey of using the "Magic Fill" feature in the UI, ensuring the loading state, the population of label/priority fields, and the user's ability to accept/override suggestions. E2E tests will also cover scenarios where the AI service is simulated to fail, verifying the UI's display of fallback suggestions.
    *   **Tools**: Playwright
*   **Security Testing**: SAST (`bandit`) and dependency scanning (`pip-audit`) will be integrated into CI. E2E tests will include scenarios to confirm the Gemini API key is not exposed client-side.
*   **Performance Testing**: API load testing for `/api/suggest` using `k6` will ensure the 1-2 second response time NFR is met. Frontend audits (`Lighthouse`) will monitor UI responsiveness.
*   **Reliability Testing**: Dedicated integration tests will mock Gemini API failures to confirm the rule-based fallback functions as designed and communicates appropriately to the user.
