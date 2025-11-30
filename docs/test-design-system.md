# System-Level Test Design

**Date:** {date}
**Author:** {user_name}
**Status:** Draft

---

## 1. Testability Assessment
<template-output>
### Controllability
- **State Control**: **PASS**. The architecture's use of a simple SQLite database and a clear REST API for data manipulation allows for excellent state control. Test data can be seeded via API calls (e.g., `POST /api/tasks`) before tests run, ensuring predictable states.
- **Dependency Mocking**: **PASS**. The primary external dependency (Google Gemini API) is well-isolated in `ai_service.py`. This allows it to be easily mocked or stubbed, enabling tests to run without incurring API costs or dealing with network instability.
- **Error Injection**: **CONCERNS**. The architecture does not specify a mechanism for injecting errors or simulating failures (e.g., failed API calls, database connection issues). This makes it difficult to test the system's resilience and fallback logic (like the keyword-based fallback for AI suggestions) under adverse conditions.

### Observability
- **State Inspection**: **PASS**. The REST API provides clear endpoints (`GET /api/tasks`, `GET /api/tasks/<id>`) for inspecting system state, which is sufficient for validation in tests.
- **Result Determinism**: **PASS**. The architecture encourages practices that support determinism, such as API-based data seeding. The risk of front-end race conditions is standard and can be mitigated with network-first interception patterns during test implementation.
- **NFR Validation**: **CONCERNS**. The PRD specifies performance NFRs (e.g., "load within 1-2 seconds"). However, the architecture only includes basic logging and lacks dedicated observability tools (e.g., metrics endpoints, integration with Prometheus/Grafana) to measure and validate these requirements under load.

### Reliability
- **Test Isolation**: **PASS**. The file-based SQLite database makes it trivial to provide a clean, isolated database for each test run, preventing state pollution and enabling parallel execution.
- **Failure Reproduction**: **PASS**. The combination of API-based state control and a simple database structure should make reproducing failures straightforward.
- **Component Coupling**: **PASS**. The core application logic (`app.py`) and AI logic (`ai_service.py`) are loosely coupled, allowing them to be tested independently. This is a strong positive for maintainable tests.
</template-output>

---

## 2. Architecturally Significant Requirements (ASRs)
<template-output>
| ASR ID | Requirement Description | Category | Justification | Risk Score (P×I) |
|--------|-------------------------|----------|---------------|------------------|
| ASR-01 | API key for Google Gemini must not be exposed on the client-side. | SEC | A compromised API key could lead to unauthorized use and significant cost. This is a critical security requirement. | 3×3 = 9 |
| ASR-02 | AI suggestion responses should be returned within 1-2 seconds. | PERF | A slow response from the core "smart" feature would lead to a poor user experience, undermining the product's value proposition. | 2×3 = 6 |
| ASR-03 | The application must provide a rule-based fallback if the AI service is unavailable. | REL | The application's core functionality should not be blocked by the failure of an external dependency. | 3×2 = 6 |
| ASR-04 | The application must follow WCAG 2.1 AA guidelines. | BUS | Ensuring accessibility is a core business requirement to serve all potential users. | 2×2 = 4 |
</template-output>

---

## 3. Test Levels Strategy
<template-output>
- **Unit Tests**: 50%
- **Integration/API Tests**: 35%
- **End-to-End (E2E) Tests**: 15%

**Rationale**: This strategy forms a stable test pyramid.
- **Unit tests (50%)** will provide a strong foundation by covering business logic in isolation (e.g., rule-based fallback logic, date calculations) quickly and reliably.
- **API tests (35%)** are critical for this architecture. They will validate the core application logic, database interactions, and API contracts without the overhead of UI rendering. This is the most efficient way to test the majority of the functionality.
- **E2E tests (15%)** will be reserved for validating critical user journeys only (e.g., creating a task, using "Magic Fill," and seeing the task in a smart list). This provides high confidence in the integrated system while minimizing slow, brittle tests.
</template-output>

