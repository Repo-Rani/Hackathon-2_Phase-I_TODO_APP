---
description: "Task list template for feature implementation"
---

# Tasks: Add Task Functionality

**Input**: Design documents from `/specs/001-add-task/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan
- [X] T002 Initialize Python project with UV dependencies
- [X] T003 [P] Configure linting and formatting tools (pylint, black, mypy)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Create data models module in src/models/__init__.py
- [X] T005 Create task model in src/models.py with dataclass
- [X] T006 Create todo manager module in src/todo_manager.py
- [X] T007 Setup basic CLI module in src/main.py
- [X] T008 Configure pytest in pyproject.toml
- [X] T009 Create test directories in tests/__init__.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add New Task (Priority: P1) 🎯 MVP

**Goal**: Enable users to add new tasks with title and optional description

**Independent Test**: User can run the app, select the "Add Task" option, enter a title and description, and see the task created with a unique ID and timestamp

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T010 [P] [US1] Contract test for add_task in tests/test_todo_manager.py
- [X] T011 [P] [US1] Integration test for add task flow in tests/test_main.py

### Implementation for User Story 1

- [X] T012 [P] [US1] Create Task model with id, title, description, completed, created_at in src/models.py
- [X] T013 [US1] Implement add_task method in TodoManager class in src/todo_manager.py
- [X] T014 [US1] Add CLI interface for add task in src/main.py
- [X] T015 [US1] Add validation for required title field (FR-001)
- [X] T016 [US1] Add validation for optional description field (FR-002)
- [X] T017 [US1] Implement unique sequential ID assignment (FR-003)
- [X] T018 [US1] Set default incomplete status for new tasks (FR-004)
- [X] T019 [US1] Store creation timestamp for tasks (FR-005)
- [X] T020 [US1] Provide clear feedback when task is created (FR-010)
- [X] T021 [US1] Show newly created task details to user (FR-011)
- [X] T022 [US1] Return user to main menu after creation (FR-012)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Add Task with Validation (Priority: P2)

**Goal**: Validate user input when adding tasks to ensure data quality

**Independent Test**: When user enters invalid data (empty title, title too long), the system shows clear error messages and allows re-entry

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [X] T023 [P] [US2] Validation test for empty title in tests/test_todo_manager.py
- [X] T024 [P] [US2] Validation test for title length in tests/test_todo_manager.py

### Implementation for User Story 2

- [X] T025 [P] [US2] Implement title length validation (1-200 chars) in src/todo_manager.py (FR-006)
- [X] T026 [P] [US2] Implement description length validation (<1000 chars) in src/todo_manager.py (FR-007)
- [X] T027 [US2] Implement standard character validation (alphanumeric + punctuation) in src/todo_manager.py (FR-008)
- [X] T028 [US2] Implement non-whitespace content validation for titles in src/todo_manager.py (FR-009)
- [X] T029 [US2] Add error message display for validation failures in src/main.py
- [X] T030 [US2] Add retry mechanism for invalid input in src/main.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Cancel Task Creation (Priority: P3)

**Goal**: Provide a graceful exit option for users who decide not to create a task

**Independent Test**: User can cancel task creation process and return to main menu without any task being created

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [X] T031 [P] [US3] Cancel flow test in tests/test_main.py

### Implementation for User Story 3

- [X] T032 [P] [US3] Add cancel option to task creation flow in src/main.py
- [X] T033 [US3] Implement cancel logic to return to main menu without creating task in src/main.py
- [X] T034 [US3] Ensure no task is created when user cancels in src/todo_manager.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T035 [P] Documentation updates in README.md
- [X] T036 Code cleanup and refactoring
- [X] T037 [P] Additional unit tests in tests/test_models.py
- [X] T038 Input sanitization for security (NFR-002) in src/todo_manager.py
- [X] T039 Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in priority order (P1 → P2 → P3)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Depends on User Story 1 completion - builds on add functionality
- **User Story 3 (P3)**: Depends on User Story 1 completion - modifies same flow

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, user stories must follow dependency order
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Example: User Story 1

```bash
# Launch all models for User Story 1 together:
Task: "Create Task model with id, title, description, completed, created_at in src/models.py"
```

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence