# Nhật ký AI-Augmented SDLC

Tài liệu này bắt đầu ngày 06/09/2026; không tái tạo giả các prompt hoặc human correction trước đó.

Prompt nguyên văn và liên kết artifact được lưu tại `docs/prompts.md`; tài liệu này chỉ giữ tóm tắt quá trình.

## Phiên 06/09/2026 — Đối chiếu hướng dẫn SDLC

- **Prompt người dùng:** đọc file hướng dẫn, đánh giá mức tuân thủ, chỉ ra và bổ sung phần thiếu.
- **Nguồn:** DOCX do người dùng cung cấp; repository; Git log; test/build local.
- **AI artifacts:** bộ project skills; requirements/stories/AC/issues; architecture/ADR/database; gates; test/review/security reports; audit.
- **Tool evidence:** đọc OOXML; `rg`; Git read-only; pytest; Vitest coverage; TypeScript/Vite/PWA build; `apply_patch`.
- **Lỗi AI/tool phát hiện:** pytest thu thập nhầm test trong ignored `deliverables/`.
- **Sửa bởi AI:** thêm `pytest.ini`; bỏ `.agents/` khỏi `.gitignore` để skill có thể quản lý bằng Git.
- **Human corrections:** Đào Minh Tâm phê duyệt Requirements Gate và quyết định RQ-001..RQ-008 ngày 06/09/2026. Baseline được cập nhật; yêu cầu app offline được ghi rõ là chưa được kiến trúc/implementation hiện tại đáp ứng.
- **MCP:** không dùng; dự án không đặt issue/external data source trong phạm vi yêu cầu này. MCP là tùy điều kiện, không nên dùng chỉ để đủ hình thức.

## Phiên 06/09/2026 — Đánh giá kiến trúc offline

- **Human input:** offline cho hầu hết tính năng trừ AI; đánh giá sync; yêu cầu mã hóa, ít nhất dữ liệu gửi AI; xóa toàn bộ tài khoản; phản hồi dưới 10 giây ở tải bình thường.
- **AI assessment:** khả thi nhưng là thay đổi trung bình-cao; implementation hiện chỉ online-first và không có local DB/sync engine.
- **Artifacts cập nhật:** requirements clarification, acceptance criteria, architecture target, ADR-007..010 và issue decisions.
- **Human Gate:** Architecture vẫn `PENDING`; chưa sửa source code.

## Phiên 06/09/2026 — Thu hẹp phạm vi kết nối

- **Human correction:** thay quyết định offline bằng online toàn bộ cho cả web và app; offline chỉ được cân nhắc sau nếu có số lượng lớn phản hồi người dùng.
- **Artifacts cập nhật:** requirements baseline v1.1, story/AC kết nối, RQ-008, architecture và ADR.
- **Scope removed:** local database, outbox, sync engine, conflict handling và mã hóa local không còn thuộc release hiện tại.
- **Human Gate:** Requirements vẫn `APPROVED` theo bản sửa của người duyệt; Architecture vẫn `PENDING`.

## Phiên 06/09/2026 — Architecture Gate

- **Human approval:** Đào Minh Tâm phê duyệt Architecture Gate.
- **Decisions:** online-only cho web/app; shared FastAPI/database; offline ngoài scope; Gemini payload tối thiểu hóa qua HTTPS; backup của tài khoản đã xóa giữ tối đa 30 ngày.
- **Artifacts cập nhật:** human gate, ADR status, privacy requirement/acceptance criterion và architecture note.
- **Next gate:** Database `PENDING`; chưa sửa implementation.

## Phiên 06/09/2026 — Chuẩn bị Database Gate

- **Scope:** review models và migration hiện tại đối chiếu requirements/architecture đã duyệt.
- **Artifact:** cập nhật `docs/database-design.md` với constraints, indexes, composite ownership FK, cascade/restrict, backup retention và migration plan.
- **Code status:** không sửa Python, TypeScript, SQL migration hoặc database.
- **Human Gate:** Database `PENDING`, chờ bốn quyết định được liệt kê trong database design.

## Phiên 06/09/2026 — Database Gate

- **Human approval:** Đào Minh Tâm phê duyệt Database Gate.
- **Decisions:** category unique theo owner/type/tên chuẩn hóa; năm ngân sách 2000–2100; migration dừng khi có collision; hard delete active data; backup retention tối đa 30 ngày.
- **Artifacts cập nhật:** gate status, database design, business rules và acceptance criteria.
- **Code status:** chưa tạo migration và chưa sửa source code/database.
- **Next gate:** Implementation/testing rồi Release Gate; Release hiện `PENDING`.

## Phiên 06/09/2026 — Bổ sung prompt evidence

- **Human prompt:** hỏi về phần prompt người dùng trong hồ sơ nộp bài.
- **Artifact:** tạo `docs/prompts.md`, ghi nguyên văn các prompt có bằng chứng và liên kết với skill/artifact/gate.
- **Integrity rule:** không tái dựng prompt cho các commit cũ khi transcript không tồn tại.
- **Code status:** không sửa source code.

## Phiên 06/09/2026 — Tạo thư viện prompt mẫu

- **Human authorization:** cho phép bổ sung prompt đầy đủ để hoàn thiện số lượng và hình thức hồ sơ.
- **Artifact:** `docs/prompt-library.md` gồm bảy prompt SDLC có role, context, input, objective, scope, constraints, outputs, verification và stopping/human-gate conditions.
- **Evidence label:** prompt hồi tố/mẫu, chưa thực thi; không được trình bày như prompt tạo implementation cũ.
- **Code status:** không sửa source code.
