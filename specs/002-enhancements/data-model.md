# Data Model: Enhanced Task with JSON Persistence

**Date**: 2026-01-01
**Feature**: Console App Enhancements
**Status**: Design Complete

## Overview

This document defines the enhanced data model for the Todo Console App, including JSON serialization support and the new JSONStorage abstraction layer.

---

## Core Entities

### 1. Task (Enhanced)

**Location**: `src/models.py`

**Purpose**: Represents a single todo item with full JSON serialization support.

#### Attributes

| Attribute | Type | Required | Validation | Description |
|-----------|------|----------|------------|-------------|
| id | int | Yes | >= 1 | Unique sequential identifier |
| title | str | Yes | 1-200 chars, non-whitespace | Task title |
| description | str | Yes | 0-1000 chars | Task description (empty string if not provided) |
| completed | bool | Yes | - | Completion status (default: False) |
| created_at | datetime | Yes | Valid datetime | Timestamp of task creation |

#### Methods (Existing)

```python
def __post_init__(self) -> None:
    """Validate task attributes after initialization."""
    # Validates title (1-200 chars, non-whitespace)
    # Validates description (0-1000 chars)
    # Validates standard characters (alphanumeric + common punctuation)
```

#### Methods (New)

```python
def to_dict(self) -> Dict[str, Any]:
    """
    Convert task to dictionary for JSON serialization.

    Returns:
        Dictionary with keys: id, title, description, completed, created_at
        created_at is serialized as ISO 8601 string

    Example:
        {
            "id": 1,
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
            "completed": false,
            "created_at": "2026-01-01T14:30:00.123456"
        }
    """
    return {
        "id": self.id,
        "title": self.title,
        "description": self.description,
        "completed": self.completed,
        "created_at": self.created_at.isoformat()
    }

@classmethod
def from_dict(cls, data: Dict[str, Any]) -> 'Task':
    """
    Create Task instance from dictionary (JSON deserialization).

    Args:
        data: Dictionary with task data

    Returns:
        Task instance

    Raises:
        ValueError: If data fails validation
        KeyError: If required fields missing

    Example:
        data = {
            "id": 1,
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
            "completed": false,
            "created_at": "2026-01-01T14:30:00.123456"
        }
        task = Task.from_dict(data)
    """
    return cls(
        id=data["id"],
        title=data["title"],
        description=data["description"],
        completed=data["completed"],
        created_at=datetime.fromisoformat(data["created_at"])
    )
```

#### Invariants

- ID must never change after creation
- Title must always contain non-whitespace content
- Description can be empty string but not None
- created_at is immutable (timestamp of creation, not modification)

---

### 2. JSONStorage (New)

**Location**: `src/storage.py`

**Purpose**: Handles all file I/O operations for task persistence, abstracting away JSON serialization details.

#### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| filepath | Path | Path to JSON file (default: `data/tasks.json`) |

#### Methods

```python
def __init__(self, filepath: str = "data/tasks.json") -> None:
    """
    Initialize storage handler.

    Args:
        filepath: Path to JSON file relative to project root

    Side Effects:
        Creates data directory if it doesn't exist
    """
    self.filepath = Path(filepath)
    self._ensure_data_directory()

def _ensure_data_directory(self) -> None:
    """
    Create data directory if it doesn't exist.

    Uses Path.mkdir(parents=True, exist_ok=True) for idempotent creation.
    Fails silently if directory already exists.
    """
    self.filepath.parent.mkdir(parents=True, exist_ok=True)

def save(self, tasks: List[Task], next_id: int) -> bool:
    """
    Save tasks to JSON file with backup.

    Args:
        tasks: List of Task objects to serialize
        next_id: Next ID counter value to preserve

    Returns:
        True if save successful, False otherwise

    Side Effects:
        - Creates backup file (.json.backup) if original exists
        - Overwrites existing tasks.json file
        - Writes pretty-printed JSON (indent=2)

    Error Handling:
        - Catches all exceptions (IOError, JSONEncodeError, etc.)
        - Prints error message to console
        - Returns False on failure

    File Format:
        {
            "tasks": [
                {"id": 1, "title": "...", ...},
                {"id": 2, "title": "...", ...}
            ],
            "next_id": 3
        }
    """
    try:
        # Create backup if file exists
        if self.filepath.exists():
            backup_path = self.filepath.with_suffix('.json.backup')
            shutil.copy(self.filepath, backup_path)

        # Serialize tasks
        data = {
            "tasks": [task.to_dict() for task in tasks],
            "next_id": next_id
        }

        # Write to file
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return True
    except Exception as e:
        print(f"Error saving tasks: {e}")
        return False

def load(self) -> Dict[str, Any]:
    """
    Load tasks from JSON file.

    Returns:
        Dictionary with structure:
        {
            "tasks": List[Task],
            "next_id": int
        }

        Returns empty state if file doesn't exist or is corrupted:
        {"tasks": [], "next_id": 1}

    Error Handling:
        - FileNotFoundError → Returns empty state (normal for first run)
        - JSONDecodeError → Returns empty state, prints error
        - Other exceptions → Returns empty state, prints error
    """
    if not self.filepath.exists():
        return {"tasks": [], "next_id": 1}

    try:
        with open(self.filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Deserialize tasks
        tasks = [Task.from_dict(task_data) for task_data in data.get("tasks", [])]
        next_id = data.get("next_id", 1)

        return {"tasks": tasks, "next_id": next_id}
    except Exception as e:
        print(f"Error loading tasks: {e}")
        return {"tasks": [], "next_id": 1}

def backup(self) -> bool:
    """
    Create manual backup of current tasks file.

    Returns:
        True if backup created, False if file doesn't exist or error occurs

    Backup Location:
        Same directory as tasks.json with .backup extension
    """
    if not self.filepath.exists():
        return False

    try:
        backup_path = self.filepath.with_suffix('.json.backup')
        shutil.copy(self.filepath, backup_path)
        return True
    except Exception as e:
        print(f"Error creating backup: {e}")
        return False
```

