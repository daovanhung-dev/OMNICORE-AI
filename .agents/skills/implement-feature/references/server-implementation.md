# Server feature implementation checklist

1. Inspect real entrypoint, dependency injection, router registration and middleware. File presence alone does not establish route.
2. API method/path and contract; request DTO, authn/authz and object/tenant ownership checked by server.
3. Validator pure parsing/normalization; business invariants owned by use case/domain service.
4. Repository/SQL ORM/prisma adapter is parameterized, transaction owner explicit, locking & concurrency intentional.
5. Provider timeout/error/retry/idempotency; external non-transactional side effects require designed ordering/outbox when necessary.
6. Correct HTTP/business errors, safe messages, trace and envelope per actual project contract.
7. Migration/schema provenance; existing DDL ≠ deployed DB; no prod destructive mutation without permission.
8. Focused API tests, auth negative, rollback, integration sandbox and build/import validation.

Never impose `models.py → validate.py → query.py → view.py` on Express, or Prisma on FastAPI; use verified adapter.
