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
<<<<<<< HEAD
    from .storage import validate_session_code
=======
>>>>>>> 64c2e05b398b06a7b7369f7b6fd3d597cb1340be
except ImportError:
    from todo_manager import TodoManager
    from ui import (
        show_header, show_menu, show_tasks_table, show_task_details,
        show_success, show_error, show_info, console, show_welcome_animation,
        show_loading, show_confirmation_dialog, show_status_bar
    )
<<<<<<< HEAD
    from storage import validate_session_code
=======
>>>>>>> 64c2e05b398b06a7b7369f7b6fd3d597cb1340be

    


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


<<<<<<< HEAD
def handle_session_command(todo_manager: TodoManager, full_command: str) -> bool:
    """
    Handle session-related commands (stop, start, sessions).

    Args:
        todo_manager: The TodoManager instance to use
        full_command: The full command string from user input

    Returns:
        True if the command was a session command, False otherwise
    """
    parts = full_command.strip().split()
    if not parts:
        return False

    command = parts[0].lower()

    # Handle "stop [session_code]" command
    if command == 'stop':
        if len(parts) < 2:
            show_error("Please provide a session code. Usage: stop [session_code]")
            input("Press Enter to continue...")
            return True

        session_code = parts[1]
        is_valid, error_msg = validate_session_code(session_code)
        if not is_valid:
            show_error(error_msg)
            input("Press Enter to continue...")
            return True

        # Save current state to session
        success = todo_manager.save_current_state(session_code, f"Manual save with 'stop {session_code}' command")
        if success:
            show_success(f"Session '{session_code}' saved successfully")
        else:
            show_error(f"Failed to save session '{session_code}'")

        input("Press Enter to continue...")
        return True

    # Handle "start [session_code]" command
    elif command == 'start':
        if len(parts) < 2:
            show_error("Please provide a session code. Usage: start [session_code]")
            input("Press Enter to continue...")
            return True

        session_code = parts[1]
        is_valid, error_msg = validate_session_code(session_code)
        if not is_valid:
            show_error(error_msg)
            input("Press Enter to continue...")
            return True

        # Load state from session
        success = todo_manager.load_session_state(session_code)
        if success:
            show_success(f"Session '{session_code}' loaded successfully")
        else:
            show_error(f"Failed to load session '{session_code}' - may not exist")

        input("Press Enter to continue...")
        return True

    # Handle "sessions [subcommand]" command
    elif command == 'sessions':
        if len(parts) < 2:
            show_error("Please specify a subcommand. Usage: sessions [list|delete|info]")
            input("Press Enter to continue...")
            return True

        subcommand = parts[1].lower()

        if subcommand == 'list':
            todo_manager.list_sessions()
            input("Press Enter to continue...")
            return True

        elif subcommand == 'delete':
            if len(parts) < 3:
                show_error("Please provide a session code. Usage: sessions delete [session_code]")
                input("Press Enter to continue...")
                return True

            session_code = parts[2]
            is_valid, error_msg = validate_session_code(session_code)
            if not is_valid:
                show_error(error_msg)
                input("Press Enter to continue...")
                return True

            # Use enhanced confirmation dialog
            confirmation = show_confirmation_dialog(f"Are you sure you want to delete session '{session_code}'?")
            if confirmation:
                success = todo_manager.delete_session(session_code)
                if success:
                    show_success(f"Session '{session_code}' deleted successfully")
                else:
                    show_error(f"Failed to delete session '{session_code}'")
            else:
                show_info(f"Deletion cancelled. Session '{session_code}' preserved.")

            input("Press Enter to continue...")
            return True

        elif subcommand == 'info':
            if len(parts) < 3:
                show_error("Please provide a session code. Usage: sessions info [session_code]")
                input("Press Enter to continue...")
                return True

            session_code = parts[2]
            is_valid, error_msg = validate_session_code(session_code)
            if not is_valid:
                show_error(error_msg)
                input("Press Enter to continue...")
                return True

            todo_manager.session_info(session_code)
            input("Press Enter to continue...")
            return True

        else:
            show_error(f"Unknown sessions subcommand: {subcommand}. Use: list, delete, or info")
            input("Press Enter to continue...")
            return True

    return False


