# Hợp đồng nạp dữ liệu năng lực

Tài liệu này áp dụng cho mọi năng lực đã đăng ký. Điểm vào `SKILL.md` định tuyến; không đủ để thực thi một mình. Trước khi thực hiện, thêm các tài nguyên bắt buộc được liên kết trong skill vào READ_PLAN, mở đúng nội dung và đọc mẫu/checklist theo nhiệm vụ. Đọc hồ sơ dự án hiện tại và hồ sơ công nghệ đã xác minh. Không thay kiến trúc dự án bằng một ví dụ tham chiếu.

| Nhóm | Nguồn cần có | Dữ liệu phải tạo | Cổng trước bàn giao |
|---|---|---|---|
| DD API | BD/AC, catalog, schema, mã, mẫu | kiểm kê, ma trận yêu cầu, bốn ma trận trường/query/mutation/response, DD | cross-check, link, lỗi, transaction, nguồn |
| DD Screen | inventory, ảnh, route, API, source, mẫu | marker map, state/element/event, API, test | UI/kỹ thuật/QA, DD gate |
| DD Module | BD, actor, phụ thuộc, mẫu | feature/function/view/import, bốn trạng thái | truy vết, quyết định, validator |
| Coding | DD, rule, source, test | kế hoạch lá, trace, diff | validator, focused/scope tests |
| Sửa lỗi | thực tế, kỳ vọng, môi trường | tái hiện, giả thuyết, hồi quy | trước/sau, không regression |
| Test | DD, source, fixture, command | case/coverage/execution | tách kế hoạch với kết quả |
| Review | diff/path, source, rule/contract | phát hiện có căn cứ | chỉ đọc, phạm vi và giới hạn |
| Codebase | profile, rule, codebase, config | cây, hợp đồng symbol, mã nền | build/test, drift, không overwrite |
| UTC | DD, ảnh, schema, mẫu Excel | 3 nhóm test, JSON, XLSX | coverage, cấu trúc, chưa chạy nếu chỉ lập kế hoạch |

Mỗi nguồn ghi path/section/version, trạng thái đọc, độ tin cậy. Các mã ID kỹ thuật giữ nguyên. Tách kỳ vọng, hiện trạng, phê duyệt và xác minh. Khi thiếu nguồn, ghi blocker và chủ quyết định; chỉ làm phần độc lập, không tự xác nhận. Bằng chứng không được tạo từ ví dụ hoặc lệnh chưa chạy. Mọi skill mới phải được đăng ký và kiểm định checksum; chỉ dùng công cụ có trạng thái hỗ trợ thật.
