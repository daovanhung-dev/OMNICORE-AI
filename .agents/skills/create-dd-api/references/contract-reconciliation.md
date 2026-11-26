# API contract reconciliation matrix

Mỗi API phải có evidence theo **hai trục**:

| Contract item | Expected requirement + version | Current executable source + path | Runtime tested? | Decision |
|---|---|---|---|---|
| Method/path | OPEN | UNKNOWN | NOT_RUN | OPEN |
| JWT/object scope | OPEN | UNKNOWN | NOT_RUN | OPEN |
| Input field nullability | OPEN | UNKNOWN | NOT_RUN | OPEN |
| Response field source | OPEN | UNKNOWN | NOT_RUN | OPEN |
| HTTP/business errors | OPEN | UNKNOWN | NOT_RUN | OPEN |
| Transaction/side effect | OPEN | UNKNOWN | NOT_RUN | OPEN |

## Sources order

1. Latest user-approved change/decision and canonical BD/DD/API contract (expected).
2. Current router + DTO/model + handler + auth guard + query/DB/provider + actual executable config (current).
3. Tests **actually run** this task and runtime environment (verification).
4. Historical docs, generated OpenAPI and old worklog are references, not overriding current source.

A route declaration may be `SOURCE_BACKED` but not `WIRED`; a handler may be `WIRED` but no FE caller; local tests may not reflect live migrations. Document all separately.

## Missing source

- Missing business rule → `OPEN QUESTION` with owner and impact, no invented fallback.
- Missing enum/field or auth policy → block dependent action, continue independent steps.
- Source contradicts approved contract → `DISCREPANCY`, preserve both, record decision gate.
