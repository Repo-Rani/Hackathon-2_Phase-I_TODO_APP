"""
Business logic for task management in the Todo Console App.

This module handles all operations related to tasks including adding, updating,
deleting, and marking tasks as complete.
"""

from datetime import datetime
from typing import List, Optional
try:
    from .models import Task
    from .storage import JSONStorage, SessionStorage, SessionData, SessionMetadata, validate_session_code
except ImportError:
    from models import Task
    from storage import JSONStorage, SessionStorage, SessionData, SessionMetadata, validate_session_code


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
            - Initializes empty state if file doesn't exist
        """
        self.storage = JSONStorage(storage_path)
        self.session_storage = SessionStorage()
        self.tasks: List[Task] = []
        self.next_id: int = 1
        self.current_session_code: Optional[str] = None
        self.last_activity: str = "Started application"
        self.phase_of_work: str = "Active"
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
            next_id=self.next_id,
            tasks=self.tasks[:]
        )

        # Save to storage
        success = self.session_storage.save_session(session_data)
        if success:
            self.current_session_code = session_code
            self.last_activity = f"Saved session {session_code}"
            print(f"[SUCCESS] Session '{session_code}' saved successfully")

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
            print(f"[ERROR] Session '{session_code}' not found")
            return False

        # Restore state from session data
        self.tasks = session_data.tasks[:]
        self.next_id = session_data.next_id
        self.current_session_code = session_data.session_code
        self.last_activity = f"Resumed session {session_code}"
        self.phase_of_work = session_data.phase_of_work

        print(f"[INFO] Resuming session '{session_code}' from {session_data.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
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
            print(f"[DELETED] Session '{session_code}' deleted successfully")
        else:
            print(f"[ERROR] Could not delete session '{session_code}' - may not exist")

        return success

    def list_sessions(self, show_output: bool = True) -> List[SessionMetadata]:
        """
        List all available sessions.

        Args:
            show_output: Whether to print the list to console (default: True)

        Returns:
            List of SessionMetadata instances for all available sessions
        """
        sessions = self.session_storage.list_sessions()

        if not sessions:
            if show_output:
                print("No saved sessions found")
            return sessions

        if show_output:
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

        return sessions

    def session_info(self, session_code: str) -> None:
        """
        Show detailed information about a specific session.

        Args:
            session_code: The session code to get info for
        """
        sessions = [s for s in self.session_storage.list_sessions() if s.session_code == session_code]

        if not sessions:
            print(f"[ERROR] Session '{session_code}' not found")
            return

        session = sessions[0]
        print(f"Session: {session.session_code}")
        print(f"Created: {session.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Modified: {session.last_modified.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Task count: {session.task_count}")
        print(f"Last activity: {session.last_activity}")
        print(f"File: {session.file_path}")
