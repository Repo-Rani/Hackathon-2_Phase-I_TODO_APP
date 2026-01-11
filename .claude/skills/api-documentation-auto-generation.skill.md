---
Skill Name: api-documentation-auto-generation
Description: This skill automatically generates interactive API documentation from code using OpenAPI/Swagger with examples, authentication flows, and Try It Out functionality.
Expertise Domain: API documentation and OpenAPI specification
Applicable To: Backend and API development agents

Components:
- OpenAPI 3.0+ specification generation
- Swagger UI integration
- Request/response examples and schemas
- Authentication documentation

Responsibilities:
- Configure FastAPI to auto-generate OpenAPI specs with proper metadata (title, version, description, contact, license)
- Add detailed docstrings to API endpoints that appear as operation descriptions in Swagger UI
- Define Pydantic models with Field descriptions and examples for automatic schema generation
- Document authentication schemes (JWT Bearer, API Key, OAuth2) with security requirement specifications
- Add response model examples showing successful responses and common error formats
- Include request body examples demonstrating proper payload structure for POST/PUT/PATCH operations
- Generate tag-based grouping for related endpoints (e.g., Tasks, Users, Authentication)
- Add deprecation warnings for endpoints scheduled for removal
- Configure Swagger UI with custom branding, theme, and Try It Out functionality
- Export OpenAPI spec as JSON/YAML for use in API gateways, code generators, and testing tools

Usage Example:
Attach to: backend-architect, api-endpoint-designer
Effect: Agent automatically generates interactive Swagger UI documentation at /docs endpoint. Every FastAPI route has detailed descriptions, request/response examples, authentication requirements, and working Try It Out buttons. OpenAPI spec is exported to api-spec.yaml for use in MCP tool generation, client SDK generation, and contract testing.
---
