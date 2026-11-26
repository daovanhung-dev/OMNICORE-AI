# API field & DB mapping reference

## Request sheet row

`field_id | path/query/header/body | key | type | required | nullable | default | format | min/max | source | validation | tests`.

A field cannot simply be “string” when protocol depends on email/UUID/date/int64/range/UTF8/trim/null/blank semantics. Path IDs from JavaScript may exceed safe integer precision: preserve as string if actual contract requires signed int64, without silently changing schema.

## Response sheet row

`field_id | response_json_path | type | nullable | source_table_or_provider | transformation | privacy | serialization | error_case`.

Example: `data.id | string decimal | false | orders.id BIGINT | decimal-string serialize | internal | preserve precision | 500 if invalid DB projection` — **example only**, not a default contract.

## Mutation map

For every table: `table | column | expression/value | predicate | effect | transaction | lock | source migration | error/rollback`.

- DB helper's ability to commit is separate from transaction ownership; verify actual implementation.
- Multi-step mutation must state atomicity and idempotency, especially external providers/queue where DB transaction cannot roll back remote effect.
- Read-only APIs must not claim an INSERT/UPDATE just because generic template has a mutation sheet; use `N/A — READ-ONLY`.

## Error contract

Precedence matters: auth 401, object scope 403/404, validation 422/400, conflict 409, provider timeout/503, unexpected 500 **are only examples**. Use approved project HTTP and business-code mappings.
