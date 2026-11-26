# Finding gate & severity

Finding only if:

1. Target is reachable in reviewed path/diff.
2. File/line/call-path evidence demonstrates bug/security risk.
3. Meaningful correctness, security, rule or maintainability impact.
4. Actionable fix direction; for diff, **introduced by the diff**.

## Severity

- P0: catastrophic data exposure, destructive issue or broad outage clearly reachable.
- P1: serious exploitable vulnerability, data corruption, severe business regression.
- P2: material correctness, privilege boundary, maintainability risks with concrete impact.
- P3: limited behavior gap/edge case; no mere style nitpick.

Report confidence and why; if not enough evidence, state unknown rather than invent a finding.
