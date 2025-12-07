# User Story: Story 2.1: Gemini API Integration

Status: in-progress

As a developer, I want to integrate the Google Gemini API with the backend, so that the application can send task descriptions for analysis.

## Requirements Context

This story is the first step in implementing Epic 2: "AI-Powered Task Intelligence". It directly addresses functional requirement FR6 ("The system can integrate with Google Gemini API to analyze task descriptions") from the PRD. The implementation must follow the patterns laid out in the Architecture Document (`docs/fase-3-solutioning/architecture.md`), specifically the creation of the `ai_service.py` module for secure, backend-only communication with the Gemini API. The recently created Tech Spec for Epic 2 (`docs/sprint-artifacts/tech-spec-epic-2.md`) provides further detailed design for the `ai_service.py` module, its responsibilities, inputs, and outputs.

## Acceptance Criteria

1.  **AC1**: Given a task description, when the backend service is called, it successfully sends the description to the Gemini API using the `google-genai` library.
2.  **AC2**: The backend service (`ai_service.py`) securely manages the `GEMINI_API_KEY` from environment variables and does not expose it to the client.
3.  **AC3**: The backend service can receive and parse a valid JSON response from the API containing `label` and `priority` keys.
4.  **AC4**: The `ai_service.py` module is created and contains a function (e.g., `get_ai_suggestions`) that encapsulates the Gemini API call logic.

## Tasks / Subtasks

*   **1. Setup & Configuration:**
    *   [x] Add `google-generativeai` to `requirements.txt`. (AC: #1)
    *   [x] Add `GEMINI_API_KEY` to `.env.example` and ensure `.env` is in `.gitignore`. (AC: #2)
    *   [x] Create the `ai_service.py` file. (AC: #4)
*   **2. AI Service Implementation (`ai_service.py`):**
    *   [x] Implement a function `get_ai_suggestions(title: str) -> dict`. (AC: #4)
    *   [x] Inside the function, retrieve the `GEMINI_API_KEY` from environment variables. (AC: #2)
    *   [x] Configure and initialize the `google.generativeai` client. (AC: #1)
    *   [x] Construct a precise prompt for the Gemini model, instructing it to return ONLY a JSON object with "priority" and "label" keys. (AC: #1, #3)
    *   [x] Implement the API call to the Gemini model. (AC: #1)
    *   [x] Parse the response and return the `priority` and `label` as a dictionary. (AC: #3)
*   **3. Verification & Testing:**
    *   [ ] **Unit Test**: Create a unit test for `get_ai_suggestions` that mocks the `google.generativeai` client and verifies that the function correctly parses a simulated successful response. (AC: #3)
    *   [ ] **Unit Test**: Create a unit test for `get_ai_suggestions` that simulates an API error and verifies the function handles it gracefully (e.g., raises an exception or returns a specific error state). (AC: #1, #3)
    *   [ ] **Manual Test**: Run the function directly with a valid API key and a sample task title to confirm a successful API call and response. (AC: #1, #2, #3)

## Dev Notes

### Architecture patterns and constraints
The implementation must adhere to the backend service pattern defined in the architecture, where the `ai_service.py` module acts as a secure and isolated interface to the Gemini API. All API communication must happen server-to-server; the client-side application must not have direct access to the API key or service.

### Source tree components to touch
- **`ai_service.py`**: New file to be created in the project root.
- **`requirements.txt`**: Modified to add the `google-generativeai` dependency.
- **`.env.example`**: Modified to include `GEMINI_API_KEY`.
- **`tests/`**: A new unit test file will be added to cover the `ai_service.py` module.

### Testing standards summary
Unit tests are required for the new `ai_service.py` module. Tests should mock the external API call to ensure a fast, isolated, and deterministic test run. The tests must cover both successful responses and potential API error states.

### References
- [Source: docs/fase-3-solutioning/architecture.md#Services]
- [Source: docs/sprint-artifacts/tech-spec-epic-2.md#Detailed-Design]

## Project Structure Alignment

This story will create one new file:
*   `ai_service.py`: This module will be created in the root directory as specified in the Architecture Document (`docs/fase-3-solutioning/architecture.md`).

And modify one existing file:
*   `requirements.txt`: To add the `google-generativeai` dependency.

This aligns with the project's modular approach of separating concerns, with AI-specific logic being encapsulated within its own service file.

## Dev Agent Record

### Context Reference
- `docs/sprint-artifacts/2-1-gemini-api-integration.context.xml`

### Agent Model Used

{{agent_model_name_version}}

### Debug Log References

### Completion Notes List

### File List

- ai_service.py

- requirements.txt

- .env.example

- tests/test_ai_service.py


