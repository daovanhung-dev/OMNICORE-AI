# Năng lực tạo UTC màn hình

Đầu ra là Excel bốn trang tính tiếng Việt (Bìa, Tổng quan, Thành phần, Sự kiện), đặc tả JSON và báo cáo kiểm định. Điểm vào `SKILL.md`. `mau/` chứa workbook sạch; `huong-dan/` quy định quy trình, ca, ánh xạ; `schema/` định nghĩa JSON; `scripts/` giải nén, kiểm tra độ bao phủ, sinh Excel, kiểm định Excel; `tham-chieu/` lưu nguồn tham khảo.

Môi trường: Python 3.10+; sinh Excel cần `artifact_tool`. Công cụ đọc archive, kiểm tra đặc tả và workbook dùng thư viện chuẩn Python. Không tự cài phụ thuộc. Công cụ không tự hiểu DD.

Lệnh thực hiện tại gốc thư mục năng lực, với đặc tả đã phân tích và lưu trong `workspace/utc-spec.json`:

```bash
python scripts/kiem_tra_utc.py --input workspace/utc-spec.json --report workspace/kiem-tra-utc.json
python scripts/tao_utc.py --input workspace/utc-spec.json --output workspace/UTC_SCREEN01.xlsx
python scripts/kiem_tra_excel.py --input workspace/UTC_SCREEN01.xlsx
```

Giới hạn workbook: Tổng quan 60 yêu cầu, 150 ca, 17 API, 8 trở ngại; Thành phần và Sự kiện mỗi loại 50 đối tượng/200 ca. Vượt giới hạn phải mở rộng vùng, kiểm tra công thức; không cắt bớt ca âm thầm. Không sửa cột phụ trợ V:W trực tiếp; sửa JSON rồi sinh lại. Trạng thái chưa duyệt và chưa chạy được giữ nguyên, không tự ghi đạt.
