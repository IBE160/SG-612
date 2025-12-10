import { test, expect } from '@playwright/test';

test.describe('Smart List Features', () => {
    test.beforeEach(async ({ page }) => {
        // Navigate to the base URL of the application
        await page.goto('/');
        await expect(page.locator('h1')).toHaveText('Your Tasks');
        
        // Add some tasks for testing smart lists
        // Ensure the database is clean before adding tasks, perhaps via API
        // For simplicity, directly adding via UI for E2E
        
        // High Priority Task 1
        await page.click('#addTaskBtn');
        await page.fill('#taskTitle', 'E2E High Priority Task 1');
        await page.selectOption('#taskPriority', 'High');
        await page.click('button[type="submit"]');
        await expect(page.locator('#addTaskModal')).not.toBeVisible();

        // Medium Priority Task
        await page.click('#addTaskBtn');
        await page.fill('#taskTitle', 'E2E Medium Priority Task');
        await page.selectOption('#taskPriority', 'Medium');
        await page.click('button[type="submit"]');
        await expect(page.locator('#addTaskModal')).not.toBeVisible();

        // High Priority Task 2
        await page.click('#addTaskBtn');
        await page.fill('#taskTitle', 'E2E High Priority Task 2');
        await page.selectOption('#taskPriority', 'High');
        await page.click('button[type="submit"]');
        await expect(page.locator('#addTaskModal')).not.toBeVisible();

        // Low Priority Task
        await page.click('#addTaskBtn');
        await page.fill('#taskTitle', 'E2E Low Priority Task');
        await page.selectOption('#taskPriority', 'Low');
        await page.click('button[type="submit"]');
        await expect(page.locator('#addTaskModal')).not.toBeVisible();
    });

    test('should filter tasks by High Priority when "High Priority" smart list is clicked', async ({ page }) => {
        // Click the "High Priority" smart list button
        await page.click('#highPriorityBtn');

        // Expect only high priority tasks to be visible
        await expect(page.locator('.task-card')).toHaveCount(2);
        await expect(page.locator('.task-card:has-text("E2E High Priority Task 1")')).toBeVisible();
        await expect(page.locator('.task-card:has-text("E2E High Priority Task 2")')).toBeVisible();
        await expect(page.locator('.task-card:has-text("E2E Medium Priority Task")')).not.toBeVisible();
        await expect(page.locator('.task-card:has-text("E2E Low Priority Task")')).not.toBeVisible();

        // Click "All Tasks" to reset filter
        await page.click('#allTasksBtn');
        await expect(page.locator('.task-card')).toHaveCount(4); // All tasks should be visible again
    });
});