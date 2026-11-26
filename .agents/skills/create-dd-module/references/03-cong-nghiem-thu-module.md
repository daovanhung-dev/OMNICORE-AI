# Nghiệm thu và bàn giao module

| Cổng | Tiêu chí | Bằng chứng |
|---|---|---|
| Sẵn sàng | nguồn BD, ID, scope, owner, phụ thuộc và mẫu đủ | bảng nguồn |
| Soạn thảo | đầy đủ 9 tệp, chức năng/luồng/quyền/dữ liệu/truy vết | ma trận và DD |
| Rà soát | quyết định nghiệp vụ, kiến trúc và testability có chủ xác nhận | quyết định hoặc câu hỏi mở |
| Kiểm định tĩnh | cấu trúc, tham chiếu, UTF-8, placeholder, hợp đồng nhất quán | lệnh và kết quả |
| Bàn giao | worklog, lịch sử, trạng thái từng trục, blocker | báo cáo |

Mọi feature phải có function hoặc lý do không áp dụng. Mọi function liên kết requirement/feature và test; mọi view có function hoặc trạng thái thuần; mọi file code có chủ và vai trò; mọi tác động ghi có hậu điều kiện lỗi. Không lấy trạng thái DD làm trạng thái runtime/device/DB/provider. Dùng validator cấu trúc, sau đó review ngữ nghĩa; không coi PASS là phê duyệt. Khi DD được duyệt mới chuyển workflow coding, đọc toàn bộ module, truy ID ảnh hưởng và import map. Khi source thay đổi, ghi delta đúng phạm vi, không âm thầm cập nhật hợp đồng đã duyệt.
