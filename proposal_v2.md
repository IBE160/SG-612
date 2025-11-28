# Project Proposal: Smart To-Do AI

## Case Title
Smart To-Do: AI-Enhanced Task Manager with Auto-Labeling

## Background
Students and busy users often struggle to maintain organized task lists. Complex project management tools create friction, while simple lists become cluttered. A minimal To-Do app with intelligent, automatic categorization can save time and maintain focus on high-priority items.

## Purpose
Create a lightweight web application where users can manage tasks efficiently. The core value proposition is the integration of Google's Gemini AI to automatically suggest a **Label** (category) and **Priority** (importance) based on the task description. This reduces manual data entry while keeping the list organized.

## Target Users
Students and beginners who want a fast, minimal task manager with intelligent assistance but without the complexity of enterprise tools.

## Core Functionality

### Must Have (MVP)
* **CRUD Operations:** Create, read, update, and delete tasks (title required; optional notes and due date).
* **AI Suggestions:** Integration with **Google Gemini API** to analyze task text and suggest:
    * **Label** (e.g., School, Work, Home, Health, Finance, Shopping, Other).
    * **Priority** (Low, Medium, High).
* **User Control:** Users can review, accept, or override AI suggestions before saving.
* **Smart Lists:** Auto-generated views for "High Priority" and "Due This Week".
* **Filtering/Sorting:** Filter by specific label and sort by priority/date.

### Nice to Have (Post-MVP Extensions)
* **Gamified UI/UX:** Introduce rewarding visual feedback, such as celebratory animations and "streaks" for consecutive days of activity, and satisfying sounds effects.
* **Shared Task Lists:** Allow users to create and collaborate on lists with others, including comments and notifications.
* **AI-Generated Sub-tasks:** Let the AI suggest breaking down larger tasks into smaller, manageable sub-tasks.
* **Simple Search:** Implement a basic text search to quickly find tasks.
* **Export/Import:** Allow users to back up and restore their tasks to a local file (CSV/JSON).
* **Dark Mode:** Provide a UI toggle for a dark-themed interface.

## Data Requirements
* **Tasks:** `id`, `title`, `notes`, `due_date`, `label`, `priority`, `is_done`, `created_at`
* **Storage:** SQLite (preferred for robust local storage) or JSON file (backup).

## Technical Architecture & Specifications

### Frontend (UI/UX)
* **Technology:** HTML5, CSS3, Jinja2 (Flask Templating).
* **Framework:** **Bootstrap 5** (via CDN). This ensures a responsive, modern design without writing complex custom CSS.
* **Key Interface Elements:**
    * **Dashboard:** A clean card-based list view with a sidebar for Smart Lists.
    * **Task Modal:** A form for adding tasks. Includes a "Magic Fill" button that triggers the Gemini API to pre-fill fields.
    * **Visual Feedback:** Color-coded badges for labels (e.g., Red for 'High Priority', Blue for 'School').

### Backend
* **Language:** Python 3.x
* **Web Framework:** Flask. Lightweight and perfect for this scope. It was chosen for its simplicity and flexibility, which is ideal for a beginner-level team, as confirmed by a comparative framework analysis.
* **Database:** SQLite via SQLAlchemy ORM.


### AI Integration & Fallback Logic
* **Model:** **Google Gemini API** (Model: `gemini-1.5-flash`).
    * *Reasoning:* Fast inference speed, strong JSON formatting capabilities, and developer-friendly free tier.
* **Implementation:** The backend sends the user's task title to Gemini with a system prompt requesting a strict JSON response containing `label` and `priority`.
* **Fallback Strategy (Reliability):** If the API is unreachable or the quota is exceeded, the app employs a Rule-Based Fallback:
    * *Keyword Matching:* (e.g., text contains "buy" -> Label: Shopping).
    * *Default:* If no match, Label="Other", Priority="Low".
    * *User Notification:* The UI will gently indicate if AI was unavailable, but the task is still saved.

