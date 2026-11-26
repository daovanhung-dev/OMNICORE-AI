# Quy trình — Risk-based tests

## Read first

- Approved requirements/DD/AC, current source, router, validation/permission, business codes, test tooling config & executable scripts.
- Ghi environment, dependency, test DB target (nếu dùng), fixture cleanup policy.

## Design matrix

`REQ-ID | Branch/condition | Setup | Action | Expected HTTP/UI/DB/provider result | Level | Test file | Execution evidence | Cleanup`.

### Test classes

1. Pure unit: transformations, validators, policy pure logic.
2. Component/UI: event/state, disabled/loading/empty/error/retry/navigation/a11y.
3. HTTP/contract: method/path/auth/request/status/DTO/envelope/edge case.
4. Integration: isolated real DB transactions, schema migrations, provider sandbox, retry/idempotency.
5. End-to-end: browser/device → real test/staging API, deep link/accessibility/responsive.
6. Deployment smoke: only approved target; evidence environment/time and metrics.

## Execution

- Verify test command from package/config; do not invent npm/pytest command.
- Run smallest failing/focused suite first; then impacted regression, typecheck/build/lint when appropriate.
- If fake DB/session is used, record limitations. Never mark environment `DEPLOYED_VERIFIED` from TestClient alone.
- For test data: confirm disposable target, record created IDs, cleanup just those IDs, query to confirm. Never truncate shared/prod DB.
- Failing tests are evidence; do not weaken assertion to match buggy code or suppress flaky failure without root cause.
- Final test report: commands, exit codes, passed/failed/skipped/warnings, code coverage if measured, blockers and untested areas.
