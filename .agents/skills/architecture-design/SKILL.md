---
name: architecture-design
description: Thiết kế hoặc điều chỉnh kiến trúc Sổ Chi Tiêu từ các yêu cầu đã được con người phê duyệt, với lập luận và khả năng truy vết rõ ràng.
---

# Thiết kế kiến trúc

## Quy trình

1. Đọc `docs/requirements.md`, `docs/user-stories.md`, `docs/acceptance-criteria.md`, `docs/requirements-issues.md` và `docs/human-gates.md`.
2. Xác nhận Requirements Gate đã `APPROVED`. Nếu chưa, chỉ tạo bản nháp, ghi rõ blocker và không chuyển sang triển khai.
3. Xác định system context: actor, client, backend, database, dịch vụ ngoài và ranh giới tin cậy.
4. Phân rã component; với mỗi component, ghi trách nhiệm, dữ liệu sở hữu, dependency được phép và interface chính.
5. Mô tả luồng dữ liệu cho xác thực, thao tác tài chính, báo cáo, AI, upload và các tích hợp ngoài có liên quan.
6. Xác định trust boundary, biện pháp bảo mật, xử lý lỗi, observability, khả năng triển khai và các điểm thất bại chính.
7. Lập bảng truy vết requirement ID tới component và luồng chịu trách nhiệm; ghi rõ yêu cầu chưa được kiến trúc bao phủ.
8. Ghi từng quyết định quan trọng, lựa chọn thay thế, lý do và trade-off vào `docs/architecture-decisions.md`.
9. Cập nhật kiến trúc tổng thể trong `docs/architecture.md`, phân biệt rõ thiết kế mục tiêu với implementation hiện tại.
10. Rà soát tính nhất quán với database design và deployment trước khi bàn giao.

## Ràng buộc và đầu ra

- Giữ nguyên FastAPI, React, SQLAlchemy, PostgreSQL/SQLite, Gemini, Resend và Tauri, trừ khi có phê duyệt của con người.
- Không triển khai mã trong skill này và không tự phê duyệt Architecture Gate.
- Đầu ra: `docs/architecture.md`, `docs/architecture-decisions.md`, traceability và danh sách blocker/rủi ro.
