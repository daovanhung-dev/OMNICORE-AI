---
name: code-review
description: Rà soát mã chỉ đọc.
---
# Rà soát mã chỉ đọc

Chỉ kích hoạt khi có yêu cầu review diff/PR/đường dẫn. Không sửa mã/test/cấu hình, không chạy test/build/lint/scanner, không đổi Git state, không đăng nhận xét PR hoặc tự sửa. Nhật ký chỉ nếu được phép.

Xác định phạm vi/base/head; đọc AGENTS, quy tắc, nguồn, hợp đồng, điểm gọi, mã kiểm thử. Kiểm tra tính đúng, ranh giới lớp, tái sử dụng, bảo trì, quyền, giao dịch, lỗi, đầu vào không tin cậy và đường thực thi. Chỉ ghi phát hiện có bằng chứng dòng mã, tình huống đến được, tác động và hướng khắc phục; review diff chỉ lỗi mới do diff. Sắp P0–P3 theo ảnh hưởng, ghi giới hạn và phần chưa chạy. Không kết luận toàn kho mã an toàn từ phạm vi hẹp.

## Tài nguyên
Đọc `references/`, `checklists/`, `examples/` và `templates/` nếu có trong phạm vi nhiệm vụ.

## Context thực thi bắt buộc

Đọc [hợp đồng thực thi và bảng bằng chứng](references/01-pham-vi-va-bang-chung.md) trước khi lập kế hoạch. Áp dụng từng cổng tương ứng phạm vi, lưu bằng chứng và giới hạn trong worklog; không chỉ dựa vào mô tả ngắn ở SKILL.md.
