# ibe160 - Epic Breakdown

**Author:** BIP
**Date:** 2025-11-27
**Project Level:** Beginner / School Project
**Target Scale:** Individual User MVP

---

## Overview

This document provides the complete epic and story breakdown for {{project_name}}, decomposing the requirements from the [PRD](./PRD.md) into implementable stories.

**Living Document Notice:** This is the initial version. It will be updated after UX Design and Architecture workflows add interaction and technical details to stories.

The project is broken down into three main epics. The first epic establishes the foundational setup and core task management capabilities. The second epic introduces the AI-powered intelligence for task categorization. The final epic enhances task organization with smart lists and advanced filtering.

---

## Functional Requirements Inventory

*   FR1: Users can create new tasks with a title, optional notes, and an optional due date.
*   FR2: Users can view a list of all their active tasks.
*   FR3: Users can update existing tasks (title, notes, due date, label, priority).
*   FR4: Users can delete tasks.
*   FR5: Users can mark tasks as complete and view them in a completed state.
*   FR6: The system can integrate with Google Gemini API to analyze task descriptions.
*   FR7: The system can suggest a label (e.g., School, Work, Home, Health, Finance, Shopping, Other) based on task description.
*   FR8: The system can suggest a priority (Low, Medium, High) based on task description.
*   FR9: Users can review and accept AI-suggested labels and priorities.
*   FR10: Users can override or edit AI-suggested labels and priorities before saving.
*   FR11: The system provides a rule-based fallback for label and priority suggestions if the AI service is unavailable or exceeds quota.
*   FR12: The system can automatically generate "High Priority" smart lists.
*   FR13: The system can automatically generate "Due This Week" smart lists.
*   FR14: Users can filter tasks by a specific label.
*   FR15: Users can sort tasks by priority.
*   FR16: Users can sort tasks by due date.

---

## FR Coverage Map

*   **Epic 1: Foundational Setup & Core Task Management** - Covers FR1, FR2, FR3, FR4, FR5.
*   **Epic 2: AI-Powered Task Intelligence** - Covers FR6, FR7, FR8, FR9, FR10, FR11.
*   **Epic 3: Smart Lists & Advanced Filtering** - Covers FR12, FR13, FR14, FR15, FR16.

---

## Epic 1: Foundational Setup & Core Task Management

**Goal:** Establish the project foundation and implement core CRUD functionality for tasks, providing the basic capability to manage tasks which forms the backbone of the application.

### Story 1.1: Project Foundation & Database Setup

As a developer, I want to set up the initial Flask project structure, database model, and dependencies, so that I have a foundation for building the application.

**Acceptance Criteria:**

**Given** the project requirements
**When** I initialize the project
**Then** a Flask project structure is created with necessary folders.
**And** a virtual environment is created with Flask and SQLAlchemy installed.
**And** a SQLite database file is created.
**And** the SQLAlchemy models for `Task` (id, title, notes, due_date, label, priority, is_done, created_at) are defined.

**Prerequisites:** None

**Technical Notes:** This story covers the initial setup as outlined in Week 1 of the project timeline. The project structure should adhere to:

```
/
|-- app.py                  # Main Flask application, routes, and API logic
|-- ai_service.py           # Module for Gemini API calls
|-- .gitignore
|-- package.json
|-- tailwind.config.js      # Configured with primary: '#607AFB', fontFamily: { display: ['Sora', 'sans-serif'] }
|-- postcss.config.js
|-- requirements.txt        # Python dependencies (Flask, SQLAlchemy)
|-- venv/                     # Virtual environment
|-- static/
|   |-- src/
|   |   |-- input.css       # TailwindCSS input
|   |-- dist/
|       |-- output.css      # Compiled CSS
|-- templates/
|   |-- base.html           # Base layout template
|   |-- index.html          # Main dashboard view
|   |-- ... (other views)
|-- instance/
|   |-- tasks.db            # SQLite database file
|-- tests/                    # Tests for the application
    |-- test_api.py
    |-- test_app.py
```

The SQLAlchemy `Task` model should define `id`, `title`, `notes`, `due_date`, `label`, `priority`, `is_done`, `created_at` with snake_case column names.

### Story 1.2: Create New Task

As a user, I want to create a new task with a title, notes, and due date, so that I can add items to my to-do list.

**Acceptance Criteria:**

