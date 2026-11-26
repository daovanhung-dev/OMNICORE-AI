# Ví dụ minh họa — MOD-DEMO-001: Notes (hypothetical)

**Status:** PROPOSED, not a verified live module.

| BD source | Feature | Function | UI/API | Test |
|---|---|---|---|---|
| REQ-DEMO-001 | F-001 own notes | FN-001 list own notes | UI-DEMO-001 / API-DEMO-001 | TC-001 auth, TC-002 empty |

- Overall: actor authenticated user, outcome list owned notes, unknown pagination policy.
- Function: input principal from trusted server auth; query owner-filtered; output array of safe projections.
- View: loading/success/empty/error; no fake saved-notes count.
- Import map: actual source path UNKNOWN; proposed module owner TBD, not claim files exist.
- Diagram: user → UI → API/auth → repository; permissions checked server-side.
- History: Draft, owner TBD, approval not granted.

Use templates/ to expand into the 9-file module DD package. Open rule owner decisions stay `OPEN QUESTION`.
