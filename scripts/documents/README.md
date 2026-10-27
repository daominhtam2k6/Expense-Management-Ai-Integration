# Công cụ tạo tài liệu

Các script trong thư mục này tạo tài liệu Word hoặc hình screenflow. Chạy từ thư mục gốc dự án bằng môi trường Python có các thư viện cần thiết; mỗi script tự xác định gốc dự án từ vị trí của nó.

- `build_05_06_documents.py`: tạo tài liệu kiểm thử và screenflow/database.
- `build_updated_ood_doc.py`, `rebuild_class_specification.py`: chuẩn bị tài liệu thiết kế/class.
- `build_browser_flow_diagrams.py`, `build_detailed_screenflows.py`, `build_login_flow_visual.py`: tạo hình từ dữ liệu và ảnh nguồn.

Word/PDF đặt trong `docs/archive/`; ảnh và dữ liệu nguồn cục bộ trong `.tools/document-assets/`. Một số script vẫn cần mẫu đầu vào trong Downloads theo cấu hình sẵn có; việc chuyển thư mục không chạy lại hoặc thay nội dung các mẫu đó. Script chụp màn hình dùng dữ liệu demo nằm ở `.tools/capture-scripts/`.
