### Design Prompt for "Smart To-Do AI" Web Application

**1. Core Concept & Audience:**

Design a responsive web application called **"Smart To-Do AI"**. It is a lightweight, AI-enhanced task manager for **students and beginners**. The app's main goal is to reduce the manual effort of organization by intelligently suggesting task categories and priorities. The overall aesthetic should feel **minimalist, clean, modern, intuitive, and calming**. The user should feel **efficient, focused, and empowered**.

**2. Layout & Structure:**

*   **Overall Layout:** A responsive, two-column layout.
    *   **Left Column (Sidebar):** A persistent navigation sidebar on desktop. It should contain "Smart Lists" (e.g., "High Priority," "Due This Week") and a list of user-created "Labels" (e.g., "School," "Work"). The active navigation item should be clearly highlighted.
    *   **Right Column (Main Content):** The primary area for displaying the user's tasks. It should have a clear header indicating the current view (e.g., "High Priority") and a prominent "Add Task" button.
*   **Responsiveness:** On smaller screens (tablet and mobile), the sidebar should collapse into an off-canvas menu accessible via a hamburger icon to maximize content visibility. The main content area should adapt to a single-column view.

**3. Color & Typography:**

*   **Color Palette:** Use a **"Modern & Focused"** theme.
    *   **Primary Color:** A professional and calming **blue or indigo** for all primary buttons, active links, and focus indicators.
    *   **Semantic Colors:** Use standard colors for feedback: green for success, red for errors, and yellow for warnings.
    *   **Neutrals:** A clean grayscale for backgrounds (light gray), surfaces (white), and text (dark gray/black) to create a spacious and readable feel.
*   **Typography:** Use a standard, highly-legible **system font stack** (e.g., Segoe UI, Roboto, -apple-system). The typography should have a clear hierarchy with responsive font sizes for headings and body text.

**4. Key Screens & Components:**

*   **Main Dashboard:**
    *   This is the main view, showing the sidebar and the main content area.
    *   The main content area displays a **spacious, vertical list of "Task Cards."**
    *   If the list is empty, display a helpful message with an icon and a clear "Add Task" button.

*   **Task Card Component:**
    *   This is the primary custom component. Design a clean, rectangular card for each task with subtle shadows to create depth.
    *   **Anatomy of a Task Card:**
        *   **Checkbox:** A circular or square checkbox on the far left. When a task is completed, the card's content should fade and the title should have a strikethrough.
        *   **Task Title:** The most prominent text element.
        *   **Due Date:** Displayed subtly below the title.
        *   **Badges:** Small, color-coded, pill-shaped badges for `Label` and `Priority` to allow for quick scanning.
        *   **Action Icons:** On hover, reveal subtle icons for "Edit" (pencil) and "Delete" (trash can) on the far right.

*   **Add/Edit Task Modal:**
    *   A modal dialog that appears on top of the dashboard.
    *   It should contain a clean form with input fields for **Title, Notes (multi-line), and Due Date.**
    *   Include select dropdowns for **Label** and **Priority**.
    *   **Buttons:**
        *   A primary **"Save"** button (solid blue/indigo).
        *   A secondary **"Cancel"** button (outline or plain text).
        *   A distinct **"Magic Fill"** button with a sparkle or wand icon next to the text. This button should stand out as a special feature.

**5. Summary of Aesthetics & Keywords:**

Minimalist, Clean, Modern, Professional, Calm, Focused, Efficient, Intuitive, Spacious, Uncluttered, Trustworthy, AI-enhanced, Smart-yet-simple.