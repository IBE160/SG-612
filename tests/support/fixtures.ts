import { test as base } from '@playwright/test';
import { seedTask, Task } from './factories/task-factory';
import { UserFactory } from './factories/user-factory';

// Define the shape of our custom fixtures
export type TestFixtures = {
  seedTasks: (tasksToSeed: Partial<Task>[]) => Promise<Task[]>;
  userFactory: UserFactory;
};

/**
 * Extend the base Playwright test object with our custom fixtures.
 */
export const test = base.extend<TestFixtures>({
  /**
   * A fixture that provides a function to seed tasks before a test.
   * It also automatically cleans up all created tasks after the test has finished.
   */
  seedTasks: async ({ request }, use) => {
    const createdTaskIds: number[] = [];

    const seedTasksFunction = async (tasksToSeed: Partial<Task>[]): Promise<Task[]> => {
      const seededTasks: Task[] = [];
      for (const taskOverrides of tasksToSeed) {
        const task = await seedTask(request, taskOverrides);
        if (task.id) {
          createdTaskIds.push(task.id);
          seededTasks.push(task);
        }
      }
      return seededTasks;
    };

    await use(seedTasksFunction);

    if (createdTaskIds.length > 0) {
      console.log(`Cleaning up ${createdTaskIds.length} tasks...`);
      for (const taskId of createdTaskIds) {
        await request.delete(`/api/tasks/${taskId}`);
      }
    }
  },

  /**
   * A fixture that provides an instance of the UserFactory.
   * It automatically handles the cleanup of any users created by the factory.
   */
  userFactory: async ({ request }, use) => {
    const factory = new UserFactory(request);
    await use(factory);
    await factory.cleanup();
  },
});

export { expect } from '@playwright/test';
