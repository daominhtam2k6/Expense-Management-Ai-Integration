---
name: code-review
description: Review thay đổi về tính đúng, hồi quy, query và khả năng bảo trì.
---

# Rà soát mã

## Đầu vào

Yêu cầu hiện tại, file liên quan, phạm vi được sửa và kết quả mong muốn. Xem [cấu trúc tài liệu](../../../docs/README.md). Prompt gợi ý: [11-review-ma-nguon.md](../../../docs/prompt-library/11-review-ma-nguon.md).

## Cách thực hiện

1. Chốt diff/module cần review; đọc ngữ cảnh, caller, AC và test.
2. Lần validation → auth/ownership → xử lý → database → response.
3. Kiểm tra tiền tệ, rollback, cạnh tranh, query lặp và nhánh lỗi khi liên quan.
4. Nêu finding với vị trí, trigger, ảnh hưởng và hướng sửa; phân biệt lỗi có căn cứ với điều cần kiểm tra thêm.
5. Review không tự sửa mã; chỉ lưu báo cáo khi nhiệm vụ yêu cầu.

## Đầu ra

Phản hồi review hoặc docs/software/testing/code-review.md.

## Hoàn tất

Kết quả đáp ứng yêu cầu, có đường dẫn và cách kiểm tra phù hợp. Nêu điều chưa rõ hoặc chưa kiểm tra; giữ nguyên file/môi trường ngoài phạm vi.
