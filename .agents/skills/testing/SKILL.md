---
name: testing
description: Lập kế hoạch, triển khai, thực thi và báo cáo các kiểm thử có khả năng truy vết về yêu cầu cho backend và frontend Sổ Chi Tiêu.
---

# Kiểm thử

Đọc yêu cầu, user story và tiêu chí chấp nhận. Bao phủ luồng tích cực, tiêu cực, giá trị biên, phân quyền/quyền sở hữu, lỗi và tích hợp. Không bao giờ hạ thấp kỳ vọng chỉ để làm test pass.

Chạy backend test bằng `python -m pytest -q`, frontend test bằng `npm.cmd test -- --coverage` và production frontend build khi có liên quan. Ghi đúng kết quả quan sát được cùng ngày thực hiện trong `docs/test-report.md`; không sao chép số liệu cũ. Ánh xạ khoảng trống kiểm thử tới ID yêu cầu trong `docs/test-plan.md`.
