# Project Plan

## Instruksjoner

1. Der hvor det står {prompt / user-input-file}, kan dere legge inn en egen prompt eller filnavn for å gi ekstra instruksjoner. Hvis dere ikke ønsker å legge til ekstra instruksjoner, kan dere bare fjerne denne delen.
2. Hvis jeg har skrevet noe der allerede, f.eks. "Root Cause Analysis and Solution Design for Player Inactivity", så kan dere bytte ut min prompt med deres egen.


## Fase 0

- [x] /run-agent-task analyst *workflow-init
  - [x] File: bmm-workflow-status.yaml
- [x] Brainstorming
  - [x] /run-agent-task analyst *brainstorm "Expanding on "Nice to Have" features for the Smart To-Do AI project."
    - [x] File: brainstorming.md
- [x] Research
  - [x] /run-agent-task analyst *research "Find the easist web framework choice for the project, considering the groups beginner level"
    - [x] File: research-technical.md
- [x] Product Brief
  - [x] /run-agent-task analyst *product-brief "Read the brainstorming session the research session and the @proposal.md file, and create a product brief for the project."
    - [x] File: product-brief.md

## Fase 1

- [x] Planning
- [x] PRD
  - [x] /run-agent-task pm *prd "Create a Product Requirements Document (PRD) for the Smart To-Do AI project based on the product brief, brainstorming session, and research findings."
    - [x] File: prd.md
  - [x] /run-agent-task pm *validate-prd "Validate the PRD created in the previous task."
    - [x] File: validation-prd.md
  - [x] UX Design  
    - [x] /run-agent-task ux-designer *create-ux-design "Create a UX design for the project based"
      - [x] File: ux-design-specification.md
      - [x] File: main dashboard.html
      - [x] File: edit taskboard.html
      - [x] File: new label.html
      - [x] File: settings menu.html 
      - [x] File: notification pref.html
      - [x] File: smart list settings.html
    - [x] /run-agent-task ux-designer *validate-ux-design "Validate the UX design created in the previous task"
    - [x] File: validation-uxdesign.md


## Fase 2

- [x] Solutioning
  - [x] /run-agent-task architect *create-architecture
    - [x] File: architecture.md
  - [x] /run-agent-task pm *create-epics-and-stories
    - [x] File: epics.md
  - [x] /run-agent-task tea *test-design
    - [x] File: test-design-system.md
    - [x] File: ci.md
    - [x] File: ci-secrets-checklist.md
  - [x] /run-agent-task architect *solutioning-gate-check
    - [x] File: implementation-readiness-report-{{date}}.md

## Fase 3

- [ ] Implementation
  - [ ] /run-agent-task sm *sprint-planning {prompt / user-input-file}
    - [ ] File: sprint-artifacts/sprint-status.yaml
  - foreach epic in sprint planning:
    - [ ] /run-agent-task sm create-epic-tech-context {prompt / user-input-file}
      - [ ] File: sprint-artifacts/tech-spec-epic-{{epic_id}}.md
    - [ ] /run-agent-task sm validate-epic-tech-context {prompt / user-input-file}
    - foreach story in epic:
      - [ ] /run-agent-task sm *create-story {prompt / user-input-file}
        - [ ] File: sprint-artifacts/{{story_key}}.md
      - [ ] /run-agent-task sm *validate-create-story {prompt / user-input-file}
      - [ ] /run-agent-task sm *create-story-context {prompt / user-input-file}
        - [ ] File: sprint-artifacts/{{story_key}}.context.xml
      - [ ] /run-agent-task sm *validate-story-context {prompt / user-input-file}
      - [ ] /run-agent-task sm *story-ready-for-dev {prompt / user-input-file}
      while code-review != approved:
        - [ ] /run-agent-task dev *develop-story {prompt / user-input-file}
        - [ ] /run-agent-task dev *code-review {prompt / user-input-file}
      - [ ] /run-agent-task dev *story-done {prompt / user-input-file}
      - [ ] /run-agent-task sm *test-review {prompt / user-input-file}
    - [ ] /run-agent-task sm *epic-retrospective {prompt / user-input-file}





## BMAD workflow

<img src="images/bmad-workflow.svg" alt="BMAD workflow">