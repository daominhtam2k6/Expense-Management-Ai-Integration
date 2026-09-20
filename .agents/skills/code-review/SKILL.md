---
name: code-review
description: Rà soát chỉ đọc dựa trên bằng chứng đối với Sổ Chi Tiêu về tính đúng đắn, tuân thủ yêu cầu và kiến trúc, khả năng bảo trì, hiệu năng và chất lượng kiểm thử.
---

# Rà soát mã nguồn

## Quy trình

1. Xác định phạm vi review: diff, commit, module hoặc toàn hệ thống; ghi rõ phần bị loại khỏi phạm vi.
2. Đọc requirements, acceptance criteria, kiến trúc và database design liên quan trước khi đánh giá mã.
3. Kiểm tra correctness theo luồng dữ liệu, validation, transaction, error path, boundary và trạng thái cạnh tranh có liên quan.
4. Kiểm tra requirement/architecture compliance, đặc biệt ownership filtering, API contract, privacy boundary và migration discipline.
5. Kiểm tra maintainability: coupling, duplication, naming, abstraction, dead code và khả năng kiểm thử; chỉ ghi finding khi có tác động cụ thể.
6. Kiểm tra performance theo query pattern, N+1, vòng lặp, payload, render và I/O; phân biệt defect đã chứng minh với rủi ro cần đo.
7. Đánh giá test: requirement coverage, negative/boundary/ownership path, độ cô lập và khả năng phát hiện regression.
8. Với mỗi finding, ghi severity `CRITICAL`, `HIGH`, `MEDIUM` hoặc `LOW`, trạng thái confirmed/risk/gap, bằng chứng file:dòng, tác động và hướng khắc phục.
9. Sắp xếp finding theo severity; ghi riêng điều đã kiểm tra không có finding và điều chưa kiểm tra.
10. Cập nhật `docs/code-review.md` với ngày, phạm vi, phương pháp, finding và giới hạn.

## Ràng buộc

- Review chỉ đọc: không sửa mã trong skill này.
- Không đưa nhận xét phong cách thuần túy nếu không ảnh hưởng correctness, maintainability hoặc yêu cầu dự án.
- “Không có finding” không đồng nghĩa “an toàn” hoặc “đã kiểm tra toàn bộ”.
