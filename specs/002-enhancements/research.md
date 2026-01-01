# Research: Rich UI & JSON Persistence Patterns

**Date**: 2026-01-01
**Feature**: Console App Enhancements
**Status**: Complete

## Overview

This document captures research findings and decisions for implementing Rich terminal UI and JSON persistence in the Todo Console App.

---

## 1. Rich Library Best Practices

### Decision: Use Singleton Console Pattern

**Rationale**:
- The Rich library recommends creating a single `Console()` instance and importing it across modules
- This ensures consistent output formatting and avoids terminal state conflicts
- Performance benefit: reduces overhead of multiple console instances

**Implementation**:
```python
# src/ui.py
from rich.console import Console

console = Console()  # Single instance

# Other modules import this
from ui import console
```

**Alternatives Considered**:
- Multiple Console instances per module → Rejected: can cause output conflicts
- Console passed as parameter → Rejected: adds boilerplate to every function

---

### Decision: Use Table for Task List Display

**Rationale**:
- Rich `Table` provides automatic column alignment, borders, and styling
- Built-in header support with styling
- Clean API for adding rows programmatically
- Better readability than manual formatting

**Implementation Pattern**:
```python
from rich.table import Table

table = Table(title="📋 Your Tasks", box=box.ROUNDED)
table.add_column("ID", style="dim", width=6)
table.add_column("Status", width=10)
table.add_column("Title", style="bold")
table.add_row("1", "[green]✓ Done[/green]", "Buy groceries")
console.print(table)
```

**Alternatives Considered**:
- Panel with formatted text → Rejected: harder to align columns
- Layout with columns → Rejected: overkill for simple task display

---

### Decision: Use Panel for Detailed Task Views

**Rationale**:
- Panel provides bordered container perfect for showing individual task details
- Supports title and subtitle for context
- Clean visual separation from other content

**Implementation Pattern**:
```python
from rich.panel import Panel

details = f"""
[bold]ID:[/bold] {task.id}
[bold]Title:[/bold] {task.title}
[bold]Status:[/bold] [green]✓ Completed[/green]
"""
panel = Panel(details, title="Task Details", box=box.ROUNDED)
console.print(panel)
```

---

### Decision: Use Progress with Spinner for Loading States

**Rationale**:
- `Progress` with `SpinnerColumn` provides professional loading feedback
- `transient=True` makes spinner disappear after completion (cleaner)
- Better UX than static "Loading..." text

**Implementation Pattern**:
```python
from rich.progress import Progress, SpinnerColumn, TextColumn

with Progress(
    SpinnerColumn(),
    TextColumn("[progress.description]{task.description}"),
    transient=True
) as progress:
    task = progress.add_task("Saving tasks...", total=None)
    # Perform operation
```

**Alternatives Considered**:
- Status spinner → Rejected: requires manual cleanup
- Simple text → Rejected: no visual feedback that something is happening

---

### Decision: Use Prompt and Confirm for User Input

**Rationale**:
- `Prompt.ask()` provides styled input with validation support
- `Confirm.ask()` handles yes/no questions with clear formatting
- Both integrate well with Rich's color scheme

**Implementation Pattern**:
```python
from rich.prompt import Prompt, Confirm

title = Prompt.ask("[cyan]Enter task title[/cyan]")
confirmed = Confirm.ask("[yellow]Are you sure?[/yellow]")
```

---

### Decision: Graceful Degradation for Limited Terminals

**Rationale**:
- Rich automatically detects terminal capabilities
- Falls back to plain text on unsupported terminals
- No special handling needed in most cases

**Handling**:
- Rich detects color support automatically
- Box drawing characters fall back to ASCII on limited terminals
- No explicit checks needed unless we need specific behavior

---

## 2. JSON Persistence Patterns

### Decision: Save After Every Mutation

**Rationale**:
- Prevents data loss if app crashes or is force-closed
- Small performance overhead (50ms) is acceptable for typical usage
- Simpler than batching or save-on-exit (no cleanup hooks needed)

**Implementation**:
```python
def add_task(self, title: str, description: str) -> Task:
    # ... create task ...
    self.tasks.append(task)
    self._save_to_storage()  # Save immediately
    return task
```

**Alternatives Considered**:
- Save on exit → Rejected: loses data on crashes
- Batch saves every N seconds → Rejected: added complexity, still risk of data loss

---

### Decision: Simple Error Handling for Corrupted JSON

**Rationale**:
- Corrupted JSON is rare in single-user CLI apps
- When it occurs, easiest recovery is to start fresh
- Keep backup for manual recovery if needed

**Implementation Strategy**:
```python
def load(self) -> Dict[str, Any]:
    try:
        with open(self.filepath, 'r') as f:
            data = json.load(f)
        return {"tasks": [...], "next_id": ...}
    except (FileNotFoundError, json.JSONDecodeError):
        # Return empty state, let user know
        return {"tasks": [], "next_id": 1}
```

