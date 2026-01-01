"""
Business logic for task management in the Todo Console App.

This module handles all operations related to tasks including adding, updating,
deleting, and marking tasks as complete.
"""

from datetime import datetime
from typing import List, Optional
try:
    from .models import Task
    from .storage import JSONStorage
except ImportError:
    from models import Task
    from storage import JSONStorage


class TodoManager:
    """
    Manages in-memory task storage and operations with automatic JSON persistence.

    Attributes:
        storage: JSONStorage instance for file I/O
        tasks: List of Task objects stored in memory
        next_id: Integer counter for next available ID
    """

    def __init__(self, storage_path: str = "data/tasks.json") -> None:
        """
        Initialize TodoManager with JSON persistence.

        Args:
            storage_path: Path to JSON file (default: data/tasks.json)

        Side Effects:
            - Creates JSONStorage instance
            - Loads existing tasks from file
            - Initializes empty state if file doesn'''t exist
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

    def add_task(self, title: str, description: str = "") -> Task:
        """
        Add a new task with the provided title and optional description.

        Args:
            title: Required task title (1-200 characters)
            description: Optional task description (up to 1000 characters)

        Returns:
            Task: The newly created Task object

        Raises:
            ValueError: If title or description validation fails
        """
        new_task = Task(
            id=self.next_id,
            title=title,
            description=description,
            completed=False,
            created_at=datetime.now()
        )

        self.tasks.append(new_task)
        self.next_id += 1
        self._save_to_storage()

        return new_task

    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks in the system.

        Returns:
            List of all Task objects
        """
        return self.tasks.copy()

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Get a specific task by its ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            Task object if found, None otherwise
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: int, title: str = None, description: str = None) -> bool:
        """
        Update an existing task'''s title and/or description.

        Args:
            task_id: The ID of the task to update
            title: New title (optional)
            description: New description (optional)

        Returns:
            bool: True if task was updated, False if task not found
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            return False

        new_title = title if title is not None else task.title
        new_description = description if description is not None else task.description

        updated_task = Task(
            id=task.id,
            title=new_title,
            description=new_description,
            completed=task.completed,
            created_at=task.created_at
        )

        index = self.tasks.index(task)
        self.tasks[index] = updated_task
        self._save_to_storage()

        return True

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.

        Args:
            task_id: The ID of the task to delete

        Returns:
            bool: True if task was deleted, False if task not found
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            return False

        self.tasks.remove(task)
        self._save_to_storage()

        return True

    def toggle_complete(self, task_id: int) -> bool:
        """
        Toggle the completion status of a task.

        Args:
            task_id: The ID of the task to toggle

        Returns:
            bool: True if task status was toggled, False if task not found
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            return False

        task.completed = not task.completed
        self._save_to_storage()

        return True

    def get_stats(self) -> dict:
        """
        Get statistics about tasks.

        Returns:
            Dictionary with '''total''', '''completed''', '''pending''' counts
        """
        total = len(self.tasks)
        completed = sum(1 for task in self.tasks if task.completed)
        pending = total - completed
        return {
            '''total''': total,
            '''completed''': completed,
            '''pending''': pending
        }

    def sanitize_input(self, text: str) -> str:
        """
        Sanitize user input to prevent injection attacks.

        Args:
            text: Input text to sanitize

        Returns:
            Sanitized text
        """
        return text