---

## 4. NFR (Non-Functional Requirement) Testing Approach
<template-output>
### Security
- **Approach**: A multi-layered approach will be used.
  1.  **SAST (Static Application Security Testing)**: Integrate a linter like `bandit` into CI to scan Python code for common vulnerabilities.
  2.  **Dependency Scanning**: Use `pip-audit` or GitHub's Dependabot to scan for known vulnerabilities in third-party libraries.
  3.  **Penetration Testing (Manual/E2E)**: E2E tests will validate authentication and authorization flows (e.g., ensure unauthenticated users cannot access API endpoints).
- **Tools**: `bandit`, `pip-audit`, Playwright.

### Performance
- **Approach**:
  1.  **API Load Testing**: The primary NFR is API response time. Key endpoints (`/api/tasks`, `/api/suggest`) will be load-tested to ensure they meet the 1-2 second response time SLA under a simulated load of concurrent users.
  2.  **Frontend Audits**: Automated Lighthouse audits will be run in CI to monitor frontend performance metrics (LCP, FCP).
- **Tools**: `k6` (for API load testing), `Lighthouse` (for frontend).

### Reliability
- **Approach**: The main reliability risk is the external Gemini API. Testing will focus on the system's resilience to its failure.
  1.  **Mocked Failures**: Integration tests will mock a failed response from `ai_service.py` to verify that the rule-based fallback is triggered correctly and the UI communicates this appropriately.
- **Tools**: `pytest-mock`, Playwright.

### Maintainability
- **Approach**:
  1.  **Code Coverage**: Enforce a minimum code coverage threshold (e.g., 80%) for backend unit and integration tests.
  2.  **Linting**: Integrate `ruff` and `black` into the CI pipeline to enforce a consistent code style.
- **Tools**: `pytest-cov`, `ruff`, `black`.
</template-output>

---

## 5. Test Environment Requirements
<template-output>
- **Local Development**: Developers will run unit and API tests locally against a local SQLite database file. This file should be gitignored.
- **Staging/QA**: A dedicated, production-like environment hosted on Render. Tests will run against a clean database on every deployment. This environment will be used for E2E tests and performance tests.
- **Production**: Monitoring and alerting will be the primary quality mechanism. No tests will run against the live production environment.
</template-output>

---

## 6. Testability Concerns
<template-output>
| Concern ID | Concern Description | Impact | Recommendation |
|------------|---------------------|--------|----------------|
| C-01 | **No built-in error injection mechanism.** The architecture lacks a defined way to simulate failures (e.g., Gemini API outage, database errors), making it difficult to test system resilience. | Medium | Implement a simple mechanism (e.g., via environment variables or special API headers) to force failure modes in the `ai_service.py` and database connection logic for testing purposes. |
| C-02 | **No dedicated observability tooling.** The architecture relies on basic logging. This makes it difficult to validate performance NFRs (e.g., "1-2 second response time") under load. | Medium | Instrument the Flask application with Prometheus metrics. Expose a `/metrics` endpoint that can be scraped to monitor API latency and error rates during performance tests. |
</template-output>

---

## 7. Recommendations for Sprint 0
<template-output>
- **Framework Setup (`*framework` workflow)**: Proceed with initializing a Playwright framework for E2E tests and `pytest` for API/unit tests. Implement a fixture to provide a clean SQLite database for each test run.
- **CI/CD Pipeline (`*ci` workflow)**: Scaffold a basic CI pipeline (e.g., GitHub Actions) that runs `ruff` for linting and executes the `pytest` suite. Add a later job for Playwright E2E tests that runs only on PRs to the main branch.
</template-output>

---
## Appendix

### Knowledge Base References
- `nfr-criteria.md`
- `test-levels-framework.md`
- `risk-governance.md`
- `test-quality.md`

### Related Documents
- PRD: `docs/prd.md`
- Architecture: `docs/architecture.md`
- Epics: `docs/epics.md`
