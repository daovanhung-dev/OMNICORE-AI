# Risk-based verification matrix

| Requirement ID | Test ID | Risk/branch | Setup | Action | Expected state/error/side effect | Level | Actual evidence |
|---|---|---|---|---|---|---|---|
| REQ-DEMO-1 | TC-DEMO-1 | access isolation | two users | user B requests A's item | server denies without data leak | HTTP contract | NOT_RUN |

Priority: auth/ownership/data integrity first; then unhappy paths and race/idempotency; UI loading/error; happy path/format. Test infrastructure-specific behavior only in controlled environment.

**Levels**: Unit, component, HTTP contract, integration, end-to-end, deployment smoke. All results tagged environment and exact command.
