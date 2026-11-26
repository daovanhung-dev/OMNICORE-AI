# Kiến trúc ứng dụng khách — một screen minh họa

**Reference:** [`apps/client/src/app/features/module1/screen01/`](apps/client/src/app/features/module1/screen01/README.md).

## Luồng Screen01

`app.routes.ts → screen01-page.ts → screen01.service.ts → api-client.service.ts → API contract → screen01.model.ts → HTML/CSS`

| File mẫu | Nhiệm vụ |
|---|---|
| `screen01-page.ts` | Events, state machine, navigation, điều phối UI |
| `screen01-page.html` | Markup, bindings, form actions, accessibility |
| `screen01-page.css` | Scoped/responsive styling, focus/disabled/error |
| `screen01.service.ts` | HTTP data-access, typed request/error mapping |
| `screen01.model.ts` | DTO/ViewModel + pure mapper |
| `screen01-widget.ts` | UI local, input/output events; không gọi backend |
| `screen01.spec.ts` | Test UI event/state/negative paths |

**Không có screen mẫu thứ hai.** Tên `.ts/.html/.css` là ví dụ, không yêu cầu source thật sử dụng Angular; khi dự án dùng React, Flutter, Vue hoặc CLI thì sinh mirror theo file thực tế.
