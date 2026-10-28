# Sổ Chi Tiêu

Ứng dụng quản lý tài chính cá nhân trên web/PWA, hỗ trợ ghi nhận thu chi, lập ngân sách, theo dõi mục tiêu tiết kiệm và hỏi đáp với trợ lý AI dựa trên dữ liệu tài chính tổng hợp.

Giao diện tiếng Việt, hỗ trợ trình duyệt máy tính và thiết bị di động. Mỗi người sử dụng quản lý tài khoản và dữ liệu của mình. Các chức năng nghiệp vụ yêu cầu kết nối Internet, kể cả khi ứng dụng được cài dưới dạng PWA.

## Mục lục

- [Chức năng](#chức-năng)
- [Công nghệ và kiến trúc](#công-nghệ-và-kiến-trúc)
- [Cấu trúc dự án](#cấu-trúc-dự-án)
- [Chạy trên máy cá nhân](#chạy-trên-máy-cá-nhân)
- [Phát triển frontend](#phát-triển-frontend)
- [Cấu hình môi trường](#cấu-hình-môi-trường)
- [Trợ lý AI và dữ liệu](#trợ-lý-ai-và-dữ-liệu)
- [Kiểm thử](#kiểm-thử)
- [Triển khai](#triển-khai)
- [Tài liệu](#tài-liệu)
- [Xử lý lỗi thường gặp](#xử-lý-lỗi-thường-gặp)

## Chức năng

| Nhóm | Khả năng chính |
|---|---|
| Tài khoản và hồ sơ | Đăng ký, đăng nhập bằng tên đăng nhập/email, đăng xuất, khôi phục mật khẩu; cập nhật thông tin, ảnh đại diện, đổi mật khẩu và xóa tài khoản. |
| Danh mục | Quản lý danh mục thu/chi, biểu tượng và màu sắc; kiểm tra trùng tên và dữ liệu đang sử dụng. |
| Giao dịch | Thêm, sửa, xóa khoản thu/chi; tìm kiếm và lọc theo thời gian, loại, danh mục hoặc ghi chú. |
| Ngân sách | Đặt hạn mức theo danh mục chi và tháng; theo dõi số đã chi, số còn lại và tình trạng vượt mức. |
| Mục tiêu tiết kiệm | Quản lý mục tiêu, hạng mục, nạp/rút tiền, lịch sử và cách xử lý tiền khi hoàn thành. |
| Tổng quan và báo cáo | Tổng hợp thu chi theo kỳ, hiển thị cơ cấu, xu hướng và so sánh với kỳ trước. |
| Trợ lý AI | Hỏi đáp tài chính, hiển thị số liệu hỗ trợ câu trả lời, lưu và quản lý hội thoại. |

AI chỉ đưa ra nội dung tham khảo; người sử dụng trực tiếp thực hiện các thay đổi tài chính. Nạp/rút tiền mục tiêu là thao tác ghi nhận trong ứng dụng, không phải chuyển tiền qua ngân hàng.

## Công nghệ và kiến trúc

| Thành phần | Công nghệ |
|---|---|
| Frontend | React 18, TypeScript, React Router, Vite, PWA |
| Backend | Python 3.13, FastAPI, Pydantic, SQLAlchemy 2 |
| Cơ sở dữ liệu | SQLite cho local; PostgreSQL 17 trong Docker Compose |
| Migration | Alembic |
| Xác thực | JWT, mật khẩu băm bằng bcrypt |
| Dịch vụ ngoài | Google Gemini, Resend |
| Kiểm thử và đóng gói | pytest, Vitest, Testing Library, GitHub Actions, Docker |

```text
Trình duyệt / PWA
        │
        ▼
FastAPI ── phục vụ React build và API /api
        ├── SQLAlchemy ── SQLite (local) / PostgreSQL (production)
        ├── uploads/ ── ảnh đại diện
        ├── Google Gemini ── nội dung tư vấn AI
        └── Resend ── email khôi phục mật khẩu
```

Frontend production được build vào `frontend/dist` và phục vụ cùng API qua FastAPI. PWA lưu tài nguyên giao diện; `/api/*` và `/uploads/*` được loại khỏi cơ chế fallback của service worker. Dữ liệu nghiệp vụ được đọc và ghi trên máy chủ.

## Cấu trúc dự án

```text
.
├── app/                   # Backend FastAPI
│   ├── core/              # Xác thực, cấu hình, tổng hợp dữ liệu và tích hợp AI
│   ├── models/            # Mô hình SQLAlchemy
│   ├── routers/           # Các nhóm API
│   └── schemas/           # Kiểm tra dữ liệu request/response
├── frontend/              # Giao diện React/TypeScript và kiểm thử frontend
├── alembic/               # Migration cơ sở dữ liệu
├── tests/                 # Kiểm thử backend
├── deploy/                # Cấu hình reverse proxy
├── docs/                  # Yêu cầu, thiết kế, sơ đồ, kiểm thử và triển khai
├── agents/                # Hồ sơ vai trò hỗ trợ phát triển
├── .agents/skills/        # Skill của dự án
├── scripts/               # Công cụ hỗ trợ và tạo tài liệu
├── tools/                 # Công cụ kiểm tra, tiện ích dự án
├── .github/workflows/     # CI
├── .env.example           # Mẫu cấu hình môi trường
├── compose.yaml           # Web và PostgreSQL
├── compose.azure.yaml     # Cấu hình bổ sung cho Azure và HTTPS
└── Dockerfile             # Build frontend và đóng gói backend
```

`expense.db`, `uploads/` và `.env` là dữ liệu/cấu hình phát sinh khi chạy; không đưa thông tin nhạy cảm hoặc dữ liệu cá nhân vào Git.

## Chạy trên máy cá nhân

Hướng dẫn dùng **Windows PowerShell**, Python **3.13**, Node.js **24**, npm và Git. Phiên bản Python/Node tương ứng với cấu hình CI và Docker của dự án.

### 1. Clone repository

```powershell
git clone https://github.com/daominhtam2k6/Expense-Management-Ai-Integration.git
Set-Location Expense-Management-Ai-Integration
```

### 2. Tạo cấu hình local

Từ thư mục gốc, với lần thiết lập đầu tiên:

```powershell
Copy-Item .env.example .env
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Gán chuỗi vừa tạo cho `SECRET_KEY` trong `.env`. Giữ các thiết lập local:

```dotenv
APP_ENV=development
DATABASE_URL=sqlite:///./expense.db
AUTO_CREATE_SCHEMA=true
ENABLE_API_DOCS=true
FRONTEND_URL=http://127.0.0.1:8000
```

Nếu đã có `.env`, cập nhật giá trị cần thiết thay vì sao chép đè. Có thể để trống khóa Gemini và Resend khi chỉ chạy các chức năng tài chính cơ bản. AI và gửi thư đặt lại mật khẩu cần cấu hình dịch vụ tương ứng.

### 3. Cài thư viện và build giao diện

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install --upgrade pip
.\venv\Scripts\python.exe -m pip install -r requirements-dev.txt

Set-Location frontend
npm.cmd ci
npm.cmd run build
Set-Location ..
```

### 4. Khởi động ứng dụng

```powershell
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

| Địa chỉ | Mục đích |
|---|---|
| <http://127.0.0.1:8000> | Mở ứng dụng, đăng ký tài khoản và bắt đầu sử dụng |
| <http://127.0.0.1:8000/api/health> | Kiểm tra tiến trình API: `{"status":"ok"}` |
| <http://127.0.0.1:8000/api/ready> | Kiểm tra kết nối database: `{"status":"ready"}` |
| <http://127.0.0.1:8000/api/docs> | Swagger UI khi `ENABLE_API_DOCS=true` |

Ở cấu hình local mặc định, backend tạo các bảng khi khởi động. Giữ cửa sổ server đang chạy; dùng `Ctrl+C` để dừng. Sau khi đăng ký và đăng nhập, tạo danh mục rồi nhập giao dịch để có số liệu cho Tổng quan, Ngân sách và Báo cáo.

## Phát triển frontend

Chạy backend ở cổng `8000`, sau đó mở cửa sổ PowerShell thứ hai tại repository:

```powershell
Set-Location frontend
npm.cmd run dev:vite
```

Mở <http://localhost:5173>. Vite chuyển tiếp `/api` tới `http://127.0.0.1:8000`.

Ảnh đại diện được backend phục vụ tại `/uploads/`; nếu kiểm tra ảnh qua Vite dev server, cần bổ sung proxy cho đường dẫn này. Có thể dùng chế độ build watch bên dưới để kiểm tra đầy đủ giao diện và ảnh trên cùng cổng backend.

Nếu muốn tiếp tục dùng giao diện do FastAPI phục vụ ở cổng `8000`, chạy `npm.cmd run dev` trong `frontend/` để theo dõi và build lại vào `dist`. Trong dự án này, `dev` là **build watch**, còn `dev:vite` mới khởi động Vite dev server.

## Cấu hình môi trường

Tham khảo [`.env.example`](.env.example). Backend đọc `.env` khi chạy local; Docker Compose truyền các biến cần thiết vào container.

| Biến | Vai trò |
|---|---|
| `SECRET_KEY` | Bắt buộc để ký token; dùng giá trị riêng cho mỗi môi trường. |
| `DATABASE_URL` | Kết nối SQLite hoặc PostgreSQL qua `psycopg`. Compose tự thiết lập URL PostgreSQL cho web. |
| `APP_ENV` | `development` hoặc `production`; ảnh hưởng mặc định của schema tự tạo và tài liệu API. |
| `AUTO_CREATE_SCHEMA` | Bật cho local đơn giản; production dùng `false` và Alembic. |
| `ENABLE_API_DOCS` | Bật/tắt Swagger, ReDoc và OpenAPI. |
| `FRONTEND_URL` | URL công khai để tạo liên kết đặt lại mật khẩu. |
| `CORS_ORIGINS` | Các origin được phép, cách nhau bằng dấu phẩy, khi frontend gọi API từ origin khác. |
| `TRUSTED_HOSTS` | Các hostname được phép, cách nhau bằng dấu phẩy. |
| `AI_API_KEY` | Khóa Gemini theo cấu hình mẫu và Compose. |
| `GEMINI_MODEL` | Model chính; mã hiện tại mặc định `gemini-3.8-flash`. |
| `GEMINI_FALLBACK_MODEL` | Model dự phòng; mặc định `gemini-3.1-pro-preview`, đặt rỗng để tắt. |
| `RESEND_API_KEY` | Khóa Resend cho email khôi phục mật khẩu. |
| `RESEND_FROM_EMAIL` | Địa chỉ người gửi phù hợp với cấu hình xác minh của Resend. |
| `POSTGRES_PASSWORD` | Mật khẩu database, bắt buộc khi chạy Compose. |
| `APP_BIND_ADDRESS` / `APP_PORT` | Địa chỉ/cổng web trên máy chủ; mặc định `127.0.0.1:8000`. |
| `VITE_API_BASE_URL` | Tùy chọn phía frontend, mặc định `/api`; được đọc khi build giao diện, cần build lại sau khi đổi. |

Tên model trên là cấu hình trong repository; khả năng gọi thực tế phụ thuộc quyền truy cập của khóa/project Gemini. Khi chạy backend trực tiếp, adapter cũng chấp nhận `GEMINI_API_KEY` và ưu tiên biến này hơn `AI_API_KEY`; Compose hiện truyền `AI_API_KEY`.

## Trợ lý AI và dữ liệu

Backend tổng hợp dữ liệu của tài khoản theo kỳ trước khi gọi Gemini, gồm thu nhập, chi tiêu, ngân sách, mục tiêu và các chỉ số liên quan. Nhãn danh mục trong context được ánh xạ sang nhãn chuẩn; context tài chính không chứa ghi chú giao dịch, email hoặc tên mục tiêu do người sử dụng đặt.

**Phạm vi quyền riêng tư hiện tại:** `build_prompt()` vẫn đưa câu hỏi và tối đa 10 tin nhắn lịch sử gần nhất vào prompt dưới dạng văn bản. Loại định danh khỏi context tài chính không đồng nghĩa toàn bộ hội thoại đã được lọc dữ liệu cá nhân. Không nhập mật khẩu, token, số tài khoản hoặc thông tin nhạy cảm không cần thiết vào hội thoại.

Lời gọi Gemini dùng `store=false`. Backend xử lý lỗi cấu hình, giới hạn yêu cầu, timeout và lỗi dịch vụ; khi thất bại, luồng lưu dữ liệu được rollback. Với lỗi tạm thời, model chính được thử tối đa hai lần rồi có thể gọi model dự phòng một lần. Timeout có thể chuyển sang model dự phòng; phản hồi rỗng/sai định dạng và lỗi cấu hình 4xx không tự đổi model.

AI chỉ tạo nội dung tư vấn và không tự sửa dữ liệu tài chính. Đối chiếu số liệu tại Tổng quan/Báo cáo trước khi áp dụng gợi ý. Chi tiết thiết kế và yêu cầu kiểm chứng xem tại [thiết kế trợ lý AI](docs/software/design/assistant-design.md).

## Kiểm thử

Từ thư mục gốc, sau khi cài thư viện phát triển:

```powershell
# Backend
.\venv\Scripts\python.exe -m pytest -q

# Frontend và coverage
Set-Location frontend
npm.cmd run test:coverage

# TypeScript và production build
npm.cmd run build
Set-Location ..
```

[CI](.github/workflows/ci.yml) gồm ba nhóm: kiểm thử backend; kiểm thử/coverage và build frontend; kiểm tra Compose Azure và build container.

Kết quả kiểm thử tự động, kiểm thử giao diện và kiểm tra dịch vụ Gemini/Resend được ghi nhận theo môi trường, phiên bản và lần chạy tương ứng. Xem kế hoạch và kết quả tại [tài liệu kiểm thử](docs/software/testing/README.md).

## Triển khai

### Docker Compose

Yêu cầu Docker Engine/Desktop với Compose. Tạo `.env` từ file mẫu nếu chưa có, rồi cấu hình tối thiểu:

```dotenv
POSTGRES_PASSWORD=replace-with-a-strong-database-password
SECRET_KEY=replace-with-a-long-random-value
FRONTEND_URL=https://your-domain.example
TRUSTED_HOSTS=your-domain.example,localhost,127.0.0.1
ENABLE_API_DOCS=false
```

Thay các giá trị mẫu theo môi trường triển khai, rồi chạy từ thư mục gốc:

```powershell
docker compose up -d --build
docker compose ps
docker compose logs --tail 100 web
```

Compose khởi động PostgreSQL và web. Container web chạy `alembic upgrade head` trước Uvicorn; hai volume `postgres_data` và `uploads_data` lưu database và ảnh đại diện. Cổng web mặc định chỉ lắng nghe trên loopback của máy chủ. Reverse proxy cần chuyển tiếp tới cổng này để phục vụ người dùng qua HTTPS.

### Azure và HTTPS

`compose.azure.yaml` bổ sung Caddy để cung cấp HTTPS. Cấu hình tên miền, DNS và biến môi trường theo [hướng dẫn Azure](docs/software/deployment/azure-deploy.md) trước khi khởi động.

### Migration và dữ liệu đang có

Với database mới được quản lý bằng Alembic, container tự áp dụng migration. Khi chạy thủ công, kiểm tra đúng `DATABASE_URL` của môi trường đích:

```powershell
.\venv\Scripts\python.exe -m alembic current
.\venv\Scripts\python.exe -m alembic upgrade head
.\venv\Scripts\python.exe -m alembic check
```

SQLite đã được tạo bằng `AUTO_CREATE_SCHEMA` cần đối chiếu schema và lịch sử revision trước khi chuyển sang Alembic. Không tự động `stamp` một revision để bỏ qua lỗi bảng đã tồn tại. Sao lưu trước khi nâng cấp database đang sử dụng và giữ các volume dữ liệu khi thay container.

## Tài liệu

API sử dụng tiền tố `/api` và Bearer token cho nghiệp vụ cần đăng nhập. OpenAPI khi được bật là nguồn tham chiếu cho request/response hiện tại.

| Nội dung | Điểm bắt đầu |
|---|---|
| Mục lục tài liệu | [docs/README.md](docs/README.md) |
| Yêu cầu và tiêu chí chấp nhận | [docs/requirements](docs/requirements/README.md) |
| API | [api.md](docs/software/design/api.md) |
| Kiến trúc | [architecture.md](docs/software/design/architecture.md) |
| Hướng dẫn sử dụng | [user-guide.md](docs/software/design/user-guide.md) |
| Sơ đồ thiết kế | [docs/diagram](docs/diagram/README.md) |
| Kiểm thử | [docs/software/testing](docs/software/testing/README.md) |
| Triển khai và vận hành | [docs/software/deployment](docs/software/deployment/README.md) |
| Báo cáo, tài liệu lưu trữ | [docs/archive](docs/archive/README.md) |
| Prompt hỗ trợ phát triển | [docs/prompt-library](docs/prompt-library/README.md) |
| Vai trò và skill | [agents](agents/README.md), [.agents/skills](.agents/skills/) |

Một số tài liệu thiết kế mô tả mục tiêu hoặc phương án đề xuất; đọc trạng thái từng tài liệu trước khi dùng làm căn cứ về chức năng đã triển khai.

## Xử lý lỗi thường gặp

| Hiện tượng | Cách xử lý |
|---|---|
| Backend thiếu `SECRET_KEY` | Tạo `.env` ở thư mục gốc, đặt khóa riêng và khởi động lại backend. |
| Trang chính trả `503` vì chưa có frontend build | Chạy `npm.cmd ci` và `npm.cmd run build` trong `frontend/`. |
| Cổng `8000` đã được dùng | Chạy Uvicorn với `--port 8001` và mở cổng mới. Nếu dùng Vite riêng, cập nhật target proxy tương ứng. |
| `npm` bị chặn trong PowerShell | Dùng `npm.cmd` như hướng dẫn. |
| `/api/ready` trả `503` | Kiểm tra `DATABASE_URL`, trạng thái database và log; với Compose, kiểm tra thêm `docker compose ps db`. |
| Không gọi được Gemini | Kiểm tra khóa ở backend, model/quyền truy cập và kết nối; có thể tắt fallback bằng giá trị rỗng. |
| Không nhận thư đặt lại mật khẩu | Kiểm tra Resend, người gửi, `FRONTEND_URL` và thư rác. Thông báo tiếp nhận không xác nhận email có tồn tại trong hệ thống. |
| Ngày hiện tại bị báo là ngày tương lai | Đối chiếu ngày trình duyệt và máy chủ. Validation hiện dùng `date.today()` của backend; kiểm tra múi giờ môi trường chạy. |
