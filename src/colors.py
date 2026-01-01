"""
Color scheme definitions for the Todo Console App.
Provides consistent color themes throughout the application.
"""

# Professional dark theme color palette
THEME = {
    # Primary colors
    'primary': 'cyan',
    'secondary': 'magenta',
    'accent': 'yellow',

    # Status colors
    'success': 'green',
    'error': 'red',
    'warning': 'bright_yellow',
    'info': 'blue',

    # Task status colors
    'completed': 'green',
    'pending': 'bright_black',
    'overdue': 'red',

    # Background and UI elements
    'background': 'black',
    'panel_border': 'bright_cyan',
    'header': 'bold cyan',
    'footer': 'dim white',

    # Menu and navigation
    'menu_item': 'white',
    'menu_highlight': 'bright_white on cyan',
    'menu_number': 'bold cyan',

    # Text styling
    'title': 'bold white',
    'subtitle': 'italic white',
    'label': 'bold',
    'value': 'white',

    # Special effects
    'gradient_start': 'cyan',
    'gradient_end': 'magenta',
}

# Box styles for different UI elements
from rich import box

BOX_STYLES = {
    'header': box.DOUBLE,
    'menu': box.ROUNDED,
    'task_card': box.HEAVY,
    'info_panel': box.SQUARE,
    'success': box.ROUNDED,
    'error': box.ASCII,
    'warning': box.HEAVY_HEAD,
}

# Emoji and icon mappings
EMOJIS = {
    'app': '📋',
    'task': '📝',
    'completed': '✅',
    'pending': '⏳',
    'add': '➕',
    'edit': '✏️',
    'delete': '🗑️',
    'exit': '🚪',
    'success': '🎉',
    'error': '❌',
    'info': 'ℹ️',
    'warning': '⚠️',
    'stats': '📊',
    'search': '🔍',
    'filter': '筛选',
    'sort': '↕️',
    'home': '🏠',
    'settings': '⚙️',
}