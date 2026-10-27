---
name: architecture-design
description: Thiết kế kiến trúc, API, giao diện và luồng AI phù hợp quy mô dự án.
---

# Thiết kế phần mềm

## Đầu vào

Yêu cầu hiện tại, file liên quan, phạm vi được sửa và kết quả mong muốn. Xem [cấu trúc tài liệu](../../../docs/README.md). Prompt gợi ý: [03-thiet-ke-kien-truc.md](../../../docs/prompt-library/03-thiet-ke-kien-truc.md).

## Cách thực hiện

1. Đọc yêu cầu, mã/config liên quan và DESIGN.md nếu có UI.
2. Nêu thành phần, trách nhiệm, API, luồng dữ liệu và xử lý lỗi.
3. Giữ FastAPI/React và cách deploy hiện tại; giải thích phương án thay đổi nếu được hỏi.
4. Với AI, xác định dữ liệu tổng hợp được gửi, prompt và giới hạn; với UI, có loading/empty/error và responsive.
5. Phân biệt mô tả hiện trạng với đề xuất; dùng uml-diagrams khi cần hình.

## Đầu ra

docs/software/design/; hình ở docs/diagram/.

## Hoàn tất

Kết quả đáp ứng yêu cầu, có đường dẫn và cách kiểm tra phù hợp. Nêu điều chưa rõ hoặc chưa kiểm tra; giữ nguyên file/môi trường ngoài phạm vi.
