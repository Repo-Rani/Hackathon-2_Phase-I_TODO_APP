---
title: "Add session management constitution"
description: "Create constitution for session management feature"
date: "2026-01-06"
feature: "003-session-management"
files:
  - ".specify/memory/constitution_session_management.md"
---

# Add session management constitution

## User Prompt
```
I need to add a session state management feature to my Python todo app that allows saving and resuming work context.

FEATURE REQUIREMENTS:

1. **Session Save Command**
   - User can type: "stop [session_code]" (e.g., "stop 123")
   - System should save:
     * All current todos (title, description, status, timestamps)
     * Current phase of work
     * Last activity performed
     * Any work in progress state
   - Save to a persistent file (JSON or pickle format)

2. **Session Resume Command**
   - User can type: "start [session_code]" (e.g., "start 123")
   - System should:
     * Load the exact state from when session was stopped
     * Restore all todos with their original IDs
     * Show a summary: "Resuming session 123 - Last activity: [description]"
     * Continue as if user never left

3. **Session Management**
   - List all saved sessions: "sessions list"
   - Delete a session: "sessions delete [code]"
   - Show session info: "sessions info [code]"

4. **Storage Structure**
   Save sessions in a `/sessions` folder with format:
sessions/
session_123.json
session_abc.json

5. **Session Metadata**
   Each session should store:
   - Session code
   - Created timestamp
   - Last modified timestamp
   - Phase of work
   - Last activity description
   - Todo list snapshot

TECHNICAL REQUIREMENTS:
- Use JSON for session storage
- Implement proper error handling (session not found, invalid code, etc.)
- Session codes should be user-defined (alphanumeric, no spaces)
- On app start, check if any session exists and prompt user to resume or start fresh

Please implement this following the spec-driven development approach with proper Constitution and specs documentation.

Alternative More Specific Prompt:
Add LinkedIn-style conversation memory to my todo app:

CORE FEATURE:
Users can save their entire work state and resume exactly where they left off using simple commands.

COMMANDS TO IMPLEMENT:

1. `stop abc` - Saves everything with code "abc":
   - All todos (with IDs, titles, descriptions, completed status)
   - Current work phase
```

## Response
Created a separate constitution file for the session management feature that outlines the core principles, architecture constraints, code quality standards, technology stack, data model principles, and user interface principles specific to the session management functionality. The constitution covers session state persistence, validation, error handling, and integration with the existing application.

## Files Created
- `.specify/memory/constitution_session_management.md` - Contains the complete constitution for the session management feature with all relevant principles and governance guidelines.