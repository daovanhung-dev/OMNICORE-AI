# Client feature implementation checklist

1. Route/layout ownership and authorized entry point.
2. Reuse shared UI vs screen-local widgets; follow project framework adapter only when verified.
3. Component events and typed input/state; presentational UI shouldn't issue raw network calls when separation exists.
4. Feature data-access delegates to HTTP/client; no direct DB key or privileged provider token in browser.
5. Map DTO and server errors correctly to loading/empty/success/error/forbidden/offline UI.
6. Auth UX guard is not server-side authorization. Unauthorized and session expiration must not expose protected data.
7. Deep links, back navigation, stale request handling, pagination, mutation retry/double-submit, accessible focus/responsive.
8. Focused component tests, browser evidence where authorized, cleanup local fixtures if used.

Source hierarchy: approved UI contract + actual router + actual API/client adapter + tests. Stub/endpoint descriptor != caller.
