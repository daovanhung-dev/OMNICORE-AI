# Module traceability and change control

`BD-REQ → MOD → FEATURE → FUNCTION → BR/API → View/State → Source file → Test`.

- `List_Features.md` is feature inventory.
- `Function_List.md` enumerates events/functions, pre/post conditions, inputs/outputs and errors.
- `Views.md` defines route/screen, states, CTA, navigation, data sources and permissions.
- `Import_File.md` maps ownership of code/contracts/assets to real or proposed modules. Do not create fake file paths as existing code.
- `Overall.md` gives module scope/actors/dependencies; history changelog records revisions/approval.

## Review rounds

1. BA/PO: business coverage and open questions.
2. Architect/backend/client: field/type, state transitions, schema/auth/contract, and ownership.
3. QA: every important rule/alternate/error flow has test cases.

If spec changes after code, log impact/consumer migration rather than silently rewriting historic approvals.
