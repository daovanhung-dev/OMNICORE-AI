# Tiếp nhận và khóa nguồn thiết kế API

## 1. Phạm vi và kiểm kê đầu vào

Mỗi đợt thiết kế phải lập bảng sau trước khi viết bất kỳ nội dung hợp đồng nào. Mở nguồn nén bằng công cụ giải nén an toàn, giới hạn kích thước và đường dẫn; không thực thi macro, HTML hoặc mã trong nguồn. Duyệt thư mục con và archive lồng trong phạm vi được cho phép. Với PDF kiểm tra trang/sơ đồ, với bảng tính kiểm tra sheet ẩn, công thức, merged cells và đơn vị; với ảnh đối chiếu chú thích và quan hệ; với mã đọc symbol, call sites, config, test và revision. Không coi tên file hoặc kết quả tìm kiếm là đã đọc nội dung.

| Mã nguồn | Đường dẫn | Loại | Phiên bản/hash | Chủ sở hữu | Phạm vi trang/sheet/symbol | Trạng thái đọc | Liên quan API | Giới hạn |
|---|---|---|---|---|---|---|---|---|

Mỗi API có bảng độ bao phủ: nguồn bắt buộc, nguồn đã đọc, nguồn thiếu, phần chưa đọc và lý do. Không báo hoàn tất nếu còn nguồn ảnh hưởng behavior chưa đọc. Nếu nguồn không truy cập được, ghi nguyên nhân, tác động và điều kiện gỡ chặn.

## 2. Phân loại và ưu tiên

Hành vi mong muốn: yêu cầu mới nhất được xác nhận → BD/AC/quyết định thiết kế đã duyệt → hợp đồng API đã duyệt. Hành vi hiện tại: source/runtime đã kiểm tra → test đã chạy và kết quả → config/hợp đồng thực thi → tài liệu hiện trạng. Hai trục độc lập; nếu catalog, sơ đồ, schema và source khác nhau lập bảng chênh lệch, không tự ưu tiên source cho thiết kế mới. Đánh dấu bằng chứng trực tiếp, suy dẫn có căn cứ, đề xuất, thiếu nguồn. Suy dẫn không thành yêu cầu đã duyệt.

## 3. Cổng mẫu

Tìm mẫu người dùng chỉ định, mẫu duyệt của dự án, mẫu đăng ký trong manifest, sau đó mẫu chuẩn đi kèm. Mở toàn bộ file mẫu và kiểm tra thứ tự, front matter, heading, bảng, code fence, anchor, link, placeholder, mục bắt buộc/tùy chọn, quy ước nhiều bảng. Ghi SHA-256 nếu có. Không tự tạo mẫu thay thế khi mẫu được yêu cầu bị thiếu/hỏng. Khi có nhiều mẫu, lập bảng ứng viên: path, khả năng đọc, file lõi, phiên bản, trạng thái duyệt, phù hợp, lý do chọn. Mẫu thực tế đã duyệt ưu tiên hơn ví dụ; không tự đổi tên sheet/file. Nếu phải chuyển đổi cấu trúc, lưu ánh xạ và yêu cầu xác nhận.

## 4. Khóa định nghĩa tác vụ

| API ID | Module/chủ sở hữu | Phương thức | Đường dẫn | Người gọi | Xác thực | Phân quyền | Mục đích | Input | Output | Bảng đọc | Bảng ghi | Tác động | Nguồn | Thư mục | Trạng thái |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

Khóa quy ước cả đợt: envelope, mã nghiệp vụ, mã HTTP, trace ID, phân trang, filter, sort, thời gian/múi giờ, null/rỗng/bỏ qua, token, idempotency, giao dịch, audit, soft delete, tên thư mục, phương thức bàn giao. Mỗi API một thư mục. Không tự thêm endpoint chỉ vì sơ đồ có hành động tương tự.

## 5. Xử lý câu hỏi và xung đột

| Mã | Nguồn A | Nguồn B | Dữ kiện xung đột | API/trường/bước ảnh hưởng | Mức chặn | Chủ quyết định | Phương án | Quyết định/bằng chứng |
|---|---|---|---|---|---|---|---|---|

Thiếu quyết định về path/method, input/output, quyền, schema, chuyển trạng thái, transaction hoặc lỗi làm thay đổi client thì chặn phần phụ thuộc. Tiếp tục phần độc lập; không tự tạo cột vì response cần cột đó. Câu hỏi không chặn (mô tả, chính tả, sắp xếp tài liệu) có thể xử lý theo quy chuẩn. Trình bày đề xuất riêng và không gắn nhãn đã duyệt.
