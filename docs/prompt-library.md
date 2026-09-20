# Thư viện prompt SDLC hoàn chỉnh

> Các prompt dưới đây được tạo hồi tố ngày 06/09/2026 theo ủy quyền của Đào Minh Tâm để chuẩn hóa hình thức hồ sơ. Chúng là **prompt mẫu sẵn sàng sử dụng**, không phải bằng chứng rằng implementation cũ đã được tạo bằng các prompt này. Khi thực sự chạy prompt, phải bổ sung ngày chạy, artifact, kết quả test và human verification vào `docs/prompts.md` và `docs/ai-process-log.md`.

## TP-ARCH-001 — Thiết kế kiến trúc tổng quan

```text
VAI TRÒ
Bạn là Software Architect của dự án Sổ Chi Tiêu. Hãy sử dụng architecture-design skill.

BỐI CẢNH
Sản phẩm quản lý tài chính cá nhân bằng tiếng Việt, gồm web/PWA và ứng dụng Windows Tauri. Cả hai online-only, dùng chung backend FastAPI và database máy chủ. Gemini chỉ phân tích dữ liệu tổng hợp, không sửa dữ liệu.

ĐẦU VÀO BẮT BUỘC
- docs/requirements.md
- docs/user-stories.md
- docs/acceptance-criteria.md
- docs/requirements-issues.md
- docs/human-gates.md

MỤC TIÊU
Thiết kế kiến trúc tổng quan đáp ứng toàn bộ requirements đã được phê duyệt và giữ traceability.

PHẠM VI
- Client React/PWA và Tauri
- FastAPI API/application layer
- SQLAlchemy, Alembic, PostgreSQL/SQLite development
- Gemini, Resend, avatar storage
- Authentication, authorization, trust boundaries, deployment và observability

RÀNG BUỘC
- Chỉ sử dụng requirements đã APPROVED.
- Không viết source code hoặc migration.
- Không đưa offline vào phạm vi hiện tại.
- Mọi dữ liệu nghiệp vụ phải tách biệt theo user.
- Dữ liệu gửi Gemini phải được tối thiểu hóa và truyền qua HTTPS.
- Mỗi quyết định lớn phải có rationale và trade-off.
- Nếu requirement chưa đủ rõ, dừng tại điểm đó và ghi issue; không tự đặt business rule.

ĐẦU RA
- Cập nhật docs/architecture.md.
- Cập nhật docs/architecture-decisions.md bằng ADR có trạng thái PROPOSED.
- Tạo bảng traceability requirement → component.
- Liệt kê rủi ro và câu hỏi cần Human Gate.

KIỂM CHỨNG
- Mỗi FR có ít nhất một component chịu trách nhiệm.
- Xác định rõ data flow, external systems và security boundaries.
- Không mô tả chức năng chưa có requirement.
- Không đánh dấu Architecture Gate APPROVED thay người dùng.
```

## TP-STACK-001 — Lựa chọn công cụ và framework

```text
VAI TRÒ
Bạn là Technical Lead. Hãy đánh giá technology stack cho Sổ Chi Tiêu dựa trên requirements và architecture đã được duyệt.

ĐẦU VÀO
- docs/requirements.md
- docs/architecture.md
- docs/architecture-decisions.md
- requirements.txt
- frontend/package.json
- frontend/src-tauri/Cargo.toml

MỤC TIÊU
Xác nhận công cụ/framework hiện tại có phù hợp hay không và chỉ đề xuất thay đổi khi có lợi ích đo được.

CẦN ĐÁNH GIÁ
- FastAPI, Pydantic, SQLAlchemy, Alembic
- PostgreSQL production và SQLite development
- React, TypeScript, Vite, Vitest, PWA
- Tauri cho Windows
- Gemini REST integration và Resend
- Docker Compose, Caddy và Azure deployment

TIÊU CHÍ
Khả năng đáp ứng requirements, bảo mật, maintainability, testability, hiệu năng ở tải bình thường, khả năng triển khai, chi phí vận hành và năng lực nhóm.

RÀNG BUỘC
- Không chạy upgrade dependency và không sửa code.
- Không thêm technology chỉ vì phổ biến.
- Phân biệt MUST, SHOULD và OPTIONAL.
- Với mỗi đề xuất thay đổi, nêu migration cost, risk và phương án giữ nguyên.

ĐẦU RA
- Tạo docs/technology-stack.md.
- Lập bảng technology → purpose → version hiện tại → quyết định → rationale.
- Ghi các quyết định cần con người duyệt thành ADR PROPOSED.

KIỂM CHỨNG
Không có framework nào thiếu mục đích rõ ràng; các phiên bản phải lấy từ repository, không đoán; không tuyên bố dependency an toàn nếu chưa chạy vulnerability scan.
```

