# API overview

Base path: `/api`. Các endpoint nghiệp vụ (trừ register, login, forgot/reset password, health và readiness) yêu cầu `Authorization: Bearer <token>`. OpenAPI có tại `/api/docs` khi `ENABLE_API_DOCS=true`.

| Nhóm | Endpoint chính |
|---|---|
| System | `GET /health`, `GET /ready` |
| Auth | `POST /auth/register`, `POST /auth/login`, `GET/PUT /auth/me`, avatar, forgot/reset password |
| Categories | `GET/POST /categories/`, `PUT/DELETE /categories/{id}` |
| Transactions | `GET/POST /transactions/`, `PUT/DELETE /transactions/{id}` |
| Budgets | `GET/POST /budgets/`, `PUT/DELETE /budgets/{id}` |
| Goals | CRUD goal, items, deposit, withdraw, complete và history dưới `/goals` |
| Analytics | `GET /dashboard/`, `GET /reports/` |
| Assistant | context, conversations và `POST /assistant/messages` dưới `/assistant` |

Schema request/response chuẩn được sinh trực tiếp từ Pydantic/OpenAPI. Không dùng bảng này thay cho OpenAPI khi cần chi tiết field và validation.

