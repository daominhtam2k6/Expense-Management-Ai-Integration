# Prompt theo các giai đoạn SDLC

15 prompt được viết theo trình tự hình thành sản phẩm. Mỗi file gồm tiêu đề và một đoạn prompt đầy đủ, dùng trực tiếp để giao việc cho Codex. Bước phân tích dùng mô tả nhu cầu và quyết định nghiệp vụ; bước thiết kế dùng kết quả phân tích; từ bước lập trình trở đi mới sử dụng mã, cấu hình và kết quả chạy. Các bước kiểm thử, sửa lỗi và review có thể lặp lại khi phát hiện vấn đề.

| Thứ tự | Giai đoạn | Prompt |
|---|---|---|
| 01 | Phân tích | [Phân tích nhu cầu và phạm vi dự án](01-phan-tich-yeu-cau.md) |
| 02 | Phân tích | [Đặc tả user story use case và tiêu chí chấp nhận](02-user-story-va-ac.md) |
| 03 | Thiết kế | [Thiết kế kiến trúc ứng dụng](03-thiet-ke-kien-truc.md) |
| 04 | Thiết kế | [Thiết kế dữ liệu và sơ đồ ERD](04-thiet-ke-co-so-du-lieu.md) |
| 05 | Thiết kế | [Thiết kế màn hình và hợp đồng API](05-thiet-ke-api-va-giao-dien.md) |
| 06 | Thiết kế | [Mô hình hóa các luồng bằng UML](06-ve-so-do-uml.md) |
| 07 | Thiết kế | [Thiết kế chức năng trợ lý Gemini](07-thiet-ke-tich-hop-gemini.md) |
| 08 | Lập trình | [Lập trình theo yêu cầu và thiết kế](08-lap-trinh-tinh-nang.md) |
| 09 | Kiểm thử | [Kiểm thử chức năng và quyền dữ liệu](09-kiem-thu-he-thong.md) |
| 10 | Sửa lỗi | [Sửa lỗi phát hiện từ kiểm thử](10-sua-loi-sau-kiem-thu.md) |
| 11 | Rà soát | [Review bản triển khai sau sửa lỗi](11-review-ma-nguon.md) |
| 12 | Rà soát | [Kiểm tra bảo mật trước phát hành](12-kiem-tra-bao-mat.md) |
| 13 | Kiểm thử AI | [So sánh chất lượng 3 prompt trên N1, mỗi prompt 1 lần](13-so-sanh-prompt-ai.md) |
| 14 | Hoàn thiện tài liệu | [Hoàn thiện báo cáo và hướng dẫn sử dụng](14-viet-bao-cao-va-tai-lieu.md) |
| 15 | Triển khai và bảo trì | [Chuẩn bị triển khai và bảo trì](15-trien-khai-va-bao-tri.md) |

Đây là thư viện nội dung giao việc theo giai đoạn. Mỗi prompt xác định nguồn, nhiệm vụ, skill, đầu ra và điều kiện hoàn tất phù hợp với bước đó; việc thực thi vẫn theo yêu cầu cụ thể trong cuộc trao đổi.

## System prompt dùng cho phép so sánh

Ngoài 15 prompt giao việc theo SDLC, thư viện có [3 system prompt P1/P2/P3](so-sanh-ai/README.md) cho TC-037: [P1 cơ bản](so-sanh-ai/p1-co-ban.md), [P2 ràng buộc số liệu](so-sanh-ai/p2-rang-buoc-so-lieu.md), [P3 thêm ràng buộc khả năng tài chính](so-sanh-ai/p3-rang-buoc-kha-nang-tai-chinh.md). Nội dung giữ nguyên theo hướng dẫn N1; không đổi số thứ tự 15 giai đoạn.
