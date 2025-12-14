import { test, expect } from '../support/fixtures';

test.describe('2.2-E2E-MagicFill @p1 @regression', () => {

  test('2.2-E2E-001: should populate fields using Magic Fill in Add Task modal', async ({ page }) => {
    // --- Given ---
    await page.goto('/');
    await page.click('#addTaskBtn');
    await expect(page.locator('#addTaskModal')).toBeVisible();

    // --- When ---
    const taskTitle = 'Plan team meeting agenda for next week';
    await page.fill('#taskTitle', taskTitle);

    const suggestResponse = page.waitForResponse(resp => resp.url().includes('/api/suggest'));
    await page.click('#magicFillAddTaskBtn');
    await suggestResponse;

    // --- Then ---
    await expect(page.locator('#taskLabel')).not.toBeEmpty();
    await expect(page.locator('#taskPriority')).not.toBeEmpty();
  });

  test('2.2-E2E-002: should populate fields using Magic Fill in Edit Task modal', async ({ page, seedTasks }) => {
    // --- Given ---
    const [task] = await seedTasks([{ title: 'Task to be edited' }]);
    await page.goto('/');
    // Explicitly wait for the initial task fetch to complete
    await page.waitForResponse(resp => resp.url().includes('/api/tasks') && resp.status() === 200);
    await expect(page.locator('.task-card')).toBeVisible();

    // --- When ---
    await page.hover(`.task-card:has-text("${task.title}")`);
    await page.click('.edit-task-btn');
    await expect(page.locator('#editTaskModal')).toBeVisible();

    const suggestResponse = page.waitForResponse(resp => resp.url().includes('/api/suggest'));
    await page.click('#magicFillEditTaskBtn');
    await suggestResponse;

    // --- Then ---
    await expect(page.locator('#editTaskLabel')).not.toBeEmpty();
    await expect(page.locator('#editTaskPriority')).not.toBeEmpty();
  });

  test('2.3-E2E-001: should show fallback notification when AI service fails', async ({ page }) => {
    // --- Given ---
    await page.route('**/api/suggest', route => {
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ priority: 'Low', label: 'Other', fallback: true }),
      });
    });
    await page.goto('/');
    await page.click('#addTaskBtn');
    await expect(page.locator('#addTaskModal')).toBeVisible();

    // --- When ---
    await page.fill('#taskTitle', 'Task title for fallback test');
    await page.click('#magicFillAddTaskBtn');

    // --- Then ---
    await expect(page.locator('#toast-fallback')).toBeVisible();
    await expect(page.locator('#toast-fallback')).toContainText('AI unavailable, used fallback suggestions.');

    await expect(page.locator('#taskLabel')).toHaveValue('Other');
    await expect(page.locator('#taskPriority')).toHaveValue('Low');
  });
});