# Hợp đồng chi tiết lát cắt tham chiếu

Phạm vi chỉ gồm mã thật trong `reference/backend/app` và `reference/frontend/src`. Chữ ký dưới đây là của hồ sơ đã chọn, không ép hồ sơ khác dùng SQLite hay DOM. Định nghĩa nghiệp vụ mẫu công khai chỉ đọc. Mọi API thật phải xác định quyền, dữ liệu và hợp đồng riêng. Mỗi đường dẫn tương đối thuộc thư mục BE hoặc FE tương ứng. Các kiểm thử ghi tên hàm có trong gói; kiểm thử trình duyệt chưa phải bằng chứng đạt nếu môi trường chặn.

## Backend

| Tệp và biểu tượng | Chữ ký, thuật toán, đầu ra và lỗi | Phụ thuộc, vòng đời, kiểm thử |
|---|---|---|
| `app/core/config.py` — `Settings` | `Settings(database_path: Path, token_config: TokenConfig | None = None, protected_items: bool = False)`; bất biến sau khởi tạo; đường dẫn tuyệt đối. `__post_init__(self) -> None` từ chối đường dẫn tương đối bằng ValueError. | Được tạo tại app_factory hoặc test; không log cấu hình token; test thiếu DB và protected mode. |
| `app/core/database.py` — `get_db` | `get_db(settings: Settings) -> Iterator[sqlite3.Connection]`; mở URI mode=ro; gắn Row; yield; finally đóng. Không commit, không tạo DB mới. Lỗi SQLite truyền tới view. | Chỉ view gọi; một vòng đời mỗi request; `test_missing_db`, `test_invalid_precedes_db`. |
| `app/core/responses.py` — `Envelope[T]` | Mô hình Pydantic generic với `data: T`; xác thực dữ liệu khi khởi tạo; không I/O. | DTO phản hồi; test_success. |
| `ErrorDetail` | `code: str`, `message: str`; không trả trace hay driver message. | ApiError; test_invalid. |
| `ErrorEnvelope` | `error: ErrorDetail`; mã HTTP ở transport, không trộn vào business code. | Handler, OpenAPI; test_invalid/test_missing_db. |
| `ApiError.__init__` | `(self, status: int, code: str, message: str) -> None`; khởi tạo Exception(code), lưu status và ErrorDetail. Không tự gửi HTTP. | Validator/view; lỗi tồn tại trong vòng đời request. |
| `handle_error` | `async (request: Request, exc: ApiError) -> JSONResponse`; chuyển ErrorEnvelope.model_dump() thành JSON, dùng status có sẵn; không ghi DB. | FastAPI exception handler; kiểm thử HTTP 422/503. |
| `app/modules/shared/api_001_items_list/models.py` — `ListParams` | `page: int` 1–100000; `page_size: int` 1–100; kiểu; giới hạn nghiệp vụ thuộc validate. | Validator tạo; không quyết định HTTP. |
| `Item` | `id: int`, `name: str`; ánh xạ hàng SQLite, không gọi DB. | View tạo; test_success. |
| `ItemPage` | `items: list[Item]`, `total`, `page`, `page_size`: int; mảng rỗng hợp lệ. | View tạo; test_pagination/test_empty. |
| `ItemResponse` | Bí danh `Envelope[ItemPage]`; schema phản hồi API. | Router và view dùng cùng kiểu. |
| `validate.py` — `validate_params` | `(page: str, page_size: str) -> ListParams`; regex ASCII giới hạn chiều dài trước int; kiểm khoảng; sai ném ApiError 422 INVALID_PAGE; đúng trả DTO. | Không SQL/side effect; sáu biến thể test_invalid; validation trước DB. |
| `query.py` — `COUNT_ITEMS`, `LIST_ITEMS` | Hằng chuỗi; đếm toàn bảng; danh sách ORDER BY id LIMIT ? OFFSET ?. Không nối đầu vào, không chạy truy vấn. | View truyền bind page_size, offset; test_pagination. |
| `view.py` — `list_items` | `(settings: Settings, page: str, page_size: str) -> ItemResponse`; validate → mở DB chỉ đọc → BEGIN → count → list → ánh xạ Item → tạo ItemPage → đóng. SQLite error chuyển 503 DATA_UNAVAILABLE. | Không ghi; count/list cùng giao dịch; lỗi không lộ chi tiết; toàn bộ test_items. |
| `app/api/v1.py` — `items` | `(request: Request, page: str = '1', page_size: str = '20') -> ItemResponse`; guard_items kiểm tra quyền tùy cấu hình; handler chỉ lấy settings từ app.state và chuyển tiếp. | Router GET `/api/v1/items`; tests gọi endpoint. |
| `app/main.py` — `create_app` | `(settings: Settings) -> FastAPI`; khởi tạo app, lưu settings, gắn error handler, middleware trace, health và router. | Test fixture tạo app độc lập; không mở DB khi khởi tạo. |
| `app_factory` | `() -> FastAPI`; lấy biến DEMO_DB, resolve đường dẫn, gọi create_app; thiếu biến lỗi khởi động, không mặc định vào production. | Uvicorn factory; lệnh smoke HTTP. |
| `seed.py` — `seed` | `(path: Path) -> None`; tạo tệp mới bằng xb, tạo schema và hai hàng trong giao dịch; lỗi xóa đúng tệp mới. Nếu đã có tệp, từ chối trước ghi. | Chỉ dùng DB cô lập; test_seed_no_overwrite, fixture. |

