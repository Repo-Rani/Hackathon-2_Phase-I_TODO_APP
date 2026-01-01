"""
Data models for the Todo Console App.

This module defines the core data structures used in the application.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass
class Task:
    """
    Represents a single todo item with id, title, description, completion status, and creation timestamp.

    Attributes:
        id: unique identifier (integer, sequential)
        title: required text (1-200 characters)
        description: optional text (0-1000 characters)
        completed: boolean status (default: false)
        created_at: timestamp of when task was created
    """
    id: int
    title: str
    description: str
    completed: bool
    created_at: datetime

    def __post_init__(self):
        """Validate task attributes after initialization."""
        # Validate title is not empty and has non-whitespace content
        if not self.title or not self.title.strip():
            raise ValueError("Task title must contain non-whitespace content")

        # Validate title length (1-200 characters)
        if len(self.title) < 1 or len(self.title) > 200:
            raise ValueError("Task title must be between 1 and 200 characters")

        # Validate description length (0-1000 characters)
        if len(self.description) > 1000:
            raise ValueError("Task description must be under 1000 characters")

        # Validate standard characters in title and description
        self._validate_standard_characters(self.title)
        self._validate_standard_characters(self.description)

    def _validate_standard_characters(self, text: str) -> None:
        """Validate that text contains only standard characters (alphanumeric + common punctuation)."""
        import re
        # Check for any character that is not alphanumeric or common punctuation
        if text and not re.match(r'^[a-zA-Z0-9\s\.,!?:;"\'\[\](){}\-_+=<>/@#$%^&*|~`]+$', text):
            raise ValueError(f"Text contains invalid characters: {text}")
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert task to dictionary for JSON serialization.

        Returns:
            Dictionary with keys: id, title, description, completed, created_at
            created_at is serialized as ISO 8601 string
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
        """
        return cls(
            id=data["id"],
            title=data["title"],
            description=data["description"],
            completed=data["completed"],
            created_at=datetime.fromisoformat(data["created_at"])
        )
