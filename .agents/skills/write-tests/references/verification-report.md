# Verification report contract

- Scope/commit/environment/config (non-secret), prereqs.
- Each command and status: `test file; command; exit code; pass/fail/skip; warning; log/evidence`.
- What was **not run**, why, and risk.
- Source vs runtime vs production evidence levels. No converting FakeSession 100% pass into DB schema verification.
- Regression impact and change-diff check.
- On failures, reproduce/minimize root cause; do not hide failures to force green build.
