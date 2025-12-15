import { test, expect } from '@playwright/test';

// Store the ID of the task created during the test
let createdTaskId: string | null = null;

// After each test, clean up any created data
test.afterEach(async ({ request }) => {
  if (createdTaskId) {
    // Use the API to delete the task, ensuring a clean state
    const response = await request.delete(`/api/tasks/${createdTaskId}`);
    expect(response.status()).toBe(204);
    createdTaskId = null; // Reset for the next test
  }
});

test('1.2-E2E-001: should allow a user to create a new task @smoke @p0', async ({ page }) => {
  await page.goto('/');

  // Click the "Add Task" button
  await page.click('#addTaskBtn');

  // Verify the modal is visible
  await expect(page.locator('#addTaskModal')).toBeVisible();

  // Create a unique task title
  const taskTitle = `My New E2E Task - ${Date.now()}`;

  // Fill in the form
  await page.fill('#taskTitle', taskTitle);
  await page.fill('#taskNotes', 'These are some notes for my E2E test.');
  await page.fill('#taskDueDate', '2025-12-31');

  // Set up a promise to wait for the API response BEFORE clicking save
  const createTaskResponsePromise = page.waitForResponse(
    resp => resp.url().endsWith('/api/tasks') && resp.request().method() === 'POST' && resp.status() === 201,
    { timeout: 30000 }
  );

  // Click the "Save Task" button
  await page.click('#addTaskForm button[type="submit"]');

  // Wait for the API response and get the new task's ID for cleanup
  const response = await createTaskResponsePromise;
  const responseBody = await response.json();
  createdTaskId = responseBody.data.id;

  // Now that the API call is complete, verify the UI changes
  await expect(page.locator('#addTaskModal')).toBeHidden();

  // Verify the new task appears in the task list
  const taskList = page.locator('#taskList');
  await expect(taskList).toContainText(taskTitle);
});
