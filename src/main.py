"""
CLI entry point and menu interface for the Todo Console App.
Enhanced with Rich UI for beautiful terminal output.
"""

import sys
from typing import Optional
try:
    from .todo_manager import TodoManager
    from .ui import (
        show_header, show_menu, show_tasks_table, show_task_details,
        show_success, show_error, show_info, console, show_welcome_animation,
        show_loading, show_confirmation_dialog, show_status_bar
    )
except ImportError:
    from todo_manager import TodoManager
    from ui import (
        show_header, show_menu, show_tasks_table, show_task_details,
        show_success, show_error, show_info, console, show_welcome_animation,
        show_loading, show_confirmation_dialog, show_status_bar
    )

    


def get_user_choice() -> str:
    """
    Get the user's menu choice.

    Returns:
        str: The user's menu selection
    """
    try:
        choice = input("\nEnter your choice (1-6): ").strip()
        return choice
    except (EOFError, KeyboardInterrupt):
        console.print("\n\nGoodbye!")
        sys.exit(0)


def handle_add_task(todo_manager: TodoManager) -> None:
    """
    Handle the add task functionality.

    Args:
        todo_manager: The TodoManager instance to use
    """
    console.print("\n[bold cyan]--- Add New Task ---[/bold cyan]")

    while True:
        title = input("\nEnter task title (or 'cancel' to return to menu): ").strip()

        if title.lower() == 'cancel':
            show_info("Task creation cancelled.")
            return

        if not title:
            show_error("Title cannot be empty. Please enter a valid title.")
            continue

        if len(title) > 200:
            show_error("Title must be under 200 characters. Please enter a shorter title.")
            continue

        # Check for non-whitespace content
        if not title.strip():
            show_error("Title must contain non-whitespace content. Please enter a valid title.")
            continue

        break

    description = input("Enter task description (optional, press Enter to skip): ").strip()

    # Check if description is too long
    if len(description) > 1000:
        show_error("Description must be under 1000 characters.")
        return

    try:
        # Sanitize inputs
        sanitized_title = todo_manager.sanitize_input(title)
        sanitized_description = todo_manager.sanitize_input(description)

        # Add the task
        task = todo_manager.add_task(sanitized_title, sanitized_description)

        show_success(f"Task #{task.id} created successfully!")
        show_task_details(task)

    except ValueError as e:
        show_error(str(e))
        console.print("[yellow]Task creation failed. Please try again.[/yellow]")


def handle_view_tasks(todo_manager: TodoManager) -> None:
    """
    Handle the view tasks functionality.

    Args:
        todo_manager: The TodoManager instance to use
    """
    tasks = todo_manager.get_all_tasks()

    console.print()
    show_tasks_table(tasks)
    console.print()

    input("\nPress Enter to continue...")


def handle_update_task(todo_manager: TodoManager) -> None:
    """
    Handle the update task functionality.

    Args:
        todo_manager: The TodoManager instance to use
    """
    tasks = todo_manager.get_all_tasks()

    if not tasks:
        show_info("No tasks available to update. Add a task first.")
        input("Press Enter to continue...")
        return

    console.print("\n[bold cyan]--- Your Tasks ---[/bold cyan]")
    for task in tasks:
        status = "[✓]" if task.completed else "[ ]"
        console.print(f"#{task.id} - {status} {task.title}")

    try:
        task_id_input = input("\nEnter task ID to update (or 'cancel' to return): ").strip()

        if task_id_input.lower() == 'cancel':
            show_info("Update cancelled.")
            return

        task_id = int(task_id_input)

        # Find the task
        task = todo_manager.get_task_by_id(task_id)
        if task is None:
            show_error(f"Task #{task_id} not found.")
            input("Press Enter to continue...")
            return

        console.print("\n[bold]Current task:[/bold]")
        show_task_details(task)

        choice_prompt = "\nUpdate [T]itle, [D]escription, or [B]oth? (or 'cancel' to return): "
        update_choice = input(choice_prompt).strip().lower()

        if update_choice == 'cancel':
            show_info("Update cancelled.")
            return

        new_title = None
        new_description = None

        if update_choice in ['t', 'b']:
            new_title = input(f"Enter new title (or press Enter to keep '{task.title}'): ").strip()
            if not new_title:
                new_title = task.title

        if update_choice in ['d', 'b']:
            new_description = input(f"Enter new description (or press Enter to keep current): ").strip()
            if not new_description:
                new_description = task.description

        # Update the task
        success = todo_manager.update_task(task_id, new_title, new_description)

        if success:
            show_success(f"Task #{task_id} updated successfully!")

            # Show before/after comparison
            updated_task = todo_manager.get_task_by_id(task_id)
            if updated_task:
                console.print("\n[bold]AFTER:[/bold]")
                show_task_details(updated_task)
        else:
            show_error(f"Failed to update task #{task_id}")

    except ValueError:
        show_error("Please enter a valid task ID (number).")

    input("\nPress Enter to continue...")


