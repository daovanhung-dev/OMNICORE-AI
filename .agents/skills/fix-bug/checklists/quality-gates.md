# Cổng chất lượng — Fix bug

- [ ] Bước tái hiện và expected/actual/environment được ghi rõ.
- [ ] Có hypotheses và root cause dựa trên source/observation.
- [ ] Regression test fail trước patch nếu khả thi, pass sau patch.
- [ ] Patch thuộc owning layer, không refactor ngoài scope.
- [ ] Test impacted + diff review, không xóa baseline failures.
- [ ] Không mutate prod/DB/infra trái quyền; remaining blocker ghi rõ.
