---
name: requirements-analysis
description: Phân tích yêu cầu cho Sổ Chi Tiêu và tạo yêu cầu, user story, tiêu chí chấp nhận cùng các vấn đề chưa giải quyết có khả năng truy vết trước khi thiết kế hoặc triển khai.
---

# Phân tích yêu cầu

Đọc `docs/customer-requirement.md` và tài liệu sản phẩm hiện có. Phân tách rõ yêu cầu đã xác nhận, giả định và câu hỏi chưa giải quyết. Không viết mã hoặc âm thầm suy diễn quy tắc nghiệp vụ từ implementation hiện tại.

Dùng ID ổn định (`FR-*`, `NFR-*`, `US-*`, `AC-*`). Truy vết từng user story và tiêu chí chấp nhận về yêu cầu tương ứng. Cập nhật `docs/requirements.md`, `docs/user-stories.md`, `docs/acceptance-criteria.md` và `docs/requirements-issues.md`.

Dừng trước bước kiến trúc hoặc triển khai nếu một vấn đề chưa giải quyết có thể làm thay đổi đáng kể hành vi. Ghi quyết định của con người trong `docs/human-gates.md`; không bao giờ tự đánh dấu gate đã được phê duyệt thay người dùng.
