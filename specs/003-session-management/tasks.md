# Implementation Tasks: Session Management

**Feature**: Session State Management for Todo App
**Branch**: `003-session-management`
**Date**: 2026-01-06
**Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)

---

## Task Summary

| Phase | User Story | Task Count | Parallel | Dependencies |
|-------|------------|------------|----------|--------------|
| 1 | Setup | 2 | 1 | None |
| 2 | Foundational | 4 | 2 | Phase 1 complete |
| 3 | US1 - Save Session | 4 | 0 | Phase 2 complete |
| 4 | US2 - Resume Session | 4 | 0 | Phase 2 complete |
| 5 | US3 - Session Management | 6 | 2 | Phase 2 complete |
| 6 | US4 - Validation & US5 - Auto-Detection | 4 | 1 | All previous phases complete |
| 7 | Polish | 2 | 0 | All user stories complete |
| **Total** | | **26** | **5** | |

**MVP Scope**: User Stories 1 + 2 (Save + Resume sessions)
**Optional**: User Stories 3 + 4 + 5 (Management, Validation, Auto-detection)

---

## Implementation Strategy

### Delivery Approach

1. **MVP First**: Implement US1 (Save Session) and US2 (Resume Session) together
   - These are both P1 priority and foundational to the session feature
   - Can be delivered as a single increment
   - US3, US4, US5 (Management, Validation, Auto-detection) are P2 and can be added later

2. **Incremental Testing**:
   - Each user story has independent test criteria
   - Verify US1: Session saves with all data (tasks, metadata)
   - Verify US2: Session restores with exact state
   - Verify US3: Management commands work (list, delete, info)
   - Verify US4: Error handling works for all scenarios
   - Verify US5: Auto-detection prompts user on startup

3. **Parallel Opportunities**:
   - Within Foundational phase: T003 and T004 can run in parallel
   - Within US3 phase: T014 and T015 can run in parallel
   - Within Polish phase: T025 can run in parallel with other tasks

---

## Phase 1: Setup

**Goal**: Prepare environment and create directory structure for session management.

**Tasks**:

- [ ] T001 Create `/sessions` directory in project root using os.path or pathlib
- [ ] T002 Update .gitignore to include `/sessions/*.json.backup` files (backup files for sessions)

**Completion Criteria**:
- [ ] `/sessions` directory exists in project root
- [ ] `.gitignore` updated to exclude session backup files
- [ ] Directory is created automatically if it doesn't exist

---

## Phase 2: Foundational (Blocking Prerequisites)

**Goal**: Create shared infrastructure needed by multiple user stories.

**Tasks**:

- [ ] T003 [P] Create SessionData dataclass in src/models.py with to_dict() and from_dict() methods for JSON serialization
- [ ] T004 [P] Create SessionMetadata dataclass in src/models.py with to_dict() and from_dict() methods for session metadata
- [ ] T005 Create SessionStorage class in src/storage.py with save_session(), load_session(), delete_session(), list_sessions(), and session_exists() methods
- [ ] T006 Create validate_session_code() function in src/storage.py for session code validation

**Completion Criteria**:
- [ ] SessionData can serialize/deserialize to/from dictionaries
- [ ] SessionMetadata can serialize/deserialize to/from dictionaries
- [ ] SessionStorage handles all session operations correctly
- [ ] Session code validation works as specified
- [ ] All existing tests still pass

**Independent Test**:
```python
# Test session data serialization
from models import SessionData, Task
from datetime import datetime

task = Task(1, "Test", "Description", False, datetime.now())
session = SessionData("test123", datetime.now(), datetime.now(), "Testing", "Active", 2, [task])
data = session.to_dict()
assert data["session_code"] == "test123"
assert len(data["tasks"]) == 1

restored = SessionData.from_dict(data)
assert restored.session_code == session.session_code
assert len(restored.tasks) == 1
```

---

## Phase 3: User Story 1 - Save Session State (P1)

**Story Goal**: Enable users to save their current work state with a session code.

**Independent Test Criteria**:
- [x] User runs app and types "stop 123" → session saved to sessions/session_123.json
- [x] Session file contains all current todos with original IDs and states
- [x] Session file includes metadata: code, timestamps, last activity, phase of work
- [x] User receives confirmation message when session is saved

