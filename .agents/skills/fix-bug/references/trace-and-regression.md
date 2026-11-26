# Root cause trace + regression recipe

1. Map entrypoint and callers, request state, validator/guard, use case, query and response. For FE-only bugs include DOM/state/routing; for backend include transaction and table ownership.
2. Form minimal reproduction, ideally a failing test **before** patch with exact observed mismatch.
3. Identify owning layer. Patch only it and tests; document any contract change approval.
4. Re-run original reproduction, new regression, impacted existing tests, relevant lint/build/typecheck and diff.
5. If not reproducible (environment unavailable), mark `PARTIAL` and provide evidence needed; never declare bug fixed.

When server auth/permission/DB behavior is implicated, do not bypass guard or relax validation to quiet the failing test. Fix core or block for decision.
