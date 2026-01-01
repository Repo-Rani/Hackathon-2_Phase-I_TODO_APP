# Quickstart Guide: Enhanced Todo Console App

**Version**: 2.0 (with Rich UI + JSON Persistence)
**Date**: 2026-01-01

## What's New

This version adds three major enhancements to the Todo Console App:

1. **🎨 Rich Terminal UI**: Beautiful colorful interface with tables, panels, and styled menus
2. **💾 JSON Persistence**: Your tasks are automatically saved to `data/tasks.json` and survive app restarts
3. **✨ Better UX**: Loading animations, confirmation dialogs, and smooth screen transitions

---

## Installation

### Prerequisites

- Python 3.13 or higher
- UV package manager (recommended) or pip

### Step 1: Install Dependencies

Using UV (recommended):

```bash
uv add rich
```

Using pip:

```bash
pip install rich
```

---

## Running the App

### Start the Application

Using UV:

```bash
uv run python src/main.py
```

Using Python directly:

```bash
python src/main.py
```

### First Run

On first run, the app will:
1. Create a `data/` directory in your project root
2. Create an empty `data/tasks.json` file
3. Display the main menu with no tasks

---

## Features Overview

### 1. Add Task

**Menu Option**: 1

**Steps**:
1. Select option 1 from main menu
2. Enter task title (1-200 characters, required)
3. Enter description (optional, press Enter to skip)
4. Task is created and automatically saved to JSON
5. Confirmation appears with task details in a styled panel

**Example**:
```
Enter task title: Buy groceries
Enter description: Milk, eggs, bread

✓ Task #1 created successfully!

┌─ Task Details ─────────────────────┐
│ ID: 1                              │
│ Title: Buy groceries               │
│ Description: Milk, eggs, bread     │
│ Status: ○ Pending                  │
│ Created: January 01, 2026 at 14:30│
└────────────────────────────────────┘
```

### 2. View All Tasks

**Menu Option**: 2

**Display**:
- Beautiful table with columns: ID, Status, Title, Description, Created
- Color-coded status badges:
  - ✓ Done (green) for completed tasks
  - ○ Pending (yellow) for incomplete tasks
- Task statistics at top (total, completed, pending)

**Example**:
```
┌────────────── 📋 Your Tasks ───────────────┐
│ ID  │ Status     │ Title          │ ...    │
├─────┼────────────┼────────────────┼────────┤
│ 1   │ ○ Pending  │ Buy groceries  │ ...    │
│ 2   │ ✓ Done     │ Write docs     │ ...    │
└─────┴────────────┴────────────────┴────────┘
```

### 3. Update Task

**Menu Option**: 3

**Steps**:
1. Select option 3 from main menu
2. View list of all tasks with IDs
3. Enter task ID to update
4. Choose to update [T]itle, [D]escription, or [B]oth
5. Enter new values
6. Changes are saved automatically

**Features**:
- Current values shown before update
- Can keep current value by pressing Enter
- Validation same as adding new task

### 4. Delete Task

**Menu Option**: 4

**Steps**:
1. Select option 4 from main menu
2. View list of all tasks with IDs
3. Enter task ID to delete
4. Review task details
5. Confirm deletion (yes/no prompt)
6. Task is removed and saved automatically

**Safety Features**:
- Confirmation required before deletion
- Task details shown before confirming
- Can cancel at any point

### 5. Mark Complete/Incomplete

**Menu Option**: 5

**Steps**:
1. Select option 5 from main menu
2. View list of all tasks with current status
3. Enter task ID to toggle
4. Status changes immediately and saves

**Features**:
- Shows before and after status
- Toggle works both ways (complete ↔ incomplete)
- Color-coded status feedback

### 6. Exit

**Menu Option**: 6

**Behavior**:
- Displays goodbye message
- Exits application
- All data is already saved (auto-save after each change)

---

## Data Management

### Where is Data Stored?

**File Location**: `data/tasks.json` (in project root)

**Format**: Human-readable JSON

**Example**:
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "completed": false,
      "created_at": "2026-01-01T14:30:00.123456"
    }
  ],
  "next_id": 2
}
```

### Automatic Saving

Tasks are saved automatically after every operation:
- ✅ After adding a task
- ✅ After updating a task
- ✅ After deleting a task
- ✅ After marking complete/incomplete

**You never need to manually save!**

### Backup Files

Before each save, a backup is created:
- **Backup Location**: `data/tasks.json.backup`
- **Use Case**: Recovery if main file gets corrupted
- **Automatic**: Created on every save operation

---

## Common Tasks

### Viewing Your Data File

```bash
# View current tasks
cat data/tasks.json

# View with pretty formatting (if jq installed)
cat data/tasks.json | jq
```

### Backing Up Your Tasks

```bash
# Create manual backup
cp data/tasks.json data/tasks-backup-2026-01-01.json

# Or just copy the entire data directory
cp -r data/ data-backup/
```

### Resetting All Tasks

```bash
# Delete the data file
rm data/tasks.json

