# Quy trình — Explicit read-only code review

## Scope boundary

Trigger only when user asks for review/audit. Read code, tests, diff, contracts, context; **do not edit code/config, run tests/build/linters, commit/push or post comments**. Worklog if repository policy permits. No automatic changes after review.

## Target selection

- Diff/PR: exact base/head and ownership, include untracked/staged/unstaged only when requested. Report defects introduced in target diff; do not attribute historical bugs to new patch.
- Named path/module audit: review current state and label findings as current-state, not introduced regressions.

## Four lenses

1. Contract/rule correctness: requirement vs source, DTO/status/errors, permission, migration and side effects.
2. Reuse/maintainability: duplicate logic causing observable drift, boundaries, testability. Style-only issues without impact are not findings.
3. Reachable edge cases: validation, race, stale cache, transaction, retry, failure branch, data loss.
4. Security: attacker-controlled input → reachable path → missing protection → impact. Check auth/ownership, SQL injection, SSRF, file path, secrets/PII, output encoding.

## Finding gate

Finding must be reachable, evidenced with path + line/symbol, significant/actionable; diff finding requires introduction by the diff. Assign severity P0/P1/P2/P3, confidence, concise scenario, suggestion not mandatory patch. Do not call narrow review a security certification.

## Final report

Scope and ref → findings ordered severity → evidence/location → why it matters → proposed change → unknowns and tests not executed. No findings != system fully correct.