**Given** I am on the main dashboard
**When** I click the "Add Task" button (a primary button with color `#607AFB`)
**Then** a modal appears with a form to add a new task.
**And** the form includes fields for title (required), notes, and due date.
**And** the modal can be dismissed by pressing the `Escape` key or clicking the backdrop.
**When** I fill out the form and click "Save"
**Then** the new task is saved to the database.
**And** the modal closes and the dashboard updates to show the new task.
**And** upon success, a non-blocking toast notification confirms "Task created."

**Prerequisites:** Story 1.1

**Technical Notes:** This covers the "Create" part of the CRUD operations. The frontend will call `POST /api/tasks` with a JSON body containing the task details.

### Story 1.3: View and Update Tasks

As a user, I want to view the details of my tasks and update them, so that I can keep my task list accurate.

**Acceptance Criteria:**

**Given** I am on the main dashboard
**When** I view my task list (a 'Spacious & Focused List' of `Task Card` components)
**Then** I can see the title, due date, label, and priority for each task. Each card shows a completion checkbox, task title, due date, and pill-shaped badges for label/priority. Edit/delete icons appear on hover.
**When** I click on a task to edit it
**Then** a modal appears with the task's details pre-filled.
**And** I can modify the title, notes, due date, label, and priority.
**When** I save my changes
**Then** the task is updated in the database and the dashboard reflects the changes.

**Prerequisites:** Story 1.2

**Technical Notes:** This covers the "Read" and "Update" parts of the CRUD operations. The task list is populated by calling `GET /api/tasks`, and updates to tasks are sent to `PUT /api/tasks/<id>`.

### Story 1.4: Delete and Complete Tasks

As a user, I want to delete tasks I no longer need and mark tasks as complete, so that I can manage my task list effectively.

**Acceptance Criteria:**

**Given** I am on the main dashboard
**When** I click a "Delete" button (an icon that appears on `Task Card` hover) on a task
**Then** I am prompted for confirmation.
**And** upon confirmation, the task is permanently removed from the database.
**When** I check a checkbox on a task
**Then** the task is marked as complete (`is_done` = true).
**And** the completed task is visually distinguished from active tasks (e.g., strikethrough, grayed out). When a task is marked complete, the title text receives a strikethrough effect and a muted color.

**Prerequisites:** Story 1.2

**Technical Notes:** This covers the "Delete" part of the CRUD operations and task completion. Deleting a task calls `DELETE /api/tasks/<id>`, and marking a task as complete calls `PUT /api/tasks/<id>` with `is_done: true`.

---

## Epic 2: AI-Powered Task Intelligence

**Goal:** Integrate the Gemini AI to provide intelligent suggestions for task labels and priorities, and implement a robust fallback mechanism, delivering the core "smart" functionality and reducing manual organization effort for the user.

### Story 2.1: Gemini API Integration

As a developer, I want to integrate the Google Gemini API with the backend, so that the application can send task descriptions for analysis.

**Acceptance Criteria:**

**Given** a task description
**When** the backend service is called
**Then** it successfully sends the description to the Gemini API.
**And** the backend service securely manages the API key.
**And** the backend can receive and parse a JSON response from the API containing `label` and `priority`.

**Prerequisites:** Story 1.1

**Technical Notes:** This covers the backend integration work outlined in Week 2 of the project timeline. Integration will be done in `ai_service.py` using the `google-genai` Python library. The API key must not be exposed to the frontend.

### Story 2.2: "Magic Fill" AI Suggestions

As a user, when creating or editing a task, I want to click a "Magic Fill" button to get AI-powered suggestions for the label and priority, so that I can organize tasks faster.

**Acceptance Criteria:** (This story is linked to the 'AI-Suggestion Flow')

**Given** I am in the "Add Task" or "Edit Task" modal
**When** I click the "Magic Fill" button
**Then** the task description is sent to the backend AI service.
**And** a subtle loading indicator appears on the button until the `label` and `priority` fields are populated.
**And** the `label` and `priority` fields in the form are populated with the suggestions returned by the AI.
**And** I can then accept or edit these suggestions before saving.

**Prerequisites:** Story 1.2, Story 1.3, Story 2.1

**Technical Notes:** This story connects the frontend UI to the backend AI service. The "Magic Fill" button triggers a `POST /api/suggest` call to the backend.

### Story 2.3: Rule-Based Fallback Mechanism

As a developer, I want to implement a rule-based fallback mechanism, so that the application can still suggest labels and priorities if the AI service is unavailable.

**Acceptance Criteria:**

