# Sự kiện, data flow and navigation

## Event contract

`EV ID | Actor/trigger | Preconditions | Inputs/source | Validation | Ordered steps | API/BR refs | State/output | Error & retry | Navigation | TC refs`.

Example: pressing search → trim query (if approved) → call GET catalog (if wired) → ignore stale response → render success/empty/error → preserve route/query parameters. Only behavior supported by source becomes real integration.

## Page/controller ownership

User event → Page/Controller → typed feature service → shared transport → API → DTO → mapper/ViewModel → render. Presentational child emits events, doesn't import API or manipulate browser store if project architecture disallows. Server is authoritative for permission.

## Failure-mode checklist

Rapid double click, pending request cancellation, outdated responses racing, validation vs server errors, 401/403/404 handling, optimistic mutation rollback, pagination boundary, route parameter invalid or too large, browser back/deep-link and stale cache.

## Cross-reference integrity

Every visible interactive EL should resolve to EV; every request-bearing EV to API; every important BR to TC. Navigation should point to registered/approved destination, never assume route from mockup exists.
