# Sổ Chi Tiêu

Ứng dụng quản lý tài chính cá nhân gồm một backend FastAPI dùng chung cho hai kênh phát hành:

- Web responsive/PWA cho Windows, Android và iOS.
- Ứng dụng Windows đóng gói bằng Tauri, kết nối tới cùng API production.

## Kiến trúc

```text
Web/PWA ───────────┐
                   ├── FastAPI ── PostgreSQL
Windows/Tauri ─────┘          ├── persistent uploads
                              ├── Gemini
                              └── Resend
```

Bản Windows hiện là online-first. Dữ liệu không được lưu thành một database riêng trên từng máy, nhờ đó tài khoản và số liệu luôn đồng bộ với web.

## Chạy local

Yêu cầu:

- Python 3.13
- Node.js 24

Tạo file môi trường từ [`.env.example`](.env.example), đặt một `SECRET_KEY` dài và ngẫu nhiên, sau đó:

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements-dev.txt
Set-Location frontend
npm.cmd ci
npm.cmd run build
Set-Location ..
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Ứng dụng chạy tại `http://127.0.0.1:8000`. Trong development, `AUTO_CREATE_SCHEMA=true` cho phép ứng dụng tiếp tục dùng SQLite và tự tạo schema như trước.

## Deploy web bằng Docker

Production mặc định dùng PostgreSQL và hai volume bền vững cho database và avatar.

1. Điền tối thiểu các biến sau trong `.env`:

   ```dotenv
   POSTGRES_PASSWORD=mat-khau-database-manh
   SECRET_KEY=chuoi-ngau-nhien-dai
   FRONTEND_URL=https://finance.example.com
   TRUSTED_HOSTS=finance.example.com
   CORS_ORIGINS=http://tauri.localhost,https://tauri.localhost
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

## Deploy trên Render

Repo có [Render Blueprint](render.yaml) tạo đồng thời:

- Docker web service tại region Singapore.
- Render PostgreSQL 18 trên private network.
- Persistent disk 1 GB gắn tại `/app/uploads` để giữ avatar qua các lần deploy.
- Health check `/api/health` và migration Alembic tự động khi container khởi động.

Blueprint sử dụng gói web `0.5c-512mb` và PostgreSQL `0.1c-256mb`. Đây là cấu hình trả phí tối thiểu phù hợp với dữ liệu lâu dài; persistent disk không hoạt động trên web service Free và Render PostgreSQL Free chỉ dành cho thử nghiệm ngắn hạn.

Các bước tạo dịch vụ:

1. Push repo lên GitHub hoặc GitLab.
2. Trong Render Dashboard, chọn **New → Blueprint** và kết nối repo.
3. Render tự đọc `render.yaml`. Kiểm tra hai tài nguyên và chi phí trước khi xác nhận tạo Blueprint instance.
4. Trong màn hình khởi tạo, nhập `AI_API_KEY`, `RESEND_API_KEY` và `RESEND_FROM_EMAIL`. Có thể để trống AI/email lúc đầu, nhưng trợ lý AI và email đặt lại mật khẩu sẽ chưa hoạt động.
5. Sau deploy, mở `https://<render-host>/api/health` và `/api/ready` để xác nhận.

Render tự sinh `SECRET_KEY` và truyền private connection string của PostgreSQL vào `DATABASE_URL`. Ứng dụng tự chuyển chuỗi `postgresql://` của Render sang driver Psycopg 3.

Khi thêm custom domain, đặt thêm:

```dotenv
FRONTEND_URL=https://finance.example.com
TRUSTED_HOSTS=finance.example.com
```

Sau khi có URL Render thật, cập nhật `frontend/.env.desktop` trước khi build Windows:

```dotenv
VITE_API_BASE_URL=https://<render-host>/api
```

### Database đã tồn tại

Migration đầu tiên được thiết kế cho database production mới. Không chạy `alembic upgrade head` trực tiếp lên file `expense.db` cũ đã có bảng. Sau khi backup và xác nhận schema cũ đã có đủ các cột hiện tại, đánh dấu revision bằng:

```powershell
.\venv\Scripts\python.exe -m alembic stamp 20260901_0001
```

## Cài web như ứng dụng

Build web đã có manifest, service worker và icon PWA. Người dùng có thể cài từ Microsoft Edge/Chrome trên Windows hoặc thêm vào màn hình chính trên mobile.

Service worker chỉ cache app shell và static assets. Các đường dẫn `/api/*` và `/uploads/*` không được cache.

## Build ứng dụng Windows

Yêu cầu bổ sung:

- Rust stable qua `rustup`.
- Visual Studio Build Tools với workload Desktop development with C++ và Windows SDK.
- WebView2 Runtime; Windows 10/11 thường đã có sẵn.

Tạo cấu hình desktop:

```powershell
Set-Location frontend
Copy-Item .env.desktop.example .env.desktop
```

Sửa `.env.desktop` để trỏ tới API production:

```dotenv
VITE_API_BASE_URL=https://finance.example.com/api
```

Chạy development shell:

```powershell
npm.cmd run desktop:dev
```

Tạo installer:

```powershell
npm.cmd run desktop:build
```

Installer `.msi` và `-setup.exe` được tạo trong `frontend/src-tauri/target/release/bundle/`. Cấu hình production bắt buộc có `VITE_API_BASE_URL`; build sẽ dừng nếu biến này bị thiếu.

Trước khi phát hành công khai, cần cấu hình chứng thư code-signing để giảm cảnh báo Microsoft SmartScreen. Auto-update nên được bật sau khi quy trình ký số và nơi lưu release artifacts đã ổn định.

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
| `CORS_ORIGINS` | Có cho desktop | Origin được phép gọi API |
| `TRUSTED_HOSTS` | Khuyến nghị | Danh sách hostname public |
| `AI_API_KEY` | Cho AI | Gemini API key |
| `GEMINI_MODEL` | Không | Model Gemini |
| `RESEND_API_KEY` | Cho email | Gửi email đặt lại mật khẩu |
| `RESEND_FROM_EMAIL` | Cho email | Địa chỉ người gửi đã xác minh |

Không commit `.env`, `.env.desktop`, database, uploads hoặc chứng thư ký số.
