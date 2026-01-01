"""
Rich UI components for beautiful console display.
Enhanced with professional styling, animations, and modern terminal aesthetics.
"""

from typing import List
import time
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
from rich.layout import Layout
from rich.live import Live
from rich.spinner import Spinner
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.align import Align
from rich.box import ROUNDED, HEAVY_HEAD, DOUBLE, MINIMAL
import pyfiglet
import colorama
from emoji import emojize

try:
    from .colors import THEME, BOX_STYLES, EMOJIS
except ImportError:
    from colors import THEME, BOX_STYLES, EMOJIS

# Initialize colorama for cross-platform color support
colorama.init()

# Singleton console instance for consistent output across the application
console = Console()

# Enhanced spinner for loading states
def show_loading(message: str = "Processing...", duration: float = 0.5) -> None:
    """
    Display a loading spinner with message.

    Args:
        message: Loading message to display
        duration: How long to show the spinner (default 0.5s)
    """
    with console.screen():
        spinner = Spinner("clock", style=THEME['accent'])
        panel = Panel(
            Align.center(spinner, vertical="middle"),
            title=f"[{THEME['accent']}]{message}[/{THEME['accent']}]",
            border_style=THEME['panel_border'],
            box=box.ROUNDED,
            padding=(1, 2)
        )
        console.print(panel)
        time.sleep(duration)

def animate_text(text: str, delay: float = 0.05) -> None:
    """
    Display text with typing animation effect.

    Args:
        text: Text to animate
        delay: Delay between characters (default 0.05s)
    """
    for char in text:
        console.print(char, end="", style=THEME['primary'])
        time.sleep(delay)
    console.print()  # New line after animation

def show_welcome_animation() -> None:
    """Display a welcome animation with ASCII art header."""
    # Create ASCII art header
    ascii_art = pyfiglet.figlet_format("TODO APP", font="slant")
    ascii_text = Text(ascii_art, style=f"bold {THEME['primary']}")

    # Create welcome panel
    welcome_panel = Panel(
        Align.center(ascii_text),
        border_style=THEME['panel_border'],
        box=box.DOUBLE,
        padding=(1, 2),
        expand=False
    )

    # Create welcome message panel
    welcome_msg = Panel(
        f"[{THEME['accent']}]{EMOJIS['app']} Welcome to  Todo Console App!{EMOJIS['app']}[/]",
        border_style=THEME['accent'],
        box=box.ROUNDED,
        padding=(1, 2)
    )

    # Show the animation
    console.clear()
    console.print(welcome_panel)
    console.print()
    console.print(Align.center(welcome_msg))
    time.sleep(1.5)

def show_header() -> None:
    """Display enhanced app header with ASCII art and styling."""
    # Create ASCII art header
    ascii_art = pyfiglet.figlet_format("TODO", font="small")
    ascii_text = Text(ascii_art, style=f"bold {THEME['primary']}")

    # Create header with gradient effect
    header_text = Text()
    header_text.append(f"  {EMOJIS['app']} TODO CONSOLE APP ", style=f"bold {THEME['primary']}")
    header_text.append(f"{EMOJIS['success']}", style=THEME['accent'])

    # Create enhanced header panel
    panel = Panel(
        Align.center(header_text),
        border_style=THEME['panel_border'],
        box=BOX_STYLES['header'],
        padding=(1, 2),
        expand=False
    )
    console.print(panel)

