# DD API acceptance gates

1. **Template**: folder, heading, schema and filename conform to approved version.
2. **Requirement**: every approved function and error condition mapped; unknowns with owner.
3. **Contract**: method/path, auth, request, response, error, privacy, pagination, version exact.
4. **Data**: DB source columns, query predicates, transaction, rollback, storage/provider and no leaked data.
5. **Trace**: each field/rule/error maps to source and at least one test target.
6. **Review**: BA/Architect/Server/Client/QA responsibilities acknowledged where project has such roles.
7. **Static validation**: run `validate-dd --type api --path ... --strict`; no broken links/template placeholders. Human review still required.

Never mark an API “working in production” from an `Approved` DD.
