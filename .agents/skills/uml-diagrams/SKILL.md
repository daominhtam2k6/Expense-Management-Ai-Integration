---
name: uml-diagrams
description: Tạo use case, class, sequence, activity và sắp xếp ERD theo nguồn dự án.
---

# Vẽ và tổ chức sơ đồ

## Đầu vào

Yêu cầu hiện tại, file liên quan, phạm vi được sửa và kết quả mong muốn. Xem [cấu trúc tài liệu](../../../docs/README.md). Prompt gợi ý: [06-ve-so-do-uml.md](../../../docs/prompt-library/06-ve-so-do-uml.md).

## Cách thực hiện

1. Chọn loại sơ đồ theo câu hỏi; đọc yêu cầu hoặc mã thực tế trước khi vẽ.
2. Giữ actor, lớp, quan hệ và thao tác đúng nguồn; không thêm service/entity chỉ để hình đẹp.
3. Use case dùng include/extend đúng ý; sequence có nhánh lỗi; activity có điều kiện; class có quan hệ rõ.
4. Nguồn PlantUML và PNG/SVG đặt trong docs/diagram/<loại>/; ERD nằm riêng erd/.
5. Render local nếu có công cụ, kiểm tra cú pháp, tiếng Việt và cỡ chữ; thiếu ảnh/công cụ thì báo để bổ sung, không lấy ảnh lỗi làm kết quả.

## Đầu ra

docs/diagram/use-case/, erd/, class/, sequence/ hoặc activity/.

## Hoàn tất

Kết quả đáp ứng yêu cầu, có đường dẫn và cách kiểm tra phù hợp. Nêu điều chưa rõ hoặc chưa kiểm tra; giữ nguyên file/môi trường ngoài phạm vi.
