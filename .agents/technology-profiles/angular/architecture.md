# Ánh xạ kiến trúc

data-access/*.service.ts, models/*.ts, pages/*.ts/.html/.css, ui/*.

Standalone component, RouterOutlet, HttpClient ở core/data-access, provider cấp ứng dụng. Tệp đăng ký framework chỉ lắp ghép, không sở hữu nghiệp vụ. Quy tắc logic chung áp dụng theo vai trò, không ép cú pháp framework.