**Tasks**:

- [ ] T007 [US1] Implement SessionStateManager.save_current_state() method in src/todo_manager.py to save current state to session
- [ ] T008 [US1] Extend TodoManager to include session state attributes (current_session_code, last_activity, phase_of_work)
- [ ] T009 [US1] Add session validation to save_current_state() using validate_session_code()
- [ ] T010 [US1] Add success/error messaging to save_current_state() method

**Files Modified**:
- src/todo_manager.py (enhanced with session save functionality)

**Completion Criteria**:
- [ ] save_current_state() saves all tasks with original IDs and states
- [ ] Session includes proper metadata (timestamps, activity, phase)
- [ ] Session code validation prevents invalid codes
- [ ] User receives appropriate feedback for success/error cases

---

## Phase 4: User Story 2 - Resume Session State (P1)

**Story Goal**: Enable users to restore their work state using a session code.

**Independent Test Criteria**:
- [x] User runs app and types "start 123" → session loaded from sessions/session_123.json
- [x] All todos restored with original IDs and states
- [x] System shows summary: "Resuming session 123 - Last activity: [description]"
- [x] User can continue working as if they never left

**Tasks**:

- [ ] T011 [US2] Implement SessionStateManager.load_session_state() method in src/todo_manager.py to load session state
- [ ] T012 [US2] Implement state restoration logic in load_session_state() to restore tasks, next_id, and metadata
- [ ] T013 [US2] Add success/error messaging to load_session_state() method with session summary
- [ ] T014 [US2] Add session existence validation to load_session_state() method

**Files Modified**:
- src/todo_manager.py (enhanced with session load functionality)

**Completion Criteria**:
- [ ] load_session_state() restores all tasks with original IDs and states
- [ ] System shows appropriate resume summary with timestamp and last activity
- [ ] Session existence validation prevents loading non-existent sessions
- [ ] User can continue working with restored state

---

## Phase 5: User Story 3 - Session Management (P2)

**Story Goal**: Enable users to manage their saved sessions.

**Independent Test Criteria**:
- [x] User types "sessions list" → shows all saved sessions with codes, time, and todo count
- [x] User types "sessions delete 123" → deletes session 123 with confirmation
- [x] User types "sessions info 123" → shows detailed session information
- [x] All management commands provide clear feedback

**Tasks**:

- [ ] T015 [US3] Implement SessionStateManager.list_sessions() method in src/todo_manager.py to list all sessions
- [ ] T016 [US3] Implement SessionStateManager.delete_session() method in src/todo_manager.py to delete a session
- [ ] T017 [US3] Implement SessionStateManager.session_info() method in src/todo_manager.py to show session details
- [ ] T018 [P] [US3] Create session command parsing logic in src/main.py to handle "sessions [subcommand]" commands
- [ ] T019 [P] [US3] Update CLI menu to recognize session management commands (list, delete, info)
- [ ] T020 [US3] Add session management command handlers to main.py

**Files Modified**:
- src/todo_manager.py (enhanced with management methods)
- src/main.py (enhanced with command parsing)

**Completion Criteria**:
- [ ] "sessions list" shows all available sessions with metadata
- [ ] "sessions delete [code]" removes specified session
- [ ] "sessions info [code]" shows detailed session information
- [ ] All management commands provide clear feedback
- [ ] Session management commands are properly integrated into CLI

---

## Phase 6: User Story 4 - Session Validation & US5 - Auto-Detection (P2)

**Story Goal**: Implement proper error handling for session operations and auto-detection of existing sessions.

**Independent Test Criteria**:
- [x] System shows error when session code is not found
- [x] System shows error when session code is invalid (non-alphanumeric)
- [x] System handles corrupted session files gracefully
- [x] On app start, system detects existing sessions and prompts user to resume

**Tasks**:

- [ ] T021 [US4] Enhance error handling in SessionStorage for corrupted JSON files
- [ ] T022 [US4] Add comprehensive validation to all session operations (save, load, delete)
- [ ] T023 [US5] Implement session auto-detection on app startup in src/main.py
- [ ] T024 [P] [US5] Add user prompt for resuming existing sessions in src/main.py

**Files Modified**:
- src/storage.py (enhanced error handling)
- src/main.py (auto-detection and prompting)