**Given** the AI service call fails
**When** a user requests AI suggestions
**Then** the fallback mechanism is triggered.
**And** the fallback uses keyword matching to suggest a label (e.g., "buy" -> "Shopping").
**And** if no keyword matches, the fallback suggests "Other" for the label and "Low" for the priority.
**And** the UI must subtly indicate that the suggestions are from the fallback system (e.g., a toast notification saying "AI unavailable, used fallback suggestions").

**Prerequisites:** Story 2.2

**Technical Notes:** This ensures application robustness, a key success criterion. The fallback logic will be triggered within `ai_service.py` if the Gemini API call fails.

---

## Epic 3: Smart Lists & Advanced Filtering

**Goal:** Implement automated smart lists and user-controlled filtering and sorting to enhance task organization and allow users to quickly focus on what's most important.

### Story 3.1: "High Priority" Smart List

As a user, I want to see a "High Priority" smart list, so that I can immediately focus on my most important tasks.

**Acceptance Criteria:**

**Given** I am on the main dashboard
**When** I view the sidebar
**Then** I see a "High Priority" smart list option.
**When** I click the "High Priority" smart list
**Then** the main task view is filtered to show only tasks with a "High" priority.

**Prerequisites:** Story 1.3

**Technical Notes:** This involves adding a specific query to the backend to filter tasks using `GET /api/tasks?priority=High`. The sidebar containing the smart lists will collapse into an offcanvas menu on tablet and mobile screens, and the active list should have a visual indicator as per the design system.

### Story 3.2: "Due This Week" Smart List

As a user, I want to see a "Due This Week" smart list, so that I can plan my upcoming week.

**Acceptance Criteria:**

**Given** I am on the main dashboard
**When** I view the sidebar
**Then** I see a "Due This Week" smart list option.
**When** I click the "Due This Week" smart list
**Then** the main task view is filtered to show only tasks with a due date within the next 7 days.

**Prerequisites:** Story 1.3

**Technical Notes:** This requires a date-based query on the task list using `GET /api/tasks?due_before=<today+7days>`. The sidebar containing the smart lists will collapse into an offcanvas menu on tablet and mobile screens, and the active list should have a visual indicator as per the design system.

### Story 3.3: Manual Filtering and Sorting

As a user, I want to be able to manually filter my tasks by label and sort them by priority or due date, so that I have full control over my task view.

**Acceptance Criteria:**

**Given** I am viewing my tasks
**When** I select a label from a "Filter by Label" dropdown
**Then** the task list is filtered to show only tasks with that label.
**When** I choose to sort by priority
**Then** the tasks are ordered from High to Low.
**When** I choose to sort by due date
**Then** the tasks are ordered with the soonest due date first.

**Prerequisites:** Story 1.3

**Technical Notes:** This implements the final filtering and sorting requirements from the PRD. UI controls for filtering and sorting will map to API parameters, e.g., `GET /api/tasks?label=Work&sort_by=priority`.

---

<!-- End epic repeat -->

---

## FR Coverage Matrix

| FR | Description | Epic | Story |
|---|---|---|---|
| FR1 | Create new tasks | 1 | 1.2 |
| FR2 | View a list of all active tasks | 1 | 1.3 |
| FR3 | Update existing tasks | 1 | 1.3 |
| FR4 | Delete tasks | 1 | 1.4 |
| FR5 | Mark tasks as complete | 1 | 1.4 |
| FR6 | Integrate with Google Gemini API | 2 | 2.1 |
| FR7 | Suggest a label | 2 | 2.2 |
| FR8 | Suggest a priority | 2 | 2.2 |
| FR9 | Review and accept AI suggestions | 2 | 2.2 |
| FR10 | Override or edit AI suggestions | 2 | 2.2 |
| FR11 | Rule-based fallback mechanism | 2 | 2.3 |
| FR12 | "High Priority" smart lists | 3 | 3.1 |
| FR13 | "Due This Week" smart lists | 3 | 3.2 |
| FR14 | Filter tasks by a specific label | 3 | 3.3 |
| FR15 | Sort tasks by priority | 3 | 3.3 |
| FR16 | Sort tasks by due date | 3 | 3.3 |

---

## Summary

This document outlines the breakdown of the Smart To-Do AI project into 3 epics and 10 user stories. Each story is designed to be a small, implementable unit of value. The epics are sequenced to deliver foundational capabilities first, followed by AI-powered features, and finally advanced organizational tools. This structure ensures a logical progression of development and incremental value delivery.

---

_For implementation: Use the `create-story` workflow to generate individual story implementation plans from this epic breakdown._

_This document will be updated after UX Design and Architecture workflows to incorporate interaction details and technical decisions._
