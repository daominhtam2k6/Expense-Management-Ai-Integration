---
name: deployment
description: Chuẩn bị hướng dẫn chạy, deploy, backup, phục hồi và bảo trì theo môi trường được giao.
---

# Triển khai và bảo trì

## Đầu vào

Yêu cầu hiện tại, file liên quan, phạm vi được sửa và kết quả mong muốn. Xem [cấu trúc tài liệu](../../../docs/README.md). Prompt gợi ý: [15-trien-khai-va-bao-tri.md](../../../docs/prompt-library/15-trien-khai-va-bao-tri.md).

## Cách thực hiện

1. Đọc Docker/Compose, cấu hình mẫu và hướng dẫn hiện có; xác định phiên bản và môi trường.
2. Lập thứ tự build, backup, migration preflight, health/readiness, smoke test và rollback.
3. Bảo vệ volume/database/uploads; backup cần có cách thử restore trên môi trường riêng.
4. Với sự cố, kiểm tra chỉ đọc và nêu nguyên nhân/giả thuyết trước khi sửa hoặc restart.
5. Chỉ thực thi khi được yêu cầu rõ; không tự deploy, xóa volume hoặc ghi secret vào tài liệu.

## Đầu ra

docs/software/deployment/ và hướng dẫn vận hành trong phạm vi.

## Hoàn tất

Kết quả đáp ứng yêu cầu, có đường dẫn và cách kiểm tra phù hợp. Nêu điều chưa rõ hoặc chưa kiểm tra; giữ nguyên file/môi trường ngoài phạm vi.
