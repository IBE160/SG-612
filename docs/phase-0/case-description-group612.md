## Case Title
Smart To-Do Auto Labels & Priority

## Background
Students and busy users often need a very simple task list. Complex tools slow them down. A minimal To-Do app with automatic label and priority suggestions can save time and keep focus on what matters.

## Purpose
Create a small web application where users can add tasks and get AI-based suggestions for a label (category) and priority (importance). Users can accept or override the suggestions. Keep the solution simple and reliable.

## Target Users
Students and beginners who want a fast, minimal task manager with light AI assistance

## Core Functionality

### Must Have (MVP)
- Create, read, update and delete tasks (title required; optional notes and due date)
- Automatic suggestions for **label** (e.g., School, Work, Home, Health, Finance, Shopping, Other)
- Automatic suggestions for **priority** (low, medium, high)
- Accept or override the suggestions before saving
- Filter by label and sort by priority

### Nice to Have (Optional Extensions)
- Smart lists (e.g., "High priority", "This week", "Overdue")
- Export/import tasks (CSV/JSON)
- Simple search

## Data Requirements

- **Tasks:** id, title, notes, due_date, label, priority, is_done, created_at
- **App settings:** default sort/filter

## User Stories (Optional)

1. As a student, I want to label and priority suggestions when I add task, so that organizing is fast
2. As a user, I want to override the suggestions, so that I can stay in control
3. As a user, I want to filter by label and sort by priority, so that the most important tasks appear first

## Technical Constraints

- Python + Flask (server-rendered pages with simple HTML/CSS)
- Storage: SQLite (preferred) or a JSON file for a minimal demo
- AI module: rule-based fallback for suggestions; optional LLM call with JSON output
- Must work locally without authentication or hosting
- If AI is unavailable, the app must still work (default to label=“Other”, priority=“low”)

## Success Criteria

- Users can complete the full task lifecycle (create, read, update, delete)
- AI suggestions appear and can be overridden; app functions with or without AI (fallback)
- Filtering by label and sorting by priority work correctly
- Project structure follows course requirements (planning docs, prompts in repo, runnable app)
