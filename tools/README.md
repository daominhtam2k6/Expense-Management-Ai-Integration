# Công cụ kiểm tra hệ thống

- `live_browser_checks.py`: kiểm tra giao diện bằng Playwright trong `.tools/browser_tools/`, dùng môi trường ứng dụng thử cô lập.
- `live_service_checks.py`: kiểm tra kết nối các dịch vụ, có thể gọi Gemini thật.
- `update_live_testing_word.py`: cập nhật bản tài liệu kiểm thử có sẵn.

Kết quả JSON ở `docs/software/testing/results/`; ảnh trình duyệt thô ở `.tools/test-results/`; tài liệu Word ở `docs/archive/ban-khac/`. Thư viện và dữ liệu local không đưa vào Git. Chỉ chạy các công cụ khi được giao kiểm tra, không chạy chúng chỉ để sắp xếp thư mục.