---

### 3. TodoManager (Enhanced)

**Location**: `src/todo_manager.py`

**Purpose**: Manages task operations with automatic persistence.

#### New/Modified Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| storage | JSONStorage | Storage handler instance (new) |
| tasks | List[Task] | In-memory task list (existing) |
| next_id | int | Next ID counter (existing) |

#### New Methods

```python
def __init__(self, storage_path: str = "data/tasks.json") -> None:
    """
    Initialize TodoManager with JSON persistence.

    Args:
        storage_path: Path to JSON file (default: data/tasks.json)

    Side Effects:
        - Creates JSONStorage instance
        - Loads existing tasks from file
        - Initializes empty state if file doesn't exist
    """
    self.storage = JSONStorage(storage_path)
    self.tasks: List[Task] = []
    self.next_id: int = 1
    self._load_from_storage()

def _load_from_storage(self) -> None:
    """
    Load tasks from JSON file on initialization.

    Side Effects:
        - Populates self.tasks with loaded Task objects
        - Sets self.next_id to loaded counter value
    """
    data = self.storage.load()
    self.tasks = data["tasks"]
    self.next_id = data["next_id"]

def _save_to_storage(self) -> bool:
    """
    Save current state to JSON file.

    Returns:
        True if save successful, False otherwise

    Called After:
        - Every add_task()
        - Every update_task()
        - Every delete_task()
        - Every toggle_complete()
    """
    return self.storage.save(self.tasks, self.next_id)
```

#### Modified Methods

All mutation methods now call `self._save_to_storage()` after modifying tasks:

```python
def add_task(self, title: str, description: str = "") -> Task:
    # ... existing logic ...
    self.tasks.append(new_task)
    self.next_id += 1
    self._save_to_storage()  # NEW
    return new_task

def update_task(self, task_id: int, title: str = None, description: str = None) -> bool:
    # ... existing logic ...
    self.tasks[index] = updated_task
    self._save_to_storage()  # NEW
    return True

def delete_task(self, task_id: int) -> bool:
    # ... existing logic ...
    self.tasks.remove(task)
    self._save_to_storage()  # NEW
    return True

def toggle_complete(self, task_id: int) -> bool:
    # ... existing logic ...
    task.completed = not task.completed
    self._save_to_storage()  # NEW
    return True
```

---

## Data Flow

### 1. Application Startup

```
main()
  → TodoManager.__init__()
    → JSONStorage.__init__()
      → _ensure_data_directory()  # Create data/ if needed
    → _load_from_storage()
      → storage.load()
        → Read data/tasks.json
        → Deserialize Task objects
        → Return {"tasks": [...], "next_id": n}
      → Populate self.tasks and self.next_id
  → Display menu (with loaded tasks)
```

### 2. Adding a Task

```
User selects "Add Task"
  → handle_add_task()
    → Get user input (title, description)
    → todo_manager.add_task(title, description)
      → Create Task object (validation happens in __post_init__)
      → Append to self.tasks
      → Increment self.next_id
      → _save_to_storage()
        → storage.save(self.tasks, self.next_id)
          → Backup existing file
          → Serialize tasks to JSON
          → Write to data/tasks.json
          → Return True
      → Return new Task object
    → Display success message with task details
```

### 3. Viewing Tasks

```
User selects "View Tasks"
  → handle_view_tasks()
    → todo_manager.get_all_tasks()
      → Return copy of self.tasks  # No persistence needed
    → Display tasks in Rich Table
```

