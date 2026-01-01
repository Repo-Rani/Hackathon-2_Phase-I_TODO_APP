# Implementation Tasks: Console App Enhancements

**Feature**: Console App Enhancements (Rich UI + JSON Persistence + Better UX)
**Branch**: `002-enhancements`
**Date**: 2026-01-01
**Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)

---

## Task Summary

| Phase | User Story | Task Count | Parallel | Dependencies |
|-------|------------|------------|----------|--------------|
| 1 | Setup | 2 | 0 | None |
| 2 | Foundational | 3 | 2 | Phase 1 complete |
| 3 | US1 - Rich Terminal UI | 6 | 0 | Phase 2 complete |
| 4 | US2 - JSON Persistence | 5 | 1 | Phase 2 complete |
| 5 | Polish | 3 | 1 | All user stories complete |
| **Total** | | **19** | **4** | |

**MVP Scope**: User Story 1 + User Story 2 (Rich UI + JSON Persistence)
**Optional**: User Story 3 (Better UX - can be added incrementally)

---

## Implementation Strategy

### Delivery Approach

1. **MVP First**: Implement US1 (Rich UI) and US2 (JSON Persistence) together
   - These are both P1 priority and foundational to the enhancement
   - Can be delivered as a single increment
   - US3 (Better UX) is P2 and can be added later

2. **Incremental Testing**:
   - Each user story has independent test criteria
   - Verify US1: Visual output meets spec (colorful menus, tables)
   - Verify US2: Data persists across app restarts
   - Verify US3: Loading animations and confirmations work

3. **Parallel Opportunities**:
   - Within Foundational phase: T003 and T004 can run in parallel
   - Within US2 phase: T011 can run in parallel with T009/T010
   - Within Polish phase: T018 can run in parallel with T017

---

## Phase 1: Setup

**Goal**: Install dependencies and prepare environment for enhancement development.

**Tasks**:

- [X] T001 Install Rich library dependency using `uv add rich`
- [X] T002 Update .gitignore to exclude data/ directory and *.backup files (already done in planning)

**Completion Criteria**:
- [X] Rich library installed and importable
- [X] .gitignore updated with data exclusions

---

## Phase 2: Foundational (Blocking Prerequisites)

**Goal**: Create shared infrastructure needed by multiple user stories.

**Tasks**:

- [X] T003 [P] Add to_dict() method to Task class in src/models.py for JSON serialization
- [X] T004 [P] Add from_dict() classmethod to Task class in src/models.py for JSON deserialization
- [X] T005 Create new src/ui.py module with console singleton and basic structure

**Completion Criteria**:
- [X] Task model can serialize to/from dictionaries
- [X] ui.py module exists with console = Console() singleton
- [X] All existing tests still pass

**Independent Test**:
```python
# Test JSON serialization
from models import Task
from datetime import datetime

task = Task(1, "Test", "Description", False, datetime.now())
data = task.to_dict()
assert data["id"] == 1
assert "created_at" in data

restored = Task.from_dict(data)
assert restored.id == task.id
assert restored.title == task.title
```

---

## Phase 3: User Story 1 - Rich Terminal UI (P1)

**Story Goal**: Transform plain text output into beautiful colorful interface with styled menus, tables, and status indicators.

**Independent Test Criteria**:
- [x] User runs app and sees colored menu with borders
- [x] Task list displays in formatted table with color-coded status badges
- [x] Success messages appear in green, errors in red
- [x] Task details display in styled panel with borders

**Tasks**:

- [X] T006 [US1] Implement show_header() in src/ui.py with styled app header using Panel
- [X] T007 [US1] Implement show_menu(stats: dict) in src/ui.py with colored menu and task statistics
- [X] T008 [US1] Implement show_tasks_table(tasks: List[Task]) in src/ui.py using Rich Table with color-coded status
- [X] T009 [US1] Implement show_task_details(task: Task) in src/ui.py using Panel for detailed view
- [X] T010 [US1] Implement show_success(), show_error(), show_info() message functions in src/ui.py
- [X] T011 [US1] Refactor src/main.py to replace all print() calls with ui.py functions (handle_view_tasks, display_menu, all handlers)

