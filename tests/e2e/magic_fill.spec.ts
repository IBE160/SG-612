import { test, expect } from '@playwright/test';

test.describe('Magic Fill AI Suggestions', () => {
    test.beforeEach(async ({ page }) => {
        // Navigate to the base URL of the application
        await page.goto('/');
        await expect(page.locator('h1')).toHaveText('Your Tasks');
    });

    test('should populate label and priority fields using Magic Fill in Add Task modal', async ({ page }) => {
        // Click the 'Add Task' button to open the modal
        await page.click('#addTaskBtn');
        await expect(page.locator('#addTaskModal')).toBeVisible();

        // Enter a task title
        const taskTitle = 'Plan team meeting agenda for next week';
        await page.fill('#taskTitle', taskTitle);

        // Click the 'Magic Fill' button
        await page.click('#magicFillAddTaskBtn');

        // Wait for the API call to complete and fields to be populated
        // The button should be disabled during the call and re-enabled afterwards
        await expect(page.locator('#magicFillAddTaskBtn')).not.toBeDisabled();

        // Verify that the label and priority fields are populated
        // Since we are mocking the AI, we expect the fallback values
        // If the AI service is functional, these would be dynamic
        await expect(page.locator('#taskLabel')).not.toBeEmpty();
        await expect(page.locator('#taskPriority')).not.toBeEmpty();

        // Optionally, check for specific values if the AI behavior is deterministic enough or mocked
        // For now, just checking they are not empty is sufficient to verify population
        console.log(`Magic Fill Add Task - Label: ${await page.locator('#taskLabel').inputValue()}, Priority: ${await page.locator('#taskPriority').inputValue()}`);

        // Close the modal
        await page.click('#closeModalBtn');
        await expect(page.locator('#addTaskModal')).not.toBeVisible();
    });

    test('should populate label and priority fields using Magic Fill in Edit Task modal', async ({ page }) => {
        // First, add a task to be able to edit it
        await page.click('#addTaskBtn');
        await page.fill('#taskTitle', 'Task to be edited');
        await page.click('button[type="submit"]'); // Save task
        await expect(page.locator('#addTaskModal')).not.toBeVisible();
        await expect(page.locator('.task-card')).toBeVisible(); // Assuming task is rendered as a .task-card

        // Click the edit button for the newly created task
        // Assuming there's only one task for simplicity, or we can get the first one
        await page.hover('.task-card'); // Trigger hover to show edit/delete buttons
        await page.click('.edit-task-btn');
        await expect(page.locator('#editTaskModal')).toBeVisible();

        // Get the task title from the edit modal
        const editTaskTitle = await page.locator('#editTaskTitle').inputValue();

        // Click the 'Magic Fill' button in the edit modal
        await page.click('#magicFillEditTaskBtn');

        // Wait for the API call to complete
        await expect(page.locator('#magicFillEditTaskBtn')).not.toBeDisabled();

        // Verify that the label and priority fields are populated
        await expect(page.locator('#editTaskLabel')).not.toBeEmpty();
        await expect(page.locator('#editTaskPriority')).not.toBeEmpty();

        console.log(`Magic Fill Edit Task - Label: ${await page.locator('#editTaskLabel').inputValue()}, Priority: ${await page.locator('#editTaskPriority').inputValue()}`);

        // Close the modal
        await page.click('#closeEditModalBtn');
        await expect(page.locator('#editTaskModal')).not.toBeVisible();
    });

    test('should show fallback notification when AI service fails', async ({ page }) => {
        // Intercept the /api/suggest call and mock a fallback response
        await page.route('**/api/suggest', route => {
            route.fulfill({
                status: 200,
                contentType: 'application/json',
                body: JSON.stringify({ priority: 'Low', label: 'Other', fallback: true }),
            });
        });

        // Click the 'Add Task' button to open the modal
        await page.click('#addTaskBtn');
        await expect(page.locator('#addTaskModal')).toBeVisible();

        // Enter a task title
        await page.fill('#taskTitle', 'Task title for fallback test');

        // Click the 'Magic Fill' button
        await page.click('#magicFillAddTaskBtn');

        // Check if the fallback notification appears
        await expect(page.locator('#toastNotification')).toBeVisible();
        await expect(page.locator('#toastNotification')).toHaveText('AI unavailable, used fallback suggestions.');

        // Verify that the fields are populated with the mocked fallback values
        await expect(page.locator('#taskLabel')).toHaveValue('Other');
        await expect(page.locator('#taskPriority')).toHaveValue('Low');

        // Close the modal
        await page.click('#closeModalBtn');
        await expect(page.locator('#addTaskModal')).not.toBeVisible();
    });
});