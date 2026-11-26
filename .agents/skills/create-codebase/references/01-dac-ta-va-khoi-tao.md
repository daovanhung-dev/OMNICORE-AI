# Hợp đồng sinh nền và đồng bộ codebase

## Cổng đầu vào

Xác định công nghệ/version, công cụ package/lock, loại app/deployable, DB/provider, mô hình auth, HTTP/envelope, lệnh build/test, quyền ghi, dữ liệu và môi trường. Đọc project profile, architecture, rules, codebase và technology profile. Chỉ sinh thành phần có nhu cầu; không tự thêm business feature. Kiểm kê hiện có trước khi thay đổi, không overwrite. Chọn `fastapi-typescript` khi đã được duyệt; các profile khác là đặc tả, không claim generator hoặc runtime đã hỗ trợ.

| Thành phần | Lớp | File | Symbol | Hợp đồng | Phụ thuộc | Lỗi/vòng đời | Test | Bắt buộc/không áp dụng |
|---|---|---|---|---|---|---|---|---|

Mỗi symbol khai báo chữ ký tham số/kiểu/giá trị trả về, tiền/hậu điều kiện, thuật toán từng bước, error, side effects, caller/callee, vòng đời, bảo mật, test, code reference; không coi AST inventory là đặc tả behavior. Kiểm tra hàm mũi tên/phương thức/namespace/class, tên trùng phân biệt theo scope; parser chưa hỗ trợ ghi thiếu thay vì suy bằng regex. Chọn source thực tế và đối chiếu với manifest/hash.

## Trình tự ghép

BE: config/env → vòng đời main → logging/trace/error/response → DB/session nếu dùng → guard/auth nếu dùng → router → validator/query/view/models → test. FE: config/router → http client/envelope → session/guard nếu dùng → layout/theme/shared → models/data-access/pages/ui → test. Shared contract producer/consumer được xác minh trước khi nối. Định danh, lỗi, route, schema và default lấy từ DD. Không đưa token hoặc DB thật vào env mẫu, không cài package ngoài quyền. DB seed chỉ local cô lập.

## Lệnh và nghiệm thu

Dùng `python3 .agents/tools/create-codebase.py --destination <thu-muc-moi> --profile fastapi-typescript`. Đọc [mã tham chiếu](../../../reference/README.md), [hồ sơ công nghệ](../../../technology-profiles/INDEX.md). Không ghi đè đích. So sánh cây sinh lặp với cùng input; kiểm định kiến trúc, import, build/type, unit và HTTP; browser test nếu có môi trường. Ghi lỗi dependency không tải được. Chạy context inventory/sync, kiểm tra drift và hồ sơ symbol. Mã mẫu không chứng minh auth/DB production hay framework khác. Đầu ra gồm source, lock/config phù hợp, tài liệu, test, log, trạng thái từng capability.
