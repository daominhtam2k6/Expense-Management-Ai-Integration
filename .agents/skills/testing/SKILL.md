---
name: testing
description: Lập ca đúng, sai, biên; kiểm tra backend/frontend và so sánh prompt AI.
---

# Kiểm thử hệ thống và AI

## Đầu vào

Yêu cầu hiện tại, file liên quan, phạm vi được sửa và kết quả mong muốn. Xem [cấu trúc tài liệu](../../../docs/README.md). Prompt gợi ý: [09-kiem-thu-he-thong.md](../../../docs/prompt-library/09-kiem-thu-he-thong.md).

## Cách thực hiện

1. Đọc AC và thay đổi cần kiểm tra; lập ca đầu vào, bước thực hiện, expected.
2. Dùng dữ liệu giả và account A/B; kiểm tra dữ liệu rỗng, validation, ownership và lỗi dịch vụ.
3. Chọn unit/API/UI phù hợp; backend dùng venv dự án và pytest, frontend dùng npm.cmd test; build khi cần.
4. Với Gemini, so sánh hai prompt trên cùng aggregate/câu hỏi, kiểm tra đúng số, grounding, thiếu dữ liệu, timeout và privacy.
5. Phân biệt kết quả thực với phần chưa chạy; không sửa expected để che bug hoặc dùng database production làm fixture.

## Đầu ra

tests/ hoặc frontend test nếu được giao; báo cáo ở docs/software/testing/.

## Hoàn tất

Kết quả đáp ứng yêu cầu, có đường dẫn và cách kiểm tra phù hợp. Nêu điều chưa rõ hoặc chưa kiểm tra; giữ nguyên file/môi trường ngoài phạm vi.
