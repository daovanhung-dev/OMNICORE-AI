# Nền mã nguồn tái sử dụng

- [Máy chủ](backend.md): hợp đồng từng tệp và biểu tượng nền.
- [Ứng dụng khách](frontend.md): tuyến, phiên, HTTP, thành phần, màn hình.
- [Quy chuẩn biểu tượng](symbol-contract.md): chữ ký, điều kiện, lỗi, tác động, điểm gọi, chứng cứ.
- [Năng lực tạo nền](../skills/create-codebase/SKILL.md) và [quy trình](../workflows/create-codebase.md).

`inventory.py --repo .` chỉ kiểm kê khai báo tĩnh và tạo hồ sơ nguồn; không sinh nghiệp vụ, không chứng minh hành vi. Mỗi lớp/hàm thuộc phạm vi phải được đọc và đối chiếu riêng.

- [Hợp đồng mã tham chiếu](reference-contracts.md): chữ ký, thuật toán, lỗi, điểm gọi và kiểm thử cho lát cắt đã triển khai.

Các hợp đồng nền tổng quát là danh mục lựa chọn; chữ ký cụ thể của lát cắt theo `reference-contracts.md` và hồ sơ công nghệ đã duyệt. Không áp đặt pool, JWT, nhà cung cấp hoặc dịch vụ ngoài nếu chưa có yêu cầu.
