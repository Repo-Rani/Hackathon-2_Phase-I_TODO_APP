# Data Model: Session Management

**Feature**: Session State Management for Todo App
**Feature ID**: 003-session-management
**Date**: 2026-01-06
**Author**: Claude Code
**Status**: Implementation

## Overview

This document defines the data structures, classes, and serialization formats for the session management feature. It specifies how session data is stored, loaded, and managed within the application.

## Class Definitions

### SessionData Class

```python
from dataclasses import dataclass
from typing import List, Dict, Any
from datetime import datetime
from src.models import Task

@dataclass
class SessionData:
    """
    Represents the complete state of a session that can be saved and restored.

    This class contains all the information needed to save and restore
    the complete application state for a given session.
    """
    session_code: str
    created_at: datetime
    last_modified: datetime
    last_activity: str
    phase_of_work: str
    next_id: int
    tasks: List[Task]

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert SessionData instance to dictionary for JSON serialization.

        Returns:
            Dictionary representation of the session data with ISO format timestamps
        """
        return {
            "session_code": self.session_code,
            "created_at": self.created_at.isoformat(),
            "last_modified": self.last_modified.isoformat(),
            "last_activity": self.last_activity,
            "phase_of_work": self.phase_of_work,
            "next_id": self.next_id,
            "tasks": [task.to_dict() for task in self.tasks]
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SessionData':
        """
        Create SessionData instance from dictionary (JSON deserialization).

        Args:
            data: Dictionary containing session data

        Returns:
            SessionData instance
        """
        from src.models import Task

        return cls(
            session_code=data["session_code"],
            created_at=datetime.fromisoformat(data["created_at"]),
            last_modified=datetime.fromisoformat(data["last_modified"]),
            last_activity=data["last_activity"],
            phase_of_work=data["phase_of_work"],
            next_id=data["next_id"],
            tasks=[Task.from_dict(task_data) for task_data in data["tasks"]]
        )
```

