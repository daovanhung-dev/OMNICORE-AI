# Coding handoff & change safety

Before any edit capture `git status --short --branch` and exact target diff. Avoid resetting uncommitted changes. Keep task scope narrow and distinguish owned vs existing dirty changes.

After edit record:

- Requirement(s), plan/milestones, sources read, files changed, why each change is necessary.
- API/DB contracts touched, migrations/provider operations and auth risks.
- Commands actually run with exit code, warnings, tests not run and environment.
- Functional demo/browser result only when executed; never infer live runtime from build.
- Worklog, DD, architecture/context updates, unresolved gates and next action/owner.

A line of code written is not a verified milestone; progress tracks accepted outputs.
