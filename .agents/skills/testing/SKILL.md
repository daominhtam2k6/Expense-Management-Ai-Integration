---
name: testing
description: Lập kế hoạch, triển khai, thực thi và báo cáo các kiểm thử có khả năng truy vết về yêu cầu cho backend và frontend Sổ Chi Tiêu.
---

# Kiểm thử

## Quy trình

1. Đọc requirements, user stories, acceptance criteria, kiến trúc và thay đổi cần kiểm thử.
2. Lập ma trận requirement/AC → loại test → file test → trạng thái bằng chứng trong `docs/test-plan.md`.
3. Chọn ca kiểm thử cho positive, negative, boundary, authorization/ownership, error handling và integration path.
4. Chuẩn bị fixture cô lập; không dùng hoặc phá hủy database/tài nguyên nghiệp vụ thật nếu chưa được yêu cầu rõ ràng.
5. Viết hoặc cập nhật test theo hành vi đã phê duyệt. Không sửa kỳ vọng chỉ để khớp implementation sai.
6. Chạy backend bằng interpreter của môi trường dự án với `python -m pytest -q`; nếu Python hệ thống thiếu dependency, ghi rõ và chạy lại bằng virtualenv phù hợp.
7. Chạy frontend bằng `npm.cmd test -- --coverage`; chạy `npm.cmd run build` khi thay đổi hoặc phạm vi liên quan tới frontend/release.
8. Khi có schema change, chạy Alembic upgrade/check trên database thử nghiệm phù hợp; phân biệt bằng chứng SQLite với PostgreSQL.
9. Ghi chính xác ngày, môi trường, lệnh, số pass/fail/skip, warning, coverage và thời gian quan sát vào `docs/test-report.md`.
10. Với mỗi fail, ghi requirement/AC, bước tái hiện, expected, actual, mức ảnh hưởng và file liên quan. Cập nhật gap còn lại trong `docs/test-plan.md`.

## Quy tắc báo cáo

- Phân biệt `PASS`, `FAIL`, `BLOCKED` và `NOT RUN`; không coi “không chạy” là “không có lỗi”.
- Không sao chép số liệu cũ hoặc tuyên bố toàn hệ thống đạt từ một suite giới hạn.
- Không sửa application code nếu tác vụ chỉ yêu cầu kiểm thử hoặc chẩn đoán.