# Next run will start with empty task list
```

### Moving Tasks to Another Machine

```bash
# Export from machine 1
cp data/tasks.json ~/todo-export.json

# Import on machine 2
cp ~/todo-export.json path/to/project/data/tasks.json
```

---

## Troubleshooting

### Problem: "Error loading tasks: [JSON decode error]"

**Cause**: The `tasks.json` file is corrupted or contains invalid JSON

**Solution**:
1. Check if `data/tasks.json.backup` exists
2. If yes, replace corrupted file:
   ```bash
   cp data/tasks.json.backup data/tasks.json
   ```
3. If no backup, delete corrupted file:
   ```bash
   rm data/tasks.json
   ```
4. Restart app (will create fresh empty file)

### Problem: "ModuleNotFoundError: No module named 'rich'"

**Cause**: The `rich` library is not installed

**Solution**:
```bash
# Using UV
uv add rich

# Or using pip
pip install rich
```

### Problem: Colors not showing / weird characters

**Cause**: Your terminal doesn't support full color or Unicode

**Solution**:
- **Windows**: Use Windows Terminal or PowerShell 7+ (not CMD)
- **Linux/Mac**: Most modern terminals work fine
- **SSH**: Ensure `TERM` environment variable is set correctly

**Fallback**: Rich library automatically degrades gracefully on limited terminals

### Problem: "Permission denied" when saving

**Cause**: No write permissions for `data/` directory

**Solution**:
```bash
# Check permissions
ls -la data/

# Fix permissions (Linux/Mac)
chmod 755 data/
chmod 644 data/tasks.json

# Windows: Right-click → Properties → Security → Edit permissions
```

### Problem: Tasks not persisting between runs

**Cause**: Multiple possible issues

**Check**:
1. Is `data/tasks.json` being created?
   ```bash
   ls -la data/
   ```
2. Are saves succeeding? (Watch for error messages)
3. Are you running from correct directory?
   ```bash
   pwd  # Should be project root
   ```

**Solution**:
- Run from project root directory
- Check console for error messages
- Verify write permissions on `data/` directory

---

## Performance Notes

### Expected Performance

| Operation | Expected Time | Note |
|-----------|---------------|------|
| Start app | <100ms | Includes loading tasks from JSON |
| Add task | <100ms | Includes validation and save |
| View tasks | <50ms | In-memory operation |
| Update task | <100ms | Includes validation and save |
| Delete task | <100ms | Includes save |
| Toggle status | <100ms | Includes save |

### Large Task Lists

For 1000+ tasks:
- File size: ~100KB
- Load time: ~15ms
- Save time: ~30ms
- UI rendering: May be slower on limited terminals

**Optimization**: App is designed for 100-1000 tasks. For larger lists, consider archiving completed tasks.

---

## Tips and Best Practices

### 1. Regular Backups

Even though auto-backup exists, periodically copy `data/tasks.json` to a safe location:

```bash
# Weekly backup
cp data/tasks.json ~/backups/tasks-$(date +%Y-%m-%d).json
```

### 2. Task Organization

Use descriptive titles and descriptions:
- ✅ Good: "Buy groceries - Milk, eggs, bread (Whole Foods)"
- ❌ Poor: "Shopping"

### 3. Clearing Completed Tasks

No bulk delete feature (by design), but you can:
1. Manually delete completed tasks one by one
2. Or edit `data/tasks.json` directly (remove completed task objects)

### 4. Archiving Old Tasks

```bash
# Archive completed tasks
# 1. Copy current file
cp data/tasks.json archive/tasks-2026-01.json

# 2. Edit data/tasks.json, remove old completed tasks
# 3. Restart app
```

---

## Keyboard Shortcuts

The app doesn't have custom keyboard shortcuts, but standard terminal shortcuts work:

- **Ctrl+C**: Exit app immediately (unsaved changes are already saved!)
- **Ctrl+D**: EOF signal (acts like cancel in input prompts)
- **Up/Down Arrow**: Navigate command history (terminal feature)

---

## Next Steps

### Learn More

- Read `data-model.md` for technical details on data structures
- Read `plan.md` for architecture decisions
- Check `contracts/tasks-schema.json` for JSON schema

### Customization

To customize colors, edit `src/ui.py`:
- Change color scheme (cyan → blue, green → purple, etc.)
- Modify table styling (borders, padding)
- Adjust loading spinner duration

---

## Support

### Reporting Issues

If you encounter bugs:
1. Check error messages in console
2. Verify `data/tasks.json` format
3. Try with fresh `tasks.json` file
4. Check Troubleshooting section above

### Feature Requests

This app follows Spec-Driven Development:
1. Write feature specification
2. Use Claude Code to implement
3. Maintain backward compatibility with JSON format

---

## Summary

**Installation**: `uv add rich`
**Run**: `uv run python src/main.py`
**Data**: Automatically saved to `data/tasks.json`
**Backup**: `data/tasks.json.backup` created on each save
**Reset**: Delete `data/tasks.json` to start fresh

Enjoy your enhanced Todo Console App! 🎉