### SessionMetadata Class

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class SessionMetadata:
    """
    Represents metadata about a saved session without loading full content.

    Used for session listing and information display.
    """
    session_code: str
    created_at: datetime
    last_modified: datetime
    last_activity: str
    task_count: int
    file_path: str

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert SessionMetadata instance to dictionary for display purposes.

        Returns:
            Dictionary representation of the session metadata
        """
        return {
            "session_code": self.session_code,
            "created_at": self.created_at.isoformat(),
            "last_modified": self.last_modified.isoformat(),
            "last_activity": self.last_activity,
            "task_count": self.task_count,
            "file_path": self.file_path
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SessionMetadata':
        """
        Create SessionMetadata instance from dictionary.

        Args:
            data: Dictionary containing session metadata

        Returns:
            SessionMetadata instance
        """
        return cls(
            session_code=data["session_code"],
            created_at=datetime.fromisoformat(data["created_at"]),
            last_modified=datetime.fromisoformat(data["last_modified"]),
            last_activity=data["last_activity"],
            task_count=data["task_count"],
            file_path=data["file_path"]
        )
```

## Session Storage Interface

### SessionStorage Class

```python
import json
import os
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime
import tempfile

class SessionStorage:
    """
    Handles session-specific save and load operations.

    Manages the persistence of session data to JSON files in the sessions directory.
    """

    def __init__(self, sessions_dir: str = "sessions"):
        """
        Initialize SessionStorage with sessions directory.

        Args:
            sessions_dir: Directory name for storing session files (default: "sessions")
        """
        self.sessions_dir = Path(sessions_dir)
        self._ensure_sessions_directory()

    def _ensure_sessions_directory(self) -> None:
        """
        Create sessions directory if it doesn't exist.
        """
        self.sessions_dir.mkdir(exist_ok=True)

    def save_session(self, session_data: SessionData) -> bool:
        """
        Save session data to a JSON file.

        Args:
            session_data: SessionData instance to save

        Returns:
            True if save was successful, False otherwise
        """
        try:
            # Create backup of existing session if it exists
            session_file = self.sessions_dir / f"session_{session_data.session_code}.json"
            if session_file.exists():
                backup_path = session_file.with_suffix(session_file.suffix + ".backup")
                if session_file.exists():
                    session_file.replace(backup_path)

            # Write session data to file using temporary file for atomic operation
            temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False,
                                                  dir=self.sessions_dir,
                                                  suffix='.json')
            try:
                json.dump(session_data.to_dict(), temp_file, indent=2)
                temp_file.close()

                # Atomically move temp file to final location
                os.replace(temp_file.name, session_file)
                return True
            except Exception:
                # If there was an error, remove the temp file
                if 'temp_file' in locals():
                    os.unlink(temp_file.name)
                raise
        except Exception as e:
            print(f"Error saving session: {e}")
            return False

    def load_session(self, session_code: str) -> Optional[SessionData]:
        """
        Load session data from a JSON file.

        Args:
            session_code: The session code to load

        Returns:
            SessionData instance if successful, None otherwise
        """
        try:
            session_file = self.sessions_dir / f"session_{session_code}.json"
            if not session_file.exists():
                return None

            with open(session_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return SessionData.from_dict(data)
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"Error loading session: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error loading session: {e}")
            return None

    def delete_session(self, session_code: str) -> bool:
        """
        Delete a session file.

        Args:
            session_code: The session code to delete

        Returns:
            True if deletion was successful, False otherwise
        """
        try:
            session_file = self.sessions_dir / f"session_{session_code}.json"
            if session_file.exists():
                session_file.unlink()
                return True
            return False
        except Exception as e:
            print(f"Error deleting session: {e}")
            return False

    def list_sessions(self) -> List[SessionMetadata]:
        """
        List all available sessions with their metadata.

        Returns:
            List of SessionMetadata instances for all available sessions
        """
        sessions = []
        for file_path in self.sessions_dir.glob("session_*.json"):
            # Extract session code from filename (remove "session_" prefix and ".json" suffix)
            filename = file_path.name
            if filename.startswith("session_") and filename.endswith(".json"):
                session_code = filename[8:-5]  # Remove "session_" (8 chars) and ".json" (5 chars)

                # Try to load basic metadata from the file
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                        metadata = SessionMetadata(
                            session_code=session_code,
                            created_at=datetime.fromisoformat(data.get("created_at", datetime.now().isoformat())),
                            last_modified=datetime.fromisoformat(data.get("last_modified", datetime.now().isoformat())),
                            last_activity=data.get("last_activity", "Unknown"),
                            task_count=len(data.get("tasks", [])),
                            file_path=str(file_path)
                        )
                        sessions.append(metadata)
                except (json.JSONDecodeError, KeyError, ValueError):
                    # If we can't read the file, create minimal metadata
                    metadata = SessionMetadata(
                        session_code=session_code,
                        created_at=datetime.fromtimestamp(file_path.stat().st_ctime),
                        last_modified=datetime.fromtimestamp(file_path.stat().st_mtime),
                        last_activity="Corrupted file",
                        task_count=0,
                        file_path=str(file_path)
                    )
                    sessions.append(metadata)

        return sessions

    def session_exists(self, session_code: str) -> bool:
        """
        Check if a session exists.

        Args:
            session_code: The session code to check

        Returns:
            True if session exists, False otherwise
        """
        session_file = self.sessions_dir / f"session_{session_code}.json"
        return session_file.exists()
```

## Session Command Interface

### Session Command Types

```python
from enum import Enum
from typing import NamedTuple, Optional

class SessionCommandType(Enum):
    """
    Types of session commands supported by the system.
    """
    STOP = "stop"          # Save current session
    START = "start"        # Resume a session
    LIST = "list"          # List all sessions
    DELETE = "delete"      # Delete a session
    INFO = "info"          # Show session info
    SESSIONS = "sessions"  # Base command for session management

class SessionCommand(NamedTuple):
    """
    Represents a parsed session command with its arguments.
    """
    command_type: SessionCommandType
    session_code: Optional[str] = None
    additional_args: Optional[list] = None
```

## Session Validation Functions

### Session Code Validation

```python
def validate_session_code(session_code: str) -> tuple[bool, str]:
    """
    Validate a session code for proper format.

    Args:
        session_code: The session code to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not session_code:
        return False, "Session code cannot be empty"

    if not session_code.isalnum():
        return False, "Session code must be alphanumeric only (no spaces or special characters)"

    if len(session_code) > 50:
        return False, "Session code too long (max 50 characters)"

    if len(session_code) < 1:
        return False, "Session code too short (min 1 character)"

    return True, ""
```

## Session State Interface

### Session State Manager (Extension to TodoManager)

```python
from typing import Optional
from datetime import datetime

