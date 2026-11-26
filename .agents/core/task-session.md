# Phiên tác vụ V11 — quy trình thực thi bắt buộc

Dùng lệnh từ root của **dự án đích**. Phiên từ định dạng cũ không tự chuyển đổi; giữ nhật ký lịch sử và dùng ID mới. SQLite lưu dữ liệu chính; target và worklog sinh lại bằng sync. Mọi lệnh kiểm tra chỉ áp dụng vào repo được phép.

```bash
python3 .agents/tools/task.py plan coding-api
python3 .agents/tools/task.py begin coding-api --id T001 --title "Kiểm tra API mẫu"
python3 .agents/tools/task.py declare T001 --path backend/docs/contract-trace.json --section "toàn bộ" --reason "truy vết test"
python3 .agents/tools/task.py declare T001 --path backend/docs/dd/API-001/02-overview.md --section "toàn bộ" --reason "nguồn quyết định"
python3 .agents/tools/task.py declare T001 --path backend/docs/dd/API-001/03-request.md --section "toàn bộ" --reason "hợp đồng đầu vào"
python3 .agents/tools/task.py declare T001 --path backend/docs/dd/API-001/06-errors.md --section "toàn bộ" --reason "hợp đồng lỗi"
python3 .agents/tools/task.py load T001
python3 .agents/tools/task.py target T001 --key T01 --name "Kiểm chứng API" --accept "Hợp đồng, kiến trúc, test và context" --checks contract architecture api-test context --paths backend
python3 .agents/tools/task.py start T001
python3 .agents/tools/task.py check T001 --key T01 --kind contract --params '{"path":"backend/docs/contract-trace.json"}'
python3 .agents/tools/task.py check T001 --key T01 --kind architecture
python3 .agents/tools/task.py check T001 --key T01 --kind api-test --params '{"cwd":"backend","tests":"tests"}'
python3 .agents/tools/task.py check T001 --key T01 --kind context
python3 .agents/tools/task.py verify T001 --key T01
python3 .agents/tools/task.py finish T001 --summary "Đạt các cổng cơ học đã đăng ký, chờ review ngữ nghĩa"
```

Trước `load`, chạy build-context.py --refresh khi được phép và đọc nội dung đã khai báo; bổ sung các tệp source/caller/callee/BD/DD cụ thể. `load` chỉ băm và xác nhận truy xuất, không làm thay bước đọc hiểu. Phụ thuộc target khai báo bằng `--deps T01 T02`. `status` xem trạng thái và tiến độ từ receipt; không tăng % tùy ý. `verify` thay lệnh evidence tự khai V10. `reopen` mở lại target và hậu duệ khi evidence hết hạn. `conflict` chặn phiên, `resolve` ghi quyết định được duyệt. `block`/`resume` phục hồi; nếu có kế hoạch thì gọi `start` lại. `sync` dựng lại bản chiếu sau gián đoạn. Cần hợp đồng được duyệt riêng, không gắn nhãn approved chỉ do validator PASS.

## Adapter và phạm vi

`api-test`, `regression`, `integration`, `migration` dùng pytest với JUnit và coverage theo ca; `coverage_source` chọn package Python trong `cwd` (mặc định `app`), regression/integration/migration phải chọn ca cụ thể. `fe-test` dành cho lát cắt TypeScript; `build` hỗ trợ TypeScript hoặc `runtime=python-uv` với tên package workspace. `architecture` kiểm định tĩnh Python/TypeScript; chế độ mặc định giữ cả hai ứng dụng, còn `backend_only=true` nhận `backend_package` và tùy chọn `allow_empty_modules` cho nền chưa có module nghiệp vụ. `context` so sánh SOURCE_MAP; `contract` kiểm tra cấu trúc truy vết và ID ca test; `dd-api`, `dd-screen`, `dd-module` kiểm tra cấu trúc, không tự duyệt nghiệp vụ; `utc` so workbook với dữ liệu tái tạo; `review-report` kiểm tra báo cáo JSON trong .agents/review-reports mà không chạy test. Các loại còn thiếu adapter không thể hoàn thành bằng mã thoát tùy ý. Quy định G0–G6 vẫn bắt buộc.

## Quy định bản phát hành

- `--paths` bắt buộc, là đường dẫn cụ thể trong kho; chuẩn hóa trước khi khóa. Với DD phải khai báo đúng thư mục sản phẩm, không chỉ thư mục cha. Khóa hợp tác giữ đến khi kết thúc phiên. Không dùng chung ID phiên cũ.
- Ví dụ kiểm tra DD: `python3 .agents/tools/task.py check T001 --key T01 --kind dd-module --params '{"path":"docs/dd/M01","template":"original","deliverable":"draft"}'`. Chỉ đóng nhiệm vụ giao bản nháp đã qua kiểm định cấu trúc; không chứng nhận Approved. `COMPLETED` đi kèm `acceptance_level=MECHANICAL_ONLY`, `semantic_review=HUMAN_REQUIRED`.
- Pytest cần `coverage` và `pytest-cov`; receipt có JUnit và coverage theo từng ca chạy. Mỗi ca được dùng trong truy vết phải thực thi thân hàm ứng dụng thuộc phạm vi target. `test`, `test-api`, `test-integration` yêu cầu thêm cổng contract. Ca chạy ở tiến trình con không có coverage được cấu hình sẽ bị chặn. Coverage không thay thế kiểm tra nội dung assertion.
- Khi target contract và target test tách riêng, target test phải phụ thuộc target contract. Đường dẫn, hash, mã phiên, mã target và phạm vi được gắn vào receipt. Root `AGENTS.md` là nguồn bắt buộc. Chưa có bằng chứng máy về hiểu ngữ nghĩa.
