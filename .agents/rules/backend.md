# Quy tắc lập trình máy chủ

## BE-01 — Khai báo mô hình
`models.*` là nơi duy nhất khai báo DTO, kiểu dữ liệu, enum, trường, giá trị mặc định có căn cứ, cấu trúc phản hồi và ánh xạ thuần riêng API. Không SQL, I/O, kiểm tra nghiệp vụ theo trạng thái, giao dịch hay sinh phản hồi HTTP. Mô hình dùng chung thuộc hợp đồng dùng chung. Không khai báo trùng DTO trong view.

## BE-02 — Kiểm tra và trả lỗi đầu vào
`validate.*` kiểm tra bắt buộc, rỗng, định dạng, độ dài, khoảng giá trị, enum, phân trang, ID và điều kiện giữa trường; chuẩn hóa đầu vào. Tất cả điều kiện và mã lỗi đầu vào theo DD; gọi bộ phản hồi chung hoặc trả lỗi có kiểu để view chuyển tiếp. Hàm dùng chung thuộc `utils/validate`. Không thực thi SQL, gọi dịch vụ, ghi dữ liệu hoặc commit. Lỗi cần trạng thái DB phải được đánh giá ở view; có thể tách điều kiện thuần thành hàm kiểm tra nhận dữ liệu đã đọc. Không suy đoán lỗi hoặc dùng ngoại lệ chung làm luồng nghiệp vụ nếu hợp đồng không cho phép.

## BE-03 — Định nghĩa truy xuất
`query.*` chỉ chứa câu SQL tham số hóa hoặc thao tác truy xuất khai báo theo ORM đã chọn. Không nhận session để tự commit, không tạo phản hồi HTTP, không kiểm tra nghiệp vụ. Cấm nối chuỗi từ đầu vào không tin cậy. Tên cột sắp xếp chọn qua danh sách cho phép. Truy vấn đếm và danh sách đồng nhất bộ lọc; thứ tự ổn định; điều kiện tenant/quyền sở hữu, xóa mềm, khóa và ràng buộc phải có bằng chứng từ lược đồ.

## BE-04 — Điều phối API
`view.*` sở hữu use case: xác thực/quyền trước truy xuất bảo vệ, gọi validator, gọi DB/dịch vụ, kiểm tra tồn tại/trạng thái/quyền đối tượng, quản lý giao dịch, ánh xạ và trả phản hồi chuẩn. Không lặp khai báo, SQL hoặc validator. Chỉ commit sau khi xác minh kết quả và ánh xạ phản hồi thành công; rollback khi lỗi. Tác vụ ngoài DB cần chiến lược nhất quán/idempotency phù hợp, không giả định rollback DB hoàn tác dịch vụ ngoài. Mã lỗi nghiệp vụ và HTTP theo hợp đồng. Chú thích ngắn tiếng Việt tại bước quan trọng, không giải thích lại cú pháp.

## BE-05 — Tuyến và nền tảng
`api/v1` chỉ đăng ký tuyến, phương thức, phụ thuộc và chuyển tham số; `main` quản lý vòng đời, middleware, xử lý lỗi, health. Core không nhập module nghiệp vụ. Cấu hình kiểm tra khi khởi động; không lộ bí mật. DB helper quản lý kết nối/session, tham số và giải phóng; không tự commit. Bộ thích nghi dịch vụ có timeout và lỗi có kiểu. Xác thực/phân quyền máy chủ là thẩm quyền; guard giao diện không thay thế.

## BE-06 — Kiểm thử
Đọc API DD, lược đồ, tuyến, điểm gọi và kiểm thử. Bao phủ thành công, sai đầu vào, chưa xác thực, không đủ quyền, không tồn tại, xung đột, lỗi phụ thuộc, rollback và idempotency khi áp dụng. Xác minh không ghi dữ liệu khi bị từ chối. Kiểm tra import, đăng ký tuyến, hợp đồng, kiểm thử tập trung, bộ kiểm thử liên quan, lint/typecheck. Session giả không chứng minh SQL/lược đồ thật. Ghi lệnh, mã thoát, môi trường, kết quả.

## BE-07 — Ngoại lệ
Bốn trách nhiệm không đổi theo công nghệ; phần không áp dụng phải được khai báo thay vì tạo logic giả. Không ép ORM thành SQL thô. Quyết định kiến trúc được phê duyệt là căn cứ ngoại lệ.

## Mã kiểm định tự động

BE-001: bốn tệp; BE-002: không khai báo lớp ở view; BE-003: không I/O ở model/validate/query; BE-005: query khai báo; BE-007: SQL ngoài query; BE-010: phụ thuộc ngược. Đây là ánh xạ kiểm định tĩnh của BE-01–07, không thay thế review ngữ nghĩa. Ví dụ sai: `view.py` chứa chuỗi `SELECT ...`; đúng: định nghĩa chuỗi tại query và import vào view. Sai: `validate` gọi `db.execute`; đúng: nhận dữ liệu đã đọc để kiểm tra điều kiện thuần.

## BE-08 — Phân biệt kiểm tra đầu vào và kiểm tra có dữ liệu
Theo quy trình nguồn, xác thực/guard dùng chung trước truy xuất bảo vệ; validator riêng chỉ trả dữ liệu chuẩn hóa hoặc lỗi chuẩn, không đọc DB. Khi cần kiểm tra quyền đối tượng, trạng thái hoặc tính tồn tại từ DB, view đọc dữ liệu rồi gọi predicate thuần trong validate hoặc policy đã được duyệt. View điều phối lỗi hệ thống, giao dịch và ánh xạ phản hồi; không đặt I/O vào validate chỉ để ép quy tắc. Với hồ sơ SQL thuần, query chỉ chứa hằng chuỗi truy vấn; bind tham số và gọi DB nằm tại view. Mô hình chỉ khai báo lớp và chuyển đổi dữ liệu, không tự chuẩn hóa hay kiểm tra nghiệp vụ. API không đọc DB có thể không có query, API chỉ dùng guard chung có thể không cần validator riêng **trong kho mã hiện hữu** nếu khai báo ngoại lệ. Codebase mới mặc định có đủ bốn tệp; không tạo SQL giả. Các hồ sơ Express/ORM hay mobile khác phải theo kiến trúc đã được duyệt, không ép mẫu FastAPI vào mọi kho.
