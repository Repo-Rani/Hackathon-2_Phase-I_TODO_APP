"""
Integration tests for CLI interface in the Todo Console App.
"""

import io
import sys
from unittest.mock import patch, MagicMock
from src.main import (
    display_menu, get_user_choice, handle_add_task, handle_view_tasks,
    handle_update_task, handle_delete_task, handle_mark_complete, main
)
from src.todo_manager import TodoManager


class TestMainMenu:
    """Integration tests for the main CLI interface."""

    def test_display_menu(self):
        """Test that the menu displays correctly."""
        # Capture printed output
        captured_output = io.StringIO()
        sys.stdout = captured_output

        display_menu()

        # Restore stdout
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()
        assert "TODO CONSOLE APP" in output
        assert "1. Add Task" in output
        assert "2. View All Tasks" in output
        assert "3. Update Task" in output
        assert "4. Delete Task" in output
        assert "5. Mark Complete/Incomplete" in output
        assert "6. Exit" in output

    def test_get_user_choice_valid(self):
        """Test getting a valid user choice."""
        with patch('builtins.input', return_value='1'):
            choice = get_user_choice()
            assert choice == '1'

    def test_get_user_choice_with_whitespace(self):
        """Test getting a user choice with leading/trailing whitespace."""
        with patch('builtins.input', return_value=' 2 '):
            choice = get_user_choice()
            assert choice == '2'

    def test_handle_add_task_basic(self):
        """Test the add task functionality."""
        todo_manager = TodoManager()

        # Simulate user input
        inputs = ['Test Task Title', 'Test Description']
        input_iter = iter(inputs)

        def mock_input(prompt):
            return next(input_iter)

        with patch('builtins.input', side_effect=mock_input):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                handle_add_task(todo_manager)

        # Verify task was added
        tasks = todo_manager.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].title == "Test Task Title"
        assert tasks[0].description == "Test Description"
        assert tasks[0].completed is False

    def test_handle_add_task_no_description(self):
        """Test adding a task without description."""
        todo_manager = TodoManager()

        # Simulate user input (empty string for description)
        inputs = ['Test Task Title', '']
        input_iter = iter(inputs)

        def mock_input(prompt):
            return next(input_iter)

        with patch('builtins.input', side_effect=mock_input):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                handle_add_task(todo_manager)

        # Verify task was added
        tasks = todo_manager.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].title == "Test Task Title"
        assert tasks[0].description == ""

    def test_handle_add_task_cancel(self):
        """Test cancelling task creation."""
        todo_manager = TodoManager()

        # Simulate user cancelling
        with patch('builtins.input', return_value='cancel'):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                handle_add_task(todo_manager)

        # Verify no task was added
        tasks = todo_manager.get_all_tasks()
        assert len(tasks) == 0

    def test_handle_view_tasks_empty(self):
        """Test viewing tasks when the list is empty."""
        todo_manager = TodoManager()

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            handle_view_tasks(todo_manager)
            output = fake_out.getvalue()

        assert "No tasks yet! Add your first task to get started." in output

    def test_handle_view_tasks_with_tasks(self):
        """Test viewing tasks when the list has tasks."""
        todo_manager = TodoManager()
        todo_manager.add_task("Task 1", "Description 1")
        todo_manager.add_task("Task 2", "Description 2")

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            handle_view_tasks(todo_manager)
            output = fake_out.getvalue()

        assert "Task 1" in output
        assert "Task 2" in output
        assert "Description 1" in output
        assert "Description 2" in output

    def test_handle_mark_complete_toggle(self):
        """Test marking a task as complete/incomplete."""
        todo_manager = TodoManager()
        task = todo_manager.add_task("Test Task")

        # Initially, task should be incomplete
        assert task.completed is False

        # Simulate user selecting the task
        inputs = [str(task.id)]
        input_iter = iter(inputs)

        def mock_input(prompt):
            return next(input_iter)

        with patch('builtins.input', side_effect=mock_input):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                handle_mark_complete(todo_manager)

        # Verify the task was marked as complete
        updated_task = todo_manager.get_task_by_id(task.id)
        assert updated_task.completed is True

    def test_handle_delete_task(self):
        """Test deleting a task."""
        todo_manager = TodoManager()
        task = todo_manager.add_task("Test Task to Delete")

        # Simulate user confirming deletion
        inputs = [str(task.id), 'yes']
        input_iter = iter(inputs)

        def mock_input(prompt):
            if 'Are you sure' in prompt:
                return next(input_iter)
            else:
                return next(input_iter)

        # Need to handle both the ID input and confirmation separately
        with patch('builtins.input', side_effect=['1', 'yes']):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                handle_delete_task(todo_manager)

        # Verify the task was deleted
        remaining_tasks = todo_manager.get_all_tasks()
        assert len(remaining_tasks) == 0

    def test_handle_update_task(self):
        """Test updating a task."""
        todo_manager = TodoManager()
        task = todo_manager.add_task("Original Title", "Original Description")

        # Simulate user inputs: task ID, update choice (title), new title
        inputs = [str(task.id), 't', 'Updated Title', '']
        input_iter = iter(inputs)

        def mock_input(prompt):
            try:
                return next(input_iter)
            except StopIteration:
                return ''  # Return empty for any remaining prompts

        with patch('builtins.input', side_effect=mock_input):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                handle_update_task(todo_manager)

        # Verify the task was updated
        updated_task = todo_manager.get_task_by_id(task.id)
        assert updated_task.title == "Updated Title"
        assert updated_task.description == "Original Description"  # Should remain unchanged


class TestIntegrationScenarios:
    """End-to-end integration tests."""

    def test_complete_workflow(self):
        """Test a complete workflow: add, view, update, mark complete, delete."""
        todo_manager = TodoManager()

        # Add a task
        inputs_add = ['My Task', 'Task description']
        input_iter = iter(inputs_add)

        def mock_input_add(prompt):
            return next(input_iter)

        with patch('builtins.input', side_effect=mock_input_add):
            with patch('sys.stdout', new=io.StringIO()):
                handle_add_task(todo_manager)

        # Verify task was added
        tasks = todo_manager.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].title == "My Task"
        assert tasks[0].description == "Task description"
        assert tasks[0].completed is False

        # Mark as complete
        with patch('builtins.input', return_value='1'):
            with patch('sys.stdout', new=io.StringIO()):
                handle_mark_complete(todo_manager)

        # Verify task was marked complete
        updated_task = todo_manager.get_task_by_id(1)
        assert updated_task.completed is True

        # Delete the task
        with patch('builtins.input', side_effect=['1', 'yes']):
            with patch('sys.stdout', new=io.StringIO()):
                handle_delete_task(todo_manager)

        # Verify task was deleted
        final_tasks = todo_manager.get_all_tasks()
        assert len(final_tasks) == 0