# OBJECTIVE

The input is a directory containing one or more completed User Flow documents.

Your responsibility is to:

1. Scan the directory `wireframe/userflow/`.
2. Discover every valid User Flow Markdown document (`*.md`).
3. Read and analyze each User Flow independently.
4. Transform each User Flow into a complete Screen Flow specification.
5. Generate one corresponding Screen Flow document for each User Flow.
6. Save the generated Screen Flow into `wireframe/screenflow/`.

Each User Flow must produce exactly one Screen Flow.

Maintain a strict one-to-one mapping between User Flows and Screen Flows.

Do NOT merge multiple User Flows.

Do NOT skip any User Flow.

Do NOT rewrite the User Flow.

Instead, translate business interactions into UI navigation and screen relationships.

Example

Input

wireframe/userflow/

├── UF-001_Authentication.md
├── UF-002_Course_Management.md
├── UF-003_Analytics.md

↓

Output

wireframe/screenflow/

├── SF-001_Authentication.md
├── SF-002_Course_Management.md
├── SF-003_Analytics.md

---

# OUTPUT REQUIREMENTS

Each generated Screen Flow must be a complete UX navigation specification and contain the following sections.

## 1. Screen Flow Overview

Include:

- Screen Flow ID
- Screen Flow Name
- Related User Flow
- Description
- Primary Actor
- User Goal
- Entry Screen
- Exit Screen(s)

---

## 2. Screen Inventory

Create a table with:

- Screen ID
- Screen Name
- Screen Type
  - Page
  - Form
  - Modal
  - Dialog
  - Drawer
  - Wizard
  - Result Page
  - Processing Page
- Purpose

Every screen must have a unique Screen ID.

---

## 3. Navigation Matrix

Create a navigation table including:

- Current Screen
- User Action
- Next Screen
- Navigation Type
  - Redirect
  - Replace Page
  - Modal
  - Dialog
  - Drawer
  - Back
  - Close
  - Inline Update
- Condition

Include both Happy Path and all Alternative / Exception Flows.

---

## 4. Screen Specifications

For every screen include a concise summary containing:

- Purpose
- Layout Summary
- Main Content
- Key Components
- User Actions
- Validation Summary (if applicable)
- Success Transition
- Error Transition

Do not describe detailed UI implementation.

---

## 5. Screen States

For each screen identify all applicable states.

Examples:

- Default
- Loading
- Empty
- Success
- Error
- Disabled
- Processing

If a state is not applicable, omit it.

---

## 6. Mermaid Screen Flow

Generate one Mermaid flowchart representing:

- Entry Screen
- All navigation paths
- Decision branches
- Alternative flows
- Exception flows
- Exit Screens

The Mermaid diagram must be consistent with the Navigation Matrix.

---

## 7. Reusable UI Components

Group reusable UI components by category.

Examples:

Layout

- Header
- Sidebar
- Footer

Navigation

- Breadcrumb
- Tabs
- Pagination

Input

- Form
- Text Field
- Dropdown
- File Upload

Feedback

- Toast
- Alert
- Inline Validation

Overlay

- Modal
- Dialog
- Drawer

Data Display

- Table
- Card
- Chart
- Progress Bar

---

## 8. Design Pattern Suggestions

Recommend suitable UX patterns including:

- Navigation Pattern
- Layout Pattern
- Form Pattern
- Validation Pattern
- Feedback Pattern
- Error Handling Pattern
- Loading Pattern
- Accessibility Considerations
- Responsive Behaviour

Recommendations must align with the User Flow.

---

## 9. Assumptions

If information is missing from the User Flow:

Do NOT invent business logic.

Instead create an **Assumptions** section listing any reasonable UX assumptions required to complete the Screen Flow.

---

# QUALITY RULES

The generated Screen Flow must:

✓ Represent every major screen.

✓ Include Entry Screen and Exit Screen.

✓ Cover every Happy Path.

✓ Cover every Alternative Flow.

✓ Cover every Exception Flow.

✓ Include navigation conditions.

✓ Specify navigation type.

✓ Distinguish Pages, Dialogs, Modals and Drawers.

✓ Keep Mermaid Diagram synchronized with Navigation Matrix.

✓ Preserve traceability back to the original User Flow.

✓ Be suitable as input for AI Wireframe generation tools (Figma AI, Stitch, Relume, Galileo AI).

---

# FINAL VALIDATION

Before finishing, verify that:

- Every User Flow inside `wireframe/userflow/` has exactly one corresponding Screen Flow.
- No User Flow has been skipped.
- No duplicate Screen Flow exists.
- Every Screen Flow contains all mandatory sections.
- Navigation Matrix and Mermaid Diagram are consistent.
- Entry Screen and Exit Screen are defined.
- Every Screen has a unique Screen ID.
- Every screen has a Screen Type.
- Every navigation has a Navigation Type.

If a User Flow cannot be fully converted because required information is missing, still generate the Screen Flow and include an **Assumptions** section instead of omitting the file.

---

# INPUT

Input directory:

`wireframe/userflow/`

Read every Markdown (`*.md`) User Flow document.

Generate the corresponding Screen Flow documents into:

`wireframe/screenflow/`