class SessionStateManager:
    """
    Interface for managing session state within TodoManager.

    This is an extension that will be integrated into the existing TodoManager class.
    """

    def __init__(self):
        """
        Initialize session state management.
        """
        self.session_storage = SessionStorage()
        self.current_session_code: Optional[str] = None
        self.last_activity: str = "Started application"
        self.phase_of_work: str = "Active"

    def save_current_state(self, session_code: str, last_activity: str = "") -> bool:
        """
        Save the current application state to a session.

        Args:
            session_code: The session code to save to
            last_activity: Description of the last activity performed

        Returns:
            True if save was successful, False otherwise
        """
        # Validate session code
        is_valid, error_msg = validate_session_code(session_code)
        if not is_valid:
            print(f"Error: {error_msg}")
            return False

        # Create session data from current state
        session_data = SessionData(
            session_code=session_code,
            created_at=datetime.now(),
            last_modified=datetime.now(),
            last_activity=last_activity or self.last_activity,
            phase_of_work=self.phase_of_work,
            next_id=self.next_id,  # Assuming TodoManager has next_id attribute
            tasks=self.tasks[:]     # Copy of current tasks list
        )

        # Save to storage
        success = self.session_storage.save_session(session_data)
        if success:
            self.current_session_code = session_code
            self.last_activity = f"Saved session {session_code}"
            print(f"✅ Session '{session_code}' saved successfully")

        return success

    def load_session_state(self, session_code: str) -> bool:
        """
        Load a saved application state from a session.

        Args:
            session_code: The session code to load

        Returns:
            True if load was successful, False otherwise
        """
        # Load from storage
        session_data = self.session_storage.load_session(session_code)
        if not session_data:
            print(f"❌ Session '{session_code}' not found")
            return False

        # Restore state from session data
        self.tasks = session_data.tasks[:]
        self.next_id = session_data.next_id
        self.current_session_code = session_data.session_code
        self.last_activity = f"Resumed session {session_code}"
        self.phase_of_work = session_data.phase_of_work

        print(f"📂 Resuming session '{session_code}' from {session_data.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Last activity: {session_data.last_activity}")

        return True

    def delete_session(self, session_code: str) -> bool:
        """
        Delete a saved session.

        Args:
            session_code: The session code to delete

        Returns:
            True if deletion was successful, False otherwise
        """
        success = self.session_storage.delete_session(session_code)
        if success:
            print(f"🗑️ Session '{session_code}' deleted successfully")
        else:
            print(f"❌ Could not delete session '{session_code}' - may not exist")

        return success

    def list_sessions(self) -> None:
        """
        List all available sessions.
        """
        sessions = self.session_storage.list_sessions()

        if not sessions:
            print("No saved sessions found")
            return

        print("Available sessions:")
        for session in sessions:
            time_diff = datetime.now() - session.last_modified
            days = time_diff.days
            hours, remainder = divmod(time_diff.seconds, 3600)

            time_ago = ""
            if days > 0:
                time_ago = f"{days} day{'s' if days != 1 else ''} ago"
            elif hours > 0:
                time_ago = f"{hours} hour{'s' if hours != 1 else ''} ago"
            else:
                time_ago = "just now"

            print(f"  {session.session_code} ({time_ago}) - {session.task_count} todos, last: {session.last_activity[:30]}{'...' if len(session.last_activity) > 30 else ''}")

    def session_info(self, session_code: str) -> None:
        """
        Show detailed information about a specific session.

        Args:
            session_code: The session code to get info for
        """
        sessions = [s for s in self.session_storage.list_sessions() if s.session_code == session_code]

        if not sessions:
            print(f"❌ Session '{session_code}' not found")
            return

        session = sessions[0]
        print(f"Session: {session.session_code}")
        print(f"Created: {session.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Modified: {session.last_modified.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Task count: {session.task_count}")
        print(f"Last activity: {session.last_activity}")
        print(f"File: {session.file_path}")
```

## JSON Session File Format

The session files follow this JSON structure:

```json
{
  "session_code": "string",
  "created_at": "2026-01-06T10:30:00",
  "last_modified": "2026-01-06T10:30:00",
  "last_activity": "string",
  "phase_of_work": "string",
  "next_id": 5,
  "tasks": [
    {
      "id": 1,
      "title": "string",
      "description": "string",
      "completed": false,
      "created_at": "2026-01-06T10:25:00"
    }
  ]
}
```

## Validation Rules

1. **Session Code Validation**:
   - Must be alphanumeric only (a-z, A-Z, 0-9)
   - No spaces or special characters allowed
   - Length: 1-50 characters
   - Case-sensitive

2. **Session File Validation**:
   - Must be valid JSON
   - Required fields: session_code, created_at, last_modified, tasks
   - Timestamps must be in ISO 8601 format
   - Task objects must match Task model structure

3. **Session State Validation**:
   - Session code must not already exist when saving (unless overwriting)
   - Session must exist when loading
   - Session file must not be corrupted when loading