**Completion Criteria**:
- [ ] Corrupted session files handled gracefully with error messages
- [ ] All error scenarios have appropriate handling
- [ ] App detects existing sessions on startup
- [ ] User can choose to resume session or start fresh on startup

---

## Phase 7: Polish & Cross-Cutting Concerns

**Goal**: Final touches, performance validation, and integration.

**Tasks**:

- [ ] T025 Add "stop [code]" and "start [code]" command recognition to main.py CLI parser
- [ ] T026 Update README.md with session management feature documentation

**Completion Criteria**:
- [ ] "stop [code]" and "start [code]" commands work as specified
- [ ] README updated with session management usage instructions
- [ ] All session functionality integrated into main app flow

---

## Dependencies & Execution Order

### Story Dependency Graph

```
Phase 1 (Setup)
    ↓
Phase 2 (Foundational: Session models + storage)
    ↓
    ├── Phase 3 (US1: Save Session)
    ├── Phase 4 (US2: Resume Session)
    └── Phase 5 (US3: Session Management)
           ↓
        Phase 6 (US4: Validation + US5: Auto-detection)
           ↓
        Phase 7 (Polish)
```

### Parallel Execution Opportunities

**Phase 2 - Foundational**:
```bash
# Run in parallel (different aspects of SessionStorage)
Task T003 & T004 (Session data models)  # Can run in parallel
Task T005 (SessionStorage class)        # Can run in parallel with T003+T004
Task T006 (Validation function)         # Can run in parallel with others
```

**Phase 5 - US3**:
```bash
# Run in parallel (management methods in todo_manager.py)
Task T015 (list_sessions)
Task T016 (delete_session)              # Can run in parallel with T015
Task T017 (session_info)                # Can run in parallel with T015+T016
# Then in parallel (CLI updates):
Task T018 (command parsing)
Task T019 (menu recognition)            # Can run in parallel with T018
# Then:
Task T020 (command handlers)            # Requires T018+T019 complete
```

**Phase 6 - US4 & US5**:
```bash
# Run in parallel (independent enhancements)
Task T021 (error handling in storage)
Task T022 (validation enhancements)      # Can run in parallel with T021
Task T023 (auto-detection in main)      # Can run in parallel with T021+T022
# Then:
Task T024 (user prompting)              # Requires T023 complete
```

**Phase 7 - Polish**:
```bash
# Run in parallel:
Task T025 (command recognition in main)
Task T026 (README update)               # Can run in parallel with T025
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

- **US1 Testing**: Save session, verify file created with correct data
- **US2 Testing**: Resume session, verify state restored exactly
- **US3 Testing**: List, delete, info commands work as expected
- **US4 Testing**: Error conditions handled gracefully
- **US5 Testing**: Auto-detection works on app startup

If you want automated tests, they can be added later as a separate task.

---

## Success Metrics

| Metric | Target | Verification |
|--------|--------|--------------|
| Session Save | All data saved correctly | Save session, inspect JSON file |
| Session Restore | Exact state restoration | Save, clear app state, load, verify identical |
| Session Management | All commands work | Test list, delete, info commands |
| Error Handling | No crashes on invalid input | Test invalid session codes, corrupted files |
| Performance | <100ms operations | Time save/load operations with 1000 tasks |
| User Experience | Intuitive commands | Verify command syntax is user-friendly |

---

## Notes

**Important Reminders**:
- Preserve all existing functionality in TodoManager
- Don't modify core business logic unnecessarily
- Follow PEP 8 style guide
- Use descriptive variable names
- Maintain backward compatibility

**Architectural Decisions Implemented**:
- Session data stored in dedicated directory
- Backup strategy for session files
- ISO 8601 datetime format in JSON
- Alphanumeric-only session codes for security

**Reference Documents**:
- [spec.md](./spec.md) - Requirements and acceptance criteria
- [plan.md](./plan.md) - Architecture and design decisions
- [data-model.md](./data-model.md) - Detailed class/method specifications
- [research.md](./research.md) - Technology patterns and best practices (if exists)
- [quickstart.md](./quickstart.md) - User guide and troubleshooting (if exists)

---

**Ready to Begin**: Start with Phase 1, Task T001 (Create /sessions directory)

Next Command: `/sp.implement` (when available) or manually implement tasks in order