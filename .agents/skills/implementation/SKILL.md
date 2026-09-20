---
name: implementation
description: Triển khai các thay đổi Sổ Chi Tiêu đã được phê duyệt, đồng thời bảo toàn yêu cầu, kiến trúc, ranh giới cơ sở dữ liệu và bằng chứng có thể kiểm chứng.
---

# Triển khai

## Quy trình

1. Xác định requirement ID và acceptance criteria của thay đổi; đọc phần kiến trúc, database design và Human Gate liên quan.
2. Kiểm tra đặc tả có đủ để quyết định hành vi bên ngoài hay không. Nếu chưa đủ, ghi issue và dừng thay vì tự đặt quy tắc.
3. Khảo sát implementation, test và migration hiện tại; xác định tập file nhỏ nhất cần thay đổi và rủi ro hồi quy.
4. Lập thay đổi nhất quán nhỏ nhất, giữ API/behavior tương thích khi yêu cầu không cho phép breaking change.
5. Triển khai mã với các invariant bắt buộc: mọi dữ liệu tài chính lọc theo owner, secret chỉ từ biến môi trường, Gemini chỉ nhận aggregate đã cho phép, lỗi ngoài không lộ chi tiết nhạy cảm.
6. Nếu thay đổi schema, tạo Alembic migration theo database design; không dùng thao tác schema thủ công thay migration.
7. Thêm hoặc cập nhật test truy vết tới AC, gồm positive, negative, boundary và ownership/error path phù hợp.
8. Chạy test theo phạm vi trước, sau đó chạy suite/build/lint-equivalent liên quan. Không hạ kỳ vọng test để làm test pass.
9. Rà soát diff để loại thay đổi ngoài phạm vi, secret, artifact sinh tự động hoặc dữ liệu người dùng không chủ ý.
10. Cập nhật tài liệu bị ảnh hưởng và ghi lệnh, kết quả, file thay đổi, giới hạn còn lại vào `docs/ai-process-log.md`.

## Điều kiện hoàn tất

- Acceptance criteria liên quan có bằng chứng pass hoặc được ghi rõ là còn fail/block.
- Migration, test và tài liệu đồng bộ với mã.
- Không tuyên bố hoàn tất nếu test bắt buộc chưa chạy hoặc đang thất bại.
