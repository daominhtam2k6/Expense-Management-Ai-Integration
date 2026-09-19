# Vấn đề và quyết định yêu cầu

Người quyết định: Đào Minh Tâm. Ngày: 06/09/2026.

| ID | Quyết định đã phê duyệt | Trạng thái triển khai hiện tại |
|---|---|---|
| RQ-001 | Email/username không phân biệt hoa thường. | Cần kiểm chứng và có thể sửa implementation/database. |
| RQ-002 | Access token hết hạn thì phiên bị đăng xuất và token bị từ chối. | Backend kiểm tra expiry; cần kiểm chứng client xóa phiên. Chính sách revoke trước hạn/đa thiết bị chưa được yêu cầu. |
| RQ-003 | Số dư khả dụng là tiền có thể dùng cho giao dịch chi hoặc nạp mục tiêu; không gồm tiền đang nằm trong mục tiêu tiết kiệm. | Có logic hiện tại; cần trace test với định nghĩa đã duyệt. |
| RQ-004 | Múi giờ Hà Nội, tiền Việt Nam đồng, làm tròn một chữ số thập phân, chốt tháng vào ngày cuối tháng. | Chưa chứng minh đầy đủ; cần thiết kế timezone/rounding. |
| RQ-005 | Giữ lịch sử hội thoại; người dùng được chủ động xóa toàn bộ tài khoản và dữ liệu cá nhân; backup hết retention trong tối đa 30 ngày. | Có xóa hội thoại; chưa có luồng xóa tài khoản, cascade và thực thi retention backup. |
| RQ-006 | Mục tiêu gần 24/7, xử lý sự cố trong 24h, thao tác dưới 10 giây ở tải bình thường; chưa hướng tới lượng người dùng lớn. | Cần định nghĩa phép đo tối thiểu; backup, RPO/RTO và accessibility vẫn để mở. |
| RQ-007 | Coverage mục tiêu dựa trên khả năng thực tế của hệ thống. | Giữ kết quả đo hiện tại làm baseline; chưa đặt ngưỡng release mới. |
| RQ-008 | Web và ứng dụng cài đặt online toàn bộ. Offline chưa thuộc phạm vi; chỉ xem xét sau nếu có số lượng lớn phản hồi người dùng yêu cầu. | Phù hợp kiến trúc hiện tại; không cần local store hoặc sync engine trong release này. |

## Chi tiết còn phải chốt ở Database/Release Gate

- Baseline đề xuất cho “tải bình thường”: một người dùng thao tác tương tác, không chạy bulk import và máy chủ chưa báo quá tải; cần định lượng concurrency/dataset nếu sau này dùng làm release SLA.
- Chính sách backup/RPO/RTO và accessibility target.
- Cơ chế chứng minh backup đã hết retention trong tối đa 30 ngày và thời hạn xóa dữ liệu active.

## Backlog có điều kiện

Offline chỉ được mở lại thành yêu cầu khi có bằng chứng phản hồi đủ lớn. Khi đó phải tạo requirement/change request mới, xác định ngưỡng định lượng, phạm vi chức năng, mã hóa local, đồng bộ và xử lý xung đột; không tự động kích hoạt từ một vài phản hồi riêng lẻ.
