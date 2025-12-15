import { faker } from '@faker-js/faker';
import { APIRequestContext } from '@playwright/test';

// Basic interface for a User, assuming these fields
export interface User {
  id?: number;
  email: string;
  password?: string; // Password may not be returned from the API
  name: string;
}

/**
 * Generates user data for creation.
 * @param overrides - Optional properties to override the defaults.
 * @returns A User object.
 */
export const createUserData = (overrides: Partial<User> = {}): Omit<User, 'id'> => {
  const password = faker.internet.password({ length: 12 });
  return {
    name: faker.person.fullName(),
    email: faker.internet.email(),
    password: password,
    ...overrides,
  };
};

/**
 * UserFactory class to manage user creation and cleanup via API requests.
 */
export class UserFactory {
  private request: APIRequestContext;
  private createdUserIds: number[] = [];

  constructor(request: APIRequestContext) {
    this.request = request;
  }

  /**
   * Creates a user via an API call and stores its ID for cleanup.
   * @param overrides - Optional properties to override the defaults.
   * @returns The created user data, including the password for login tests.
   */
  async createUser(overrides: Partial<User> = {}): Promise<User> {
    const userData = createUserData(overrides);
    
    // The previous error log indicated this endpoint was being called.
    // I am assuming it should be /api/users, not /users.
    const response = await this.request.post(`/api/users`, {
      data: userData,
    });

    if (!response.ok()) {
      console.error(`Failed to create user via API: ${await response.text()}`);
      throw new Error(`API call to create user failed with status ${response.status()}`);
    }

    const createdUser = await response.json();
    
    if (createdUser.data && createdUser.data.id) {
        this.createdUserIds.push(createdUser.data.id);
    }

    return { ...createdUser.data, password: userData.password };
  }

  /**
   * Cleans up all users created by this factory instance.
   */
  async cleanup() {
    for (const userId of this.createdUserIds) {
      await this.request.delete(`/api/users/${userId}`);
    }
    this.createdUserIds = [];
  }
}