def check_existing_sessions(todo_manager: TodoManager) -> None:
    """
    Check if any sessions exist and prompt user to resume or start fresh.

    Args:
        todo_manager: The TodoManager instance to use
    """
    sessions = todo_manager.list_sessions(show_output=False)  # Get sessions without printing

    if sessions:
        console.print("\n[bold yellow]Saved sessions detected:[/bold yellow]")
        for session in sessions:
            time_diff = __import__('datetime').datetime.now() - session.last_modified
            days = time_diff.days
            hours, remainder = divmod(time_diff.seconds, 3600)

            time_ago = ""
            if days > 0:
                time_ago = f"{days} day{'s' if days != 1 else ''} ago"
            elif hours > 0:
                time_ago = f"{hours} hour{'s' if hours != 1 else ''} ago"
            else:
                time_ago = "just now"

            console.print(f"  • {session.session_code} ({time_ago}) - {session.task_count} todos")

        console.print("\n[yellow]Would you like to resume a session or start fresh?[/yellow]")
        choice = input("Enter session code to resume, or 'new' to start fresh: ").strip()

        if choice.lower() != 'new' and choice:
            is_valid, error_msg = validate_session_code(choice)
            if is_valid:
                success = todo_manager.load_session_state(choice)
                if success:
                    show_success(f"Session '{choice}' loaded successfully")
                    input("Press Enter to continue...")
                else:
                    show_error(f"Failed to load session '{choice}' - may not exist")
                    input("Press Enter to continue...")
            else:
                show_error(error_msg)
                input("Press Enter to continue...")


=======
>>>>>>> 64c2e05b398b06a7b7369f7b6fd3d597cb1340be
def main() -> None:
    """Main entry point for the Todo Console App."""
    # Show enhanced welcome animation
    show_welcome_animation()

    # Initialize the todo manager
    todo_manager = TodoManager()

<<<<<<< HEAD
    # Check for existing sessions and prompt user
    check_existing_sessions(todo_manager)

=======
>>>>>>> 64c2e05b398b06a7b7369f7b6fd3d597cb1340be
    while True:
        # Show header and menu with stats
        console.clear()
        show_header()
        stats = todo_manager.get_stats()
        show_menu(stats)

<<<<<<< HEAD
        # Get user input - could be menu choice or session command
        try:
            user_input = input("\nEnter your choice (1-6) or session command (stop/start/sessions): ").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n\nGoodbye!")
            sys.exit(0)

        # Handle session commands first
        if handle_session_command(todo_manager, user_input):
            continue  # Skip menu processing if it was a session command

        # Handle traditional menu choices
        if user_input == '1':
            handle_add_task(todo_manager)
        elif user_input == '2':
            handle_view_tasks(todo_manager)
        elif user_input == '3':
            handle_update_task(todo_manager)
        elif user_input == '4':
            handle_delete_task(todo_manager)
        elif user_input == '5':
            handle_mark_complete(todo_manager)
        elif user_input == '6':
=======
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
>>>>>>> 64c2e05b398b06a7b7369f7b6fd3d597cb1340be
            console.clear()
            show_header()
            show_success("Thank you for using the Todo Console App!")
            console.print("[dim]Goodbye! ✨[/dim]\n")
            break
        else:
<<<<<<< HEAD
            show_error(f"Invalid choice: '{user_input}'. Please enter a number between 1-6 or use session commands (stop/start/sessions).")
=======
            show_error(f"Invalid choice: '{choice}'. Please enter a number between 1-6.")
>>>>>>> 64c2e05b398b06a7b7369f7b6fd3d597cb1340be
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()
