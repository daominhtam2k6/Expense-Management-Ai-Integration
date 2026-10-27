---
name: requirements-analysis
description: Phân tích nhu cầu, use case, user story và tiêu chí chấp nhận.
---

# Phân tích yêu cầu

## Đầu vào

Yêu cầu hiện tại, file liên quan, phạm vi được sửa và kết quả mong muốn. Xem [cấu trúc tài liệu](../../../docs/README.md). Prompt gợi ý: [01-phan-tich-yeu-cau.md](../../../docs/prompt-library/01-phan-tich-yeu-cau.md).

## Cách thực hiện

1. Đọc yêu cầu người dùng và docs/requirements/.
2. Tách chức năng, quy tắc, NFR và câu hỏi chưa rõ; giữ ID đã có.
3. Mô tả luồng đúng, sai, biên; viết AC có kết quả kiểm tra được.
4. Liên kết yêu cầu → use case/story → AC; chỉ cập nhật tài liệu được giao.

## Đầu ra

docs/requirements/; không sửa mã trong nhiệm vụ phân tích.

## Hoàn tất

Kết quả đáp ứng yêu cầu, có đường dẫn và cách kiểm tra phù hợp. Nêu điều chưa rõ hoặc chưa kiểm tra; giữ nguyên file/môi trường ngoài phạm vi.