## User Stories
1.  **As a student**, I want the app to automatically tag my "Study for math exam" task as "School" and "High Priority", so I spend less time organizing.
2.  **As a user**, I want to click a "High Priority" smart list, so I can immediately see what needs my urgent attention.
3.  **As a developer**, I want the app to work even if I have no internet connection (using fallback logic), so the tool is always reliable.

## Timeline and Weekly Milestones (6 Weeks)

* **Week 1: Foundation & Database**
    * Set up Python virtual environment and Flask project structure.
    * Design and implement SQLite database model (SQLAlchemy).
    * Create basic API routes for CRUD operations (Create, Read, Update, Delete).
    * *Deliverable:* A running backend where tasks can be managed via Postman/Console.

* **Week 2: Gemini AI Integration**
    * Obtain Google AI Studio API Key.
    * Write the Python service to communicate with Gemini API.
    * Design the prompt to ensure consistent JSON output.
    * Implement the Rule-Based fallback logic.
    * *Deliverable:* A Python script that takes text input and prints categorized JSON output.

* **Week 3: Frontend Implementation**
    * Integrate Bootstrap 5 templates.
    * Build the Main Dashboard (Task List) and Add/Edit Task Forms.
    * Connect Jinja2 templates to Flask routes.
    * *Deliverable:* A functional web interface showing tasks from the database.

* **Week 4: Smart Features & Polish (MVP Completion)**
    * Connect the frontend "Auto-Suggest" button to the backend AI service.
    * Implement "Smart Lists" logic (SQL queries for filtering).
    * Add sorting and manual filtering functionality.
    * *Deliverable:* Feature-complete MVP where AI actively helps categorize tasks.

* **Week 5: Testing & Refinement**
    * Manual testing of edge cases (empty inputs, long text, API errors).
    * Verify fallback logic (simulate offline mode).
    * UI tweaks (spacing, colors, badges).
    * *Deliverable:* Stable, bug-free application.

* **Week 6: Documentation & Submission**
    * Write `README.md` with setup instructions (install requirements, API key setup).
    * Code cleanup and commenting.
    * Final project report/presentation preparation.

## Future Vision: The AI-Powered Productivity Coach

Beyond the initial implementation, the long-term vision for this project is to evolve from a simple task manager into a proactive, AI-powered productivity coach. This includes:

*   **Hyper-Personalized AI Assistance:** An AI that learns from a user's habits to provide personalized advice, suggest optimal times to work on tasks, and help manage workload to prevent burnout.
*   **Automated Project Decomposition:** The ability for the AI to take a high-level goal (e.g., "launch a new blog") and automatically generate a complete project plan with milestones and individual tasks.
*   **The True "Universal Inbox":** A fully integrated system that can connect to various services (email, calendars, messaging apps) to automatically capture commitments and turn them into actionable tasks, creating a single source of truth for all of a user's obligations.

## Success Criteria
* Users can complete the full task lifecycle (CRUD) via the web interface.
* Gemini API correctly categorizes simple tasks (e.g., "Buy milk" -> Shopping).
* The application remains functional (via fallback) if the AI service is disconnected.
* Smart Lists accurately display filtered views of the data.
* Code is well-structured and follows the defined timeline.
* Project structure follows course requirements (e.g., planning documents in repo, runnable app).

## User Flows

### Student / User Flow
1. **Entry:** User opens the web application.
2. **Dashboard View:** User sees the dashboard with "Smart Lists" (High Priority, Due This Week) and a list of current tasks.
3. **Create Task:** User clicks "Add Task" button -> Opens Modal -> User types "Study for math".
4. **AI Assistance:** User clicks "Magic Fill". System auto-selects Label: "School" and Priority: "High".
5. **Review:** User confirms or edits the suggestion -> Clicks "Save".
6. **Confirmation:** Modal closes, dashboard updates immediately with the new task sorted correctly.
7. **Complete Task:** User checks the box next to the task -> Task moves to "Completed" state visually.
8. **Exit:** User leaves the page (data is stored).