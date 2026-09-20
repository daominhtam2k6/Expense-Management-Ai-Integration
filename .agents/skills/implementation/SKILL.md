---
name: implementation
description: Triển khai các thay đổi Sổ Chi Tiêu đã được phê duyệt, đồng thời bảo toàn yêu cầu, kiến trúc, ranh giới cơ sở dữ liệu và bằng chứng có thể kiểm chứng.
---

# Triển khai

Đọc yêu cầu, tiêu chí chấp nhận, kiến trúc và thiết kế cơ sở dữ liệu đã được phê duyệt có liên quan đến tác vụ. Nếu đặc tả chưa đủ và điểm mơ hồ làm thay đổi hành vi bên ngoài, hãy dừng và ghi nhận vấn đề thay vì tự đặt ra quy tắc.

Thực hiện thay đổi nhất quán nhỏ nhất. Duy trì bộ lọc quyền sở hữu người dùng trên toàn bộ dữ liệu tài chính, giữ secret trong biến môi trường, chỉ gửi dữ liệu tổng hợp cho Gemini và mọi thay đổi cơ sở dữ liệu phải có migration. Thêm hoặc cập nhật test, chạy test theo phạm vi cùng kiểm tra tương đương build/lint, rà soát diff, rồi ghi lệnh, kết quả và artifact đã thay đổi vào `docs/ai-process-log.md`.
