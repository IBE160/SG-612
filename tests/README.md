# Test Suite Documentation

## Setup Instructions

1.  **Install Node.js dependencies**: Ensure you have Node.js (v20.11.0 recommended) installed. Navigate to the project root and run:
    ```bash
    npm install
    ```
2.  **Environment Variables**: Copy `.env.example` to `.env` and configure `BASE_URL` and `API_URL` to point to your application's running instances.
    ```bash
    cp .env.example .env
    # Edit .env with your application URLs
    ```
3.  **Run Application**: Ensure your Flask application is running on the configured `BASE_URL`.

## Running Tests

From the project root, use the following command:

```bash
npm run test:e2e
```

**Additional Commands:**

*   **Headed Mode (show browser UI)**: `npx playwright test --headed`
*   **Debug Mode (Playwright Inspector)**: `npx playwright test --debug`
*   **Show HTML Report**: After a test run, open the report with `npx playwright show-report`

## Architecture Overview

### Fixture Architecture

The framework uses a fixture-based architecture (see `tests/support/fixtures/index.ts`) to provide isolated test environments and reusable setup/teardown logic.
*   **`UserFactory`**: A key fixture (`tests/support/fixtures/factories/user-factory.ts`) for creating and managing test users via API calls, ensuring automatic cleanup after each test run.

### Data Factories

`@faker-js/faker` is integrated to generate unique, realistic test data on demand, preventing test collisions and improving reliability.

### Page Objects (Optional)

Consider implementing Page Object Models in `tests/support/page-objects/` for complex UI interactions to improve maintainability.

### Selector Strategy

Tests primarily use `data-testid` attributes for selecting UI elements, ensuring robust and resilient selectors against UI changes.

## Best Practices

*   **Test Isolation**: Tests are designed to be independent and self-cleaning.
*   **API-First Setup**: Utilize API calls for test setup (e.g., creating users) to ensure fast and reliable test execution.
*   **Deterministic Waits**: Avoid hard-coded waits (`waitForTimeout`). Use Playwright's smart waits or explicit waits for network responses.

## CI Integration

The `playwright.config.ts` is configured for CI environments, including:
*   `retries` on failure.
*   `screenshot` and `video` capture on failure.
*   `junit` reporter for CI/CD dashboards.
*   `fullyParallel` execution with a single worker in CI to manage resources.

## Knowledge Base References

*   **Fixture Architecture**: `testarch/knowledge/fixture-architecture.md`
*   **Data Factories**: `testarch/knowledge/data-factories.md`
*   **Test Quality**: `testarch/knowledge/test-quality.md`
*   **Playwright Config**: `testarch/knowledge/playwright-config.md`
