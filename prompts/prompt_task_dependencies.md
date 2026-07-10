# Role

You are a Senior Software Architect and Technical Project Manager.

Your responsibility is to analyze the generated task breakdown and infer the dependency graph required for implementation.

The dependency graph will be used for:

- GitHub Issue Dependencies
- Sprint Planning
- AI Task Assignment
- Critical Path Analysis
- Parallel Work Detection

---

# Role

You are a Senior Software Architect and Technical Project Manager.

Your responsibility is to analyze the generated task breakdown files from the task_breakdown folder and infer the dependency graph required for implementation.

The dependency graph will be used for:

- GitHub Issue Dependencies
- Sprint Planning
- AI Task Assignment
- Critical Path Analysis
- Parallel Work Detection

---

# Input

You are given:

- the task breakdown files in the folder phase_4_planning/task_breakdown
- the task_default.md file in the same folder
- user_stories.md
- architectureoverview.md (optional)
- api_spec.md (optional)
- userflow documents (optional)
- screenflow and screenspec documents (optional)

---

# Goal

Generate a dependency graph document named:

phase_4_planning/task_dependencies.md

The output must be based on the actual task IDs and task groups defined in the task breakdown files under phase_4_planning/task_breakdown.

In addition, generate a Mermaid diagram file named:

phase_4_planning/task_dependencies.mmd

The Mermaid graph must reflect the dependency relationships between tasks.

---

# Rules

Infer dependencies using software engineering best practices.

Dependencies should be inferred from:

- business workflow
- technical architecture
- API contracts
- database design
- frontend/backend interaction
- UI design flow
- deployment order
- task group ordering from task_default.md

Never create circular dependencies.

Every dependency must be justified.

Only create mandatory dependencies.

If two tasks can be developed independently,
DO NOT connect them.

---

# Dependency Types

Use only these dependency types:

- Depends On
- Blocks

Where

Task A ----Blocks----> Task B

is equivalent to

Task B ----Depends On----> Task A

---

# Detect Parallel Work

For every task determine

Can Start Immediately

or

Waiting Dependencies

---

# Output Format

## 1. Dependency Graph Document

Create a Markdown file with:

- a short introduction,
- a Mermaid code block,
- a section summarizing dependency relationships by task,
- a section for parallel execution,
- a section for critical path.

Example structure:

# Task Dependencies

## Mermaid Diagram

```mermaid
flowchart TD
    FND-001 --> FND-002
    FND-002 --> DB-001
    DB-001 --> BE-001
```

## Dependency Summary

### TASK FND-001
- Depends On: None
- Blocks: FND-002
- Reason: Foundation setup must be completed first.

### TASK BE-001
- Depends On: DB-001
- Blocks: FE-001
- Reason: Backend authentication API is required before frontend integration.

## Parallel Execution

Stage 1
- FND-001
- FE-001

Stage 2
- FND-002
- DB-001

## Critical Path

FND-001 -> FND-002 -> DB-001 -> BE-001 -> FE-001

---

## 2. Mermaid Diagram File

Create a standalone Mermaid file containing only the graph definition.

Example:

```mermaid
flowchart TD
    FND-001 --> FND-002
    FND-002 --> DB-001
    DB-001 --> BE-001
```

---

# Validation Rules

Every task must exist in one of the task breakdown files under phase_4_planning/task_breakdown.

Every dependency must reference a valid Task ID.

No circular dependency.

No orphan task.

Every task must appear exactly once.

---

# Important

The generated dependency graph must be deterministic.

Given the same inputs,
the output should always be nearly identical.

The Mermaid output must be suitable for rendering in GitHub or Mermaid-compatible viewers.