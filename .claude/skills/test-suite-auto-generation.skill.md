---
Skill Name: test-suite-auto-generation
Description: This skill automatically generates comprehensive test suites for backend (pytest) and frontend (Jest) with proper fixtures, mocks, and assertions.
Expertise Domain: Automated test generation and test-driven development
Applicable To: Backend, frontend, and quality assurance agents

Components:
- Pytest test generation for FastAPI endpoints
- Jest/React Testing Library tests for components
- Test fixtures and factory patterns
- Mock/stub generation for external dependencies

Responsibilities:
- Generate pytest test files for each FastAPI router with tests for happy paths, error cases, and edge conditions
- Create pytest fixtures for database sessions, authenticated users, and test data using factories
- Implement FastAPI TestClient tests with proper request/response validation and status code assertions
- Generate Jest test suites for React components with render tests, user interaction simulation, and prop validation
- Create mock implementations for external APIs, databases, and third-party services
- Add integration tests that verify end-to-end flows across multiple components
- Implement test data builders/factories using tools like FactoryBoy (Python) or faker.js (JavaScript)
- Generate test coverage reports and identify untested code paths
- Add snapshot tests for UI components to catch unintended visual changes

Usage Example:
Attach to: backend-architect, frontend-architect, api-endpoint-designer, ui-component-designer
Effect: When agent creates a new FastAPI endpoint POST /tasks, it automatically generates pytest tests covering success (201), validation errors (422), authentication failures (401), and database constraint violations (409). For React components, generates Jest tests with render checks, user interactions, and accessibility validation. Achieves 80%+ test coverage automatically.
---
