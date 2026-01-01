"""
JSON storage handler for task persistence.

This module provides the JSONStorage class for saving and loading tasks
to/from JSON files with backup and error handling.
"""

import json
import shutil
from pathlib import Path
from typing import Dict, Any, List


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
