import { faker } from '@faker-js/faker';
import { APIRequestContext } from '@playwright/test';

// Interface for a Task object, matching the backend model
export interface Task {
  id?: number;
  title: string;
  notes?: string;
  due_date?: string | null;
  priority: 'High' | 'Medium' | 'Low';
  label?: string;
  is_done?: boolean;
}

/**
 * Generates a single task object with default or overridden properties.
 * Uses faker to generate realistic and unique data.
 * @param overrides - Optional: An object with properties to override the defaults.
 * @returns A Task object.
 */
export const createTaskData = (overrides: Partial<Task> = {}): Task => {
  return {
    title: faker.lorem.sentence(),
    notes: faker.lorem.paragraph(),
    due_date: faker.date.future().toISOString().split('T')[0], // Format as YYYY-MM-DD
    priority: faker.helpers.arrayElement(['High', 'Medium', 'Low']),
    label: faker.helpers.arrayElement(['Work', 'Personal', 'Home', 'Health']),
    is_done: false,
    ...overrides,
  };
};

/**
 * Creates a task directly via an API request.
 * This is much faster and more reliable than creating a task through the UI.
 * @param request - The Playwright APIRequestContext to use for the API call.
 * @param overrides - Optional: An object with properties to override the defaults for the new task.
 * @returns The created task object from the API response.
 */
export const seedTask = async (request: APIRequestContext, overrides: Partial<Task> = {}): Promise<Task> => {
  const taskData = createTaskData(overrides);
  const response = await request.post('/api/tasks', {
    data: taskData,
  });
  if (!response.ok()) {
    console.error(`Failed to seed task: ${await response.text()}`);
    throw new Error(`API call failed with status ${response.status()}`);
  }
  const responseBody = await response.json();
  return responseBody.data;
};
