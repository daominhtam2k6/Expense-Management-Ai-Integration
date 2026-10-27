# Các agent hỗ trợ dự án

Có **10 agent chuyên môn**. Codex trong phiên làm việc hiện tại nhận yêu cầu và giao việc; không cần tạo thêm profile Codex chính.

| Agent | Công việc | Skill |
|---|---|---|
| [requirement](requirement/prompt.md) | Làm rõ nhu cầu, FR/NFR, use case và AC. | [requirements-analysis](../.agents/skills/requirements-analysis/SKILL.md) |
| [design](design/prompt.md) | Thiết kế phần mềm, dữ liệu, API và giao diện. | [architecture-design](../.agents/skills/architecture-design/SKILL.md), [database-design](../.agents/skills/database-design/SKILL.md), [uml-diagrams](../.agents/skills/uml-diagrams/SKILL.md) |
| [coding](coding/prompt.md) | Viết tính năng hoặc sửa lỗi theo yêu cầu. | [implementation](../.agents/skills/implementation/SKILL.md) |
| [testing](testing/prompt.md) | Lập và thực hiện test, ghi expected/actual và lỗi. | [testing](../.agents/skills/testing/SKILL.md) |
| [critic](critic/prompt.md) | Đọc mã và phản biện kết quả, nêu lỗi cần sửa. | [code-review](../.agents/skills/code-review/SKILL.md) |
| [security](security/prompt.md) | Kiểm tra auth, quyền dữ liệu, key và privacy AI. | [security-review](../.agents/skills/security-review/SKILL.md) |
| [ai](ai/prompt.md) | Thiết kế prompt Gemini và so sánh chất lượng trả lời. | [architecture-design](../.agents/skills/architecture-design/SKILL.md), [testing](../.agents/skills/testing/SKILL.md) |
| [documentation](documentation/prompt.md) | Biên soạn báo cáo, tài liệu và sơ đồ. | [documentation](../.agents/skills/documentation/SKILL.md), [uml-diagrams](../.agents/skills/uml-diagrams/SKILL.md) |
| [deployment](deployment/prompt.md) | Chuẩn bị hoặc thực hiện triển khai trong phạm vi được giao. | [deployment](../.agents/skills/deployment/SKILL.md) |
| [maintenance](maintenance/prompt.md) | Chẩn đoán, đề xuất sửa và kiểm tra phục hồi hệ thống. | [deployment](../.agents/skills/deployment/SKILL.md), [implementation](../.agents/skills/implementation/SKILL.md), [testing](../.agents/skills/testing/SKILL.md) |

Mỗi thư mục có `prompt.md` (vai trò/cách nhận việc), `skill.md` (skill sử dụng), `config.yaml` (thông tin profile). Config mô tả công việc, không tự khởi chạy agent. Khi được giao dùng subagent, Codex chọn công cụ đang có và phân công file rõ ràng để tránh sửa chồng.

Prompt đầy đủ tại [docs/prompt-library](../docs/prompt-library/README.md); tài liệu và sơ đồ tại [docs](../docs/README.md). Không cần thư mục đánh giá agent riêng.