### 4. Updating/Deleting/Toggling

```
User performs mutation operation
  → Mutation method (update_task/delete_task/toggle_complete)
    → Modify self.tasks in-memory
    → _save_to_storage()  # Automatic persistence
      → storage.save(self.tasks, self.next_id)
    → Return success/failure
```

---

## File Format

### tasks.json Structure

```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "completed": false,
      "created_at": "2026-01-01T14:30:00.123456"
    },
    {
      "id": 2,
      "title": "Write documentation",
      "description": "",
      "completed": true,
      "created_at": "2026-01-01T15:45:00.789012"
    }
  ],
  "next_id": 3
}
```

### Field Details

- **tasks**: Array of task objects (can be empty `[]`)
- **next_id**: Integer counter for next task ID (minimum: 1)
- **created_at**: ISO 8601 datetime string (Python `isoformat()` output)

### Encoding

- **Encoding**: UTF-8
- **Indentation**: 2 spaces (for human readability)
- **ensure_ascii**: False (allow Unicode characters in titles/descriptions)

---

## Error Handling

### Corrupted JSON File

**Scenario**: File contains invalid JSON syntax

**Handling**:
1. `JSONStorage.load()` catches `JSONDecodeError`
2. Prints error message: "Error loading tasks: [details]"
3. Returns empty state: `{"tasks": [], "next_id": 1}`
4. User starts with clean slate (old file preserved as backup)

### Missing Fields

**Scenario**: JSON file missing required fields (e.g., "next_id")

**Handling**:
1. `data.get("next_id", 1)` provides default value
2. `data.get("tasks", [])` provides empty list
3. App continues with partial/default data

### Invalid Task Data

**Scenario**: Task object fails validation (e.g., title too long)

**Handling**:
1. `Task.from_dict()` raises `ValueError` in `__post_init__`
2. Exception propagates up to `JSONStorage.load()`
3. Entire load operation fails → returns empty state
4. User notified via error message

### Save Failures

**Scenario**: Disk full, permissions denied, etc.

**Handling**:
1. `JSONStorage.save()` catches all exceptions
2. Prints error message: "Error saving tasks: [details]"
3. Returns False (but doesn't crash app)
4. In-memory data still intact, user can retry or exit

---

## Testing Strategy

### Unit Tests for Task

- ✅ Test `to_dict()` produces correct structure
- ✅ Test `from_dict()` recreates Task correctly
- ✅ Test datetime serialization (ISO format)
- ✅ Test validation errors propagate from `from_dict()`

### Unit Tests for JSONStorage

- ✅ Test save creates file with correct structure
- ✅ Test load reads file correctly
- ✅ Test load handles missing file (returns empty state)
- ✅ Test load handles corrupted JSON (returns empty state)
- ✅ Test backup creates .backup file
- ✅ Test _ensure_data_directory creates directory

### Integration Tests for TodoManager

- ✅ Test tasks persist across TodoManager instances
- ✅ Test next_id preserved correctly
- ✅ Test mutations trigger saves
- ✅ Test save failures don't crash app

---

## Migration Strategy

**Current State**: No existing JSON files (in-memory only)

**Migration**:
- No migration needed
- First run creates empty `data/tasks.json`
- Users start fresh with new persistence system

**Future Schema Changes**:
If we add new fields to Task in the future:
1. Add field with default value in Task dataclass
2. Update `to_dict()` to include new field
3. Update `from_dict()` with `.get(field, default)`
4. Old JSON files load successfully (missing fields use defaults)

---

## Performance Considerations

### Typical Case (100 tasks)

- **File Size**: ~10KB
- **Save Time**: <10ms
- **Load Time**: <5ms
- **Well within 50ms goal** ✅

### Large Case (1000 tasks)

- **File Size**: ~100KB
- **Save Time**: ~30ms
- **Load Time**: ~15ms
- **Still within 50ms goal** ✅

### Optimization Opportunities (if needed later)

- Use `ujson` instead of stdlib `json` (3-5x faster)
- Implement incremental saves (append-only log)
- Add compression for large files
- **Decision**: Not needed now, monitor in production

---

## Summary

| Component | Purpose | Key Methods |
|-----------|---------|-------------|
| **Task** | Data model with JSON support | `to_dict()`, `from_dict()` |
| **JSONStorage** | File I/O abstraction | `save()`, `load()`, `backup()` |
| **TodoManager** | Business logic with auto-save | `_load_from_storage()`, `_save_to_storage()` |

**Design Principles**:
- Single source of truth: JSON file
- In-memory operations: Fast reads
- Automatic persistence: No user action required
- Graceful degradation: Errors don't crash app
- Simple recovery: Backup files for safety
