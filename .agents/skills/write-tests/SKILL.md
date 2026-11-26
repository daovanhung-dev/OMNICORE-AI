---
name: write-tests
description: Thiết kế và thực hiện kiểm thử.
---
# Thiết kế và thực hiện kiểm thử

Đọc yêu cầu/DD/AC, nguồn và cấu hình test. Lập ma trận theo hành vi, đầu vào, chuẩn bị, kết quả/tác động, cấp kiểm thử, rủi ro, dọn dữ liệu. Ưu tiên quyền, tính toàn vẹn, sai đầu vào, HTTP/mã lỗi, phân trang, đồng thời/retry khi áp dụng. Chọn unit, component, HTTP, DB/dịch vụ và E2E. Fixture cô lập, xác minh DB đích trước ghi, lưu/xóa đúng ID; không seed production. Chạy test tập trung và bộ liên quan, build/lint/kiểu theo cấu hình. Ghi lệnh và kết quả, ca không chạy và lý do; test giả không chứng minh triển khai. Đầu ra: ca, ma trận, kết quả và giới hạn. Không đổi nghiệp vụ để làm test sai đạt.

## Tài nguyên
Đọc `references/`, `checklists/`, `examples/` và `templates/` nếu có trong phạm vi nhiệm vụ.

## Context thực thi bắt buộc

Đọc [hợp đồng thực thi và bảng bằng chứng](references/01-thiet-ke-va-thuc-thi-test.md) trước khi lập kế hoạch. Áp dụng từng cổng tương ứng phạm vi, lưu bằng chứng và giới hạn trong worklog; không chỉ dựa vào mô tả ngắn ở SKILL.md.
