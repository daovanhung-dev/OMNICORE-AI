# Fixture / test database safety

1. Confirm disposable/local test DB by database name/server identity before any insert.
2. Never seed production or shared user database. If connection target ambiguous, stop.
3. Predefine fixture IDs/data owner and dependency order; create rows with tracking IDs.
4. After demo/delete test-owned rows only, in dependency-safe order; query recorded IDs to verify cleanup.
5. No `TRUNCATE`/global DELETE, no leaked tokens/PII, redact logs. Fake DB mocks are allowed for unit/HTTP but do not verify migrations.
6. For external providers use sandbox/doubles and bounded fake outputs, clearly label `TEST_DOUBLE`.
