"""
Unit tests for data models in the Todo Console App.
"""

import pytest
from datetime import datetime
from src.models import Task


class TestTask:
    """Test cases for the Task model."""

    def test_task_creation_valid(self):
        """Test creating a valid task."""
        task = Task(
            id=1,
            title="Test Task",
            description="This is a test task",
            completed=False,
            created_at=datetime.now()
        )

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "This is a test task"
        assert task.completed is False

    def test_task_title_validation_empty(self):
        """Test that creating a task with an empty title raises ValueError."""
        with pytest.raises(ValueError, match="Task title must contain non-whitespace content"):
            Task(
                id=1,
                title="",
                description="",
                completed=False,
                created_at=datetime.now()
            )

    def test_task_title_validation_whitespace_only(self):
        """Test that creating a task with only whitespace in title raises ValueError."""
        with pytest.raises(ValueError, match="Task title must contain non-whitespace content"):
            Task(
                id=1,
                title="   ",
                description="",
                completed=False,
                created_at=datetime.now()
            )

    def test_task_title_validation_too_long(self):
        """Test that creating a task with a title longer than 200 characters raises ValueError."""
        long_title = "A" * 201
        with pytest.raises(ValueError, match="Task title must be between 1 and 200 characters"):
            Task(
                id=1,
                title=long_title,
                description="",
                completed=False,
                created_at=datetime.now()
            )

    def test_task_title_validation_too_short(self):
        """Test that creating a task with an empty title raises ValueError."""
        with pytest.raises(ValueError, match="Task title must contain non-whitespace content"):
            Task(
                id=1,
                title="",
                description="",
                completed=False,
                created_at=datetime.now()
            )

    def test_task_description_validation_too_long(self):
        """Test that creating a task with a description longer than 1000 characters raises ValueError."""
        long_description = "A" * 1001
        with pytest.raises(ValueError, match="Task description must be under 1000 characters"):
            Task(
                id=1,
                title="Test Task",
                description=long_description,
                completed=False,
                created_at=datetime.now()
            )

    def test_task_title_standard_characters(self):
        """Test that creating a task with invalid characters in title raises ValueError."""
        with pytest.raises(ValueError, match="Text contains invalid characters"):
            Task(
                id=1,
                title="Test\x00Task",  # Null character should be invalid
                description="",
                completed=False,
                created_at=datetime.now()
            )

    def test_task_description_standard_characters(self):
        """Test that creating a task with invalid characters in description raises ValueError."""
        with pytest.raises(ValueError, match="Text contains invalid characters"):
            Task(
                id=1,
                title="Test Task",
                description="Test\x00Description",  # Null character should be invalid
                completed=False,
                created_at=datetime.now()
            )

    def test_task_title_valid_characters(self):
        """Test that creating a task with valid characters works correctly."""
        valid_title = "Test Task with valid chars: .,!?;:\"'[](){}-_+=<>/@#$%^&*|~`"
        task = Task(
            id=1,
            title=valid_title,
            description="",
            completed=False,
            created_at=datetime.now()
        )
        assert task.title == valid_title

    def test_task_description_valid_characters(self):
        """Test that creating a task with valid characters in description works correctly."""
        valid_description = "Test Description with valid chars: .,!?;:\"'[](){}-_+=<>/@#$%^&*|~`"
        task = Task(
            id=1,
            title="Test Task",
            description=valid_description,
            completed=False,
            created_at=datetime.now()
        )
        assert task.description == valid_description