## Frontend

| Tệp và biểu tượng | Chữ ký, xử lý, kết quả/lỗi | Phụ thuộc, vòng đời, kiểm thử |
|---|---|---|
| `src/main.ts` | Điểm vào; lấy HTMLElement `#app`; thiếu vùng hiển thị ném Error; gọi mountRoute với location.pathname. | Không truy cập API trực tiếp. |
| `src/app/app.routes.ts` — `mountRoute` | `(root: HTMLElement, path: string) -> void`; `/` và `/items` lắp layout/trang và gọi load; tuyến khác hiển thị không tìm thấy. | Nhập route nhóm và layout; kiểm tra trực tiếp/gốc bằng browser_check. |
| `layouts/shared/layout.ts` — `mountLayout` | `(root: HTMLElement) -> HTMLElement`; tạo div outlet, thay con root, trả outlet. | Không gọi HTTP. |
| `features/shared/shared.route.ts` — `mountShared` | `(root: HTMLElement) -> ItemPageController`; tạo controller cho screen. | Chỉ nhóm sở hữu tuyến; app routes gọi. |
| `core/http/api-client.ts` — `getJson` | `(path: string, signal: AbortSignal, timeoutMs = 10000) -> Promise<unknown>`; chỉ đường dẫn API nội bộ, Bearer từ bộ nhớ, timeout, cancellation, HTTP lỗi có kiểu, 401 xóa phiên. | Data-access gọi; không tự retry, không lưu token lâu dài. |
| `SH01/models/item.model.ts` — `Item` | Interface `id: number`, `name: string`; chỉ định nghĩa kiểu. | UI dùng để render. |
| `ItemPage` | Interface `items: Item[]`, `total`, `page`, `page_size`: number. | Page nhận sau decode; data-access trả dữ liệu thô. |
| `decodePage` | `(raw: unknown) -> ItemPage`; xác nhận object có data, mảng, item id nguyên an toàn, name string, số phân trang hợp lệ; sai ném Error; không DOM/HTTP. | Page gọi; kiểm thử Node riêng. |
| `SH01/data-access/item.service.ts` — `fetchItems` | `(page: number, signal: AbortSignal) -> Promise<unknown>`; URLSearchParams page + page_size=1; gọi getJson, giữ dữ liệu thô. | Page gọi; signal do page sở hữu; không đổi DOM. |
| `SH01/ui/item-list.ts` — `renderItems` | `(container: HTMLElement, items: Item[]) -> void`; tạo ul/li; gán textContent; thay con container. | Page gọi; tên dữ liệu không bị diễn giải thành HTML. |
| `SH01/pages/item-page.ts` — `ItemPageController` | Lớp sở hữu root, page hiện tại, AbortController và DOM status/list/next/previous/retry. Bất biến: phản hồi chỉ cập nhật khi request còn là request hiện tại. | Được tạo ở route nhóm; không tự lưu dữ liệu toàn cục. |
| `ItemPageController.constructor` | `(root: HTMLElement)`; tạo tiêu đề, trạng thái có role=status, nút; nối sự kiện gọi load; thay nội dung root. | Trình duyệt; không gọi HTTP cho đến load. |
| `ItemPageController.load` | `async (page: number = 1) -> Promise<void>`; hủy yêu cầu cũ, khóa nút, trạng thái tải; gọi fetchItems; bỏ kết quả cũ; gọi decodePage; cập nhật trang/trạng thái/danh sách; khóa nút theo biên; lỗi hiện thông báo nếu request hiện hành chưa hủy. | Browser_check: tải, trước/sau, lỗi và thử lại, rỗng. |
| `ItemPageController.destroy` | `() -> void`; hủy request, xóa root; không giữ node hiển thị. | Gọi khi chủ sở hữu tháo trang; mẫu điều hướng full-page do trình duyệt giải phóng. |

