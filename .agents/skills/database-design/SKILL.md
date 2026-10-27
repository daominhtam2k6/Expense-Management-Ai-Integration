---
name: database-design
description: Mô tả bảng, quan hệ, constraint và dữ liệu tài chính của hệ thống.
---

# Thiết kế cơ sở dữ liệu

## Đầu vào

Yêu cầu hiện tại, file liên quan, phạm vi được sửa và kết quả mong muốn. Xem [cấu trúc tài liệu](../../../docs/README.md). Prompt gợi ý: [04-thiet-ke-co-so-du-lieu.md](../../../docs/prompt-library/04-thiet-ke-co-so-du-lieu.md).

## Cách thực hiện

1. Đọc app/models/, migration và yêu cầu liên quan.
2. Xác định PK/FK, cardinality, owner và kiểu dữ liệu; số tiền dùng Decimal/NUMERIC.
3. Kiểm tra uniqueness category, miền năm ngân sách, cascade và dữ liệu khác tài khoản.
4. Nêu index cần cho query thực, kế hoạch thay schema và ca dữ liệu xung đột.
5. Thiết kế không tự chạy migration hoặc chỉnh database thật.

## Đầu ra

docs/software/design/database-design.md và docs/diagram/erd/.

## Hoàn tất

Kết quả đáp ứng yêu cầu, có đường dẫn và cách kiểm tra phù hợp. Nêu điều chưa rõ hoặc chưa kiểm tra; giữ nguyên file/môi trường ngoài phạm vi.
