# Quy trình — Root cause & minimal correction

## 1. Reproduce accurately

- Capture expected vs actual, version/revision, environment and clear steps/input.
- Identify frequency, impact, first bad version if known, constraints, log correlation IDs; redact secrets/PII.
- If not reproducible, use evidence sources/logging and declare `NOT_REPRODUCED`; do not claim root cause certainty.

## 2. Trace actual ownership

`User action/request → client caller → transport → server handler → auth/validation → domain logic → DB/provider → response → client state`. For one-side bugs follow the reachable subset only; distinguish symptom vs root cause.

## 3. Hypothesis table

For each candidate cause record evidence for/against, minimal observation/test, confidence; isolate configuration/test drift from product bugs. Avoid indiscriminate refactor or running unsafe prod mutations.

## 4. Regression-first when feasible

Write a focused test that fails for **the specific wrong behavior**, preferably before patch. Record baseline state and why test failed; if impossible, note reason and use manual isolated reproduction.

## 5. Fix smallest owning layer

Preserve API contract and behavior not in scope. Avoid hiding exception, altering expected tests, broad rewrites, destructive data repair without approval, or changing environment security policy as workaround.

## 6. Verify & handoff

Run regression, linked tests, type/build where applicable; compare baseline warnings and diff. Describe root cause, patch, tests, exact unchanged limitations, owner of unresolved policy, rollback.

**Bug is not closed** solely when the process starts; confirm original reproduction no longer occurs in tested environment.