## Giới hạn và phần tùy chọn

Đặc tả cơ sở dữ liệu pool, JWT, refresh token, mật khẩu, mail, AI, lưu trữ đối tượng và quản lý phiên trong các trang codebase khác là hợp đồng logic cần lựa chọn theo yêu cầu. V11 đã triển khai JWT tùy chọn, refresh store SQLite, migration, trace và cache TTL; PostgreSQL pool, Redis và đăng nhập thực tế vẫn chưa triển khai. Không đánh dấu chúng đã chạy hoặc sinh các chính sách bảo mật mặc định cho dự án mới.

## Nền bổ sung V11 — hợp đồng symbol

| Tệp / symbol | Input → xử lý → output / lỗi | Caller, kiểm thử |
|---|---|---|
| security.py / TokenConfig, __post_init__ | secret ≥32 byte, issuer/audience không rỗng, ttl 1–900 giây; bất biến; repr không lộ secret; sai ValueError | app_factory, test_protected |
| Principal | subject: str, roles: tuple[str,...]; immutable; không I/O | authenticate, policy |
| issue_access | config, Principal → HS256 typ access, jti, exp, iat, nbf → str; sai định danh ValueError | caller tin cậy sau đăng nhập, test_protected |
| authenticate | Authorization Bearer → kiểm chữ ký, issuer, audience, thời hạn và claims → Principal; sai ApiError 401 | guard_items, test_jwt_wrong_audience, test_jwt_expired |
| require_role | Principal và frozenset → kiểm giao quyền; thiếu 403 | guard_items, test_protected |
| require_owner | Principal và owner → so chủ thể; thiếu 403 | policy đối tượng, test_owner |
| dependencies.py / guard_items | Request → đọc settings → xác thực/quyền nếu protected; không đọc DB | router, test_protected |
| refresh_tokens.py / token_digest | token → SHA-256 hex | RefreshStore, test_refresh_and_migration |
| RefreshStore.__init__ | path DB đã migration → lưu path, không mở kết nối | caller kỹ thuật |
| RefreshStore.issue | subject, ttl → token opaque ngẫu nhiên; lưu hash, expiry; lỗi DB rollback | test_refresh_and_migration |
| RefreshStore.rotate | token → BEGIN IMMEDIATE, đọc hạn, xóa cũ, chèn hash mới cùng hạn; trả subject, token mới; token sai 401 | test_refresh_and_migration |
| RefreshStore.revoke | token → xóa đúng hash, không xóa phiên khác | test_refresh_and_migration |
| migration.py / migrate | path tồn tại, folder SQL tin cậy → đọc phiên bản/hash, áp dụng mỗi phiên bản nguyên tử → list[int]; lỗi checksum/SQL rollback | test_refresh_and_migration, test_migration_rollback |
| cache.py / TTLCache.__init__ | maxsize dương, RLock, OrderedDict | test_cache |
| TTLCache.get | key → kiểm expiry monotonic, cập nhật LRU, trả value hoặc None | test_cache |
| TTLCache.set | key/value/ttl dương → lưu, loại mục cũ quá giới hạn | test_cache |
| TTLCache.invalidate | key → xóa đúng mục nếu có | test_cache |
| observability.py / trace_request | Request, call_next → ID ngẫu nhiên, log method/status/duration, gắn X-Request-ID; không ghi header/body | middleware, test_protected |
| main.py / live, ready | live trả status ok; ready thử đọc bảng items, lỗi SQLite trả 503 | test_health |
| core/auth/session.ts / setAccessToken, getAccessToken, clearSession | token tùy chọn → lưu/đọc/xóa bộ nhớ module; không localStorage | getJson, http-auth-and-401 |
| core/http/api-client.ts / HttpError | status, traceId → Error có kiểu, không log token | getJson, http-auth-and-401 |
| shared/components/button.ts / button | label, callback tùy chọn → HTMLButtonElement type=button, textContent, event listener | ItemPageController; browser chưa xác minh |
| getJson | đường dẫn /api/, AbortSignal, timeout → header Bearer tùy chọn, fetch, lỗi HttpError, xóa token 401, hủy timer/listener finally | fetchItems, test http-auth-and-401/external-path/timeout |

Các thành phần kỹ thuật này chưa thay thế quản lý định danh thật, rotation key, refresh family replay detection, CSRF, Redis, pool PostgreSQL hoặc policy production. Không dùng khóa test hoặc quyền mẫu làm mặc định thật.
