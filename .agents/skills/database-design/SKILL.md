---
name: database-design
description: Thiết kế và rà soát schema quan hệ, migration, constraint, index, ranh giới sở hữu dữ liệu và khả năng truy vết của Sổ Chi Tiêu.
---

# Thiết kế cơ sở dữ liệu

## Quy trình

1. Đọc requirements đã phê duyệt, `docs/architecture.md`, `docs/human-gates.md`, toàn bộ model SQLAlchemy và Alembic migration hiện có.
2. Lập danh sách entity, thuộc tính, khóa chính, khóa ngoại, quan hệ và chủ sở hữu dữ liệu.
3. Đối chiếu schema triển khai với yêu cầu; ghi riêng trạng thái “đã có”, “thiếu”, “khác thiết kế” và “chưa kiểm chứng”.
4. Kiểm tra normalization, nullability, uniqueness, CHECK constraint, default, kiểu dữ liệu và độ chính xác tiền tệ.
5. Kiểm tra mọi quan hệ theo `ON DELETE`/cascade/restrict, khả năng tạo orphan và tính nguyên tử của luồng nghiệp vụ.
6. Kiểm tra cô lập theo người dùng: `user_id`, ownership FK/composite constraint và nguy cơ tham chiếu chéo tài khoản.
7. Đánh giá index theo khóa ngoại, bộ lọc, sắp xếp, uniqueness và truy vấn tổng hợp; chỉ đề xuất index có workload hoặc query hỗ trợ.
8. Thiết kế kế hoạch migration gồm preflight, xử lý collision, upgrade, kiểm chứng, rollback/restore và khác biệt PostgreSQL/SQLite.
9. Cập nhật `docs/database-design.md` với schema mục tiêu, schema hiện tại, gap, traceability và migration plan.
10. Kiểm tra Database Gate trước khi bàn giao cho implementation.

## Điểm dừng và đầu ra

- Không sửa application code hoặc tạo migration khi Database Gate chưa được phê duyệt.
- Mọi schema change phải đi qua Alembic migration; không sửa database production trực tiếp.
- Đầu ra: `docs/database-design.md`, danh sách gap và kế hoạch migration có thể kiểm chứng.
