# Nhật ký công việc

Mỗi nhiệm vụ ghi một tệp `.agents/worklog/YYYY-MM-DD/<task-id>.md`. Mẫu cấu trúc tại `TEMPLATE.md`. `python3 .agents/tools/select-worklogs.py --type coding --limit 3` chọn tối đa ba nhật ký cùng loại, theo ngày giảm dần, đường dẫn tăng dần. Ghi đường dẫn vào READ_PLAN trước khi đọc. Không lấy nhật ký làm chứng cứ runtime thay cho mã nguồn và kết quả kiểm thử.
