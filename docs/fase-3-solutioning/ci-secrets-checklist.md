# CI/CD Secrets Checklist

This document outlines the secrets required for the CI/CD pipeline and provides guidance on how to configure them securely in your CI platform (GitHub Actions).

---

## 1. Required Secrets

| Secret Name        | Description                                                               | Where Used               | Example Value        |
| :----------------- | :------------------------------------------------------------------------ | :----------------------- | :------------------- |
| `BASE_URL`         | Base URL of the application under test (staging/deployed instance)        | Playwright tests         | `https://my-app.com` |
| `API_URL`          | Base URL for API calls (staging/deployed instance)                        | Playwright tests         | `https://api.my-app.com` |
| `TEST_USER_EMAIL`  | Email of a dedicated test user for E2E authentication                     | Playwright tests         | `e2e@example.com`    |
| `TEST_USER_PASSWORD` | Password for the dedicated test user                                      | Playwright tests         | `superSecretPa$$word` |
| `API_TOKEN`        | API token for seeding test data or making authenticated backend calls     | Data factories           | `ghp_abcdef12345`    |
| `SLACK_WEBHOOK`    | Webhook URL for Slack notifications on CI failure (Optional)              | Notification action      | `https://hooks.slack.com/...` |
| `GEMINI_API_KEY`   | API Key for Google Gemini (used by AI service) - if not managed otherwise | AI service integration   | `AIzaSyB-xxxxxxxxxx` |

---

## 2. How to Configure Secrets in GitHub Actions

GitHub Actions secrets are stored securely in your repository settings and are not exposed in logs.

1.  **Navigate to your repository**: Go to your GitHub repository on `github.com`.
2.  **Go to Settings**: Click on the "Settings" tab.
3.  **Secrets and variables**: In the left sidebar, click on "Secrets and variables" and then select "Actions".
4.  **New repository secret**: Click the "New repository secret" button.
5.  **Add Secret**:
    *   **Name**: Enter the `Secret Name` exactly as listed in Section 1 (e.g., `BASE_URL`).
    *   **Value**: Enter the corresponding `Example Value` (your actual secret value).
6.  **Repeat**: Repeat steps 4-5 for all required secrets.

---

## 3. Best Practices for Secrets Management

*   **Never hardcode secrets**: Secrets should never be committed directly into your codebase.
*   **Use environment variables**: Access secrets in your CI workflow via `secrets.<SECRET_NAME>`.
*   **Rotate secrets regularly**: Change API keys and passwords periodically.
*   **Least privilege**: Grant secrets only the minimum necessary permissions.
*   **Do not log secrets**: Ensure secrets are not accidentally printed in CI logs.
*   **Dedicated test accounts**: Use separate test user accounts with limited privileges for automated tests.

---

## 4. Local Environment Variables

For local testing, you can use a `.env` file in your project root to store environment variables.

*   Copy `/.env.example` to `/.env`.
*   Fill in values for `BASE_URL`, `API_URL`, etc.
*   **NEVER commit your `.env` file to Git.** Ensure it's listed in `.gitignore`.

---
