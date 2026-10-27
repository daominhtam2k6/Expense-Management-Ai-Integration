# Các quyết định của dự án

- Sản phẩm là web/PWA online; không xây bộ cài native hay cơ chế đồng bộ offline trong phạm vi này.
- Người sử dụng quản lý dữ liệu tài chính của chính mình. User là tài khoản, tồn tại độc lập với phiên đăng nhập.
- Category không trùng tên sau trim, không phân biệt hoa thường trong cùng owner và loại. Năm ngân sách từ 2000 đến 2100.
- Tiền tệ, kỳ và cách làm tròn theo [yêu cầu](requirements.md) và [AC](acceptance-criteria.md).
- Gemini chỉ hỗ trợ giải thích và gợi ý từ dữ liệu tổng hợp được cho phép, không sửa dữ liệu.
- Xóa tài khoản yêu cầu mật khẩu hiện tại và chuỗi xác nhận theo AC; dữ liệu active xóa nguyên tử, không ảnh hưởng tài khoản khác. Retention backup theo yêu cầu đã chốt.

Chi tiết và ID quyết định ở [requirements-issues.md](requirements-issues.md). Việc sắp xếp tài liệu không thay đổi chức năng đã triển khai hay quyết định phát hành.
