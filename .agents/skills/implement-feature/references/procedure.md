# Quy trình — Feature implementation

## Tiền kiểm

- Lấy hiện trạng branch/status/diff; hiểu dirty file ownership; không reset/clean/checkout.
- Requirement + DD/AC/rule đã duyệt, routes/DTO/DB migrations, stack versions, auth/permission, source tests, CI commands. So expected/current và ghi discrepancies.
- Dò existing components/helpers/repos trước khi tạo mới. Xác định scope và thiết kế cross-boundary nếu có.

## Trace before patch

`Caller → Router/handler → Principal/authorization → Validation → Use-case → Query/DB/external side effect → Response → Consumer state → Test`. Ghi file/symbol cụ thể, không suy ra behavior từ tên file.

## Implementation sequence

1. Chốt plan với steps / dependency / acceptance / rollback khi phù hợp.
2. Làm vertical slice hẹp nhất; model/contract đúng, server policy có authority, UI displays correct loading/error/empty.
3. Tại client: route/page → typed data-access → shared HTTP → ViewModel; không gọi network trong presentational component nếu architecture cấm.
4. Tại server: DTO/guard/validator → application service → repository/provider → transaction/error response; không ép Python 4-file pattern vào Express hoặc ngược lại.
5. Thay contract phải làm compatibility audit và update producer/consumer docs trước khi bật behavior chưa có API.
6. Gắn targeted tests, chạy unit/contract/build/lint theo scope, rồi kiểm tra diff. Không coi build compile là test API live.
7. Update worklog, docs, architecture/manifest khi wiring thay đổi thật. Ghi file changed, limitation và next actions.

## Blockers

Permission, DB schema, external provider, API source, state machine chưa có nguồn → chỉ triển khai phần độc lập, để UI gate/disabled trung thực. Không mock thành dữ liệu thành công.
