# Code review report structure

1. Scope: repo/ref/branch/commit, changed files/path and excluded areas.
2. Findings (P0→P3), each with title, file:line, scenario, source evidence, impact, suggestion, confidence.
3. Optional questions/uncertainties: ask only when they affect conclusion.
4. Verification limits: test/build not executed, live deployment unknown, external dependencies not accessed.
5. If no actionable findings, say so without claiming entire system correct/secure.

Source code excerpts short and precise. Never include secret values or PII from reviewed content.