def handle_delete_task(todo_manager: TodoManager) -> None:
    """
    Handle the delete task functionality.

    Args:
        todo_manager: The TodoManager instance to use
    """
    tasks = todo_manager.get_all_tasks()

    if not tasks:
        show_info("No tasks available to delete.")
        input("Press Enter to continue...")
        return

    console.print("\n[bold cyan]--- Your Tasks ---[/bold cyan]")
    for task in tasks:
        status = "[✓]" if task.completed else "[ ]"
        console.print(f"#{task.id} - {status} {task.title}")

    try:
        task_id_input = input("\nEnter task ID to delete (or 'cancel' to return): ").strip()

        if task_id_input.lower() == 'cancel':
            show_info("Deletion cancelled.")
            return

        task_id = int(task_id_input)

        # Find the task
        task = todo_manager.get_task_by_id(task_id)
        if task is None:
            show_error(f"Task #{task_id} not found.")
            input("Press Enter to continue...")
            return

        console.print("\n[bold]Task to delete:[/bold]")
        show_task_details(task)

        # Use enhanced confirmation dialog
        confirmation = show_confirmation_dialog(f"Are you sure you want to delete task #{task.id} - '{task.title}'?")

        if confirmation:
            success = todo_manager.delete_task(task_id)

            if success:
                show_success(f"Task #{task_id} deleted successfully!")
            else:
                show_error(f"Failed to delete task #{task_id}")
        else:
            show_info(f"Deletion cancelled. Task #{task_id} preserved.")

    except ValueError:
        show_error("Please enter a valid task ID (number).")

    input("\nPress Enter to continue...")


def handle_mark_complete(todo_manager: TodoManager) -> None:
    """
    Handle the mark complete/incomplete functionality.

    Args:
        todo_manager: The TodoManager instance to use
    """
    tasks = todo_manager.get_all_tasks()

    if not tasks:
        show_info("No tasks available to mark.")
        input("Press Enter to continue...")
        return

    console.print("\n[bold cyan]--- Your Tasks ---[/bold cyan]")
    for task in tasks:
        status = "[✓]" if task.completed else "[ ]"
        console.print(f"#{task.id} - {status} {task.title}")

    try:
        task_id_input = input("\nEnter task ID to mark complete/incomplete (or 'cancel' to return): ").strip()

        if task_id_input.lower() == 'cancel':
            show_info("Operation cancelled.")
            return

        task_id = int(task_id_input)

        # Find the task
        task = todo_manager.get_task_by_id(task_id)
        if task is None:
            show_error(f"Task #{task_id} not found.")
            input("Press Enter to continue...")
            return

        console.print(f"\n[bold]Task #{task.id} - {task.title}[/bold]")

        # Get current status
        old_status = "Completed" if task.completed else "Pending"
        new_status = "Pending" if task.completed else "Completed"

        # Toggle the status
        success = todo_manager.toggle_complete(task_id)

        if success:
            updated_task = todo_manager.get_task_by_id(task_id)
            if updated_task:
                new_status_indicator = "Completed" if updated_task.completed else "Pending"
                console.print(f"\n[bold]Status changed:[/bold] [{old_status}] → [{new_status_indicator}]")
                show_success(f"Task marked as {new_status_indicator.lower()}!")
                show_task_details(updated_task)
        else:
            show_error(f"Failed to toggle task #{task_id}")

    except ValueError:
        show_error("Please enter a valid task ID (number).")

    input("\nPress Enter to continue...")


def main() -> None:
    """Main entry point for the Todo Console App."""
    # Show enhanced welcome animation
    show_welcome_animation()

    # Initialize the todo manager
    todo_manager = TodoManager()

    while True:
        # Show header and menu with stats
        console.clear()
        show_header()
        stats = todo_manager.get_stats()
        show_menu(stats)

        choice = get_user_choice()

        if choice == '1':
            handle_add_task(todo_manager)
        elif choice == '2':
            handle_view_tasks(todo_manager)
        elif choice == '3':
            handle_update_task(todo_manager)
        elif choice == '4':
            handle_delete_task(todo_manager)
        elif choice == '5':
            handle_mark_complete(todo_manager)
        elif choice == '6':
            console.clear()
            show_header()
            show_success("Thank you for using the Todo Console App!")
            console.print("[dim]Goodbye! ✨[/dim]\n")
            break
        else:
            show_error(f"Invalid choice: '{choice}'. Please enter a number between 1-6.")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()
