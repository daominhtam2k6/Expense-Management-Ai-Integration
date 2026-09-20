---
name: database-design
description: Thiết kế và rà soát schema quan hệ, migration, constraint, index, ranh giới sở hữu dữ liệu và khả năng truy vết của Sổ Chi Tiêu.
---

# Thiết kế cơ sở dữ liệu

Đọc yêu cầu đã phê duyệt, kiến trúc, model SQLAlchemy và migration Alembic. Kiểm tra entity, quan hệ, chuẩn hóa, PK/FK, nullability, uniqueness, CHECK constraint, index, độ chính xác tiền tệ, hành vi xóa và khả năng cô lập theo người dùng.

Ghi riêng các khoảng trống so với schema đã triển khai. Không thay đổi mã ứng dụng. Cập nhật `docs/database-design.md`; mọi thay đổi schema phải dùng Alembic migration và yêu cầu Database Gate trong `docs/human-gates.md` trước khi triển khai.