def show_menu(stats: dict) -> None:
    """
    Display enhanced main menu with task stats and beautiful styling.

    Args:
        stats: Dictionary with 'total', 'completed', 'pending' counts
    """
    # Create menu items with enhanced styling
    menu_items = [
        f"[{THEME['menu_number']}]1.[/{THEME['menu_number']}] {EMOJIS['add']} Add Task",
        f"[{THEME['menu_number']}]2.[/{THEME['menu_number']}] {EMOJIS['task']} View All Tasks",
        f"[{THEME['menu_number']}]3.[/{THEME['menu_number']}] {EMOJIS['edit']} Update Task",
        f"[{THEME['menu_number']}]4.[/{THEME['menu_number']}] {EMOJIS['delete']} Delete Task",
        f"[{THEME['menu_number']}]5.[/{THEME['menu_number']}] {EMOJIS['completed']} Mark Complete/Incomplete",
        f"[{THEME['menu_number']}]6.[/{THEME['menu_number']}] {EMOJIS['exit']} Exit"
    ]

    # Create menu text with enhanced formatting
    menu_text = "\n".join(menu_items)

    # Create stats line with color coding
    stats_line = f"\n\n[{THEME['label']}]Stats: {stats['total']} total | [{THEME['completed']}]✓ {stats['completed']} completed[/{THEME['completed']}] | [{THEME['pending']}]○ {stats['pending']} pending[/{THEME['pending']}]"

    # Create enhanced menu panel
    panel = Panel(
        menu_text + stats_line,
        title=f"[bold {THEME['header']}]Main Menu[/]",
        border_style=THEME['panel_border'],
        box=BOX_STYLES['menu'],
        padding=(1, 2),
        style=THEME['menu_item']
    )
    console.print(panel)

def show_tasks_table(tasks: List) -> None:
    """
    Display tasks in a professional table with enhanced styling.

    Args:
        tasks: List of Task objects to display
    """
    if not tasks:
        # Enhanced empty state panel
        empty_panel = Panel(
            Align.center(
                Text(f"{EMOJIS['task']} No tasks yet! Add your first task to get started.", style=f"italic {THEME['warning']}")
            ),
            border_style=THEME['warning'],
            box=BOX_STYLES['info_panel'],
            padding=(2, 4)
        )
        console.print(empty_panel)
        return

    # Create enhanced table with gradient header
    table = Table(
        title=f"{EMOJIS['task']} Your Tasks",
        title_style=f"bold {THEME['primary']}",
        box=BOX_STYLES['task_card'],
        show_header=True,
        header_style=f"bold {THEME['header']}",
        border_style=THEME['panel_border'],
        row_styles=["none", "dim"]  # Alternate row styling
    )

    # Add columns with enhanced styling
    table.add_column("ID", style="dim", width=6, justify="center")
    table.add_column("Status", width=12, justify="center")
    table.add_column("Title", style="bold", min_width=20)
    table.add_column("Description", style="dim", min_width=25)
    table.add_column("Created", style="dim", width=18)

    for i, task in enumerate(tasks):
        # Enhanced status display with strikethrough for completed tasks
        if task.completed:
            status = f"[{THEME['completed']}]{EMOJIS['completed']} Done[/{THEME['completed']}]"
            title = f"[strikethrough]{task.title}[/strikethrough]"
        else:
            status = f"[{THEME['pending']}]{EMOJIS['pending']} Pending[/{THEME['pending']}]"
            title = task.title

        desc = task.description[:40] + "..." if len(task.description) > 40 else task.description or f"[dim]{EMOJIS['info']} (none)[/dim]"
        created = task.created_at.strftime("%b %d, %Y %H:%M")

        # Add row with conditional styling
        table.add_row(
            f"[bold]{task.id}[/bold]",
            status,
            title,
            desc,
            created
        )

    console.print(table)