**Alternatives Considered**:
- Complex repair logic → Rejected: rare case, not worth complexity
- Crash on corruption → Rejected: poor UX
- Auto-backup rotation → Rejected: overkill for single-user app

---

### Decision: Create Backup Before Overwrite

**Rationale**:
- Provides safety net if save operation corrupts file
- Simple copy operation has minimal overhead
- Allows manual recovery if needed

**Implementation**:
```python
def save(self, tasks: List[Task], next_id: int) -> bool:
    if self.filepath.exists():
        backup_path = self.filepath.with_suffix('.json.backup')
        shutil.copy(self.filepath, backup_path)

    # Write new data
    with open(self.filepath, 'w') as f:
        json.dump(data, f, indent=2)
```

**Alternatives Considered**:
- No backup → Rejected: risky, no recovery option
- Multiple backup versions → Rejected: overkill, wastes disk space

---

### Decision: Auto-Create data/ Directory

**Rationale**:
- User shouldn't need to manually create directories
- `Path.mkdir(parents=True, exist_ok=True)` is idempotent
- Fails gracefully if permissions denied

**Implementation**:
```python
def _ensure_data_directory(self) -> None:
    self.filepath.parent.mkdir(parents=True, exist_ok=True)
```

---

### Decision: ISO 8601 for DateTime Serialization

**Rationale**:
- Python's `datetime.isoformat()` produces standard ISO 8601 strings
- Human-readable in JSON files
- Easy to parse back with `datetime.fromisoformat()`

**Implementation**:
```python
def to_dict(self) -> Dict[str, Any]:
    return {
        ...
        "created_at": self.created_at.isoformat()
    }

@classmethod
def from_dict(cls, data: Dict) -> 'Task':
    return cls(
        ...
        created_at=datetime.fromisoformat(data["created_at"])
    )
```

---

### Decision: No File Locking

**Rationale**:
- Single-user CLI app, not designed for concurrent access
- File locking adds platform-specific complexity
- If needed later, can add with `fcntl` (Unix) / `msvcrt` (Windows)

**Risk**: User runs multiple instances → data could be overwritten
**Mitigation**: Document as single-instance app, add warning if needed later

---

## 3. Integration Patterns

### Decision: Separate ui.py Module for Rich Components

**Rationale**:
- Keeps presentation logic separate from business logic
- Makes testing easier (can mock UI functions)
- All Rich imports centralized in one place

**Structure**:
```text
src/ui.py          # All Rich components
src/main.py        # Uses ui.py functions, no direct Rich imports
src/todo_manager.py  # No UI code, purely business logic
```

---

### Decision: Type Hints for All New Code

**Rationale**:
- Constitution requires type hints
- Helps catch bugs early
- Better IDE support

**Pattern**:
```python
def save(self, tasks: List[Task], next_id: int) -> bool:
    ...

def load(self) -> Dict[str, Any]:
    ...
```

---

### Decision: Unit Test Rich UI Where Feasible

**Rationale**:
- Test logic in UI functions (e.g., formatting, filtering)
- Skip visual rendering tests (hard to assert)
- Focus on input validation and data transformation

**What to Test**:
- ✅ `show_tasks_table()` handles empty list
- ✅ `show_task_details()` formats dates correctly
- ✅ `get_input()` returns user input
- ❌ Visual appearance of tables (manual QA)

---

### Decision: Performance Testing for JSON I/O

**Rationale**:
- Need to verify <50ms save goal
- Test with realistic task counts (100, 1000 tasks)
- Benchmark on target platforms

**Test Approach**:
```python
import time

def test_save_performance():
    tasks = [create_task(i) for i in range(1000)]
    start = time.perf_counter()
    storage.save(tasks, 1001)
    duration = time.perf_counter() - start
    assert duration < 0.05  # 50ms
```

---

## Summary of Decisions

| Area | Decision | Rationale |
|------|----------|-----------|
| **Rich Console** | Singleton pattern | Consistent output, no conflicts |
| **Task Display** | Table with columns | Clean alignment, built-in styling |
| **Task Details** | Panel with formatted text | Visual separation, bordered container |
| **Loading UX** | Progress with Spinner | Professional, auto-cleanup |
| **User Input** | Prompt and Confirm | Styled, consistent with theme |
| **Save Strategy** | After every mutation | No data loss on crash |
| **Error Handling** | Return empty state | Simple, graceful recovery |
| **Backup** | Before overwrite | Safety net for corruption |
| **DateTime Format** | ISO 8601 | Standard, human-readable |
| **File Locking** | None (single-user app) | Simple, sufficient for use case |
| **Module Structure** | Separate ui.py | Clean separation of concerns |
| **Testing** | Unit tests for logic only | Practical, maintainable |

---

## Next Steps

With research complete, proceed to Phase 1:
1. Create `data-model.md` with enhanced Task and new JSONStorage class
2. Create `contracts/tasks-schema.json` with JSON schema
3. Create `quickstart.md` with usage instructions
4. Update agent context with Rich library knowledge
