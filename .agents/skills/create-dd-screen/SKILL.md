---
name: create-dd-screen
description: Tạo thiết kế chi tiết màn hình.
---
# Tạo thiết kế chi tiết màn hình

Đầu vào: luồng, danh mục màn hình, đối tượng, tuyến, ảnh thiết kế, HTML, nguồn UI, API, thiết kế chung, quyền và tiêu chí kiểm thử. Không có ảnh thì ghi thiếu nguồn hình, không tạo marker giả.

1. Xác minh ID, phạm vi, đối tượng, vào/ra, tham số tuyến, phiên bản. Đối chiếu ảnh sạch và đánh số; ánh xạ marker với ID thành phần, ghi mâu thuẫn.
2. Điền 00 tổng quan, 01 thành phần, 05 quy tắc, 04 tích hợp API, 03 dữ liệu, 02 sự kiện, 06 điều hướng, 07 ca kiểm thử. Mỗi sự kiện có kích hoạt, điều kiện, đầu vào, xử lý, API, tác động, trạng thái, điều hướng, lỗi/retry và ca kiểm thử. Mỗi thành phần có dữ liệu, trạng thái hiển thị/disabled và sự kiện.
3. Truy marker → element → event → rule/API → test. Kiểm tra tải/rỗng/lỗi/thành công, phân trang, cache, hủy request, truy cập trực tiếp, quyền và khả năng tiếp cận theo nguồn. Chỉ phê duyệt khi quyết định chặn đã giải quyết. Dùng `agentkit.py new-dd --type screen`, giữ đủ tám tệp và provenance ảnh.

## Tài nguyên
Đọc `references/`, `checklists/`, `examples/` và `templates/` nếu có trong phạm vi nhiệm vụ.

## Tài nguyên bắt buộc

- [Phân tích gói màn hình và quyền sở hữu thông tin](references/01-phan-tich-screen-package.md): đọc trước khi lập kế hoạch.
- [Hợp đồng sự kiện, dữ liệu, trạng thái, điều hướng](references/02-event-state-va-dieu-huong.md): áp dụng cho từng event và element.
- [Ví dụ truy vết](examples/trace-event-thuc-te.md): minh họa cách liên kết DD với nguồn.

Đọc toàn bộ mẫu tám tệp và checklist trước khi tạo nội dung. Chỉ dùng mẫu ảnh/HTML có provenance, không suy ra runtime. Mỗi event phải có khối mô tả đầy đủ, không chỉ có một hàng index. Chạy kiểm định tĩnh và rà soát ba vòng; DD bị chặn vẫn có thể mô tả phần độc lập nhưng không được gắn đã duyệt.