def show_task_details(task) -> None:
    """
    Display detailed task information in a card-like panel.

    Args:
        task: Task object to display
    """
    # Enhanced status display
    if task.completed:
        status_icon = EMOJIS['completed']
        status_color = THEME['completed']
        status_text = "Completed"
    else:
        status_icon = EMOJIS['pending']
        status_color = THEME['pending']
        status_text = "Pending"

    # Create detailed information layout
    details_content = f"""
[bold]{EMOJIS['task']} ID:[/bold]          [bold]{task.id}[/bold]
[bold]{EMOJIS['task']} Title:[/bold]       [bold]{task.title}[/bold]
[bold]{EMOJIS['task']} Description:[/bold] {task.description or f'[dim]{EMOJIS['info']} (none)[/dim]'}
[bold]{EMOJIS['task']} Status:[/bold]      [{status_color}]{status_icon} {status_text}[/{status_color}]
[bold]{EMOJIS['task']} Created:[/bold]     {task.created_at.strftime('%B %d, %Y at %H:%M')}
    """

    # Create enhanced task details panel
    panel = Panel(
        details_content,
        title=f"[bold {THEME['primary']}]{EMOJIS['task']} Task Details[/bold {THEME['primary']}]",
        border_style=status_color,
        box=BOX_STYLES['task_card'],
        padding=(1, 2),
        style=THEME['value']
    )
    console.print(panel)

def show_success(message: str) -> None:
    """
    Display success message with enhanced styling and animation.

    Args:
        message: Success message to display
    """
    # Create success panel with enhanced styling
    success_text = Text(f"{EMOJIS['success']} {message}", style=f"bold {THEME['success']}")

    panel = Panel(
        Align.center(success_text),
        border_style=THEME['success'],
        box=BOX_STYLES['success'],
        padding=(1, 2)
    )
    console.print(panel)

def show_error(message: str) -> None:
    """
    Display error message with enhanced styling and animation.

    Args:
        message: Error message to display
    """
    # Create error panel with enhanced styling
    error_text = Text(f"{EMOJIS['error']} {message}", style=f"bold {THEME['error']}")

    panel = Panel(
        Align.center(error_text),
        border_style=THEME['error'],
        box=BOX_STYLES['error'],
        padding=(1, 2)
    )
    console.print(panel)

def show_info(message: str) -> None:
    """
    Display info message with enhanced styling and animation.

    Args:
        message: Info message to display
    """
    # Create info panel with enhanced styling
    info_text = Text(f"{EMOJIS['info']} {message}", style=f"bold {THEME['info']}")

    panel = Panel(
        Align.center(info_text),
        border_style=THEME['info'],
        box=BOX_STYLES['info_panel'],
        padding=(1, 2)
    )
    console.print(panel)

def show_confirmation_dialog(message: str) -> bool:
    """
    Display a confirmation dialog with enhanced styling.

    Args:
        message: Confirmation message to display

    Returns:
        bool: True if confirmed, False otherwise
    """
    # Create confirmation panel
    confirm_text = Text(f"{EMOJIS['warning']} {message}", style=f"bold {THEME['warning']}")

    panel = Panel(
        confirm_text,
        title="[bold yellow]Confirmation[/bold yellow]",
        border_style=THEME['warning'],
        box=BOX_STYLES['warning'],
        padding=(1, 2)
    )
    console.print(panel)

    # Get user response
    response = input(f"\nEnter [bold]{THEME['accent']}]yes[/{THEME['accent']}] to confirm or [bold]{THEME['warning']}]no[/{THEME['warning']}] to cancel: ").strip().lower()
    return response in ['yes', 'y', 'YES', 'Y']

def show_progress_bar(task_name: str, total: int = 100) -> Progress:
    """
    Create and return a progress bar for long operations.

    Args:
        task_name: Name of the task being performed
        total: Total amount of work (default 100)

    Returns:
        Progress: Progress bar instance
    """
    progress = Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console
    )

    progress.add_task(description=task_name, total=total)
    return progress

def show_status_bar(current_screen: str = "Main Menu") -> None:
    """
    Display a status bar at the bottom of the screen.

    Args:
        current_screen: Name of the current screen
    """
    status_text = f" {EMOJIS['home']} {current_screen} | {datetime.now().strftime('%H:%M:%S')} "
    status_panel = Panel(
        f"[{THEME['footer']}]{status_text}[/{THEME['footer']}]",
        border_style=THEME['footer'],
        box=MINIMAL,
        padding=(0, 1),
        expand=True
    )
    console.print(status_panel)