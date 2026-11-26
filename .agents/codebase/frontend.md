# Đặc tả nền ứng dụng khách
Tên tệp và biểu tượng dưới đây là hợp đồng trách nhiệm của nền được tạo, không phải khẳng định nguồn hiện hành. Chọn thành phần theo phạm vi được duyệt. Khi hiện thực, bổ sung chữ ký kiểu cụ thể, trạng thái, lỗi và ca kiểm thử theo `symbol-contract.md`.
| Tệp | Biểu tượng | Đặc tả |
|---|---|---|
| [`src/main.*`](frontend/01-src-main.md) | `bootstrap()` | Quyền sở hữu, đầu vào/ra, lỗi và kiểm thử theo trang chi tiết. |
| [`src/app/app.routes.*`](frontend/02-src-app-app-routes.md) | `appRoutes` | Quyền sở hữu, đầu vào/ra, lỗi và kiểm thử theo trang chi tiết. |
| [`core/constant/api.constants.*`](frontend/03-core-constant-api-constants.md) | `ApiDescriptor`, `ApiMethod / API_BASE_PATH` | Quyền sở hữu, đầu vào/ra, lỗi và kiểm thử theo trang chi tiết. |
| [`core/http/api-envelope.*`](frontend/04-core-http-api-envelope.md) | `ApiEnvelope<T>` | Quyền sở hữu, đầu vào/ra, lỗi và kiểm thử theo trang chi tiết. |
| [`core/http/api-client.service.*`](frontend/05-core-http-api-client-service.md) | `request<T>(descriptor, input)`, `requestWithResponse<T>(descriptor, input)`, `resolveApiPath(descriptor, parameters)`, `assertClientCallable(descriptor)` | Quyền sở hữu, đầu vào/ra, lỗi và kiểm thử theo trang chi tiết. |
| [`core/http/<nhom>-api.service.*`](frontend/06-core-http--nhom--api-service.md) | `request<T>(descriptor, input)` | Quyền sở hữu, đầu vào/ra, lỗi và kiểm thử theo trang chi tiết. |
| [`core/auth/<nhom>-session.service.*`](frontend/07-core-auth--nhom--session-service.md) | `login(credentials)`, `acceptLoginEnvelope(response)`, `getAccessToken()`, `refreshAccessToken()`, `endLocalSession()` | Quyền sở hữu, đầu vào/ra, lỗi và kiểm thử theo trang chi tiết. |
| [`core/auth/authorization-error.*`](frontend/08-core-auth-authorization-error.md) | `AuthorizationError` | Quyền sở hữu, đầu vào/ra, lỗi và kiểm thử theo trang chi tiết. |
| [`core/localStorage/local-storage.service.*`](frontend/09-core-localStorage-local-storage-service.md) | `setItem<T>(key, value)`, `getItem<T>(key)`, `removeItem(key)` | Quyền sở hữu, đầu vào/ra, lỗi và kiểm thử theo trang chi tiết. |
| [`layouts/<nhom>/<nhom>-layout.*`](frontend/10-layouts--nhom---nhom--layout.md) | `LayoutComponent` | Quyền sở hữu, đầu vào/ra, lỗi và kiểm thử theo trang chi tiết. |
| [`shared/ui/<thanh_phan>.*`](frontend/11-shared-ui--thanh_phan.md) | `Component` | Quyền sở hữu, đầu vào/ra, lỗi và kiểm thử theo trang chi tiết. |
| [`features/<nhom>/<nhom>.route.*`](frontend/12-features--nhom---nhom--route.md) | `groupRoutes` | Quyền sở hữu, đầu vào/ra, lỗi và kiểm thử theo trang chi tiết. |
| [`features/<nhom>/<ma>/data-access/<ma>.service.*`](frontend/13-features--nhom---ma--data-access--ma--service.md) | `ScreenService.load(input)`, `ScreenService.submit(input)` | Quyền sở hữu, đầu vào/ra, lỗi và kiểm thử theo trang chi tiết. |
| [`features/<nhom>/<ma>/models/<ma>.model.*`](frontend/14-features--nhom---ma--models--ma--model.md) | `ScreenModel / ViewState`, `mapDtoToViewModel(dto)` | Quyền sở hữu, đầu vào/ra, lỗi và kiểm thử theo trang chi tiết. |
| [`features/<nhom>/<ma>/pages/<ma>-page.*`](frontend/15-features--nhom---ma--pages--ma--page.md) | `ScreenPage`, `init()/load()`, `onEvent(event)`, `dispose()` | Quyền sở hữu, đầu vào/ra, lỗi và kiểm thử theo trang chi tiết. |
| [`features/<nhom>/<ma>/ui/<thanh_phan>.*`](frontend/16-features--nhom---ma--ui--thanh_phan.md) | `ScreenWidget` | Quyền sở hữu, đầu vào/ra, lỗi và kiểm thử theo trang chi tiết. |
