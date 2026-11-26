---
name: fix-bug
description: Chẩn đoán và sửa lỗi.
---
# Chẩn đoán và sửa lỗi

Kích hoạt cho lỗi, hồi quy, ca test sai hoặc hành vi bất thường. Ghi thực tế/kỳ vọng, tái hiện, môi trường, phiên bản, ảnh hưởng. Kiểm tra Git và baseline, truy điểm vào đến tác động và phản hồi. Lập giả thuyết cạnh tranh, loại bỏ bằng bằng chứng, phân biệt lỗi ứng dụng/test/phụ thuộc/thiết kế. Tạo ca hồi quy thất bại đúng nguyên nhân nếu khả thi; sửa nguyên nhân ở lớp nhỏ nhất, không nuốt lỗi hoặc refactor rộng. Chạy lại test liên quan, kiểm tra diff và an toàn. Ghi nguyên nhân, tệp, lệnh/kết quả và giới hạn. Thiếu quyết định quyền/DB/hợp đồng thì chặn phần phụ thuộc.

## Tài nguyên
Đọc `references/`, `checklists/`, `examples/` và `templates/` nếu có trong phạm vi nhiệm vụ.

## Context thực thi bắt buộc

Đọc [hợp đồng thực thi và bảng bằng chứng](references/01-chan-doan-va-hoi-quy.md) trước khi lập kế hoạch. Áp dụng từng cổng tương ứng phạm vi, lưu bằng chứng và giới hạn trong worklog; không chỉ dựa vào mô tả ngắn ở SKILL.md.