**Files Modified**:
- src/ui.py (new functions)
- src/main.py (refactored to use Rich UI)

**Completion Criteria**:
- [X] All menu and task displays use Rich components
- [X] Colors match spec (cyan headers, green success, yellow pending, red errors)
- [X] Tables have proper column alignment and borders
- [X] No plain print() statements remain in main.py (except errors before ui import)

---

## Phase 4: User Story 2 - JSON Persistence (P1)

**Story Goal**: Automatically save tasks to data/tasks.json and load on startup so data persists across sessions.

**Independent Test Criteria**:
- [x] User adds task, closes app, reopens → task still present
- [x] data/tasks.json created automatically in data/ directory
- [x] Missing JSON file handled gracefully (empty task list)
- [x] Corrupted JSON file handled gracefully (error message, empty state)
- [x] All mutations (add/update/delete/toggle) trigger immediate save

**Tasks**:

- [ ] T012 [US2] Create new src/storage.py module with JSONStorage class skeleton
- [ ] T013 [US2] Implement JSONStorage._ensure_data_directory() and __init__() methods
- [ ] T014 [US2] Implement JSONStorage.save(tasks, next_id) with backup-before-save logic
- [ ] T015 [US2] Implement JSONStorage.load() with error handling for missing/corrupted files
- [ ] T016 [P] [US2] Enhance TodoManager in src/todo_manager.py: add storage attribute, _load_from_storage(), _save_to_storage(), call save after all mutations

**Files Created/Modified**:
- src/storage.py (new module)
- src/todo_manager.py (enhanced with persistence)

**Completion Criteria**:
- [ ] data/tasks.json created on first save
- [ ] Backup file (.json.backup) created before each save
- [ ] Tasks persist across app restarts
- [ ] Missing file returns empty state (no crash)
- [ ] Corrupted JSON returns empty state with error message
- [ ] All CRUD operations trigger auto-save

**Integration Test**:
```python
# Test persistence across instances
manager1 = TodoManager("test_data/tasks.json")
task = manager1.add_task("Test Task", "Description")
task_id = task.id

# Simulate app restart
manager2 = TodoManager("test_data/tasks.json")
loaded_task = manager2.get_task_by_id(task_id)
assert loaded_task is not None
assert loaded_task.title == "Test Task"
```

---

## Phase 5: User Story 3 - Better UX (P2)

**Story Goal**: Add loading animations, confirmation dialogs, and smooth screen transitions for professional feel.

**Independent Test Criteria**:
- [x] Loading spinner appears during save/load operations
- [x] Delete operation shows confirmation dialog with task details
- [x] Screen clears between operations
- [x] "Press Enter to continue" prompts appear after operations

**Tasks**:

- [ ] T017 [US3] Implement show_loading(message, duration) in src/ui.py using Progress with SpinnerColumn
- [ ] T018 [P] [US3] Implement get_input(prompt) and get_confirmation(prompt) in src/ui.py using Prompt and Confirm
- [ ] T019 [US3] Implement clear_screen() and pause() utility functions in src/ui.py
- [ ] T020 [US3] Enhance all handlers in src/main.py to use clear_screen(), show_loading(), and confirmation dialogs

**Files Modified**:
- src/ui.py (new UX functions)
- src/main.py (enhanced handlers)

**Completion Criteria**:
- [ ] Loading spinner shows during long operations
- [ ] Delete requires confirmation
- [ ] Screen clears between menu transitions
- [ ] All prompts use styled Rich inputs

---

## Phase 6: Polish & Cross-Cutting Concerns

**Goal**: Final touches, performance validation, and documentation.

**Tasks**:

- [ ] T021 Add comprehensive error handling for all edge cases (corrupted JSON, disk full, terminal compatibility)
- [ ] T022 [P] Performance test: Verify JSON save/load <50ms for 1000 tasks, UI rendering <100ms
- [ ] T023 Update README.md with installation instructions, features overview, and quickstart guide

