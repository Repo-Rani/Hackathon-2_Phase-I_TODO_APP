# Data Model: Add Task Functionality

## Task Entity

### Fields
- **id**: integer, unique identifier (sequential, starting from 1)
- **title**: string, required text (1-200 characters)
- **description**: string, optional text (0-1000 characters)
- **completed**: boolean, status flag (default: false)
- **created_at**: datetime, timestamp of creation

### Validation Rules
- `id`: Auto-generated, unique, immutable once assigned
- `title`: Required, 1-200 characters, standard characters only (alphanumeric + common punctuation), non-whitespace content required
- `description`: Optional, 0-1000 characters, standard characters only
- `completed`: Boolean value, default false for new tasks
- `created_at`: Auto-generated timestamp at task creation

### State Transitions
- New task: `completed = false` (default)
- Task can transition from `completed = false` to `completed = true` (via mark complete feature)
- Task can transition from `completed = true` to `completed = false` (via mark complete feature)

## TodoManager (Business Logic Container)

### Collections
- **tasks**: List of Task objects, stored in-memory
- **next_id**: Integer counter for next available ID

### Relationships
- TodoManager contains multiple Task objects
- Each Task has a unique id within the TodoManager's tasks list