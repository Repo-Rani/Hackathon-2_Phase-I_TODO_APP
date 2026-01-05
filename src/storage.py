"""
<<<<<<< HEAD
JSON storage handler for task persistence and session management.

This module provides the JSONStorage class for saving and loading tasks
to/from JSON files with backup and error handling, and the SessionStorage
class for managing session state.
=======
JSON storage handler for task persistence.

This module provides the JSONStorage class for saving and loading tasks
to/from JSON files with backup and error handling.
>>>>>>> 64c2e05b398b06a7b7369f7b6fd3d597cb1340be
"""

import json
import shutil
<<<<<<< HEAD
import tempfile
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import os
=======
from pathlib import Path
from typing import Dict, Any, List
>>>>>>> 64c2e05b398b06a7b7369f7b6fd3d597cb1340be


class JSONStorage:
    """Handles file I/O operations for task persistence."""

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

    def save(self, tasks: List, next_id: int) -> bool:
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

            # Import Task here to avoid circular dependency
            from models import Task

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
<<<<<<< HEAD


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


class SessionData:
    """
    Represents the complete state of a session that can be saved and restored.

    This class contains all the information needed to save and restore
    the complete application state for a given session.
    """
    def __init__(self, session_code: str, created_at: datetime, last_modified: datetime,
                 last_activity: str, phase_of_work: str, next_id: int, tasks: List):
        self.session_code = session_code
        self.created_at = created_at
        self.last_modified = last_modified
        self.last_activity = last_activity
        self.phase_of_work = phase_of_work
        self.next_id = next_id
        self.tasks = tasks

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
        from models import Task

        return cls(
            session_code=data["session_code"],
            created_at=datetime.fromisoformat(data["created_at"]),
            last_modified=datetime.fromisoformat(data["last_modified"]),
            last_activity=data["last_activity"],
            phase_of_work=data["phase_of_work"],
            next_id=data["next_id"],
            tasks=[Task.from_dict(task_data) for task_data in data["tasks"]]
        )


class SessionMetadata:
    """
    Represents metadata about a saved session without loading full content.

    Used for session listing and information display.
    """
    def __init__(self, session_code: str, created_at: datetime, last_modified: datetime,
                 last_activity: str, task_count: int, file_path: str):
        self.session_code = session_code
        self.created_at = created_at
        self.last_modified = last_modified
        self.last_activity = last_activity
        self.task_count = task_count
        self.file_path = file_path

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
=======
>>>>>>> 64c2e05b398b06a7b7369f7b6fd3d597cb1340be
