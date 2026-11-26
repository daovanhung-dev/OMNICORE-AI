# Module scope, actors, business states

## Scope definition

`Purpose | Actors | In scope | Out of scope | Dependencies | Success metrics | Source/version | Decision owner`.

Feature row: `Feature ID | Business outcome | Preconditions | Main flow | Alternatives | Failures | Permissions | Entities | Acceptance criteria`.

Function row: `Function ID | Feature ID | Trigger | Request/State | Rules | Query/side effect | Output | Failure | View/API IDs | Test IDs`.

## State machine

Use explicit valid transitions and owners, e.g. `DRAFT → SUBMITTED → APPROVED/REJECTED` only **when requirement actually specifies them**. For each transition record event, guard, action, rollback, audit, idempotency and test.

## Source status

`DESIGN_ONLY`, `CURRENT`, `WIRED`, `TESTED_LOCAL`, `DEPLOYED_VERIFIED`, `BLOCKED` are separate axes. Approved DD only approves a design decision.
