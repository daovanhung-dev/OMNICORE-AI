# Folder mẫu: `apps/client/src/app/features/module1/screen01/pages/`

**Trách nhiệm:** Route-level page gồm component source, HTML và CSS minh họa.

**Mức bằng chứng:** `TEMPLATE_ONLY`, không phải cây source đã được xác minh.

## File và tài liệu 1:1

- [`screen01-page.css`](screen01-page.css.md) — **Screen styles**: CSS scoped, responsive, focus and error visual states; ưu tiên design tokens.
- [`screen01-page.html`](screen01-page.html.md) — **Screen template**: Mô tả DOM/markup, data binding, form events, focus, accessible labels, loading/empty/error.
- [`screen01-page.ts`](screen01-page.ts.md) — **Screen controller/page**: Nhận route params và user events, điều phối loading/empty/error/success, gọi data-access; không raw SQL.

**Khi onboarding:** thay cây ví dụ này bằng `project/tree/` sinh từ repository thật; không tự thêm folder vào source.
