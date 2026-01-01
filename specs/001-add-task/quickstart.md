# Quickstart Guide: Add Task Functionality

## Prerequisites
- Python 3.13+
- UV package manager

## Setup
1. Clone the repository
2. Navigate to project directory
3. Run `uv sync` to install dependencies (minimal dependencies for this feature)

## Running the Application
```bash
uv run python src/main.py
```

## Using the Add Task Feature
1. Launch the application
2. Select option "1" or "Add Task" from the main menu
3. Enter a task title (1-200 characters, non-whitespace content)
4. Optionally enter a description (up to 1000 characters)
5. The system will assign a unique ID and timestamp
6. Task will be marked as incomplete by default
7. You'll be returned to the main menu

## Validation Rules
- Title must be 1-200 characters
- Title must contain non-whitespace content
- Title and description must use standard characters (alphanumeric + common punctuation)
- Description is optional, up to 1000 characters if provided
- New tasks are automatically marked as incomplete
- Each task gets a unique sequential ID

## Error Handling
- Invalid input will show clear error messages
- You'll be prompted to re-enter valid input
- Cancel option available to return to main menu without creating task