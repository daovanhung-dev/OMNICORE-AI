# Rà soát chỉ đọc theo bốn tiêu chí

Chỉ kích hoạt khi được yêu cầu review diff/PR hoặc audit path. Không sửa code/test/config/docs, không chạy test/build/lint/scanner, không đổi index/HEAD/branch/PR, không post nhận xét; chỉ ghi worklog nếu được phép. Đọc đúng AGENTS/manifest/scope và worklog cùng loại. Nếu page context thiếu, ghi thiếu; không tái tạo khi đang review.

Xác định base/head/merge-base theo yêu cầu, không checkout. Với working tree, bao gồm staged, unstaged và untracked có liên quan; ghi phạm vi. Không có diff nhưng có path thì audit hiện trạng; không gán lỗi cũ cho diff. Không rõ phạm vi thì ghi chặn, không suy đoán.

| Tiêu chí | Cách kiểm chứng |
|---|---|
| Quy tắc kho mã | đối chiếu rule bắt buộc, DD/contract, layer và trace caller/callee/side effect/response/test |
| Tái sử dụng | tìm helper/component đúng trách nhiệm; chỉ nêu trùng lặp có drift hoặc chi phí bảo trì thật; không ép chia sẻ xuyên boundary |
| Bảo trì | lỗi ở nhánh đến được, trạng thái không rõ, nuốt lỗi, fallback sai, vi phạm rule; không nêu gu style |
| Bảo mật | truy nguồn không tin cậy → kiểm soát thiếu/sai → đường thực thi → tác động; auth/object/tenant, injection, log/secret, path/URL, storage/provider |

Cổng phát hiện: (1) đường chạy thuộc phạm vi đến được; (2) bằng chứng dòng code và tác động; (3) đáng sửa, có hướng xử lý; (4) nếu diff review, lỗi do diff tạo. Không đủ thì ghi thiếu bằng chứng hoặc bỏ phát hiện suy đoán. Kiểm tra toàn phạm vi kể cả đã phát hiện lỗi. Đọc test source để đánh giá coverage, không thực thi.

| Mức | Tiêu chí |
|---|---|
| P0 | sự cố nghiêm trọng, chặn phát hành hoặc ảnh hưởng rộng có chứng cứ |
| P1 | lỗi nghiêm trọng cần ưu tiên |
| P2 | ảnh hưởng rõ tính đúng/bảo mật/bảo trì |
| P3 | tác động thấp nhưng có bằng chứng và đáng xử lý |

Báo cáo: mục tiêu, range/file, bốn tiêu chí (không thấy vấn đề / có phát hiện / chưa đủ bằng chứng), phát hiện theo mức, file:dòng, nhãn diff hay hiện trạng, tình huống, tác động, chứng cứ, hướng sửa, giới hạn. Không tạo finding để lấp từng nhóm. Không khẳng định toàn hệ thống an toàn; nói rõ test không chạy. Không tự apply patch.
