# Folder mẫu: `apps/client/src/app/features/module1/screen01/ui/`

**Trách nhiệm:** Các widget local chỉ được screen dùng.

**Mức bằng chứng:** `TEMPLATE_ONLY`, không phải cây source đã được xác minh.

## File và tài liệu 1:1

- [`screen01-widget.ts`](screen01-widget.ts.md) — **Local UI component**: Widget chỉ phục vụ screen01, nhận inputs/phát events, không sở hữu policy server.

**Khi onboarding:** thay cây ví dụ này bằng `project/tree/` sinh từ repository thật; không tự thêm folder vào source.
