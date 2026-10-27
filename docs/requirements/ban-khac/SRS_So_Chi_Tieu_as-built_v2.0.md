# HỆ THỐNG QUẢN LÝ CHI TIÊU CÁ NHÂN CÓ TÍCH HỢP AI

## SỔ CHI TIÊU

### ĐẶC TẢ YÊU CẦU PHẦN MỀM (SRS) — AS-BUILT

**Phiên bản:** 2.0<br>
**Nhóm thực hiện:** Nhóm 21<br>
**Ngày cập nhật:** 02/09/2026<br>
**Nguồn chuẩn:** Mã nguồn và kiểm thử của dự án `Expense_Management_AI` tại thời điểm rà soát

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# MỤC LỤC

[[TOC]]

```{=openxml}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

# LỊCH SỬ PHIÊN BẢN

| Phiên bản | Ngày | Người cập nhật | Mô tả thay đổi |
|---|---|---|---|
| 1.0 | Chưa ghi nhận | Nhóm 21 | Phiên bản SRS ban đầu. |
| 1.1 | Chưa ghi nhận | Nhóm 21 | Bổ sung đồng bộ thủ công, thông báo, yêu cầu AI và truy vết. |
| 2.0 | 02/09/2026 | Nhóm 21 | Rà soát toàn bộ theo mã nguồn hiện tại; chuẩn hóa phạm vi web/PWA/Windows, xác thực và khôi phục mật khẩu, hồ sơ và ảnh đại diện, báo cáo so sánh, trợ lý AI, quy tắc mục tiêu tiết kiệm, kiến trúc triển khai, dữ liệu, NFR và truy vết. Loại bỏ các chức năng không tồn tại như đồng bộ thủ công, AI Report độc lập và AI tự động đề xuất ngân sách. |

# 1. GIỚI THIỆU

## 1.1. Mục đích

Tài liệu này đặc tả hành vi của hệ thống **Sổ Chi Tiêu** theo trạng thái đã được triển khai trong mã nguồn tại thời điểm ngày 02/09/2026. Đây là tài liệu SRS dạng **as-built**: mã nguồn backend, frontend, mô hình dữ liệu, migration, cấu hình triển khai và kiểm thử tự động là căn cứ ưu tiên khi có khác biệt với các tài liệu cũ.

Tài liệu phục vụ các mục đích:

- thống nhất phạm vi chức năng thực tế của sản phẩm;
- làm cơ sở kiểm thử nghiệm thu và bảo trì;
- chỉ ra ràng buộc, phụ thuộc và giới hạn hiện hữu;
- phân biệt chức năng đã có với mục tiêu hoặc ý tưởng chưa được triển khai.

## 1.2. Phạm vi sản phẩm

Sổ Chi Tiêu là hệ thống quản lý tài chính cá nhân bằng tiếng Việt, hỗ trợ một người dùng quản lý dữ liệu riêng của mình qua một backend dùng chung. Sản phẩm được phát hành dưới các hình thức:

- web responsive;
- Progressive Web App (PWA) có thể cài đặt trên trình duyệt hỗ trợ;
- ứng dụng Windows đóng gói bằng Tauri, kết nối tới cùng API production.

Các nhóm chức năng thuộc phạm vi:

- đăng ký, đăng nhập bằng username hoặc email, đăng xuất;
- quên và đặt lại mật khẩu qua email;
- cập nhật hồ sơ và ảnh đại diện;
- quản lý danh mục thu/chi;
- quản lý giao dịch và lọc giao dịch;
- quản lý ngân sách chi theo danh mục và tháng;
- quản lý mục tiêu tiết kiệm, hạng mục, nạp/rút tiền và hoàn thành mục tiêu;
- Dashboard theo tháng;
- báo cáo xác định so sánh tháng được chọn với tháng liền trước;
- trợ lý AI dùng dữ liệu tổng hợp, có lịch sử hội thoại;
- chế độ sáng/tối, giao diện thích ứng và trạng thái ngoại tuyến.

## 1.3. Ngoài phạm vi hiện tại

Các nội dung sau **không phải chức năng đã triển khai**:

- ghi dữ liệu khi ngoại tuyến hoặc cơ chế giải quyết xung đột offline-first;
- nút “đồng bộ thủ công”; dữ liệu luôn được đọc/ghi qua API tập trung;
- thông báo đẩy, hộp thư thông báo hoặc lưu lịch sử thông báo;
- AI tự tạo, sửa hoặc xóa giao dịch, ngân sách, danh mục hay mục tiêu;
- một quy trình “AI sinh báo cáo” độc lập và lưu vào bảng `AIReport`;
- một quy trình “AI gợi ý ngân sách” độc lập có khả năng ghi ngân sách;
- đổi mật khẩu trong màn hình hồ sơ khi người dùng đang đăng nhập;
- tài khoản quản trị, phân quyền nhiều vai trò, chia sẻ ví hoặc dữ liệu giữa người dùng;
- liên kết ngân hàng, nhập file sao kê, đa tiền tệ, đầu tư, thuế hoặc tín dụng;
- ứng dụng mobile native riêng cho Android/iOS.

## 1.4. Đối tượng đọc

- Nhóm phát triển và bảo trì phần mềm.
- Nhóm kiểm thử và nghiệm thu.
- Giảng viên hướng dẫn và người quản lý dự án.
- Người phụ trách triển khai và vận hành.

## 1.5. Thuật ngữ và từ viết tắt

| Thuật ngữ | Giải thích |
|---|---|
| SRS | Software Requirements Specification — Đặc tả yêu cầu phần mềm. |
| API | Giao diện lập trình ứng dụng do FastAPI cung cấp dưới tiền tố `/api`. |
| PWA | Ứng dụng web có manifest và service worker, có thể cài đặt như ứng dụng. |
| Tauri | Khung đóng gói frontend web thành ứng dụng Windows. |
| JWT | JSON Web Token dùng làm bearer token xác thực. |
| CRUD | Tạo, đọc, cập nhật và xóa dữ liệu. |
| Số dư thuần theo tháng | Thu nhập trong tháng trừ chi tiêu trong tháng. |
| Số dư khả dụng | Tổng thu trừ tổng chi, trừ tiền đã nạp vào mục tiêu, cộng tiền đã rút khỏi mục tiêu, tính đến ngày giới hạn nếu có. |
| Kỳ hiện tại | Tháng/năm do người dùng chọn. |
| Kỳ trước | Tháng liền trước kỳ hiện tại. |
| Dữ liệu tổng hợp AI | Các tổng số, tỷ lệ, số lượng và nhãn danh mục an toàn; không gồm giao dịch thô hay thông tin định danh. |

## 1.6. Tài liệu và bằng chứng tham chiếu

| Nguồn | Vai trò |
|---|---|
| `app/routers`, `app/core`, `app/models`, `app/schemas` | Hành vi API, quy tắc nghiệp vụ, dữ liệu và validation. |
| `frontend/src` | Luồng giao diện, điều hướng và phản hồi tới người dùng. |
| `alembic/versions` | Schema production. |
| `Dockerfile`, `compose.yaml`, cấu hình Tauri/PWA | Kiến trúc đóng gói và triển khai. |
| `tests` và test frontend | Bằng chứng kiểm thử tự động hiện có. |
| `README.md`, `PRODUCT.md`, `DESIGN.md` | Bối cảnh sản phẩm và thiết kế; không được ưu tiên hơn mã nguồn khi có mâu thuẫn. |

# 2. MÔ TẢ TỔNG QUAN

## 2.1. Góc nhìn sản phẩm và kiến trúc

| Lớp/Thành phần | Công nghệ và trách nhiệm |
|---|---|
| Kênh người dùng | React + TypeScript; web responsive, PWA và Windows/Tauri. |
| API | FastAPI; cung cấp xác thực và nghiệp vụ dưới `/api`. |
| ORM và migration | SQLAlchemy và Alembic. |
| Dữ liệu development | SQLite theo cấu hình mặc định. |
| Dữ liệu production | PostgreSQL qua Psycopg 3; container chạy migration trước khi mở API. |
| Tệp người dùng | Ảnh đại diện lưu trong `uploads/avatars`; production cần storage bền vững. |
| AI bên ngoài | Google Gemini qua Gemini Interactions API. |
| Email bên ngoài | Resend để gửi liên kết đặt lại mật khẩu. |

Web/PWA và Windows/Tauri không duy trì cơ sở dữ liệu tài chính riêng trên thiết bị. Cả hai truy cập cùng API, vì vậy dữ liệu được nhất quán theo trạng thái máy chủ khi thiết bị có mạng. Service worker chỉ cache app shell và tài nguyên tĩnh; không cache `/api/*` hoặc `/uploads/*`.

## 2.2. Tác nhân

| Tác nhân | Mô tả |
|---|---|
| Khách chưa xác thực | Có thể đăng ký, đăng nhập, yêu cầu và thực hiện đặt lại mật khẩu. |
| Người dùng đã xác thực | Quản lý toàn bộ dữ liệu tài chính và hồ sơ thuộc tài khoản của mình. |
| Google Gemini | Nhận câu hỏi, lịch sử hội thoại dạng văn bản và ngữ cảnh tài chính tổng hợp để sinh nội dung tư vấn. |
| Resend | Gửi email chứa liên kết đặt lại mật khẩu. |
| Cơ sở dữ liệu | Lưu tài khoản, tài chính, mục tiêu và hội thoại. |

## 2.3. Điều kiện vận hành

- Development yêu cầu Python 3.13 và Node.js 24 theo cấu hình hiện tại.
- Web production phục vụ frontend và API từ cùng FastAPI container; PostgreSQL là cấu hình khuyến nghị.
- Windows cần Windows 10/11 có WebView2 Runtime và URL API HTTPS hợp lệ khi build.
- Người dùng cần kết nối Internet để đọc/ghi dữ liệu và sử dụng AI; PWA có thể mở app shell đã cache nhưng không hỗ trợ thao tác dữ liệu ngoại tuyến.
- Chức năng AI cần `AI_API_KEY`; khôi phục mật khẩu qua email cần cấu hình Resend và `FRONTEND_URL` chính xác.

## 2.4. Trạng thái hoàn thiện làm cơ sở SRS

Tại thời điểm rà soát:

- 69 bài test backend và 22 subtest đều đạt;
- 50 bài test frontend đều đạt;
- TypeScript và bản build production/PWA hoàn tất thành công;
- schema production có migration Alembic ban đầu;
- có health check `/api/health` và readiness check `/api/ready`.

Kết luận: dự án **đủ hoàn thiện để lập SRS as-built cho phạm vi chức năng hiện tại**. Tuy nhiên, các chỉ tiêu tải, độ sẵn sàng, sao lưu/khôi phục, bảo mật vận hành và chất lượng trả lời AI chưa có đủ bằng chứng đo lường để tuyên bố đã đạt.

# 3. YÊU CẦU CHỨC NĂNG

## 3.1. Tài khoản và xác thực

| ID | Yêu cầu |
|---|---|
| FR-AUTH-01 | Hệ thống phải cho phép đăng ký bằng username, email và mật khẩu. |
| FR-AUTH-02 | Username phải dài 3–50 ký tự và duy nhất; email phải hợp lệ và duy nhất không phân biệt hoa/thường. |
| FR-AUTH-03 | Mật khẩu đăng ký và đặt lại phải có ít nhất 6 ký tự và được băm bằng bcrypt trước khi lưu. |
| FR-AUTH-04 | Hệ thống phải cho phép đăng nhập bằng username hoặc email và mật khẩu. |
| FR-AUTH-05 | Khi đăng nhập thành công, hệ thống cấp JWT bearer token có thời hạn 24 giờ. |
| FR-AUTH-06 | Frontend phải xóa trạng thái đăng nhập và chuyển về trang đăng nhập khi người dùng đăng xuất hoặc API trả 401 cho phiên hiện có. |
| FR-AUTH-07 | Người dùng có thể yêu cầu đặt lại mật khẩu qua email mà hệ thống không tiết lộ email có tồn tại hay không. |
| FR-AUTH-08 | Liên kết đặt lại mật khẩu có hiệu lực 15 phút, dùng một lần; token thô không được lưu, chỉ lưu SHA-256 của token. |
| FR-AUTH-09 | Hệ thống giới hạn tối đa 3 yêu cầu khôi phục cho mỗi email trong một giờ bằng bộ đếm trong bộ nhớ của tiến trình. |

## 3.2. Hồ sơ cá nhân

| ID | Yêu cầu |
|---|---|
| FR-PRO-01 | Người dùng có thể xem và sửa tên hiển thị, username và email. |
| FR-PRO-02 | Tên hiển thị là tùy chọn, tối đa 80 ký tự; username và email vẫn là định danh đăng nhập. |
| FR-PRO-03 | Khi email thay đổi, hệ thống phải vô hiệu token đặt lại mật khẩu đang tồn tại. |
| FR-PRO-04 | Người dùng có thể tải lên, thay hoặc xóa ảnh đại diện. |
| FR-PRO-05 | Ảnh phải là PNG, JPEG hoặc WebP, đúng chữ ký tệp và không vượt quá 2 MB. |
| FR-PRO-06 | Khi thay/xóa ảnh thành công, tệp avatar cũ trên storage cục bộ phải được xóa. |

## 3.3. Danh mục

| ID | Yêu cầu |
|---|---|
| FR-CAT-01 | Người dùng có thể xem, tạo, sửa và xóa danh mục thuộc tài khoản mình. |
| FR-CAT-02 | Danh mục gồm tên, loại `income`/`expense`, màu và một icon thuộc danh sách hệ thống hỗ trợ. |
| FR-CAT-03 | Không cho phép hai danh mục cùng người dùng có cùng tên và cùng loại. |
| FR-CAT-04 | Không cho phép xóa danh mục đang được giao dịch sử dụng. |
| FR-CAT-05 | Danh mục của người dùng khác không được đọc hoặc sửa qua ID. |

## 3.4. Giao dịch

| ID | Yêu cầu |
|---|---|
| FR-TXN-01 | Người dùng có thể xem, tạo, sửa và xóa giao dịch thuộc tài khoản mình. |
| FR-TXN-02 | Giao dịch gồm danh mục, số tiền, ngày và ghi chú tùy chọn. |
| FR-TXN-03 | Số tiền phải lớn hơn 0; ngày giao dịch không được ở tương lai. |
| FR-TXN-04 | Loại giao dịch phải được hệ thống suy ra từ danh mục, không tin tưởng giá trị loại do client gửi. |
| FR-TXN-05 | Danh mục gán cho giao dịch phải thuộc chính người dùng hiện tại. |
| FR-TXN-06 | Người dùng có thể lọc theo danh mục, loại, từ ngày, đến ngày và từ khóa trong ghi chú. |
| FR-TXN-07 | Kết quả phải được sắp theo ngày giao dịch giảm dần. |

## 3.5. Ngân sách

| ID | Yêu cầu |
|---|---|
| FR-BUD-01 | Người dùng có thể xem ngân sách theo tháng/năm, tạo, sửa hạn mức và xóa ngân sách. |
| FR-BUD-02 | Ngân sách chỉ được gắn với danh mục chi tiêu thuộc người dùng. |
| FR-BUD-03 | Mỗi danh mục chỉ có tối đa một ngân sách trong cùng tháng và năm. |
| FR-BUD-04 | Hạn mức phải lớn hơn 0; tháng nằm trong 1–12. |
| FR-BUD-05 | Số đã chi là tổng giao dịch chi thuộc danh mục trong tháng/năm ngân sách. |
| FR-BUD-06 | Trạng thái vượt ngân sách xảy ra khi số đã chi lớn hơn hạn mức; bằng hạn mức chưa được tính là vượt. |
| FR-BUD-07 | Dashboard phân loại trạng thái: `safe` dưới 80%, `warning` từ 80% đến không quá 100%, `over` trên 100%. |

## 3.6. Mục tiêu tiết kiệm

| ID | Yêu cầu |
|---|---|
| FR-GOL-01 | Người dùng có thể tạo, xem, sửa mục tiêu với tên, số tiền đích và thời hạn tùy chọn. |
| FR-GOL-02 | Tên mục tiêu sau khi bỏ khoảng trắng đầu/cuối phải có 1–100 ký tự; số tiền đích phải lớn hơn 0. |
| FR-GOL-03 | Số đã tiết kiệm được tính bằng tổng các lần nạp trừ tổng các lần rút; không lưu ở cột riêng. |
| FR-GOL-04 | Người dùng có thể thêm, đánh dấu mua/chưa mua, sửa hoặc xóa các hạng mục con có tên và chi phí lớn hơn 0. |
| FR-GOL-05 | Mỗi lần nạp/rút phải có số tiền lớn hơn 0, ngày là ngày máy chủ và ghi chú tùy chọn. |
| FR-GOL-06 | Không cho nạp vào mục tiêu đã hoàn thành và không cho nạp quá số dư khả dụng hiện tại. |
| FR-GOL-07 | Không cho rút quá số đã tiết kiệm trong mục tiêu. |
| FR-GOL-08 | Không cho hoàn thành khi số đã tiết kiệm nhỏ hơn số tiền đích. |
| FR-GOL-09 | Khi hoàn thành, người dùng chọn một trong ba cách: `keep` giữ tiền dành riêng; `release` rút toàn bộ về số dư khả dụng; `spend` rút toàn bộ và tạo một giao dịch chi bằng số tiền đó. |
| FR-GOL-10 | Chế độ `spend` bắt buộc chọn danh mục chi thuộc người dùng. |
| FR-GOL-11 | Mục tiêu đã có lịch sử nạp/rút không được xóa; mục tiêu chưa có lịch sử tiền có thể xóa cùng các hạng mục con. |
| FR-GOL-12 | Người dùng có thể xem lịch sử nạp/rút của từng mục tiêu, sắp theo ngày giảm dần. |

## 3.7. Dashboard

| ID | Yêu cầu |
|---|---|
| FR-DAS-01 | Người dùng có thể chọn tháng/năm để xem Dashboard. |
| FR-DAS-02 | Dashboard hiển thị tổng thu, tổng chi, số dư thuần của tháng và số dư khả dụng đến ngày cuối kỳ. |
| FR-DAS-03 | Dashboard hiển thị cơ cấu chi theo danh mục và tỷ trọng từng danh mục. |
| FR-DAS-04 | Dashboard hiển thị xu hướng thu/chi của ba tháng kết thúc tại kỳ được chọn. |
| FR-DAS-05 | Dashboard hiển thị ngân sách trong kỳ, số đã chi, còn lại, tỷ lệ sử dụng và trạng thái. |
| FR-DAS-06 | Dashboard hiển thị tối đa ba mục tiêu được ưu tiên theo trạng thái/thời hạn và tối đa năm giao dịch gần nhất trong kỳ. |

## 3.8. Báo cáo tài chính

| ID | Yêu cầu |
|---|---|
| FR-REP-01 | Người dùng có thể chọn một tháng/năm và xem báo cáo so sánh với tháng liền trước. |
| FR-REP-02 | Báo cáo phải tính tổng thu, tổng chi, số dư thuần, chênh lệch tuyệt đối và phần trăm thay đổi của hai kỳ. |
| FR-REP-03 | Khi giá trị kỳ trước bằng 0, phần trăm thay đổi là 0 nếu kỳ này cũng bằng 0; nếu kỳ này khác 0 thì trả về `null` và giao diện hiển thị “mới phát sinh”. |
| FR-REP-04 | Báo cáo phân tích chi tiêu theo từng danh mục: số tiền, tỷ trọng, số giao dịch, chênh lệch và phần trăm thay đổi. |
| FR-REP-05 | Biểu đồ có thể gộp các danh mục ngoài sáu danh mục lớn nhất thành “Danh mục khác”, nhưng bảng chi tiết phải giữ từng danh mục riêng. |
| FR-REP-06 | Người dùng có thể mở danh sách giao dịch đã lọc từ từng dòng danh mục trong báo cáo. |
| FR-REP-07 | Báo cáo này được tính xác định từ cơ sở dữ liệu và **không sử dụng AI**. |

## 3.9. Trợ lý AI và lịch sử hội thoại

| ID | Yêu cầu |
|---|---|
| FR-AI-01 | Người dùng có thể chọn kỳ, nhập câu hỏi tối đa 2.000 ký tự và gửi tới trợ lý. |
| FR-AI-02 | Giao diện cung cấp bốn câu hỏi khởi đầu: phân tích chi tiêu, phát hiện bất thường, dự báo dòng tiền và lập kế hoạch tài chính. |
| FR-AI-03 | Hệ thống phải tạo ngữ cảnh tổng hợp cho kỳ được chọn và kỳ liền trước. |
| FR-AI-04 | Ngữ cảnh gồm tổng thu/chi/số dư/số giao dịch, số dư khả dụng, chênh lệch chi, tối đa bảy nhóm chi an toàn, dự báo tuyến tính cuối tháng, số ngân sách/vượt ngân sách và tổng hợp mục tiêu đang hoạt động. |
| FR-AI-05 | Không gửi username, email, tên mục tiêu, ghi chú giao dịch, giao dịch thô, ID nội bộ hoặc tên danh mục do người dùng tự đặt trong phần ngữ cảnh tài chính. |
| FR-AI-06 | Câu hỏi hiện tại và lịch sử tin nhắn trước đó của cuộc hội thoại được gửi cho Gemini để duy trì ngữ cảnh hội thoại; người dùng không nên nhập dữ liệu nhạy cảm vào nội dung câu hỏi. |
| FR-AI-07 | AI chỉ tư vấn bằng văn bản, phải phân biệt dữ liệu thực tế với ước tính, nêu độ không chắc chắn khi dữ liệu ít và không được tuyên bố đã thay đổi dữ liệu. |
| FR-AI-08 | Hệ thống lưu câu hỏi, câu trả lời, kỳ tham chiếu và snapshot bằng chứng tổng hợp của câu trả lời. |
| FR-AI-09 | Người dùng có thể xem danh sách, tìm kiếm ở giao diện, mở và xóa cuộc hội thoại thuộc tài khoản mình. |
| FR-AI-10 | Khi Gemini thiếu cấu hình hoặc lỗi, API phải trả mã lỗi phù hợp: 503 khi chưa cấu hình/không sẵn sàng, 429 khi giới hạn, 504 khi timeout, 502 cho lỗi dịch vụ khác. |
| FR-AI-11 | AI không được đưa lời khuyên đầu tư, tín dụng, thuế hoặc pháp lý mang tính quyết định. |

## 3.10. Giao diện, kết nối và phản hồi

| ID | Yêu cầu |
|---|---|
| FR-UI-01 | Giao diện phải hỗ trợ tiếng Việt, chế độ sáng/tối và bố cục thích ứng desktop/mobile. |
| FR-UI-02 | Các màn hình tạo/sửa chính sử dụng panel có thể đóng bằng Escape, scrim và nút đóng; focus được giữ trong panel và trả về phần tử mở khi đóng. |
| FR-UI-03 | Hệ thống phải hiển thị trạng thái tải, rỗng và lỗi phù hợp cho các màn hình dữ liệu. |
| FR-UI-04 | Khi trình duyệt báo ngoại tuyến, giao diện hiển thị cảnh báo rằng dữ liệu chỉ cập nhật khi kết nối lại. |
| FR-UI-05 | Thông báo thành công/lỗi hiện tại là phản hồi giao diện cục bộ; không phải một use case hay thực thể thông báo được lưu trữ. |

# 4. ĐẶC TẢ USE CASE

## 4.1. UC001 — Đăng ký tài khoản

| Thuộc tính | Nội dung |
|---|---|
| Tác nhân | Khách chưa xác thực. |
| Tiền điều kiện | Truy cập được màn hình đăng ký và API/cơ sở dữ liệu hoạt động. |
| Hậu điều kiện | Tài khoản mới được lưu; người dùng được chuyển đến đăng nhập. |
| Luồng chính | 1) Mở đăng ký. 2) Nhập username, email, mật khẩu và xác nhận. 3) Frontend kiểm tra username ≥3, mật khẩu ≥6 và hai mật khẩu khớp. 4) API chuẩn hóa email về chữ thường, kiểm tra trùng. 5) Băm mật khẩu, lưu tài khoản. 6) Hiển thị thành công và chuyển đến đăng nhập. |
| Ngoại lệ | Username/email đã tồn tại; email sai định dạng; dữ liệu không đạt validation; lỗi máy chủ. |

## 4.2. UC002 — Đăng nhập và đăng xuất

| Thuộc tính | Nội dung |
|---|---|
| Tác nhân | Khách chưa xác thực/người dùng đã xác thực. |
| Tiền điều kiện | Có tài khoản hợp lệ để đăng nhập. |
| Hậu điều kiện | Đăng nhập: token được lưu ở client và mở Dashboard. Đăng xuất: token/trạng thái người dùng bị xóa và trở về đăng nhập. |
| Luồng chính | 1) Nhập username hoặc email và mật khẩu. 2) API tìm theo username, nếu không có thì tìm email không phân biệt hoa/thường. 3) Xác minh bcrypt. 4) Cấp JWT 24 giờ. 5) Frontend lấy hồ sơ hiện tại và mở Dashboard. |
| Ngoại lệ | Thông tin sai được trả bằng một thông báo chung; token thiếu/hết hạn/sai dẫn tới 401 và đăng xuất ở frontend. Hệ thống không có trạng thái khóa tài khoản. |

## 4.3. UC003 — Khôi phục mật khẩu

| Thuộc tính | Nội dung |
|---|---|
| Tác nhân | Khách chưa xác thực; Resend. |
| Tiền điều kiện | Email hợp lệ; muốn nhận thư thực tế thì Resend và URL frontend phải được cấu hình. |
| Hậu điều kiện | Nếu token hợp lệ, mật khẩu được băm và thay; token bị vô hiệu ngay sau khi dùng. |
| Luồng chính | 1) Nhập email. 2) Hệ thống luôn trả thông báo chung. 3) Nếu tài khoản tồn tại và chưa vượt giới hạn, sinh token ngẫu nhiên, lưu hash và hạn 15 phút, gửi link qua Resend. 4) Người dùng mở link, nhập mật khẩu mới ≥6 ký tự và xác nhận. 5) API kiểm tra token/hash/hạn, cập nhật mật khẩu và xóa token. |
| Ngoại lệ | Email không tồn tại hoặc vượt rate limit vẫn nhận thông báo chung; token sai/hết hạn bị từ chối; lỗi gửi email hiện không làm API yêu cầu quên mật khẩu thất bại. |

## 4.4. UC004 — Quản lý hồ sơ

| Thuộc tính | Nội dung |
|---|---|
| Tác nhân | Người dùng đã xác thực. |
| Tiền điều kiện | Đã đăng nhập. |
| Hậu điều kiện | Thông tin hoặc avatar mới xuất hiện ngay trong shell ứng dụng. |
| Luồng chính | 1) Mở panel hồ sơ. 2) Sửa tên hiển thị, username, email và lưu; hoặc tải/thay/xóa avatar. 3) API kiểm tra uniqueness/định dạng. 4) Cập nhật hồ sơ dùng chung. |
| Ngoại lệ | Username/email trùng; avatar sai MIME/chữ ký, rỗng hoặc >2 MB; lỗi lưu. Đổi mật khẩu không thuộc panel này. |

## 4.5. UC005 — Quản lý danh mục

| Thuộc tính | Nội dung |
|---|---|
| Tác nhân | Người dùng đã xác thực. |
| Tiền điều kiện | Đã đăng nhập. |
| Hậu điều kiện | Danh mục được thêm/sửa/xóa và danh sách được cập nhật. |
| Luồng chính | 1) Mở Danh mục. 2) Chọn loại Thu/Chi, tên, màu, icon. 3) Lưu. 4) Có thể mở lại để sửa hoặc xác nhận xóa. |
| Ngoại lệ | Trùng tên trong cùng loại; danh mục không thuộc người dùng; danh mục đã có giao dịch thì không thể xóa. |

## 4.6. UC006 — Quản lý giao dịch

| Thuộc tính | Nội dung |
|---|---|
| Tác nhân | Người dùng đã xác thực. |
| Tiền điều kiện | Có ít nhất một danh mục phù hợp. |
| Hậu điều kiện | Giao dịch và các số liệu suy ra ở Dashboard, ngân sách, báo cáo, mục tiêu/AI được phản ánh ở lần tải tiếp theo. |
| Luồng chính | 1) Chọn kỳ/danh sách giao dịch. 2) Tạo hoặc mở giao dịch. 3) Chọn danh mục, nhập số tiền, ngày, ghi chú. 4) API suy ra loại từ danh mục và lưu. 5) Có thể sửa hoặc xác nhận xóa. 6) Có thể lọc theo loại, danh mục, ngày và từ khóa. |
| Ngoại lệ | Số tiền ≤0; ngày tương lai; danh mục không tồn tại/không thuộc người dùng; giao dịch không thuộc người dùng. |

## 4.7. UC007 — Quản lý ngân sách

| Thuộc tính | Nội dung |
|---|---|
| Tác nhân | Người dùng đã xác thực. |
| Tiền điều kiện | Có danh mục chi. |
| Hậu điều kiện | Ngân sách kỳ được lưu; số đã chi và trạng thái được tính lại từ giao dịch. |
| Luồng chính | 1) Chọn tháng/năm. 2) Chọn danh mục chi và hạn mức. 3) Lưu. 4) Xem số đã chi, còn lại/tỷ lệ và trạng thái. 5) Có thể sửa hạn mức hoặc xóa ngân sách. |
| Ngoại lệ | Danh mục không phải loại chi/không thuộc người dùng; hạn mức ≤0; đã có ngân sách cho danh mục trong kỳ. |

## 4.8. UC008 — Quản lý mục tiêu tiết kiệm

| Thuộc tính | Nội dung |
|---|---|
| Tác nhân | Người dùng đã xác thực. |
| Tiền điều kiện | Đã đăng nhập; muốn nạp tiền thì phải có số dư khả dụng đủ. |
| Hậu điều kiện | Mục tiêu, hạng mục và lịch sử tiền được cập nhật; số dư khả dụng thay đổi theo nạp/rút. |
| Luồng chính | 1) Tạo mục tiêu. 2) Tùy chọn thêm hạng mục chi tiết. 3) Nạp/rút và xem lịch sử. 4) Khi đạt đích, chọn giữ riêng, trả về số dư hoặc ghi nhận chi tiêu. 5) Hệ thống lưu số hoàn thành, chế độ và chuyển trạng thái `completed`. |
| Ngoại lệ | Nạp quá số dư; nạp vào mục tiêu hoàn thành; rút quá số đã tiết kiệm; hoàn thành khi chưa đạt đích; chế độ chi không có danh mục chi; xóa mục tiêu đã có lịch sử tiền. |

## 4.9. UC009 — Xem Dashboard

| Thuộc tính | Nội dung |
|---|---|
| Tác nhân | Người dùng đã xác thực. |
| Tiền điều kiện | Đã đăng nhập. |
| Hậu điều kiện | Không thay đổi dữ liệu. |
| Luồng chính | 1) Mở Tổng quan. 2) Chọn một trong 24 tháng gần nhất ở giao diện. 3) Hệ thống tải tổng thu/chi, số dư, cơ cấu chi, xu hướng ba tháng, ngân sách, mục tiêu và giao dịch gần đây. 4) Người dùng có thể đi đến màn hình chi tiết. |
| Ngoại lệ | Không có dữ liệu thì hiển thị empty state; lỗi tải có nút thử lại. |

## 4.10. UC010 — Xem báo cáo so sánh

| Thuộc tính | Nội dung |
|---|---|
| Tác nhân | Người dùng đã xác thực. |
| Tiền điều kiện | Đã đăng nhập. |
| Hậu điều kiện | Không thay đổi dữ liệu. |
| Luồng chính | 1) Chọn kỳ. 2) API tính kỳ hiện tại và liền trước. 3) Giao diện hiển thị tổng quan, biểu đồ cột, cơ cấu, biến động nổi bật và bảng chi tiết. 4) Chọn “Xem giao dịch” để mở danh sách đã lọc. |
| Ngoại lệ | Hai kỳ không có dữ liệu thì hiển thị hướng dẫn thêm giao dịch; lỗi tải có thể thử lại. |

## 4.11. UC011 — Sử dụng trợ lý AI

| Thuộc tính | Nội dung |
|---|---|
| Tác nhân | Người dùng đã xác thực; Google Gemini. |
| Tiền điều kiện | Có mạng và API key Gemini hợp lệ. |
| Hậu điều kiện | Cuộc hội thoại, câu hỏi, câu trả lời và snapshot bằng chứng được lưu; dữ liệu tài chính nghiệp vụ không bị AI thay đổi. |
| Luồng chính | 1) Mở Trợ lý và chọn kỳ. 2) Chọn câu hỏi gợi ý hoặc nhập câu hỏi. 3) Hệ thống tính ngữ cảnh tổng hợp và gửi cùng lịch sử hội thoại tới Gemini. 4) Hiển thị câu trả lời, bằng chứng, độ tin cậy và liên kết sang Báo cáo/Giao dịch. 5) Người dùng tiếp tục hội thoại, tạo hội thoại mới hoặc xem/xóa lịch sử. |
| Ngoại lệ | Câu hỏi rỗng; thiếu cấu hình; giới hạn API; timeout; Gemini không sẵn sàng; cuộc hội thoại không thuộc người dùng. Giao diện cho phép thử lại câu hỏi thất bại. |

# 5. QUY TẮC NGHIỆP VỤ VÀ CÔNG THỨC

| ID | Quy tắc |
|---|---|
| BR-01 | Mọi truy vấn nghiệp vụ phải giới hạn theo `current_user.id`; ID do client cung cấp không làm mất điều kiện sở hữu. |
| BR-02 | Loại giao dịch bằng loại danh mục tại thời điểm tạo/sửa danh mục của giao dịch. |
| BR-03 | `monthly_net = monthly_income - monthly_expense`. |
| BR-04 | `available_balance = total_income - total_expense - goal_deposits + goal_withdrawals`. Khi có ngày giới hạn, chỉ lấy nghiệp vụ đến ngày đó. |
| BR-05 | `goal_current = deposits - withdrawals`; vì vậy nạp tiền làm giảm số dư khả dụng, rút tiền làm tăng số dư khả dụng. |
| BR-06 | `budget_spent` là tổng giao dịch `expense` của đúng danh mục, tháng và năm. |
| BR-07 | Tỷ lệ ngân sách = `spent / limit × 100`; `warning` từ 80%, `over` chỉ khi `spent > limit`. |
| BR-08 | Dự báo AI dùng `average_expense_per_day = current_expense / elapsed_days`; `projected_expense = average × days_in_month`; độ tin cậy `medium` khi kỳ có ít nhất 7 giao dịch, ngược lại là `low`. |
| BR-09 | Khi hoàn thành mục tiêu theo `spend`, hệ thống đồng thời ghi một lần rút toàn bộ khỏi mục tiêu và một giao dịch chi cùng số tiền để tránh tiền tiếp tục bị giữ riêng. |
| BR-10 | AI chỉ đọc snapshot tổng hợp; mọi lệnh ghi dữ liệu tài chính vẫn phải thực hiện qua màn hình nghiệp vụ tương ứng. |

# 6. MÔ HÌNH VÀ TỪ ĐIỂN DỮ LIỆU

| Thực thể | Thuộc tính chính | Ràng buộc/ý nghĩa |
|---|---|---|
| User | id, username, email, display_name, password_hash, avatar_url, created_at, reset_token_hash, reset_token_expiry | Username/email duy nhất; hồ sơ và thông tin khôi phục mật khẩu. |
| Category | id, user_id, name, type, color, icon | Danh mục riêng của người dùng; `type` là income/expense. |
| Transaction | id, user_id, category_id, amount, type, txn_date, note | `Numeric(14,2)`; loại được sao chép từ danh mục. |
| Budget | id, user_id, category_id, month, year, limit_amount | Hạn mức theo danh mục chi và kỳ. |
| SavingGoal | id, user_id, name, target_amount, deadline, status, completion_amount, completion_mode | Không có `current_amount`; giá trị hiện tại được tính. |
| GoalItem | id, goal_id, name, cost, is_purchased | Hạng mục kế hoạch bên trong mục tiêu. |
| GoalTransaction | id, goal_id, amount, type, txn_date, note | Lịch sử `deposit`/`withdraw`. |
| AIConversation | id, user_id, title, created_at, updated_at | Chủ đề hội thoại AI thuộc người dùng. |
| AIMessage | id, conversation_id, role, content, context_month, context_year, evidence_json, created_at | Lưu câu hỏi/câu trả lời và bằng chứng tổng hợp của câu trả lời. |
| AIReport | id, user_id, month, year, summary, suggestions, created_at | Bảng hiện có trong schema nhưng không có API hoặc luồng giao diện sử dụng; không thuộc chức năng nghiệm thu hiện tại. |

Các quan hệ chính:

- User 1–N Category, Transaction, Budget, SavingGoal, AIConversation.
- Category 1–N Transaction và Budget.
- SavingGoal 1–N GoalItem và GoalTransaction.
- AIConversation 1–N AIMessage.

# 7. YÊU CẦU GIAO DIỆN NGOÀI

## 7.1. Giao diện người dùng

- Điều hướng bảo vệ các trang Dashboard, Giao dịch, Danh mục, Ngân sách, Mục tiêu, Báo cáo và Trợ lý.
- Desktop dùng sidebar; mobile dùng thanh điều hướng dưới với các mục chính và khu vực “Thêm”.
- Màn hình báo cáo và bảng tài chính rộng phải cho phép cuộn ngang bằng bàn phím và có nhãn truy cập.
- Giá trị tiền hiển thị theo định dạng tiền Việt Nam; dữ liệu tiền trong backend dùng Decimal/Numeric thay vì Float.
- Side panel và drawer phải hỗ trợ focus management, Escape và reduced motion theo thiết kế hiện tại.

## 7.2. Giao diện API

Các nhóm endpoint đã triển khai:

| Nhóm | Endpoint chính |
|---|---|
| Hệ thống | `GET /api/health`, `GET /api/ready` |
| Xác thực/hồ sơ | `/api/auth/register`, `/login`, `/me`, `/me/avatar`, `/forgot-password`, `/reset-password` |
| Danh mục | CRUD `/api/categories/` |
| Giao dịch | CRUD và lọc `/api/transactions/` |
| Ngân sách | CRUD `/api/budgets/` |
| Mục tiêu | CRUD `/api/goals/`; items, deposit, withdraw, complete, history |
| Dashboard | `GET /api/dashboard/` |
| Báo cáo | `GET /api/reports/` |
| Trợ lý | context, conversations và messages dưới `/api/assistant` |

Trừ đăng ký, đăng nhập, quên/đặt lại mật khẩu và health/readiness, endpoint nghiệp vụ yêu cầu `Authorization: Bearer <token>`.

## 7.3. Dịch vụ bên ngoài

- Gemini: HTTPS, connect timeout 10 giây, read timeout 90 giây, tối đa 2 lần thử ở service hiện tại.
- Resend: HTTPS, timeout 10 giây; gửi email HTML chứa link đặt lại mật khẩu.

# 8. YÊU CẦU PHI CHỨC NĂNG

## 8.1. Bảo mật và riêng tư

| ID | Yêu cầu/trạng thái |
|---|---|
| NFR-SEC-01 | Production phải cấu hình `SECRET_KEY` dài, ngẫu nhiên và không commit vào mã nguồn. |
| NFR-SEC-02 | Mật khẩu phải được băm bcrypt; reset token chỉ lưu dạng SHA-256 và dùng một lần. |
| NFR-SEC-03 | Production phải dùng HTTPS; desktop build bắt buộc URL API HTTPS kết thúc bằng `/api`. |
| NFR-SEC-04 | CORS và trusted hosts phải được cấu hình theo hostname/origin thực tế. |
| NFR-SEC-05 | Mỗi người dùng chỉ truy cập dữ liệu của mình; cần tiếp tục duy trì test chống truy cập chéo. |
| NFR-SEC-06 | Avatar phải được kiểm tra MIME, chữ ký và kích thước. |
| NFR-SEC-07 | Ngữ cảnh tài chính gửi AI không chứa thông tin định danh, ghi chú, tên mục tiêu, ID, giao dịch thô hoặc tên danh mục tùy biến. |
| NFR-SEC-08 | Chính sách riêng tư phải nói rõ câu hỏi và lịch sử hội thoại dạng văn bản vẫn được gửi tới Gemini. |

## 8.2. Độ tin cậy và toàn vẹn dữ liệu

- Tiền phải dùng `Numeric(14,2)`/Decimal ở backend và cơ sở dữ liệu.
- Production phải chạy `alembic upgrade head` trước khi khởi động API.
- Kết nối cơ sở dữ liệu bật `pool_pre_ping`; readiness phải trả 503 khi DB không sẵn sàng.
- Upload và PostgreSQL cần storage bền vững trong môi trường triển khai.
- Chưa có job sao lưu/khôi phục trong repository; chính sách backup, retention và diễn tập phục hồi phải do môi trường vận hành quy định trước khi go-live.

## 8.3. Hiệu năng và khả năng mở rộng

Repository chưa chứa kết quả load test đủ để xác nhận ngưỡng 3 giây hoặc 100 người dùng đồng thời. Vì vậy:

- mục tiêu thời gian phản hồi CRUD, số người dùng đồng thời và percentile phải được chủ sản phẩm xác nhận;
- phải chạy load test trên hạ tầng production-like trước khi ghi các số này thành tiêu chí đạt;
- các truy vấn danh sách giao dịch hiện chưa phân trang, cần đánh giá khi dữ liệu lớn;
- rate limit quên mật khẩu nằm trong bộ nhớ và không chia sẻ giữa nhiều worker, nên cần Redis hoặc cơ chế tập trung nếu mở rộng ngang.

## 8.4. Khả dụng, tương thích và tiếp cận

- Web hỗ trợ các trình duyệt hiện đại; PWA cache tài nguyên tĩnh và tự cập nhật service worker.
- Ứng dụng Windows có kích thước tối thiểu 1024×700 và dùng WebView2.
- Giao diện thích ứng xuống mobile web; không có mobile native.
- Các dialog/panel quan trọng phải có semantics, focus trap, đóng bằng Escape và phục hồi focus.
- Trạng thái không chỉ được truyền bằng màu; bảng/biểu đồ cần nhãn và focus hiển thị.

## 8.5. Khả năng bảo trì và kiểm thử

- Backend được chia thành router, schema, model và core service; frontend chia theo page/component/lib.
- Mọi thay đổi schema production phải đi qua Alembic.
- Pipeline kiểm thử tối thiểu gồm pytest backend, Vitest frontend và TypeScript/Vite build.
- Các cảnh báo Pydantic `class Config` đã deprecated không làm test thất bại nhưng cần xử lý trước khi nâng lên Pydantic 3.

## 8.6. Khả năng quan sát

- Hệ thống có health và readiness endpoint.
- Mã AI có logging cho lỗi dịch vụ; toàn hệ thống chưa có chiến lược logging có cấu trúc, correlation ID, metrics hoặc alerting đầy đủ.
- Trước production chính thức cần xác định nơi thu log, thời gian lưu, che dữ liệu nhạy cảm và cảnh báo sự cố.

# 9. TRUY VẾT YÊU CẦU

| Use case | Nhóm yêu cầu | Thành phần thực thi chính | Bằng chứng kiểm thử |
|---|---|---|---|
| UC001 | FR-AUTH-01..03 | auth router, RegisterPage | test_auth, AuthPages tests |
| UC002 | FR-AUTH-04..06 | security/deps, AuthContext, LoginPage | test_auth, test_auth_branches, AuthContext tests |
| UC003 | FR-AUTH-07..09 | auth router, email core, Forgot/Reset pages | test_auth, AuthPages tests |
| UC004 | FR-PRO-01..06 | auth router, ProfilePanel | auth branch tests, component tests |
| UC005 | FR-CAT-* | categories router/page | test_crud_routes, category icon tests |
| UC006 | FR-TXN-* | transactions router/page | test_crud_routes, system tests |
| UC007 | FR-BUD-* | budgets router/page | test_crud_routes, dashboard tests |
| UC008 | FR-GOL-* | goals router/page, finance core | test_goals, test_goal_branches, core tests |
| UC009 | FR-DAS-* | dashboard router/page | test_dashboard, system tests |
| UC010 | FR-REP-* | reports router/page | test_reports |
| UC011 | FR-AI-* | assistant router/context/Gemini/page | test_assistant, test_assistant_branches, test_gemini |

# 10. TIÊU CHÍ NGHIỆM THU

## 10.1. Tiêu chí chức năng

1. Người dùng đăng ký, đăng nhập bằng username/email và đăng xuất thành công.
2. Luồng quên mật khẩu không tiết lộ sự tồn tại email; token hợp lệ đặt lại được mật khẩu một lần trong 15 phút.
3. Người dùng cập nhật hồ sơ và xử lý avatar đúng loại/dung lượng.
4. CRUD danh mục, giao dịch và ngân sách tuân thủ quyền sở hữu và validation.
5. Giao dịch tương lai hoặc số tiền không dương bị từ chối; loại giao dịch theo danh mục.
6. Ngân sách tính đúng số đã chi và trạng thái theo kỳ.
7. Mục tiêu tính đúng số hiện tại, số dư khả dụng và ba chế độ hoàn thành.
8. Dashboard tính đúng số liệu theo tháng và ba tháng xu hướng.
9. Báo cáo so sánh đúng kỳ trước, chênh lệch, tỷ lệ và liên kết lọc giao dịch; không phụ thuộc Gemini.
10. Trợ lý chỉ nhận ngữ cảnh tổng hợp theo hợp đồng, lưu hội thoại/snapshot và không ghi dữ liệu tài chính.
11. Người dùng không thể truy cập dữ liệu của tài khoản khác qua ID.
12. Web/PWA build thành công; app hiển thị trạng thái lỗi/rỗng/ngoại tuyến phù hợp.

## 10.2. Cổng nghiệm thu kỹ thuật hiện tại

- `pytest -q`: phải đạt toàn bộ test backend.
- `npm test -- --run`: phải đạt toàn bộ test frontend.
- `npm run build`: TypeScript và Vite/PWA phải build thành công.
- Migration phải chạy được trên một database production mới; readiness phải xác nhận kết nối DB.

## 10.3. Tiêu chí chưa được chứng minh

Các mục sau chưa được xem là “đạt” chỉ dựa trên repository hiện tại:

- số người dùng đồng thời cụ thể;
- thời gian phản hồi percentile cụ thể;
- uptime/SLA;
- RPO/RTO và khôi phục backup;
- chất lượng, độ đúng hoặc độ an toàn của câu trả lời AI trên một bộ eval đại diện;
- code signing và auto-update của bản Windows.

# 11. ĐIỂM CẦN HOÀN THIỆN VÀ QUYẾT ĐỊNH MỞ

| Mức độ | Nội dung | Ảnh hưởng/khuyến nghị |
|---|---|---|
| Cao | Chưa có load test, backup policy, observability đầy đủ và security review production. | Hoàn tất trước khi tuyên bố production-ready hoặc ghi SLA. |
| Cao | Gửi email quên mật khẩu không kiểm tra kết quả Resend trước khi trả thành công; token vẫn được tạo dù thư có thể không gửi. | Ghi log có kiểm soát, xử lý retry/queue và theo dõi delivery. |
| Trung bình | Rate limit quên mật khẩu nằm trong bộ nhớ một tiến trình. | Dùng store tập trung khi chạy nhiều worker/instance. |
| Trung bình | Danh sách giao dịch và một số danh sách khác chưa phân trang. | Thiết kế pagination trước khi dữ liệu tăng lớn. |
| Trung bình | Quy tắc uniqueness ngân sách theo danh mục/kỳ chỉ được kiểm tra ở tầng ứng dụng, chưa có unique constraint trong migration. | Thêm constraint để chống race condition. |
| Trung bình | Xóa danh mục chỉ kiểm tra giao dịch; danh mục còn ngân sách có thể bị chặn bởi FK nhưng phản hồi không được chuẩn hóa. | Kiểm tra budget tham chiếu và trả lỗi nghiệp vụ rõ ràng. |
| Trung bình | Backend cho phép endpoint rút tiền không kiểm tra trạng thái completed; UI hiện không chủ động cung cấp luồng này cho mục tiêu hoàn thành. | Chốt quy tắc và khóa ở backend nếu completed phải bất biến. |
| Trung bình | Mật khẩu tối thiểu 6 ký tự là đúng với code nhưng yếu cho production. | Nâng chính sách sau khi có kế hoạch tương thích và test. |
| Thấp | Model `AIReport` tồn tại nhưng không được sử dụng. | Xóa bằng migration hoặc chính thức thiết kế use case trước khi đưa vào SRS. |
| Thấp | Cảnh báo Pydantic về `class Config` deprecated. | Chuyển sang `ConfigDict` trước Pydantic 3. |
| Mở | Chỉ tiêu hiệu năng, retention hội thoại, xóa tài khoản, export dữ liệu và chính sách riêng tư AI. | Cần chủ sản phẩm xác nhận và bổ sung ở phiên bản SRS sau. |

# PHỤ LỤC A — CÁC ĐIỂM ĐÃ SỬA SO VỚI SRS CŨ

1. Đổi nền tảng từ “HTML/CSS/JavaScript + SQLite cục bộ” thành React/TypeScript, FastAPI, PostgreSQL production, SQLite development, PWA và Windows/Tauri online-first.
2. Bổ sung luồng quên/đặt lại mật khẩu đã tồn tại; loại bỏ mô tả “đang phát triển”.
3. Sửa mật khẩu tối thiểu từ 8 thành 6 ký tự theo validation hiện tại.
4. Sửa đăng nhập từ chỉ email thành username hoặc email; hệ thống trả lỗi chung thay vì tiết lộ email/sai mật khẩu riêng.
5. Bổ sung avatar và cập nhật username/email/tên hiển thị; loại bỏ đổi mật khẩu khỏi hồ sơ.
6. Sửa giao dịch: loại được suy ra từ danh mục; bổ sung lọc và cấm ngày tương lai.
7. Sửa ngân sách thành phạm vi danh mục chi theo tháng/năm; bỏ trường ghi chú và phạm vi năm độc lập.
8. Viết lại mục tiêu tiết kiệm theo sổ nạp/rút, số dư khả dụng, hạng mục con và ba chế độ hoàn thành.
9. Viết lại Dashboard theo đúng dữ liệu và giới hạn hiển thị hiện tại.
10. Đổi “AI sinh báo cáo” thành báo cáo so sánh xác định, không dùng Gemini.
11. Gộp phân tích, bất thường, dự báo, kế hoạch/gợi ý vào Trợ lý AI; mô tả đúng hợp đồng dữ liệu tổng hợp và lịch sử hội thoại.
12. Loại UC “Đồng bộ thủ công”; dữ liệu tập trung tự nhất quán qua API và không có offline writes.
13. Loại UC “Thông báo” như một chức năng độc lập; phản hồi hiện chỉ là trạng thái giao diện cục bộ.
14. Loại các chỉ tiêu hiệu năng/100 người dùng khỏi danh sách đã đạt vì chưa có bằng chứng đo.
15. Mở rộng từ điển dữ liệu, truy vết, tiêu chí nghiệm thu và danh sách khoảng trống production.
