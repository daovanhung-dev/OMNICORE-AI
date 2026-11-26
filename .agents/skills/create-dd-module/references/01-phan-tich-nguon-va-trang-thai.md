# Phân tích BD thành thiết kế module

Đọc yêu cầu/BD, luồng sản phẩm, module phụ thuộc, source hiện hành, chính sách quyền và dữ liệu. Kiểm kê phiên bản, vị trí mục, loại trực tiếp/suy dẫn/đề xuất, độ tin cậy, tác động. Xác định actor, mục tiêu, trigger, điều kiện vào/ra, ranh giới sở hữu, in/out scope; không gộp module chỉ vì dùng chung UI. Ghi thực thể, trường, chủ sở hữu, nguồn/đích, nhạy cảm, thời hạn lưu, state transition, bất biến, khóa/idempotency; không bịa schema, quyền hoặc dữ liệu.

| Mã yêu cầu | Nguồn/mục | Actor | Mục tiêu | Điều kiện | Kết quả | Trạng thái | Chủ quyết định |
|---|---|---|---|---|---|---|---|

Mỗi capability có feature ID; mỗi trách nhiệm độc lập có function ID; view/rule/API/test có ID ổn định. Giữ ID nguồn, alias tường minh nếu cần. Trace BD → feature → function/rule → view → source/import → test; mỗi ID có link ngược. Chỉ dùng nguồn thực tế cho hiện trạng. Khi source khác BD ghi chênh lệch, không tự sửa DD hoặc code để che mâu thuẫn.

Bốn trục độc lập: vòng đời (hiện hành/lịch sử/tham chiếu/sinh tự động), quyết định thiết kế (chưa duyệt/đang rà soát/đã duyệt/ngừng dùng), hiện thực (đã có/một phần/chỉ khung/chưa có/không áp dụng), xác minh (tĩnh/runtime chưa xác minh/runtime đã kiểm tra/môi trường cụ thể). Không suy từ Approved sang chạy được. Thiếu quyết định ảnh hưởng dữ liệu/quyền/chi phí/tác động hoặc nghiệm thu thì chặn phần phụ thuộc.
