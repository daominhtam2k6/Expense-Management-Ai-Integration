# Code review report

Ngày review: 06/09/2026. Phạm vi: as-built structure, API boundaries, tests và release configuration. Đây là review read-only; lỗi test-discovery được sửa ở bước testing riêng.

## Findings

- **MEDIUM — CR-001:** routers chứa nhiều nghiệp vụ và transaction orchestration, làm tăng coupling và khó kiểm thử transaction boundary. Nên tách service cho goal completion/budget aggregation khi tiếp tục mở rộng.
- **MEDIUM — CR-002:** database invariants chủ yếu được giữ ở Pydantic/application, chưa có đủ CHECK/unique/composite constraints; xem `docs/database-design.md`.
- **LOW — CR-003:** 7 output schema dùng Pydantic class `Config` deprecated, tạo rủi ro khi nâng lên Pydantic 3.
- **LOW — CR-004:** `WHITE_BOX_TEST_REPORT.md` chứa số coverage snapshot không còn trùng kết quả chạy hiện tại; nên ghi rõ snapshot hoặc sinh report tự động trong CI.

## Điểm tích cực đã kiểm chứng

Ownership filter xuất hiện xuyên suốt API nghiệp vụ; Gemini được tách khỏi database và có timeout/retry/error mapping; production build chặn API fallback và path traversal; test hiện tại chạy pass sau khi sửa discovery.