## TP-BE-001 — Thiết kế backend

```text
VAI TRÒ
Bạn là Backend Architect chuyên FastAPI/SQLAlchemy. Hãy sử dụng architecture-design skill; đây là task thiết kế, không implementation.

ĐẦU VÀO
- docs/requirements.md
- docs/acceptance-criteria.md
- docs/architecture.md
- docs/database-design.md
- app/routers, app/schemas, app/models, app/core chỉ để đọc hiện trạng

MỤC TIÊU
Thiết kế backend module boundaries, API contracts, transaction boundaries và error model đáp ứng requirements đã duyệt.

PHẠM VI
- Auth/profile/password reset/account deletion
- Category, transaction, budget và saving goal
- Dashboard/report aggregation
- Assistant conversation và aggregate-only Gemini gateway
- Health/readiness, uploads và external email

RÀNG BUỘC
- Không sửa source code, schema hoặc migration.
- Mọi query nghiệp vụ ràng buộc current_user.id.
- Xóa tài khoản yêu cầu re-authentication và hard-delete dữ liệu active.
- Tiền dùng Decimal; API hiển thị/làm tròn theo requirements.
- Lỗi không lộ stack trace, secret hoặc dữ liệu người khác.
- Gemini không truy cập database trực tiếp.

ĐẦU RA
- Tạo docs/backend-design.md.
- Sơ đồ router → service → repository/model.
- API/error/transaction/idempotency rules.
- Traceability endpoint/service → FR/AC.
- Danh sách khác biệt giữa as-built và target design.

KIỂM CHỨNG
Bao phủ positive, negative, authorization, rollback và external-service failure paths. Dừng và báo cáo nếu thiết kế đòi hỏi thay đổi requirement/architecture đã duyệt.
```

## TP-FE-001 — Thiết kế frontend

```text
VAI TRÒ
Bạn là Frontend Architect/UX Engineer cho React + TypeScript. Hãy thiết kế frontend dựa trên requirements và DESIGN.md đã duyệt.

ĐẦU VÀO
- docs/requirements.md
- docs/user-stories.md
- docs/acceptance-criteria.md
- docs/architecture.md
- DESIGN.md
- frontend/src chỉ để phân tích hiện trạng

MỤC TIÊU
Thiết kế cấu trúc frontend, routing, state/data flow, accessibility và error handling thống nhất cho web/PWA/Tauri online-only.

PHẠM VI
- Authentication và route guards
- Dashboard, categories, transactions, budgets, goals, reports, assistant
- Profile/avatar và xóa tài khoản
- Loading, empty, validation, error, retry và mất kết nối
- Responsive, keyboard/focus, reduced motion và theme

RÀNG BUỘC
- Không viết hoặc sửa source code.
- Không lưu dữ liệu nghiệp vụ như một offline database.
- Không hiển thị mutation thành công trước khi server xác nhận.
- Không đưa Gemini/API secret vào frontend.
- Giữ design tokens và nguyên tắc trong DESIGN.md.
- Không thay đổi API contract đã duyệt mà không ghi issue.

ĐẦU RA
- Tạo docs/frontend-design.md.
- Component/page hierarchy, route map và data-flow diagram.
- State/error/accessibility checklist.
- Mapping US/AC → screen/component/test scenario.

KIỂM CHỨNG
Mỗi user story có UI path; mọi mutation có loading/success/error; 401 dẫn đến xóa phiên; mất mạng có thông báo và không tạo false success; modal/drawer quản lý focus đúng.
```

## TP-DB-001 — Thiết kế database và migration

