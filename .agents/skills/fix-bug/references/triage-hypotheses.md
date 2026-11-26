# Bug triage and competing hypotheses

## Reproduction report

`Summary | actual/expected | steps/input | branch/SHA | environment | frequency | severity | screenshot/log trace (redacted) | source references`.

## Hypothesis ledger

| Hypothesis | Supporting evidence | Contradicting evidence | Minimal test/observation | Result | Next |
|---|---|---|---|---|---|
| H1 (example) stale client cache | unknown | unknown | compare raw API vs UI state | NOT_RUN | inspect caller |

Look for invalid input, stale config, missing migration, token/role mismatch, false mock assumptions, race, DB side-effect failure and external provider. Do not jump to an attractive symptom fix without tracing.
