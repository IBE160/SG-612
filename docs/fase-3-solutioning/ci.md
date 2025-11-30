# CI/CD Pipeline Guide

This document provides an overview of the CI/CD pipeline set up for the project using GitHub Actions. It covers the pipeline stages, how to run tests locally, debugging CI failures, and secrets management.

---

## 1. Pipeline Overview

The CI/CD pipeline is defined in `.github/workflows/test.yml` and consists of the following stages:

*   **Lint**: Code quality checks (e.g., ESLint, Prettier, Python linting) to ensure code style and catch basic errors.
*   **Test**: Parallel execution of end-to-end (E2E) tests across multiple shards for faster feedback.
*   **Burn-in**: A loop that runs the test suite multiple times to detect flaky tests (non-deterministic failures).
*   **Report**: Aggregates test results and provides a summary.

### Performance Targets

*   **Lint stage**: <2 minutes
*   **Test stage** (per shard): <10 minutes
*   **Burn-in stage**: <30 minutes (10 iterations)
*   **Total pipeline**: <45 minutes (approx. 20x faster than sequential execution)

---

## 2. Running CI Stages Locally

Several helper scripts are provided in the `scripts/` directory to mirror CI behavior locally.

### `scripts/ci-local.sh`

This script simulates the full CI pipeline locally (with reduced burn-in iterations) for debugging.

```bash
./scripts/ci-local.sh
```

### `scripts/test-changed.sh`

This script runs only tests affected by recent Git changes (based on changed `.ts` files). Useful for faster feedback during development.

```bash
./scripts/test-changed.sh
```

### `scripts/burn-in.sh`

Execute the burn-in loop independently for deeper investigation of flaky tests. You can specify the number of iterations.

```bash
./scripts/burn-in.sh           # Runs 10 iterations (default)
./scripts/burn-in.sh 50        # Runs 50 iterations
```

---

## 3. Debugging CI Failures

### Check Workflow Logs

Always start by reviewing the logs of the failed job in GitHub Actions. Look for specific error messages or stack traces.

### Download Artifacts

On test failures, Playwright traces, screenshots, and videos are automatically uploaded as artifacts. Download these artifacts from the GitHub Actions run to debug failures locally.

### Local CI Mirror

Use `./scripts/ci-local.sh` to reproduce the CI environment and debug failures on your local machine.

### Playwright Debugger

For Playwright E2E tests, use `npx playwright test --debug` or `npm run test:e2e -- --debug` to launch the Playwright Inspector and step through tests.

---

## 4. Secrets and Environment Variables

The CI pipeline may require secrets for sensitive information (e.g., API keys, slack webhooks). These must be configured in your GitHub repository's secrets settings.

### Required Secrets Checklist (`docs/ci-secrets-checklist.md`)

Refer to `docs/ci-secrets-checklist.md` for a list of secrets required by the pipeline and instructions on how to configure them.

### Environment Variables

*   **`BASE_URL`**: The base URL of the application under test (e.g., `http://localhost:3000` for local, staging URL for CI).
*   **`API_URL`**: The base URL for API calls (e.g., `http://localhost:3001/api`).
*   **`CI`**: Automatically set to `true` by most CI platforms. Used in Playwright config for CI-specific behavior (e.g., retries).

---

## 5. Pipeline Stages Details

### Lint Stage

*   **Purpose**: Ensure code quality, style consistency, and early detection of syntax errors across the entire codebase.
*   **Tools**:
    *   **Python**: `ruff` for fast linting and `black` for code formatting. These are run directly in the CI pipeline.
    *   **JavaScript/TypeScript**: If applicable, tools like ESLint and Prettier would be configured and run via a script like `npm run lint`.
*   **Failure Impact**: Blocks subsequent stages to ensure no low-quality code is tested or merged.

### Test Stage (Parallel Sharding)

*   **Purpose**: Execute E2E tests across multiple parallel jobs to reduce overall execution time.
*   **Shards**: The pipeline is configured for 4 parallel shards by default. Each shard runs a subset of the tests.
*   **Test Command**: `npm run test:e2e -- --shard=${{ matrix.shard }}/4`
*   **Artifacts**: On failure, Playwright traces, screenshots, and reports are uploaded.

### Burn-in Stage

*   **Purpose**: Detect flaky (non-deterministic) tests by running the full test suite multiple times.
*   **Iterations**: Configured for 10 iterations. Even a single failure indicates flakiness that needs to be addressed.
*   **Trigger**: Runs on Pull Requests to `main`/`develop` branches and on a weekly schedule.
*   **Failure Impact**: A failing burn-in indicates a critical quality issue and should block merges.

### Report Stage

*   **Purpose**: Aggregate results from all test and burn-in jobs and provide a summary.
*   **Output**: Creates a summary directly visible in the GitHub Actions UI.

---

## 6. Optimization Features

*   **Caching**: Node.js dependencies (`~/.npm`) and Playwright browser binaries (`~/.cache/ms-playwright`) are cached to speed up subsequent CI runs.
*   **Parallelization**: Tests are split into 4 shards to run concurrently, significantly reducing total execution time.
*   **Artifacts on Failure**: Only test artifacts from failing jobs are uploaded, saving storage and improving performance for successful runs.

---

## 7. Knowledge Base References

*   `ci-burn-in.md`: Burn-in loop patterns, shard orchestration.
*   `selective-testing.md`: Changed test detection strategies.
*   `visual-debugging.md`: Artifact collection best practices.
*   `test-quality.md`: CI-specific test quality criteria.
*   `playwright-config.md`: CI-optimized Playwright configuration.
