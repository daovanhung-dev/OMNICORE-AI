# Ánh xạ kiến trúc

data-access, models, pages, ui.

Router theo nhóm, hook lấy dữ liệu ở data-access, page sở hữu trạng thái. Tệp đăng ký framework chỉ lắp ghép, không sở hữu nghiệp vụ. Quy tắc logic chung áp dụng theo vai trò, không ép cú pháp framework.

## Quy tắc theo context nguồn

Mẫu tham chiếu nguồn mô tả React + TypeScript + Vite, client API tập trung, schema kiểm tra response ở ranh giới dữ liệu/mô hình và thư viện query quản lý cache, loading, retry, invalidation. Kiểm tra package và wiring thật trước khi chọn thư viện; không bắt buộc React Query hay Zod khi dự án dùng giải pháp khác. Route trình bày chưa nối API không được gọi là lưu dữ liệu; quyền do server quyết định. Thiết kế dùng semantic token, primitive dùng chung, focus-visible, trạng thái hover/disabled, responsive và reduced motion. Chính sách token/storage phải có hợp đồng riêng. Không áp Angular RouterOutlet hoặc cấu trúc component Angular lên React hiện hữu. Chưa chạy React trong gói.
