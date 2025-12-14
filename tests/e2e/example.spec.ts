import { test, expect } from '../support/fixtures';

test.describe.skip('AUTH-E2E @p0 @smoke', () => {
  test('AUTH-E2E-001: should load homepage', async ({ page }) => {
    await page.goto('/');
    // Corrected title to match the actual application title
    await expect(page).toHaveTitle(/Smart To-Do List/);
  });

  test('AUTH-E2E-002: should create user and login', async ({ page, userFactory }) => {
    // --- Given ---
    // Create test user via factory, which also handles API creation
    const user = await userFactory.createUser();

    // --- When ---
    await page.goto('/login');
    await page.fill('[data-testid="email-input"]', user.email);
    await page.fill('[data-testid="password-input"]', user.password);

    // Set up explicit wait for the login network response
    const loginResponsePromise = page.waitForResponse(resp =>
      resp.url().includes('/api/login') && resp.status() === 200
    );
    await page.click('[data-testid="login-button"]');
    await loginResponsePromise;

    // --- Then ---
    // Assert login success by checking for a user-specific element
    await expect(page.locator('[data-testid="user-menu"]')).toBeVisible();
  });
});
