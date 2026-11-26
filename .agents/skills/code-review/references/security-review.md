# Security review lens (read-only)

Trace attacker-controlled input into auth, validation, DB/query, file paths, shell commands, provider URLs and response. Check object/tenant ownership and role permission. Consider injection/SSRF/XSS/CSRF (when relevant), path traversal, unsafe deserialization, log/PII/secret leakage, insecure state changes and dependency exposure.

An identified risk requires reachable scenario and missing mitigation shown in code; a label like “SQL injection” without data path/evidence is speculative.

Do not run live exploits, scanners or tests during review-only workflow. Do not mutate repo or PR comments. Scope may be narrowed by user; disclose limits.
