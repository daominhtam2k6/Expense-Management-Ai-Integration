# Luồng màn hình tổng quát của Sổ Chi Tiêu

- Một sơ đồ tổng quát, gồm 12 hộp màn hình/bảng; không phân rã các thao tác tạo, sửa, xóa hoặc luồng kiểm tra lỗi.
- Nhóm công khai: Đăng nhập, Đăng ký, Quên mật khẩu, Đặt lại mật khẩu qua liên kết email. Đăng ký thành công hoặc trở về đều đưa đến Đăng nhập.
- Đăng nhập thành công mở Dashboard. Từ menu dùng chung có thể mở Giao dịch, Danh mục, Ngân sách, Mục tiêu tiết kiệm, Báo cáo so sánh và Trợ lý AI; chọn Tổng quan để quay lại Dashboard. Trên thực tế các trang cũng có thể chuyển trực tiếp qua menu, sơ đồ gom các đường này qua Dashboard để biểu diễn tổng quát.
- Menu tài khoản mở bảng Thông tin cá nhân trên màn hình hiện tại. Đường quay về biểu thị đóng bảng, không yêu cầu luôn điều hướng về Dashboard.
- Đăng xuất là một thao tác điều hướng về Đăng nhập, không phải một màn hình riêng. Gộp đường đăng xuất tại Dashboard để đại diện cho menu tài khoản dùng chung.
- Các liên kết chéo từ Báo cáo/Trợ lý AI đến Giao dịch và các biểu mẫu/bảng chi tiết không được vẽ riêng trong bản tổng quan theo yêu cầu rút gọn. Sơ đồ không phải bản liệt kê mọi điều hướng.
- Nguồn: mục 5.1 trong DOCX người dùng cung cấp ở Downloads/Tai lieu du an; frontend/src/App.tsx; components/AppShell.tsx; pages/auth; GoalsPage, ReportsPage, AssistantPage.
- Đây là screen flow, không gán nhãn UML và không dùng ký hiệu use case/hoạt động để thay thế màn hình.
- SVG vector, PNG 600 DPI; khuyến nghị A4 ngang, lề 2 cm, đặt rộng 24,7 cm và giữ tỷ lệ. Ảnh cao khoảng 16,16 cm. Đặt caption bên dưới nếu còn đủ vùng in; giảm đồng đều xuống 24 cm nếu mẫu có header/footer lớn.
- Nguồn .drawio mở bằng diagrams.net; SVG cũng có thể chỉnh sửa bằng phần mềm vector.
- Đã đối chiếu các tuyến và bảng hồ sơ trong mã nguồn, kiểm tra cấu trúc XML và xem bản PNG. Không sửa DOCX gốc hoặc mã ứng dụng.
