# Contract: Add Task API

## Endpoint: add_task(title: str, description: str = "")

### Description
Creates a new task with the provided title and optional description.

### Parameters
- **title** (required): string, 1-200 characters, standard characters only (alphanumeric + common punctuation), non-whitespace content required
- **description** (optional): string, 0-1000 characters, standard characters only

### Returns
- **Task object** with fields:
  - id: integer (unique sequential ID)
  - title: string (validated input)
  - description: string (validated input or empty)
  - completed: boolean (default: false)
  - created_at: datetime (auto-generated timestamp)

### Errors
- **ValidationError**: When title doesn't meet validation requirements
  - Empty title
  - Title too long (>200 characters)
  - Title with only whitespace
  - Invalid characters in title or description

### Success Criteria
- New task is added to in-memory storage
- Unique sequential ID is assigned
- Creation timestamp is recorded
- Task is marked as incomplete by default
- Clear success feedback is provided to user