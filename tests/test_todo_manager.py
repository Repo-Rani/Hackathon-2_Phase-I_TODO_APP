"""
Unit tests for todo manager in the Todo Console App.
"""

import pytest
from datetime import datetime
from src.todo_manager import TodoManager
from src.models import Task


class TestTodoManager:
    """Test cases for the TodoManager class."""

    def test_add_task_basic(self):
        """Test adding a basic task."""
        tm = TodoManager()
        task = tm.add_task("Test Task", "Test Description")

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.completed is False
        assert isinstance(task.created_at, datetime)

        # Verify the task was added to the list
        tasks = tm.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].id == 1

    def test_add_task_no_description(self):
        """Test adding a task without a description."""
        tm = TodoManager()
        task = tm.add_task("Test Task")

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == ""
        assert task.completed is False

    def test_add_multiple_tasks_sequential_ids(self):
        """Test that multiple tasks get sequential IDs."""
        tm = TodoManager()
        task1 = tm.add_task("Task 1")
        task2 = tm.add_task("Task 2")
        task3 = tm.add_task("Task 3")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_get_all_tasks(self):
        """Test getting all tasks."""
        tm = TodoManager()
        tm.add_task("Task 1")
        tm.add_task("Task 2")

        tasks = tm.get_all_tasks()
        assert len(tasks) == 2
        assert tasks[0].id == 1
        assert tasks[1].id == 2

    def test_get_task_by_id_found(self):
        """Test getting a task by ID that exists."""
        tm = TodoManager()
        tm.add_task("Test Task")
        task2 = tm.add_task("Task 2")

        found_task = tm.get_task_by_id(2)
        assert found_task is not None
        assert found_task.id == 2
        assert found_task.title == "Task 2"

    def test_get_task_by_id_not_found(self):
        """Test getting a task by ID that doesn't exist."""
        tm = TodoManager()
        tm.add_task("Test Task")

        found_task = tm.get_task_by_id(99)
        assert found_task is None

    def test_update_task_title(self):
        """Test updating a task's title."""
        tm = TodoManager()
        tm.add_task("Original Title", "Original Description")

        success = tm.update_task(1, "New Title")
        assert success is True

        updated_task = tm.get_task_by_id(1)
        assert updated_task.title == "New Title"
        assert updated_task.description == "Original Description"  # Should remain unchanged

    def test_update_task_description(self):
        """Test updating a task's description."""
        tm = TodoManager()
        tm.add_task("Original Title", "Original Description")

        success = tm.update_task(1, description="New Description")
        assert success is True

        updated_task = tm.get_task_by_id(1)
        assert updated_task.title == "Original Title"  # Should remain unchanged
        assert updated_task.description == "New Description"

    def test_update_task_both(self):
        """Test updating both title and description."""
        tm = TodoManager()
        tm.add_task("Original Title", "Original Description")

        success = tm.update_task(1, "New Title", "New Description")
        assert success is True

        updated_task = tm.get_task_by_id(1)
        assert updated_task.title == "New Title"
        assert updated_task.description == "New Description"

    def test_update_task_not_found(self):
        """Test updating a task that doesn't exist."""
        tm = TodoManager()
        tm.add_task("Test Task")

        success = tm.update_task(99, "New Title")
        assert success is False

    def test_delete_task_exists(self):
        """Test deleting a task that exists."""
        tm = TodoManager()
        tm.add_task("Task 1")
        tm.add_task("Task 2")

        success = tm.delete_task(1)
        assert success is True

        tasks = tm.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].id == 2

    def test_delete_task_not_exists(self):
        """Test deleting a task that doesn't exist."""
        tm = TodoManager()
        tm.add_task("Test Task")

        success = tm.delete_task(99)
        assert success is False

        tasks = tm.get_all_tasks()
        assert len(tasks) == 1

    def test_toggle_complete(self):
        """Test toggling a task's completion status."""
        tm = TodoManager()
        tm.add_task("Test Task")

        # Initially incomplete
        task = tm.get_task_by_id(1)
        assert task.completed is False

        # Toggle to complete
        success = tm.toggle_complete(1)
        assert success is True

        task = tm.get_task_by_id(1)
        assert task.completed is True

        # Toggle back to incomplete
        success = tm.toggle_complete(1)
        assert success is True

        task = tm.get_task_by_id(1)
        assert task.completed is False

    def test_toggle_complete_not_exists(self):
        """Test toggling completion status for a task that doesn't exist."""
        tm = TodoManager()
        tm.add_task("Test Task")

        success = tm.toggle_complete(99)
        assert success is False

    def test_add_task_validation_title_empty(self):
        """Test that adding a task with an empty title raises an error."""
        tm = TodoManager()
        with pytest.raises(ValueError):
            tm.add_task("")

    def test_add_task_validation_title_whitespace_only(self):
        """Test that adding a task with only whitespace in title raises an error."""
        tm = TodoManager()
        with pytest.raises(ValueError):
            tm.add_task("   ")

    def test_add_task_validation_title_too_long(self):
        """Test that adding a task with a title longer than 200 chars raises an error."""
        tm = TodoManager()
        with pytest.raises(ValueError):
            tm.add_task("A" * 201)

    def test_add_task_validation_description_too_long(self):
        """Test that adding a task with a description longer than 1000 chars raises an error."""
        tm = TodoManager()
        with pytest.raises(ValueError):
            tm.add_task("Test Title", "A" * 1001)

    def test_sanitize_input(self):
        """Test input sanitization."""
        tm = TodoManager()
        result = tm.sanitize_input("Test Input")
        assert result == "Test Input"