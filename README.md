# Sổ Chi Tiêu

> Tra cứu tài liệu theo nhóm tại [docs/README.md](docs/README.md).
>
> Hồ sơ AI-Augmented SDLC: xem [đánh giá tuân thủ](docs/governance/sdlc-compliance-audit.md),
> [prompt register](docs/ai-engineering/history/prompts.md), [thư viện prompt mẫu](docs/ai-engineering/prompt-library.md), [human gates](docs/governance/human-gates.md) và
> [nhật ký AI](docs/ai-engineering/history/ai-process-log.md).

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

Bản Windows hiện yêu cầu kết nối Internet cho toàn bộ chức năng. Dữ liệu không được lưu thành một database nghiệp vụ riêng trên từng máy, nhờ đó tài khoản và số liệu dùng chung nguồn dữ liệu với web. Offline chỉ được xem xét trong tương lai nếu phản hồi người dùng cho thấy nhu cầu đủ lớn.

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

## Deploy web lên Azure for Students

Lộ trình hiện tại: triển khai web, kiểm tra với người dùng thử, rồi phát hành
Windows Tauri kết nối cùng backend. Xem [hướng dẫn Azure](docs/software/deployment/azure-deploy.md)
để chọn VM, cấu hình HTTPS, lưu dữ liệu, sao lưu và kiểm tra sau triển khai.

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
