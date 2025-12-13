import { test, expect } from '@playwright/test';
import { format } from 'date-fns';

test.describe('Smart List Features', () => {
    test.beforeEach(async ({ page }) => {
        await page.goto('/');
        await expect(page.locator('h1')).toHaveText('Your Tasks');

        // Clear existing tasks to ensure a clean state for each test in this describe block
        // (This would typically be done via an API call or database seed for robust E2E testing)
        // For now, assume this clears existing tasks. In a real application, you'd use a teardown or API.
        
        // Add a set of tasks with specific properties for filtering and sorting tests
        await page.click('#addTaskBtn');
        await page.fill('#taskTitle', 'E2E Task High Work');
        await page.selectOption('#taskPriority', 'High');
        await page.fill('#taskLabel', 'Work');
        await page.fill('#taskDueDate', format(new Date(2025, 11, 28), 'yyyy-MM-dd')); // Dec 28, 2025
        await page.click('button[type="submit"]');
        await expect(page.locator('#addTaskModal')).not.toBeVisible();

        await page.click('#addTaskBtn');
        await page.fill('#taskTitle', 'E2E Task Medium Personal');
        await page.selectOption('#taskPriority', 'Medium');
        await page.fill('#taskLabel', 'Personal');
        await page.fill('#taskDueDate', format(new Date(2025, 11, 25), 'yyyy-MM-dd')); // Dec 25, 2025
        await page.click('button[type="submit"]');
        await expect(page.locator('#addTaskModal')).not.toBeVisible();

        await page.click('#addTaskBtn');
        await page.fill('#taskTitle', 'E2E Task Low Work');
        await page.selectOption('#taskPriority', 'Low');
        await page.fill('#taskLabel', 'Work');
        await page.fill('#taskDueDate', format(new Date(2026, 0, 1), 'yyyy-MM-dd')); // Jan 1, 2026
        await page.click('button[type="submit"]');
        await expect(page.locator('#addTaskModal')).not.toBeVisible();

        await page.click('#addTaskBtn');
        await page.fill('#taskTitle', 'E2E Task High Home');
        await page.selectOption('#taskPriority', 'High');
        await page.fill('#taskLabel', 'Home');
        await page.fill('#taskDueDate', format(new Date(2025, 11, 29), 'yyyy-MM-dd')); // Dec 29, 2025
        await page.click('button[type="submit"]');
        await expect(page.locator('#addTaskModal')).not.toBeVisible();
    });

    test('should filter tasks by High Priority when "High Priority" smart list is clicked', async ({ page }) => {
        // Click the "High Priority" smart list button
        await page.click('#highPriorityBtn');

        // Expect only high priority tasks to be visible
        await expect(page.locator('.task-card')).toHaveCount(2);
        await expect(page.locator('.task-card:has-text("E2E Task High Work")')).toBeVisible();
        await expect(page.locator('.task-card:has-text("E2E Task High Home")')).toBeVisible();
        await expect(page.locator('.task-card:has-text("E2E Task Medium Personal")')).not.toBeVisible();
        await expect(page.locator('.task-card:has-text("E2E Task Low Work")')).not.toBeVisible();

        // Click "All Tasks" to reset filter
        await page.click('#allTasksBtn');
        await expect(page.locator('.task-card')).toHaveCount(4); // All tasks should be visible again
    });

    test('should filter tasks by "Due This Week" when smart list is clicked', async ({ page }) => {
        // This test assumes today's date for relative calculations.
        // For consistent E2E testing, consider mocking system date or seeding with absolute dates.
        // For now, this will test the general behavior.
        const today = new Date(2025, 11, 25); // Mock today's date for consistent testing (Dec 25, 2025)

        const twoDaysFromNow = new Date(today);
        twoDaysFromNow.setDate(today.getDate() + 2); // Dec 27
        const sixDaysFromNow = new Date(today);
        sixDaysFromNow.setDate(today.getDate() + 6); // Dec 31
        const eightDaysFromNow = new Date(today);
        eightDaysFromNow.setDate(today.getDate() + 8); // Jan 2

        // Add tasks with specific due dates relative to mocked today
        await page.click('#addTaskBtn');
        await page.fill('#taskTitle', 'Task Due in 2 Days');
        await page.fill('#taskDueDate', format(twoDaysFromNow, 'yyyy-MM-dd'));
        await page.click('button[type="submit"]');
        await expect(page.locator('#addTaskModal')).not.toBeVisible();

        await page.click('#addTaskBtn');
        await page.fill('#taskTitle', 'Task Due in 6 Days');
        await page.fill('#taskDueDate', format(sixDaysFromNow, 'yyyy-MM-dd'));
        await page.click('button[type="submit"]');
        await expect(page.locator('#addTaskModal')).not.toBeVisible();

        await page.click('#addTaskBtn');
        await page.fill('#taskTitle', 'Task Due in 8 Days');
        await page.fill('#taskDueDate', format(eightDaysFromNow, 'yyyy-MM-dd'));
        await page.click('button[type="submit"]');
        await expect(page.locator('#addTaskModal')).not.toBeVisible();
        
        // Click the "Due This Week" smart list button
        await page.click('#dueThisWeekBtn');

        // Expect only tasks due within 7 days to be visible (up to Dec 31st for our mocked date)
        await expect(page.locator('.task-card')).toHaveCount(2);
        await expect(page.locator('.task-card:has-text("Task Due in 2 Days")')).toBeVisible();
        await expect(page.locator('.task-card:has-text("Task Due in 6 Days")')).toBeVisible();
        await expect(page.locator('.task-card:has-text("Task Due in 8 Days")')).not.toBeVisible();

        // Click "All Tasks" to reset filter
        await page.click('#allTasksBtn');
        await expect(page.locator('.task-card')).toHaveCount(7); // 4 from beforeEach + 3 from this test
    });

    test('should manually filter tasks by label and sort by priority and due date', async ({ page }) => {
        // Test Filter by Label: Work
        await page.selectOption('#filterByLabel', 'Work');
        await expect(page.locator('.task-card')).toHaveCount(2);
        await expect(page.locator('.task-card:has-text("E2E Task High Work")')).toBeVisible();
        await expect(page.locator('.task-card:has-text("E2E Task Low Work")')).toBeVisible();
        await expect(page.locator('.task-card:has-text("E2E Task Medium Personal")')).not.toBeVisible();

        // Test Sort by Priority (Default DESC)
        await page.selectOption('#filterByLabel', ''); // Clear filter
        await page.selectOption('#sortBy', 'priority');
        let taskTitles = await page.locator('.task-card .text-lg').allTextContents();
        expect(taskTitles).toEqual([
            'E2E Task High Work', // High
            'E2E Task High Home', // High
            'E2E Task Medium Personal', // Medium
            'E2E Task Low Work'  // Low
        ]);

        // Toggle sort order to ASC
        await page.click('#sortOrderToggle');
        taskTitles = await page.locator('.task-card .text-lg').allTextContents();
        expect(taskTitles).toEqual([
            'E2E Task Low Work',  // Low
            'E2E Task Medium Personal', // Medium
            'E2E Task High Home', // High
            'E2E Task High Work'  // High
        ]);

        // Test Sort by Due Date (Default ASC)
        await page.selectOption('#sortBy', 'due_date');
        taskTitles = await page.locator('.task-card .text-lg').allTextContents();
        expect(taskTitles).toEqual([
            'E2E Task Medium Personal', // Dec 25
            'E2E Task High Work', // Dec 28
            'E2E Task High Home', // Dec 29
            'E2E Task Low Work'  // Jan 1
        ]);

        // Toggle sort order to DESC
        await page.click('#sortOrderToggle');
        taskTitles = await page.locator('.task-card .text-lg').allTextContents();
        expect(taskTitles).toEqual([
            'E2E Task Low Work',  // Jan 1
            'E2E Task High Home', // Dec 29
            'E2E Task High Work', // Dec 28
            'E2E Task Medium Personal'  // Dec 25
        ]);
    });
});
