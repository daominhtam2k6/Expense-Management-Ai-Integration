# Sổ Chi Tiêu

> Tra cứu tài liệu theo nhóm tại [docs/README.md](docs/README.md).
>
> Hồ sơ AI-Augmented SDLC: xem [đánh giá tuân thủ](docs/governance/sdlc-compliance-audit.md),
> [prompt register](docs/ai-engineering/history/prompts.md), [thư viện prompt mẫu](docs/ai-engineering/prompts.md), [human gates](docs/governance/human-gates.md) và
> [nhật ký AI](docs/ai-engineering/history/ai-process-log.md).

Ứng dụng quản lý tài chính cá nhân trên web responsive/PWA, sử dụng backend FastAPI. Người dùng truy cập bằng trình duyệt trên máy tính, Android và iOS.

## Kiến trúc

```text
Web/PWA ── FastAPI ── PostgreSQL
                ├── persistent uploads
                ├── Gemini
                └── Resend
```

Phiên bản web/PWA yêu cầu kết nối Internet cho toàn bộ chức năng. Dữ liệu nghiệp vụ được lưu trên máy chủ. Offline chỉ được xem xét trong tương lai nếu phản hồi người dùng cho thấy nhu cầu đủ lớn.

## Clone và chạy thử trên local

### 1. Yêu cầu môi trường

- Git.
- Python 3.13.
- Node.js 24, kèm npm.

Kiểm tra các công cụ trong PowerShell:

```powershell
git --version
python --version
node --version
npm.cmd --version
```

### 2. Clone repository

```powershell
git clone https://github.com/daominhtam2k6/Expense-Management-Ai-Integration.git
Set-Location Expense-Management-Ai-Integration
```

Nếu đã clone từ trước, cập nhật nhánh chính bằng `git pull origin main` và bảo đảm
không có thay đổi local cần giữ trước khi pull.

### 3. Tạo cấu hình local

Sao chép file môi trường mẫu:

```powershell
Copy-Item .env.example .env
```

Mở `.env` và thay `SECRET_KEY` bằng một giá trị riêng, dài và ngẫu nhiên. Có thể
tạo giá trị bằng Python:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Cấu hình mặc định trong `.env.example` sử dụng SQLite tại `expense.db`, bật
`AUTO_CREATE_SCHEMA=true` và không yêu cầu PostgreSQL. Các chức năng Gemini và
gửi email là tùy chọn; để trống `AI_API_KEY` và `RESEND_API_KEY` nếu chỉ kiểm thử
các chức năng local cơ bản. Không commit file `.env`.

### 4. Cài dependency và build frontend

Từ thư mục gốc repository:

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install --upgrade pip
.\venv\Scripts\python.exe -m pip install -r requirements-dev.txt
Set-Location frontend
npm.cmd ci
npm.cmd run build
Set-Location ..
```

Lệnh build tạo `frontend/dist`; FastAPI sẽ phục vụ frontend này cùng API trên
một cổng. Không cần chạy Vite riêng cho quy trình kiểm thử local cơ bản.

### 5. Khởi động ứng dụng

```powershell
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Giữ cửa sổ PowerShell này đang chạy, sau đó truy cập:

- Ứng dụng: `http://127.0.0.1:8000`
- Kiểm tra API: `http://127.0.0.1:8000/api/health`
- Kiểm tra database: `http://127.0.0.1:8000/api/ready`
- Swagger UI: `http://127.0.0.1:8000/api/docs`

Kết quả mong đợi của hai endpoint kiểm tra lần lượt là `{"status":"ok"}` và
`{"status":"ready"}`. Ở lần chạy đầu, ứng dụng tự tạo schema SQLite vì cấu
hình local bật `AUTO_CREATE_SCHEMA=true`.

### 6. Chạy kiểm thử tự động

Dừng server bằng `Ctrl+C` hoặc mở một cửa sổ PowerShell khác tại thư mục gốc:

```powershell
.\venv\Scripts\python.exe -m pytest -q
Set-Location frontend
npm.cmd test
npm.cmd run build
Set-Location ..
```

Nếu cổng `8000` đang được chương trình khác sử dụng, có thể chạy thử ở cổng khác:

```powershell
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8001
```

Khi đó mở `http://127.0.0.1:8001`. Nếu frontend chưa được build, API sẽ trả lỗi
`503` ở trang chính; chạy lại `npm.cmd ci` và `npm.cmd run build` trong thư mục
`frontend`.

## Deploy web lên Azure for Students

Lộ trình hiện tại: triển khai web và kiểm tra với người dùng thử. Xem [hướng dẫn Azure](docs/software/deployment/azure-deploy.md)
để chọn VM, cấu hình HTTPS, lưu dữ liệu, sao lưu và kiểm tra sau triển khai.

## Deploy web bằng Docker

Production mặc định dùng PostgreSQL và hai volume bền vững cho database và avatar.

1. Điền tối thiểu các biến sau trong `.env`:

   ```dotenv
   POSTGRES_PASSWORD=mat-khau-database-manh
   SECRET_KEY=chuoi-ngau-nhien-dai
   FRONTEND_URL=https://finance.example.com
   TRUSTED_HOSTS=finance.example.com
   ```

2. Build và khởi động:

   ```powershell
   docker compose up -d --build
   docker compose ps
   ```

3. Kiểm tra:

   ```text
   GET https://finance.example.com/api/health
   GET https://finance.example.com/api/ready
   ```

Container tự chạy `alembic upgrade head` trước khi khởi động API. Reverse proxy hoặc cloud load balancer phải cung cấp HTTPS và chuyển tiếp traffic tới cổng ứng dụng.

### Database đã tồn tại

Migration đầu tiên được thiết kế cho database production mới. Không chạy `alembic upgrade head` trực tiếp lên file `expense.db` cũ đã có bảng. Sau khi backup và xác nhận schema cũ đã có đủ các cột hiện tại, đánh dấu revision bằng:

```powershell
.\venv\Scripts\python.exe -m alembic stamp 20260901_0001
```

## Cài web như ứng dụng

Build web đã có manifest, service worker và icon PWA. Người dùng có thể cài từ Microsoft Edge/Chrome trên Windows hoặc thêm vào màn hình chính trên mobile.

Service worker chỉ cache app shell và static assets. Các đường dẫn `/api/*` và `/uploads/*` không được cache.

## Kiểm thử

```powershell
.\venv\Scripts\python.exe -m pytest -q
Set-Location frontend
npm.cmd test -- --coverage
npm.cmd run build
```

Kiểm tra migration độc lập:

```powershell
.\venv\Scripts\python.exe -m alembic upgrade head
.\venv\Scripts\python.exe -m alembic check
```

## Biến môi trường production

| Biến | Bắt buộc | Mục đích |
|---|---:|---|
| `DATABASE_URL` | Có | Chuỗi kết nối PostgreSQL dùng driver `psycopg` |
| `SECRET_KEY` | Có | Ký access token |
| `FRONTEND_URL` | Có | Tạo link đặt lại mật khẩu |
| `CORS_ORIGINS` | Khi frontend khác origin với API | Origin web được phép gọi API; để trống khi cùng origin |
| `TRUSTED_HOSTS` | Khuyến nghị | Danh sách hostname public |
| `AI_API_KEY` | Cho AI | Gemini API key |
| `GEMINI_MODEL` | Không | Model Gemini |
| `RESEND_API_KEY` | Cho email | Gửi email đặt lại mật khẩu |
| `RESEND_FROM_EMAIL` | Cho email | Địa chỉ người gửi đã xác minh |

Không commit `.env`, database hoặc uploads.
