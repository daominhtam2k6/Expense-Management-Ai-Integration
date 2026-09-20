---
name: security-review
description: Thực hiện rà soát bảo mật chỉ đọc cho Sổ Chi Tiêu trên các khía cạnh xác thực, phân quyền, đầu vào, upload, secret, quyền riêng tư AI, dependency và triển khai.
---

# Rà soát bảo mật

Không sửa mã trong quá trình rà soát. Kiểm tra injection, XSS, khả năng áp dụng CSRF, xác thực, phân quyền cấp đối tượng, xử lý mật khẩu/token, luồng reset, upload, secret, CORS/host, rò rỉ lỗi, rủi ro dependency và ranh giới dữ liệu Gemini. Xác minh mọi truy vấn dữ liệu đều giới hạn theo chủ sở hữu đã xác thực và AI chỉ nhận dữ liệu tổng hợp đã được lập tài liệu.

Phân loại các phát hiện có bằng chứng theo mức độ nghiêm trọng và ghi nhận giới hạn, bao gồm các scan chưa chạy, trong `docs/security-review.md`. Con người phải chấp nhận hoặc khắc phục các phát hiện HIGH/CRITICAL còn mở trước khi Security Gate được phê duyệt.
