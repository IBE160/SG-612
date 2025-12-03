# User Story: Story 2.3: Rule-Based Fallback Mechanism

Status: ready-for-dev

As a developer, I want to implement a rule-based fallback mechanism, so that the application can still suggest labels and priorities if the AI service is unavailable.

## Requirements Context

This story is a critical part of Epic 2, ensuring the application is robust and reliable, which is one of the key success criteria from the PRD (FR11). It directly addresses the need for a fallback mechanism as specified in the "AI-Suggestion Flow (Magic Fill)" pattern in the Architecture Document (`docs/fase-3-solutioning/architecture.md`) and the Epic 2 Tech Spec (`docs/sprint-artifacts/tech-spec-epic-2.md`). This story makes the AI-powered features resilient to external service failures.

## Acceptance Criteria

1.  **AC1**: Given the AI service call fails (e.g., returns an error, times out, or provides a malformed response), the `ai_service.py` module triggers the internal fallback mechanism.
2.  **AC2**: The fallback mechanism uses keyword matching against the task title to suggest a `label` and `priority`.
3.  **AC3**: If no keywords match, the fallback defaults to suggesting "Other" for the label and "Low" for the priority.
4.  **AC4**: The frontend UI provides a subtle, non-blocking notification (e.g., a toast) to the user indicating that fallback suggestions were used (e.g., "AI unavailable, used fallback suggestions").

## Tasks / Subtasks

*   **1. AI Service Implementation (`ai_service.py`):**
    *   [ ] In the `get_ai_suggestions` function, add error handling (e.g., a `try...except` block) around the Gemini API call. (AC: #1)
    *   [ ] In the `except` block, implement the rule-based fallback logic. (AC: #1, #2)
    *   [ ] The logic should check for keywords in the task title and return a corresponding label and priority. (AC: #2)
    *   [ ] Implement the default suggestion ("Other", "Low") if no keywords match. (AC: #3)
*   **2. Frontend Implementation (templates/index.html & custom JS):**
    *   [ ] Modify the JavaScript function that calls `/api/suggest` to handle a new flag in the response (e.g., `{"fallback": true}`). (AC: #4)
    *   [ ] If the `fallback` flag is true, trigger a toast notification with the message "AI unavailable, used fallback suggestions." (AC: #4)
*   **3. Backend API Endpoint (app.py):**
    *   [ ] Modify the `/api/suggest` endpoint to include the `fallback` flag in its response if the AI service indicates that the fallback was used. (AC: #4)
*   **4. Verification & Testing:**
    *   [ ] **Unit Test**: Write a unit test for the `get_ai_suggestions` function in `ai_service.py` that specifically tests the fallback logic by mocking a failed API call. (AC: #1, #2, #3)
    *   [ ] **Integration Test**: Write a test for the `/api/suggest` endpoint that simulates a failure in the `ai_service` and verifies that the endpoint returns the fallback suggestions with the `fallback: true` flag. (AC: #4)
    *   [ ] **E2E Test**: Write a test using Playwright that mocks the `/api/suggest` endpoint to return a fallback response, and verifies that the toast notification appears on the UI. (AC: #4)

## Dev Notes

### Architecture patterns and constraints
The implementation must enhance the `ai_service.py` module with a `try...except` block to gracefully handle failures from the external Gemini API call. This triggers the rule-based fallback logic, ensuring the system degrades gracefully rather than failing. The `/api/suggest` endpoint will be modified to communicate this fallback status to the frontend.

### Testing standards summary
Testing is crucial for this story. Unit tests must specifically target the fallback logic within `ai_service.py` by mocking an API failure. An integration test must verify the `/api/suggest` endpoint correctly returns the `fallback: true` flag. An E2E test should mock the API response to confirm the frontend displays the required toast notification.

### References
- [Architecture: AI-Suggestion Flow](docs/fase-3-solutioning/architecture.md#pattern-ai-suggestion-flow-magic-fill)
- [Tech Spec: Epic 2](docs/sprint-artifacts/tech-spec-epic-2.md)
- [Product Requirements Document (PRD)](docs/fase-2-planning/prd.md)

## Project Structure Alignment

This story primarily modifies existing components to add resilience:
*   **AI Service (`ai_service.py`)**: The core fallback logic will be added here.
*   **Backend (`app.py`)**: The `/api/suggest` endpoint will be slightly modified to pass along the fallback status.
*   **Frontend (`templates/index.html` & custom JS)**: The frontend will be updated to display the fallback notification.

This enhances the robustness of the existing architecture without introducing new structural components.

## Dev Agent Record

### Context Reference
- `docs/sprint-artifacts/2-3-rule-based-fallback-mechanism.context.xml`

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List
