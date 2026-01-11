---
Skill Name: speckit-workflow-enforcement
Description: This skill enforces the Agentic Dev Stack workflow ensuring systematic spec-driven development with complete traceability from requirements to implementation.
Expertise Domain: Spec-driven development lifecycle management
Applicable To: Any agent doing planning or implementation (backend, frontend, AI, DevOps)

Components:
- Specify phase management (requirements definition)
- Plan phase documentation (architecture design)
- Task breakdown with ID tracking
- Implementation validation

Responsibilities:
- Ensure all work starts with speckit.specify files defining WHAT to build with clear requirements and acceptance criteria
- Document architecture decisions in speckit.plan defining HOW to implement with component breakdowns and interfaces
- Break work into atomic tasks in speckit.tasks with Task IDs, dependencies, and expected outputs
- Validate code implementation only proceeds when valid Task ID exists and references back to specs
- Check speckit.constitution for project principles before proposing solutions
- Update specifications when requirements change
- Organize all artifacts in /specs directory with proper subdirectories (features/, api/, database/, ui/, deployment/, events/)
- Prevent "vibe coding" by ensuring every line of code maps to validated requirements

Usage Example:
Attach to: backend-architect, frontend-architect, ai-integration-architect, devops-architect, event-architect, project-architect
Effect: All agents follow systematic spec-driven workflow - requirements are documented in spec.md, architecture decisions in plan.md, work broken into trackable tasks in tasks.md with Task IDs, and every code change references a Task ID ensuring complete traceability from idea to implementation. No work proceeds without validated specifications.
---
