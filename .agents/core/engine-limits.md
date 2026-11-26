# Ranh giới thực thi

- Nguồn đọc có hash, ma trận truy vết và kiểm định freshness; không khẳng định tác nhân đã hiểu ngữ nghĩa chỉ từ hash.
- Kế hoạch có DAG; SQLite lưu transaction; target Markdown và worklog phiên là bản chiếu có thể sinh lại. Khóa đường dẫn chỉ hợp tác giữa các phiên dùng công cụ, không khóa hệ điều hành. Không chỉnh trực tiếp worklog đang quản lý; ghi nhận qua lệnh. Không coi đây là hệ thống chống tác nhân có toàn quyền sửa mã, DB và verifier.
- Check chỉ chấp nhận adapter định danh; pytest có JUnit và coverage theo ca thực thi thân hàm app đúng phạm vi target, Node có TAP, build phải có sản phẩm, kiểm tra DD/UTC có artifact. Contract yêu cầu nguồn đã khai báo và ID test xuất hiện trong kết quả. Vẫn cần review ngữ nghĩa và kiểm tra độc lập trong CI.
- Kết quả COMPLETED (MECHANICAL_ONLY, HUMAN_REQUIRED) là đã đạt cổng **được cấu hình và có adapter**, không phải chứng nhận sản xuất. Các tuyến thiếu adapter sẽ báo lỗi và phải giữ BLOCKED. Kiểm thử FE trình duyệt, PostgreSQL, Angular, Redis và triển khai thật chưa nghiệm thu. Không hạ cổng.
- Tệp kỹ thuật tham chiếu, codebase và hợp đồng là mẫu trung lập; ví dụ trong skill nguyên bản chỉ phục vụ học phương pháp. Không tự suy ra yêu cầu từ chúng.
- Snapshot ngoài .agents bỏ qua DB, bí mật theo tên, cache và sản phẩm build; không quét tuyệt đối mọi bí mật. Bằng chứng build/UTC/DD có hash artifact riêng; chỉ đủ nếu các nguồn và sản phẩm liên quan còn nguyên. Đọc nguồn bắt buộc không gửi nội dung bí mật vào log.

- DD chỉ đóng ở mức bản nháp khi chọn deliverable=draft, có heading/bảng/truy vết tối thiểu và đúng thư mục target; không tự phê duyệt. Test chạm mã chưa chứng minh assertion đúng hoặc yêu cầu đầy đủ.

## Điều kiện áp dụng

- Hồ sơ sinh nền: FastAPI, SQLite và TypeScript. Chưa hỗ trợ sinh Angular, PostgreSQL hoặc Redis đã kiểm chứng. Không sử dụng mã tham chiếu làm hệ thống xác thực production; chưa có đầy đủ luồng đăng nhập/cấp token, quản trị phiên, xoay khóa và phòng replay/CSRF.
- Các adapter browser, deployment, bd-report, worklog-report và utc-api chưa đầy đủ; giữ trạng thái BLOCKED khi thiếu adapter. Kiểm tra trước/sau sửa lỗi, hợp đồng và test cần đối chiếu đúng nghiệp vụ; kiểm định tĩnh không bao phủ mọi framework, import động, ORM hoặc I/O gián tiếp.
- Khóa phiên chỉ có tác dụng hợp tác trong cùng kho; chưa có khóa phân tán hoặc tự chuyển đổi phiên từ định dạng cũ. Coverage Python không bao phủ mọi tiến trình con.
- Kiểm định DD không chứng thực danh tính người phê duyệt, không kiểm chứng mọi link, marker, field hay quy tắc nghiệp vụ. Kiểm thử giao diện thực tế và triển khai phải được xác minh riêng.
