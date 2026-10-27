---
name: implementation
description: Thực hiện tính năng, sửa lỗi và migration được giao trong phạm vi rõ.
---

# Lập trình và sửa lỗi

## Đầu vào

Yêu cầu hiện tại, file liên quan, phạm vi được sửa và kết quả mong muốn. Xem [cấu trúc tài liệu](../../../docs/README.md). Prompt gợi ý: [08-lap-trinh-tinh-nang.md](../../../docs/prompt-library/08-lap-trinh-tinh-nang.md).

## Cách thực hiện

1. Xác định expected/actual và AC; đọc mã, caller, test trước khi sửa.
2. Với bug, tìm nguyên nhân; với tính năng, chọn thay đổi nhỏ nhất phù hợp cấu trúc hiện có.
3. Giữ ownership, tiền tệ, transaction và API ngoài phạm vi; không refactor toàn dự án.
4. Nếu đổi schema, viết Alembic revision mới, preflight dữ liệu và thử trên database cô lập.
5. Chạy test phù hợp và đọc lại diff; chỉ commit/push/deploy khi được yêu cầu.

## Đầu ra

Mã/test theo nhiệm vụ và ghi chú thay đổi cần thiết.

## Hoàn tất

Kết quả đáp ứng yêu cầu, có đường dẫn và cách kiểm tra phù hợp. Nêu điều chưa rõ hoặc chưa kiểm tra; giữ nguyên file/môi trường ngoài phạm vi.
