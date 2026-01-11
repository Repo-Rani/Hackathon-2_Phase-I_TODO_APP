---
Skill Name: database-migration-management
Description: This skill manages database schema evolution using Alembic migrations with proper versioning, rollback support, and data safety.
Expertise Domain: Database schema migration and version control
Applicable To: Backend and database management agents

Components:
- Alembic migration file generation
- Schema change detection and diffing
- Migration ordering and dependency management
- Rollback and data migration strategies

Responsibilities:
- Initialize Alembic configuration in backend projects with proper directory structure and env.py setup
- Generate migration files from SQLAlchemy model changes using alembic revision --autogenerate
- Review and validate auto-generated migrations for accuracy and safety before committing
- Add data migrations for transforming existing records when schema changes require it
- Implement proper upgrade() and downgrade() functions for bidirectional migration support
- Create migration naming conventions with timestamps and descriptive slugs (e.g., 2024_01_15_add_user_roles)
- Add migration tests to verify schema changes apply cleanly and rollback correctly
- Document breaking changes and coordinate migrations across microservices
- Handle foreign key constraints, indexes, and unique constraints safely during migrations

Usage Example:
Attach to: backend-architect, db-schema-manager
Effect: Agent automatically generates Alembic migrations when SQLAlchemy models change, validates them for safety, adds proper downgrade paths, and includes data migrations when needed. All schema changes are versioned, reversible, and tested before deployment.
---
