# Ví dụ minh họa — API-DEMO-001: GET own notes (hypothetical)

**Status:** DESIGN_ONLY; no live route, table or deployment is claimed.

## Requirement and contract

`REQ-DEMO-001`: signed-in person lists notes they own; returns an empty collection when none.

| Field | Location | Type | Rule | Source |
|---|---|---|---|---|
| Authorization | header | Bearer JWT | authenticated; principal from token | REQ-DEMO-001 |
| page | query | int | positive; default requires approval | OPEN Q-1 |
| data[].id | response | decimal string | preserve server ID | PROPOSED |
| data[].title | response | string | sanitized/output encoded | PROPOSED |

## Flow

1. Authenticate and authorize principal.
2. Validate query. Policy for page size/order is `OPEN Q-1` (owner: API architect).
3. Repository selects owner-filtered rows (only after DB table/migration source approved).
4. Map DTO/errors and trace to HTTP boundary.

## Tests

- TC-001: own notes returned, foreign notes excluded.
- TC-002: anonymous 401 before DB.
- TC-003: empty page response consistent with approved envelope.
- TC-004: malformed query, DB failure safe response.

**Important:** This example shows the writing standard, not authorization rules imported into another project. Use templates/ to author actual DD.
