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

## RQ-009 — Gộp tác nhân và làm rõ trách nhiệm lớp USER

Ngày ghi nhận: 20/09/2026. Nguồn: người dùng chốt trực tiếp trong cuộc trao đổi về góp ý của giảng viên. Quyết định này bổ sung cho các quyết định ngày 06/09/2026 ở trên.

**Trạng thái:** Đã chốt phương án; mới ghi nhận quyết định, chưa cập nhật đồng bộ SRS, sơ đồ hoặc implementation.

> “vậy chốt gộp 2 tác nhân, giữ lớp USER lưu thông tin người dùng đã đăng ký, tồn tại ngay cả khi đã đăng xuất, đặt thao tác xác thực về đúng vị trí. Hãy ghi nhận phương án này.”

- Gộp hai tác nhân Khách và Người dùng thành một tác nhân **Người sử dụng**, bao gồm cá nhân tương tác trước và sau khi đăng ký/đăng nhập.
- Giữ lớp **USER** (`User` trong mã, bảng `users`) lưu thông tin người dùng đã đăng ký. Bản ghi tồn tại độc lập với phiên đăng nhập, kể cả sau khi đăng xuất. Không tạo bản ghi USER chỉ vì một người truy cập giao diện.
- Thể hiện điều kiện tài khoản, phiên xác thực hợp lệ và quyền sở hữu dữ liệu trong đặc tả từng use case. Đăng nhập là use case độc lập; không mặc định dùng `«include» Đăng nhập` cho mọi chức năng được bảo vệ. Phân rã use case theo nhóm chức năng không đồng nghĩa với quan hệ `«include»`.
- Đặt thao tác xác thực về đúng thành phần chịu trách nhiệm. Các hàm đăng ký, đăng nhập, yêu cầu khôi phục và đặt lại mật khẩu hiện nằm trong `app/routers/auth.py`; không mô tả chúng là phương thức đã triển khai của entity `User`. Khi cập nhật sơ đồ, phản ánh đúng thành phần thực tế và phân biệt rõ thiết kế đề xuất với hiện trạng.
- Quyết định này không yêu cầu tạo service/lớp mới, đổi tên lớp/bảng, thay đổi schema hoặc migration. Việc tái cấu trúc tầng xử lý, nếu có, là công việc riêng; không phát sinh tự động từ việc gộp tác nhân.

**Truy vết:** `FR-AUTH-001`, `FR-AUTH-002`, `NFR-SEC-001`, `US-001`; `app/models/user.py`, `app/routers/auth.py`. Các tài liệu/sơ đồ hiện hữu chưa phản ánh quyết định này cần được đồng bộ trong đợt chỉnh sửa tiếp theo; việc ghi nhận không xác nhận chúng đã được sửa hoặc kiểm chứng lại.

## Chi tiết còn phải chốt ở Database/Release Gate

- Baseline đề xuất cho “tải bình thường”: một người dùng thao tác tương tác, không chạy bulk import và máy chủ chưa báo quá tải; cần định lượng concurrency/dataset nếu sau này dùng làm release SLA.
- Chính sách backup/RPO/RTO và accessibility target.
- Cơ chế chứng minh backup đã hết retention trong tối đa 30 ngày và thời hạn xóa dữ liệu active.

## Backlog có điều kiện

Offline chỉ được mở lại thành yêu cầu khi có bằng chứng phản hồi đủ lớn. Khi đó phải tạo requirement/change request mới, xác định ngưỡng định lượng, phạm vi chức năng, mã hóa local, đồng bộ và xử lý xung đột; không tự động kích hoạt từ một vài phản hồi riêng lẻ.