**Completion Criteria**:
- [ ] All edge cases handled gracefully
- [ ] Performance goals met (<50ms JSON I/O, <100ms UI)
- [ ] README updated with enhancement documentation

---

## Dependencies & Execution Order

### Story Dependency Graph

```
Phase 1 (Setup)
    ↓
Phase 2 (Foundational: Task JSON methods + ui.py skeleton)
    ↓
    ├── Phase 3 (US1: Rich UI)
    │      ↓
    └── Phase 4 (US2: JSON Persistence)
           ↓
        Phase 5 (US3: Better UX)
           ↓
        Phase 6 (Polish)
```

### Parallel Execution Opportunities

**Phase 2 - Foundational**:
```bash
# Run in parallel (different files)
Task T003 & T004 (Task model methods)  # Same file, run sequentially
Task T005 (ui.py skeleton)              # Different file, can run in parallel with T003+T004
```

**Phase 4 - US2**:
```bash
# After T012-T015 complete, run in parallel:
Task T016 (TodoManager enhancement)     # Can start after storage.py is complete
```

**Phase 5 - US3**:
```bash
# Run in parallel (independent functions in ui.py)
Task T017 (loading functions)
Task T018 (input functions)              # Can run in parallel with T017
Task T019 (utility functions)            # Can run in parallel with T017+T018
# Then sequentially:
Task T020 (main.py refactor)             # Requires T017-T019 complete
```

**Phase 6 - Polish**:
```bash
# Run in parallel:
Task T021 (error handling)
Task T022 (performance tests)            # Can run in parallel with T021
# Then:
Task T023 (documentation)                # After all code complete
```

---

## Task Execution Guidelines

### For Each Task:

1. **Before Starting**:
   - Read the relevant design docs (data-model.md, research.md)
   - Understand the file you're modifying
   - Check dependencies are met

2. **During Implementation**:
   - Follow the exact specifications in data-model.md
   - Use type hints for all functions
   - Add docstrings following the patterns in data-model.md
   - Preserve existing functionality (don't break working features)

3. **After Completing**:
   - Run existing tests to ensure nothing broke
   - Manually test the specific feature you implemented
   - Check off the task and completion criteria

### Testing Approach:

Since tests are not explicitly requested in the spec, we focus on **manual acceptance testing**:

- **US1 Testing**: Visual inspection (colors, tables, panels)
- **US2 Testing**: Add task, restart app, verify task present
- **US3 Testing**: Observe spinners, confirmations, screen transitions

If you want automated tests, they can be added later as a separate task.

---

## Success Metrics

| Metric | Target | Verification |
|--------|--------|--------------|
| Rich UI Coverage | 100% of output uses Rich | No plain print() in main.py |
| JSON Persistence | Data survives restart | Add task, close, reopen, verify present |
| Auto-save | All mutations save | Check tasks.json after each operation |
| Performance (JSON) | <50ms save/load | Performance test with 1000 tasks |
| Performance (UI) | <100ms render | Manual observation, no lag |
| Error Handling | No crashes | Test missing file, corrupted JSON |

---

## Notes

**Important Reminders**:
- Preserve all existing validation logic in Task model
- Don't modify core business logic unnecessarily
- Keep Rich imports isolated to ui.py
- Follow PEP 8 style guide
- Use descriptive variable names

**Architectural Decisions Implemented**:
- Rich Console singleton pattern (see research.md)
- Save-on-every-mutation for data safety
- Backup-before-save for corruption recovery
- ISO 8601 datetime format in JSON

**Reference Documents**:
- [spec.md](./spec.md) - Requirements and acceptance criteria
- [plan.md](./plan.md) - Architecture and design decisions
- [data-model.md](./data-model.md) - Detailed class/method specifications
- [research.md](./research.md) - Technology patterns and best practices
- [quickstart.md](./quickstart.md) - User guide and troubleshooting

---

**Ready to Begin**: Start with Phase 1, Task T001 (Install Rich library)

Next Command: `/sp.implement` (when available) or manually implement tasks in order
