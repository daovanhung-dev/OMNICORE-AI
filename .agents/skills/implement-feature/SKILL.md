---
name: implement-feature
description: Hiện thực chức năng có nguồn.
---
# Hiện thực chức năng có nguồn

Kích hoạt cho yêu cầu lập trình BE/FE đã xác định. Đầu vào là yêu cầu/AC, DD, mã nguồn, hợp đồng API/DB/quyền, thành phần và lệnh kiểm thử. Đọc quy trình `coding` và quy tắc theo lớp.

1. Truy vết yêu cầu → UI/API → chủ mã → kiểm thử; truy từ điểm gọi tới dữ liệu, lỗi, quyền và tác động.
2. Lập kế hoạch thay đổi nhỏ theo DTO, validator, query, view, dịch vụ, trang/UI, tuyến, test. Tìm mã dùng chung trước; giữ kiến trúc và thay đổi người dùng.
3. Hiện thực lát cắt nhỏ nhất; giữ hợp đồng, mã lỗi và trạng thái. FE xử lý tải, rỗng, lỗi và phiên. Không nối giả khi API chưa sẵn sàng.
4. Chạy kiểm thử tập trung rồi bộ liên quan/build/lint/kiểu; sửa nguyên nhân, rà soát diff. Cập nhật hồ sơ và nhật ký. Chỉ nghiệm thu khi có hành vi và chứng cứ cần thiết; thiếu quyết định thì chặn phần phụ thuộc.

## Tài nguyên
Đọc `references/`, `checklists/`, `examples/` và `templates/` nếu có trong phạm vi nhiệm vụ.

## Context thực thi bắt buộc

Đọc [hợp đồng thực thi và bảng bằng chứng](references/01-truy-vet-va-hien-thuc.md) trước khi lập kế hoạch. Áp dụng từng cổng tương ứng phạm vi, lưu bằng chứng và giới hạn trong worklog; không chỉ dựa vào mô tả ngắn ở SKILL.md.
