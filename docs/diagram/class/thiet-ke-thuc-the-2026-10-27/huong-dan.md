# Sơ đồ và đặc tả theo phương thức người dùng chọn

- 9 lớp thực thể, 63 thuộc tính lưu trữ cộng /evidence dẫn xuất, 27 phương thức và 10 quan hệ. Giữ phong cách tham chiếu trước đó.
- Phương thức theo thiết kế giả định được người dùng cho phép; không phải bản kiểm kê phương thức trong mã nguồn. Không sửa mã sản phẩm hoặc DOCX gốc.
- Tên, tham số, kiểu trả về theo danh sách đã thống nhất. Phương thức cấp lớp được gạch chân; (...) chỉ lược tham số trên sơ đồ. Chi tiết đủ trong bảng đặc tả.
- User.updateAccount chỉ cập nhật hồ sơ; recoverPassword khởi tạo yêu cầu qua email. SavingGoal.isTargetReached chỉ trả kết quả kiểm tra tiến độ, không tự hoàn thành mục tiêu. AIConversation.create tạo hội thoại, không thêm tin nhắn. AIMessageOutput là cấu trúc đầu ra, không thêm một lớp thực thể.
- Hai phương thức GoalTransaction nhận ngày ghi nhận theo thiết kế đã thống nhất; đây là giả định thiết kế, không khẳng định API hiện tại đã cho nhập ngày.
- Các phương thức đăng nhập, đăng xuất, khôi phục thể hiện trách nhiệm nghiệp vụ giả định được phối hợp qua tầng xác thực; mô hình không bổ sung lớp Session hoặc dịch vụ vào danh sách thực thể.
- Đặc tả gồm 9 bảng thuộc tính và 27 bảng phương thức, đánh từ Bảng 4.2 đến Bảng 4.37, giả định Bảng 4.1 là danh sách lớp. Không có sơ đồ tuần tự.
- SVG vector mặc định rộng 25 cm; PNG 600 DPI rộng 5.906 pixel. Đặt A4 ngang, lề hai bên 2 cm, rộng 25 cm, giữ tỷ lệ; chiều cao hình 15.68 cm. Bản xem trước dành cho kiểm tra, không thay bản SVG.
- Render local PlantUML 1.2026.8: SVG/PNG exit code 0. Đã kiểm tra 9 lớp, 27 tên phương thức theo từng lớp, 64 thuộc tính và 10 quan hệ; xem ảnh tiếng Việt và đường nối. Chưa chèn vào file Word.
- HTML chứa nội dung và bảng để mở trong trình duyệt rồi sao chép vào Word; Markdown là bản văn bản tương ứng.
