import { test, expect } from '../support/fixtures';
import { format, addDays } from 'date-fns';

test.describe('3.1/3.2/3.3-E2E-SmartLists @p1 @regression', () => {

  test('3.1-E2E-001: should filter tasks by High Priority when "High Priority" smart list is clicked', async ({ page, seedTasks }) => {
    // --- Given ---
    // Seed specific tasks for this test via API
    await seedTasks([
      { title: 'High Prio Task 1', priority: 'High' },
      { title: 'High Prio Task 2', priority: 'High' },
      { title: 'Medium Prio Task', priority: 'Medium' },
      { title: 'Low Prio Task', priority: 'Low' },
    ]);
    await page.goto('/');
    await page.waitForResponse(resp => resp.url().includes('/api/tasks') && resp.status() === 200);
    await expect(page.locator('.task-card')).toHaveCount(4);

    // --- When ---
    // Use waitForResponse to ensure the filter action completes
    const filterResponse = page.waitForResponse(resp => resp.url().includes('/api/tasks?priority=High'));
    await page.click('#highPriorityBtn');
    await filterResponse;

    // --- Then ---
    await expect(page.locator('.task-card')).toHaveCount(2);
    await expect(page.locator('.task-card:has-text("High Prio Task 1")')).toBeVisible();
    await expect(page.locator('.task-card:has-text("High Prio Task 2")')).toBeVisible();
    await expect(page.locator('.task-card:has-text("Medium Prio Task")')).not.toBeVisible();
  });

  test('3.2-E2E-001: should filter tasks by "Due This Week" when smart list is clicked', async ({ page, seedTasks }) => {
    // --- Given ---
    const today = new Date();
    await seedTasks([
      { title: 'Task due in 2 days', due_date: format(addDays(today, 2), 'yyyy-MM-dd') },
      { title: 'Task due in 6 days', due_date: format(addDays(today, 6), 'yyyy-MM-dd') },
      { title: 'Task due in 8 days', due_date: format(addDays(today, 8), 'yyyy-MM-dd') },
    ]);
    await page.goto('/');
    await page.waitForResponse(resp => resp.url().includes('/api/tasks') && resp.status() === 200);
    await expect(page.locator('.task-card')).toHaveCount(3);

    // --- When ---
    const filterResponse = page.waitForResponse(resp => resp.url().includes('/api/tasks?due_date_within_days=7'));
    await page.click('#dueThisWeekBtn');
    await filterResponse;

    // --- Then ---
    await expect(page.locator('.task-card')).toHaveCount(2);
    await expect(page.locator('.task-card:has-text("Task due in 2 days")')).toBeVisible();
    await expect(page.locator('.task-card:has-text("Task due in 6 days")')).toBeVisible();
    await expect(page.locator('.task-card:has-text("Task due in 8 days")')).not.toBeVisible();
  });

  test('3.3-E2E-001: should manually filter tasks by label and sort by priority and due date', async ({ page, seedTasks }) => {
    // --- Given ---
    const today = new Date();
    await seedTasks([
      { title: 'Filter Task - High Work', priority: 'High', label: 'Work', due_date: format(addDays(today, 2), 'yyyy-MM-dd') },
      { title: 'Filter Task - Medium Personal', priority: 'Medium', label: 'Personal', due_date: format(addDays(today, 1), 'yyyy-MM-dd') },
      { title: 'Filter Task - Low Work', priority: 'Low', label: 'Work', due_date: format(addDays(today, 3), 'yyyy-MM-dd') },
    ]);
    await page.goto('/');
    await page.waitForResponse(resp => resp.url().includes('/api/tasks') && resp.status() === 200);
    await expect(page.locator('.task-card')).toHaveCount(3);

    // --- When / Then ---
    // 1. Filter by Label: Work
    await page.selectOption('#filterByLabel', 'Work');
    await page.waitForResponse(resp => resp.url().includes('/api/tasks'));
    await expect(page.locator('.task-card')).toHaveCount(2);
    await expect(page.locator('.task-card:has-text("Filter Task - High Work")')).toBeVisible();
    await expect(page.locator('.task-card:has-text("Filter Task - Low Work")')).toBeVisible();

    // 2. Sort by Priority (DESC)
    await page.selectOption('#filterByLabel', ''); // Clear filter
    await page.selectOption('#sortBy', 'priority');
    await page.waitForResponse(resp => resp.url().includes('/api/tasks')); // Wait for re-sort
    let taskTitles = await page.locator('.task-card h3').allTextContents();
    expect(taskTitles).toEqual([
        'Filter Task - High Work',
        'Filter Task - Medium Personal',
        'Filter Task - Low Work'
    ]);

    // 3. Sort by Due Date (ASC)
    await page.selectOption('#sortBy', 'due_date');
    await page.waitForResponse(resp => resp.url().includes('/api/tasks')); // Wait for re-sort
    taskTitles = await page.locator('.task-card h3').allTextContents();
    expect(taskTitles).toEqual([
        'Filter Task - Medium Personal', // Due in 1 day
        'Filter Task - High Work',      // Due in 2 days
        'Filter Task - Low Work'        // Due in 3 days
    ]);
  });
});