```text
VAI TRÒ
Bạn là Database Architect. Hãy sử dụng database-design skill.

ĐẦU VÀO
- docs/requirements.md
- docs/architecture.md
- docs/database-design.md
- app/models
- alembic/versions

MỤC TIÊU
Tạo thiết kế migration cho constraints, indexes, normalized identity, ownership và account deletion đã được Database Gate phê duyệt.

RÀNG BUỘC
- Chưa viết migration hoặc sửa models trong bước thiết kế.
- Không sửa migration ban đầu đã phát hành.
- Category unique theo owner/type/tên đã trim và không phân biệt hoa thường.
- Năm ngân sách 2000–2100.
- Gặp collision/duplicate phải dừng và báo cáo, không tự sửa hoặc xóa.
- Hard delete dữ liệu active; backup retention tối đa 30 ngày.
- Thiết kế phải dùng được với PostgreSQL production và SQLite development.

ĐẦU RA
- ERD dạng text.
- Danh sách PK/FK/UNIQUE/CHECK/INDEX/ON DELETE.
- Kế hoạch audit, backfill, upgrade, rollback và verification.
- Traceability constraint/index → requirement.

KIỂM CHỨNG
Kiểm tra normalization, money precision, cross-user references, delete order, duplicate data và query patterns. Không đánh dấu migration hoàn thành khi chưa chạy trên database đại diện.
```

## TP-AI-001 — Thiết kế backend cho trợ lý Gemini

```text
VAI TRÒ
Bạn là AI Application Architect chịu trách nhiệm privacy và grounding cho trợ lý tài chính.

ĐẦU VÀO
- docs/requirements.md
- docs/acceptance-criteria.md
- docs/architecture.md
- app/core/assistant_context.py
- app/core/gemini.py
- app/routers/assistant.py

MỤC TIÊU
Thiết kế luồng Question → Aggregate Context → Prompt → Gemini → Response/Evidence mà không gửi dữ liệu thô hoặc cho AI sửa dữ liệu.

RÀNG BUỘC
- Chỉ dùng aggregate theo kỳ và category label an toàn.
- Cấm identity, internal ID, note, raw transaction và category name tự nhập.
- API key chỉ ở backend/environment; kết nối Gemini qua HTTPS.
- Không tuyên bố end-to-end encryption với Gemini.
- Có timeout, retry hữu hạn, rate-limit/error mapping và store=false khi API hỗ trợ.
- Câu trả lời là tham khảo, tách actual với forecast và nêu confidence.
- Không sửa code trong task này.

ĐẦU RA
- Tạo docs/assistant-design.md.
- Data classification và allowlist/denylist.
- Sequence/data-flow diagram.
- Prompt contract, failure modes và security controls.
- Mapping FR-AI/NFR-PRIV → module/test.

KIỂM CHỨNG
Chứng minh payload mẫu không chứa trường bị cấm; empty/sparse context không tạo số liệu; upstream failure không lộ secret/stack trace; Gemini không có đường truy cập database.
```

## TP-DEPLOY-001 — Thiết kế triển khai và vận hành

```text
VAI TRÒ
Bạn là DevOps/SRE Architect cho hệ thống quy mô nhỏ, online-only.

ĐẦU VÀO
- docs/requirements.md
- docs/architecture.md
- docs/database-design.md
- README.md
- docs/azure-deploy.md
- Dockerfile, compose*.yaml, deploy/Caddyfile, .env.example

MỤC TIÊU
Thiết kế deployment đáp ứng gần 24/7, xử lý sự cố trong 24 giờ, phản hồi dưới 10 giây ở tải bình thường và backup retention sau account deletion tối đa 30 ngày.

PHẠM VI
Build/release, HTTPS, PostgreSQL, migration, persistent avatar, secrets, health/readiness, logs, metrics, backup/restore và incident runbook.

RÀNG BUỘC
- Không deploy và không thay đổi hạ tầng/source code.
- Không ghi secret vào tài liệu.
- Migration chạy trước traffic và phải dừng khi phát hiện dữ liệu xung đột.
- Backup cần lịch, encryption, restore test và retention evidence.
- Phân biệt mục tiêu đã duyệt với RPO/RTO hoặc capacity chưa được quyết định.

ĐẦU RA
- Cập nhật docs/deployment.md hoặc tạo proposal riêng.
- Deployment diagram và pre/post-deploy checklist.
- Backup/restore/retention plan.
- Monitoring/incident checklist và rollback conditions.

KIỂM CHỨNG
Mỗi NFR vận hành có metric/evidence hoặc được đánh dấu chưa quyết định; không tuyên bố SLA/security compliance nếu chưa đo hoặc kiểm thử.
```
