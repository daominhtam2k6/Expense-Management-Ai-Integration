# Tài liệu Expense Management AI

```text
docs/
├── prompt-library/    15 prompt giao việc cho Codex
├── archive/           Tài liệu 01–07 và báo cáo
├── diagram/
│   ├── use-case/
│   ├── erd/
│   ├── class/
│   ├── sequence/
│   └── activity/
├── requirements/      Yêu cầu người dùng
└── software/
    ├── design/
    ├── testing/
    └── deployment/
```

| Cần xem | Điểm bắt đầu |
|---|---|
| Prompt nhập cho Codex | [prompt-library](prompt-library/README.md) |
| Tài liệu nộp và báo cáo | [archive](archive/README.md) |
| Sơ đồ | [diagram](diagram/README.md) |
| Yêu cầu và AC | [requirements](requirements/README.md) |
| Thiết kế, test và deploy | [software](software/README.md) |
| 10 agent chuyên môn | [agents](../agents/README.md) |
| 10 skill | [.agents/skills](../.agents/skills/) |

Bộ tài liệu 01–07 và báo cáo được tra cứu tại archive. Việc sắp xếp tài liệu và sơ đồ không thay đổi hệ thống đang chạy.

Công cụ tạo tài liệu: [scripts/documents](../scripts/documents/README.md). Công cụ kiểm tra: [tools](../tools/README.md). Tài nguyên trung gian và dữ liệu demo đặt trong `.tools/`, được Git và Docker bỏ qua.
