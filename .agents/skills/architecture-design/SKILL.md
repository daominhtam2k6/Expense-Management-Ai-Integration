---
name: architecture-design
description: Thiết kế hoặc điều chỉnh kiến trúc Sổ Chi Tiêu từ các yêu cầu đã được con người phê duyệt, với lập luận và khả năng truy vết rõ ràng.
---

# Thiết kế kiến trúc

Đọc các artifact yêu cầu và yêu cầu Requirements Gate đã được phê duyệt trong `docs/human-gates.md`. Nếu chưa có, chỉ tạo bản nháp và xác định rõ điểm chặn.

Mô tả thành phần, trách nhiệm, dependency, luồng dữ liệu, dịch vụ ngoài, trust boundary và mức bao phủ yêu cầu. Giữ nguyên các ràng buộc đã chọn gồm FastAPI, React, SQLAlchemy, PostgreSQL/SQLite, Gemini, Resend và Tauri, trừ khi con người phê duyệt thay đổi. Không triển khai mã. Cập nhật `docs/architecture.md` và `docs/architecture-decisions.md`.
