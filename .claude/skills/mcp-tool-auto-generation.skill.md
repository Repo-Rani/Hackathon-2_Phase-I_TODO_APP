---
Skill Name: mcp-tool-auto-generation
Description: This skill automatically generates MCP server tools from API specifications enabling AI agents to interact with backend services.
Expertise Domain: Model Context Protocol (MCP) tool development
Applicable To: AI integration and MCP server development agents

Components:
- MCP tool schema generation from OpenAPI specs
- Tool function implementations with proper error handling
- Type-safe request/response mappings
- Authentication and authorization integration

Responsibilities:
- Parse OpenAPI/Swagger specifications to identify API endpoints suitable for MCP tool exposure
- Generate MCP tool definitions with proper JSON schemas for inputs and outputs matching API contracts
- Create tool handler functions that call backend APIs with proper HTTP methods, headers, and body serialization
- Implement authentication flows (JWT token passing, API key injection) for secure tool execution
- Add error handling and validation for tool inputs before making API calls
- Generate TypeScript/Python MCP server boilerplate with all tools registered
- Create tool documentation with clear descriptions, parameter explanations, and usage examples
- Implement rate limiting and retry logic for resilient tool execution

Usage Example:
Attach to: ai-integration-architect, mcp-tool-developer
Effect: Agent reads your FastAPI OpenAPI spec and automatically generates a complete MCP server with tools for add_task, list_tasks, update_task, delete_task, complete_task. Each tool has proper schemas, authentication, error handling, and documentation. AI agents can immediately use these tools to manage tasks via natural language.
---
