---
name: security-review
description: Rà soát đăng nhập, quyền dữ liệu, API key, upload và dữ liệu gửi AI.
---

# Kiểm tra bảo mật cơ bản

## Đầu vào

Yêu cầu hiện tại, file liên quan, phạm vi được sửa và kết quả mong muốn. Xem [cấu trúc tài liệu](../../../docs/README.md). Prompt gợi ý: [12-kiem-tra-bao-mat.md](../../../docs/prompt-library/12-kiem-tra-bao-mat.md).

## Cách thực hiện

1. Đọc auth, API, upload, Gemini và cấu hình mẫu; không đọc/chia sẻ secret thật.
2. Kiểm tra password/token, quyền tài nguyên của account A/B và dữ liệu trả về.
3. Kiểm tra input, path upload, lỗi lộ chi tiết và key không xuất hiện trong frontend/log.
4. Kiểm tra payload AI không lộ danh tính, ghi chú hoặc raw transaction; câu hỏi/hội thoại không được cấp quyền thao tác.
5. Báo lỗi, tác động và cách khắc phục; không thử tấn công production hoặc tự chứng nhận an toàn.

## Đầu ra

docs/software/testing/security-review.md hoặc nhận xét theo yêu cầu.

## Hoàn tất

Kết quả đáp ứng yêu cầu, có đường dẫn và cách kiểm tra phù hợp. Nêu điều chưa rõ hoặc chưa kiểm tra; giữ nguyên file/môi trường ngoài phạm vi.
