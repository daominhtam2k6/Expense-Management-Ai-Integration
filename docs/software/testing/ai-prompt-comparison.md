# So sánh prompt — TC-037, chỉ N1

Ngày nhận và đánh giá: **28/10/2026**, Asia/Saigon. Thiết kế: **3 prompt, mỗi prompt 1 lần, tổng 3 phản hồi**. **TC-037: PASS trên N1**, theo ba phản hồi người dùng cung cấp và xác nhận cùng điều kiện. **Chọn P3** cho lượt so sánh này.

Nguồn: [kế hoạch](test-plan.md), [hướng dẫn và snapshot N1](ai-prompt-n1-guide.md), [phản hồi và xác nhận của người dùng](evidence/tc037-n1-2026-10-28-user-responses.md). Codex chỉ đối chiếu nội dung, không gọi thêm AI hoặc tạo lại phản hồi.

## Điều kiện và giới hạn bằng chứng

- Người dùng cung cấp ba phản hồi P1/P2/P3 và xác nhận: “cùng cấu hình model, cùng dữ liệu, chỉ thay đổi system prompt theo hướng dẫn”.
- Câu hỏi theo hướng dẫn: `Tháng 10/2026 tôi chi bao nhiêu, tăng bao nhiêu so với tháng 09?`
- Snapshot/system prompt tham chiếu: N1 và P1/P2/P3 trong hướng dẫn. Việc dùng theo hướng dẫn được người dùng xác nhận, chưa có bản xuất request để đối chiếu độc lập.
- Tên model/version cụ thể, temperature/top-p/giới hạn đầu ra và giờ thực thi chưa được cung cấp. Không suy ra từ các lần kiểm thử live trước; khả năng tái lập còn hạn chế.
- Đây là đánh giá prompt độc lập do người dùng thực hiện; không chứng minh ba prompt đã được tích hợp vào web.
- Chỉ kết luận trên ba phản hồi N1 này, không suy ra độ ổn định nhiều lượt, chống ép đoán, xử lý dữ liệu thiếu hoặc khả năng tư vấn trong các tình huống thiếu hụt tài chính.

## Đáp án độc lập

| Nội dung | Phép tính / đáp án |
|---|---|
| Chi tháng 10/2026 | 3.000.000 + 1.000.000 = **4.000.000 VND** |
| Chi tháng 09/2026 | **2.000.000 VND** |
| Tăng tuyệt đối | 4.000.000 − 2.000.000 = **2.000.000 VND** |
| Tăng tương đối | (4.000.000 − 2.000.000) / 2.000.000 × 100 = **100%** |
| Ăn uống | Tăng **1.000.000 VND / 50%**; chiếm **75%** tổng chi tháng 10 |
| Đi lại | Tăng **1.000.000 VND** từ 0, khoản mới phát sinh; không chia cho 0 |
| Thu nhập | 10.000.000 → 12.000.000, tăng **2.000.000 VND** |
| Chênh lệch thu–chi | **8.000.000 VND** mỗi kỳ; chưa xác định tiền thực sự có thể phân bổ |
| Số giao dịch tháng 10 nếu nhắc | **3 tổng cộng = 2 chi + 1 thu**; cả ba phản hồi không khẳng định sai số giao dịch |

Cả ba đều đúng ba kết quả bắt buộc của N1 và các số liệu thực tế được nhắc. Không phát hiện bịa số tiền thực tế hoặc sai phép tính trong ba phản hồi này. Căn cứ của lời khuyên được đánh giá riêng.

## Bảng so sánh chất lượng

| Phiên bản | Phản hồi / dẫn chứng | Đối chiếu số liệu | Nhận xét chất lượng | Kết luận |
|---|---|---|---|---|
| P1 | [P1](evidence/tc037-n1-2026-10-28-user-responses.md#p1): tăng 2 triệu/100%; “trích ngay ít nhất 50% ... khoảng 1.000.000 VND” | PASS số liệu N1; tổng chi, mức tăng, danh mục, net 8 triệu, tỷ trọng 75% đều đúng | Dễ hiểu, có phân tích danh mục. Khoản 1 triệu là đề xuất; hạn mức 2,5 triệu có nhãn ví dụ, không phải dữ liệu thực tế bịa. Tuy nhiên “trích ngay” chưa kèm điều kiện về nghĩa vụ/tiền dành riêng. “Cảnh giác lạm phát lối sống” là cảnh báo, chưa đủ căn cứ để xác nhận nguyên nhân tăng chi | Đạt số liệu N1; không chọn vì lời khuyên cần điều kiện rõ hơn |
| P2 | [P2](evidence/tc037-n1-2026-10-28-user-responses.md#p2): dẫn current.expense/previous.expense; “chuyển ngay khoản tích lũy 8.000.000 VND ... vào quỹ tiết kiệm/đầu tư” | PASS số liệu N1; phép tính và tỷ lệ đều đúng. Có thể bổ sung phép chia cho kỳ trước để giải thích 100% đầy đủ hơn | Nêu nguồn rõ; nhưng dùng net 8 triệu để khuyên chuyển ngay toàn bộ như tiền có thể phân bổ, dù snapshot chưa xác định khả dụng/nghĩa vụ/tiền dành riêng. Đây là suy luận thiếu căn cứ trong lời khuyên, không phải bịa con số 8 triệu | Đạt số liệu N1; không chọn vì lời khuyên sử dụng tiền chưa đủ căn cứ |
| P3 | [P3](evidence/tc037-n1-2026-10-28-user-responses.md#p3): “khoản 8.000.000 VND này chưa được coi là số dư khả dụng” | PASS số liệu N1; tổng chi, mức tăng, tỷ lệ, danh mục và net đều đúng | Trả lời N1 trước khi nêu giới hạn; phân biệt net và khả dụng. Nêu các thông tin còn thiếu mà không mặc định người dùng có nợ; không trì hoãn trả lời câu hỏi chính để đòi thêm dữ liệu. Hơi dài so với câu hỏi số liệu | Đạt; **chọn P3** trên ba phản hồi này |

## Kết luận

- **TC-037 PASS:** có đủ ba phản hồi được người dùng xác nhận cùng điều kiện, đối chiếu số liệu và nhận xét cụ thể; P3 đạt tiêu chí để chọn. Không yêu cầu mọi prompt đối chứng có chất lượng tư vấn ngang nhau.
- Chỉ xét ba đáp án số liệu chính, **P1/P2/P3 đều đạt**; chưa có bằng chứng P3 tính toán tốt hơn hai prompt còn lại trên N1.
- **Chọn P3 vì cách diễn giải và giới hạn của lời khuyên:** không coi net là tiền chắc chắn có thể chuyển ngay. Không chọn chỉ vì prompt hoặc câu trả lời dài hơn.
- P2 nên sửa cách gọi net là “tích lũy” và điều kiện chuyển ngay 8 triệu; P1 nên thêm điều kiện trước lời khuyên trích tiền ngay. Các nhận xét này chỉ dựa trên ba phản hồi N1, chưa chứng minh khả năng tư vấn trong các tình huống thiếu hụt tài chính.
- Chưa chạy lại, chưa triển khai prompt được chọn, chưa sửa kết quả các lần kiểm thử live cũ.

Muốn tái lập cần bổ sung tên model/version, tham số và bản xuất đầu vào; không cần thêm lượt để chấm ba phản hồi đã có.
