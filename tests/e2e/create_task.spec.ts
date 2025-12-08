import { test, expect } from '@playwright/test';

test('should allow a user to create a new task', async ({ page }) => {
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

  // Click the "Save Task" button
  await page.click('#addTaskForm button[type="submit"]');

  // Verify the modal is hidden
  await expect(page.locator('#addTaskModal')).toBeHidden();

  // Verify the new task appears in the task list
  const taskList = page.locator('#taskList');
  await expect(taskList).toContainText(taskTitle);
});
