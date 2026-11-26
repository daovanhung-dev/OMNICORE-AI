# Bảo mật, kiểm thử và mức độ bằng chứng

- Authn + authz/object ownership kiểm tra server-side; browser guard chỉ hỗ trợ UX.
- Input validation, SQL binding, output encoding; logs không chứa secrets hoặc thông tin nhạy cảm.
- Tests: unit, API/contract, isolated DB integration, UI/browser/device, smoke deployment (nếu có).
- Test fixtures cần cleanup chính xác; không truncate shared databases.
- `NOT_RUN` khi chưa chạy command. `TESTED` cần command, exit code, môi trường và phạm vi test.
- Review read-only nếu chỉ được giao code review.

[Một test API mẫu](apps/server/tests/test_api01.md) và [một test screen mẫu](apps/client/src/app/features/module1/screen01/screen01.spec.ts.md).
