# Kiến trúc máy chủ và ứng dụng khách

## Máy chủ
```text
apps/server/
  app/main.*
  app/api/v1.*
  app/core/{config,constants,database,responses,middleware,trace}.*
  app/core/security/{password,access_token,refresh_token}.*
  app/modules/<nhom>/<ma_api>_<ten>/
    models.*
    validate.*
    query.*
    view.*
  app/utils/{auth,validate}.*
  app/service/<nha_cung_cap>/
  docs/dd/<nhom>/<ma_api>/
  tests/modules/<nhom>/<ma_api>/
  migrations/
```
`main` lắp ghép ứng dụng; `api` đăng ký phương thức/đường dẫn và tiêm phụ thuộc; `core` chứa nền tảng dùng chung; `modules` chia theo vai trò hoặc năng lực được duyệt; `utils` là hàm chung; `service` là bộ thích nghi dịch vụ ngoài; `tests` đối xứng với API; `docs/dd` lưu hợp đồng; `migrations` quản lý thay đổi lược đồ theo phiên bản. Một API có bốn tệp trách nhiệm: `models` (khai báo), `validate` (kiểm tra đầu vào), `query` (định nghĩa thao tác truy xuất), `view` (điều phối thực thi). `__init__.py` chỉ đánh dấu gói nếu Python cần. Mỗi API mới có đủ bốn tệp trách nhiệm. Nếu không truy xuất dữ liệu, `query` ghi rõ không áp dụng; không tạo logic giả. Chi tiết và ngoại lệ tại `../rules/backend.md`.

## Ứng dụng khách
```text
apps/client/src/app/
  app.routes.*
  core/{auth,constant,http,localStorage}/
  features/<nhom>/
    <nhom>.route.*
    <ma_man_hinh>/
      data-access/
      models/
      pages/
      ui/
  layouts/<nhom>/
  shared/ui/
apps/client/docs/{dd_screens,screen_stitch}/
```
Mỗi màn hình có đúng bốn thư mục trực tiếp. `data-access` phụ trách gọi API; `models` khai báo kiểu và chuyển đổi thuần; `pages` điều phối trạng thái, sự kiện, vòng đời; `ui` chứa thành phần hiển thị riêng. Mỗi nhóm sở hữu tệp tuyến và một khung giao diện. `shared/ui` chỉ chứa thành phần trung lập dùng chung. `core` sở hữu HTTP, phiên, mã API và lưu trữ dùng chung. Tài liệu thiết kế không phải mã chạy thật.

## Quan hệ và hướng phụ thuộc
Tuyến máy chủ → `view` → `validate`/xác thực → `query` hoặc dịch vụ → dữ liệu → bộ phản hồi. Máy khách: tuyến → khung → trang → dịch vụ → HTTP → API; trang truyền mô hình cho UI và nhận sự kiện. UI không gọi DB hay API trực tiếp. `core` không phụ thuộc `features`/`modules`. Trình tự xác thực, kiểm tra và giao dịch phải tuân thủ hợp đồng bảo mật. Các tệp ví dụ có mô tả đối xứng dưới `apps/`.

## Tương thích công nghệ
Python sử dụng `.py`, TypeScript dùng `.ts`, Java/C# dùng tệp/lớp bản địa; Vue/React/Flutter giữ bốn trách nhiệm màn hình dù phần hiển thị có thể nằm chung tệp. Không buộc dùng SQL thô khi ORM là chuẩn được duyệt. Ngoại lệ được ghi trong quyết định kiến trúc. Không gán sẵn vai trò, bảng, API hoặc nghiệp vụ.
