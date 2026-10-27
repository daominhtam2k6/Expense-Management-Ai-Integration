# Kế hoạch kiểm thử chức năng và nhập liệu

Cập nhật: 28/10/2026. Tổng cộng **38 test case**, đánh số liên tục từ **TC-001 đến TC-038**, cho 12 Use Case của hệ thống Sổ Chi Tiêu.

Điều chỉnh ngày 28/10/2026: TC-037 chỉ dùng N1, mỗi prompt P1/P2/P3 chạy 1 lần, tổng 3 phản hồi. Ca thông báo timeout dùng mã **TC-038** (trước đây là TC-039), được người dùng chấp nhận PASS dựa trên bằng chứng UI đã có. Hai ca so sánh khả năng tài chính và kiểm tra payload riêng tư đã bỏ khỏi phạm vi. Xem [bảng đối chiếu mã](test-case-id-map.md), [kết quả hiện tại theo 3 nhóm](current-test-case-results.md), [hướng dẫn N1](ai-prompt-n1-guide.md) và [kết quả timeout](ai-timeout-test-result.md).

## 1. Phạm vi và cách thực hiện

- Kiểm tra chức năng trong UC và tính hợp lệ của dữ liệu nhập trên web/PWA: luồng thành công, thao tác hủy, dữ liệu thiếu/sai/trùng và giới hạn nghiệp vụ. Riêng UC012 bổ sung so sánh 3 phiên bản prompt, kiểm tra độ đúng số liệu trên N1 và thông báo timeout của AI theo yêu cầu ngày 27/10/2026.
- Không đưa kiểm thử hiệu năng, bảo mật chuyên sâu, hạ tầng, migration, backup, build hay đánh giá giao diện vào danh mục này. TC-038 chỉ kiểm tra thông báo khi AI timeout; không còn ma trận lỗi nhà cung cấp, phục hồi/retry hoặc bắt payload outbound trong phạm vi hiện tại.
- Mã UC theo [ghi chú mô hình hiện hành](../../diagram/use-case/model-notes.md): UC003 là Đăng xuất, UC004 là Khôi phục mật khẩu, UC005 là Quản lý hồ sơ; UC006–UC012 lần lượt là Danh mục, Giao dịch, Ngân sách, Mục tiêu, Dashboard, Báo cáo, Trợ lý AI. Không dùng cách đánh số cũ trong SRS as-built v2.0.
- Mỗi mã TC là một kịch bản có các bước hoặc bộ dữ liệu liên quan. Với ca nhập liệu, lần lượt thay một trường, giữ các trường còn lại hợp lệ; ghi kết quả từng bộ dữ liệu trong cùng mã TC. Chỉ PASS khi tất cả bước/bộ dữ liệu đạt, không tách thêm mã ngoài danh mục 38 ca hiện tại.
- Các bảng dưới đây là **thiết kế ca kiểm thử**, không tự gán kết quả. Kết quả từng đợt xem báo cáo tương ứng; không dùng kết quả lịch sử thay cho bằng chứng của đợt mới.

## 2. Điều kiện và dữ liệu chung

1. Dùng môi trường kiểm thử và dữ liệu giả; chuẩn bị tài khoản A để thao tác thông thường, B để kiểm tra dữ liệu được giữ nguyên, D chỉ dành cho ca xóa tài khoản. Không sử dụng tài khoản thật.
2. Tài khoản mẫu A: username `tester_a`, email hộp thư thử có thể nhận thư, mật khẩu `Test@123`. Không lưu mật khẩu thật hoặc liên kết đặt lại mật khẩu vào báo cáo.
3. Trừ ca đăng ký/đăng nhập/khôi phục, đăng nhập A trước khi chạy. Mỗi ca bắt đầu từ dữ liệu tiền điều kiện riêng; khôi phục dữ liệu thử giữa các ca để không phụ thuộc thứ tự.
4. Bộ số liệu F: tháng 09/2026 có thu 10.000.000 VND, chi Ăn uống 2.000.000 VND; tháng 10/2026 có thu 12.000.000 VND, chi Ăn uống 3.000.000 VND và Đi lại 1.000.000 VND. Không có giao dịch khác trong hai tháng. Tháng 08/2026 rỗng. B có dữ liệu riêng không tính vào F.
5. Chuẩn bị danh mục thu Lương, chi Ăn uống và Đi lại; danh mục Tạm chưa được sử dụng. Email reset cần hộp thư thử và dịch vụ gửi thư hoạt động; ca hỏi AI cần Gemini hoạt động. Thiếu điều kiện thì ghi BLOCKED, không ghi PASS.
6. Sau thao tác lưu/xóa, tải lại màn hình để kiểm tra kết quả còn đúng. Với dữ liệu sai, kiểm tra thông báo và xác nhận dữ liệu trước đó không bị thay đổi.

## 3. Phân bổ test case

| UC | Chức năng | Mã ca | Số ca |
|---|---|---|---:|
| UC001 | Đăng ký tài khoản | TC-001–TC-003 | 3 |
| UC002 | Đăng nhập | TC-004–TC-005 | 2 |
| UC003 | Đăng xuất | TC-006 | 1 |
| UC004 | Khôi phục mật khẩu | TC-007–TC-008 | 2 |
| UC005 | Quản lý hồ sơ | TC-009–TC-013 | 5 |
| UC006 | Quản lý danh mục | TC-014–TC-016 | 3 |
| UC007 | Quản lý giao dịch | TC-017–TC-020 | 4 |
| UC008 | Quản lý ngân sách | TC-021–TC-023 | 3 |
| UC009 | Quản lý mục tiêu tiết kiệm | TC-024–TC-029 | 6 |
| UC010 | Xem Dashboard | TC-030–TC-031 | 2 |
| UC011 | Xem báo cáo so sánh | TC-032–TC-033 | 2 |
| UC012 | Trợ lý AI | TC-034–TC-038 | 5 |
| **Tổng** | | | **38** |

## 4. Các ca kiểm thử soạn sẵn

### UC001 — Đăng ký tài khoản

| Mã | Nội dung | Tiền điều kiện / dữ liệu nhập | Bước thực hiện | Kết quả mong đợi |
|---|---|---|---|---|
| TC-001 | Đăng ký hợp lệ | Chưa đăng nhập; username/email mới, username `newtester`, mật khẩu `Test@123` | 1. Mở Đăng ký. 2. Điền đầy đủ thông tin; xác nhận mật khẩu nếu biểu mẫu có. 3. Gửi. 4. Đăng nhập bằng tài khoản vừa tạo. | Tạo tài khoản thành công; đăng nhập được bằng thông tin đã đăng ký. |
| TC-002 | Kiểm tra dữ liệu đăng ký | Các bộ: bỏ trống từng trường bắt buộc; email `abc@`; username 2/3/50/51 ký tự; mật khẩu 5/6 ký tự; xác nhận không khớp nếu có. Mỗi lần hợp lệ dùng email/username mới. | 1. Nhập từng bộ vào biểu mẫu. 2. Gửi đăng ký. | Trường bắt buộc/email sai bị từ chối; username 3 và 50 ký tự, mật khẩu 6 ký tự được nhận khi các trường khác đúng; username 2/51, mật khẩu 5 ký tự và xác nhận lệch bị chặn. Không tạo tài khoản cho bộ sai. |
| TC-003 | Đăng ký trùng định danh | A đã tồn tại; dùng username hoặc email của A; thử lại với chữ hoa/thường và khoảng trắng đầu/cuối | 1. Giữ các trường khác hợp lệ. 2. Gửi từng biến thể trùng username, rồi trùng email. | Từ chối định danh trùng sau chuẩn hóa; không tạo thêm tài khoản. |

### UC002 — Đăng nhập

| Mã | Nội dung | Tiền điều kiện / dữ liệu nhập | Bước thực hiện | Kết quả mong đợi |
|---|---|---|---|---|
| TC-004 | Đăng nhập bằng username/email | A tồn tại; mật khẩu đúng | 1. Đăng nhập bằng username. 2. Đăng xuất. 3. Đăng nhập bằng email. 4. Lặp lại với định danh khác hoa/thường và có khoảng trắng đầu/cuối. | Các cách nhập đều nhận diện đúng A và mở được màn hình sau đăng nhập. |
| TC-005 | Đăng nhập với dữ liệu sai | Các bộ: trống định danh; trống mật khẩu; định danh không tồn tại; mật khẩu sai | 1. Mở Đăng nhập. 2. Nhập từng bộ và gửi. | Yêu cầu bổ sung trường thiếu hoặc báo thông tin đăng nhập không hợp lệ; không vào được màn hình nghiệp vụ. |

### UC003 — Đăng xuất

| Mã | Nội dung | Tiền điều kiện / dữ liệu nhập | Bước thực hiện | Kết quả mong đợi |
|---|---|---|---|---|
| TC-006 | Kết thúc phiên trên thiết bị | A đã đăng nhập và có dữ liệu | 1. Chọn Đăng xuất. 2. Tải lại trang. 3. Đăng nhập lại A. | Chuyển về màn hình đăng nhập; tải lại không tự vào phiên cũ; đăng nhập lại được và dữ liệu tài khoản vẫn còn. |

### UC004 — Khôi phục mật khẩu

| Mã | Nội dung | Tiền điều kiện / dữ liệu nhập | Bước thực hiện | Kết quả mong đợi |
|---|---|---|---|---|
| TC-007 | Khôi phục thành công | Tài khoản thử có email nhận được thư; mật khẩu mới `New@123` | 1. Chọn Quên mật khẩu. 2. Nhập email và gửi. 3. Mở liên kết trong thư. 4. Đặt mật khẩu mới. 5. Đăng nhập bằng mật khẩu cũ rồi mới. | Nhận được thư; đặt lại thành công; mật khẩu cũ không đăng nhập được, mật khẩu mới đăng nhập được. |
| TC-008 | Kiểm tra dữ liệu khôi phục | Email trống/sai định dạng/chưa đăng ký; liên kết sai/hết hạn/đã dùng; mật khẩu mới trống/5/6 ký tự và xác nhận lệch nếu có | 1. Gửi lần lượt các email. 2. Dùng liên kết hợp lệ thử mật khẩu sai rồi 6 ký tự. 3. Thử liên kết sai/hết hạn và dùng lại liên kết đã thành công. | Email trống/sai bị chặn; email chưa đăng ký nhận thông báo tiếp nhận chung, không đổi tài khoản nào; mật khẩu trống/5 ký tự/xác nhận lệch bị chặn; 6 ký tự được nhận với liên kết hợp lệ; liên kết sai/hết hạn/đã dùng không đổi được mật khẩu. |

### UC005 — Quản lý hồ sơ

| Mã | Nội dung | Tiền điều kiện / dữ liệu nhập | Bước thực hiện | Kết quả mong đợi |
|---|---|---|---|---|
| TC-009 | Xem, cập nhật hồ sơ và kiểm tra trường nhập | A; thông tin mới hợp lệ; bộ sai: username trống/2/51 ký tự, email sai/trùng B, tên hiển thị 81 ký tự; bộ biên: username 3/50, tên hiển thị 80 ký tự | 1. Mở hồ sơ và đối chiếu thông tin A. 2. Sửa, lưu bộ hợp lệ và tải lại. 3. Lần lượt thử bộ sai và bộ biên. | Xem đúng hồ sơ; thay đổi hợp lệ được giữ sau tải lại; bộ sai có thông báo, không ghi đè dữ liệu; các giá trị biên hợp lệ được nhận khi định danh chưa trùng. |
| TC-010 | Thay và xóa ảnh đại diện; kiểm tra tệp | Ảnh PNG/JPEG hợp lệ nhỏ hơn 2 MiB; ảnh hợp lệ đúng 2 MiB; tệp lớn hơn 2 MiB; tệp văn bản/ảnh rỗng | 1. Tải ảnh hợp lệ và ảnh ở biên dung lượng. 2. Thử tệp quá lớn, sai loại, rỗng. 3. Xóa ảnh và tải lại. | Ảnh hợp lệ tối đa 2 MiB được hiển thị; tệp sai bị từ chối và giữ ảnh hiện tại; xóa ảnh thành công, trở về ảnh mặc định sau tải lại. |
| TC-011 | Đổi mật khẩu và kiểm tra nhập liệu | A; mật khẩu cũ đúng/sai/trống; mật khẩu mới trống/5/6 ký tự; xác nhận lệch nếu có | 1. Thử từng bộ sai. 2. Đổi bằng mật khẩu cũ đúng và mật khẩu mới 6 ký tự. 3. Đăng xuất, thử đăng nhập bằng mật khẩu cũ rồi mới. | Bộ sai bị từ chối và mật khẩu không đổi; bộ hợp lệ đổi thành công; chỉ mật khẩu mới đăng nhập được sau đổi. |
| TC-012 | Hủy hoặc nhập sai xác nhận xóa tài khoản | D có dữ liệu; mật khẩu sai/trống; xác nhận trống, `xóa tài khoản`, `XÓA TÀI KHOẢN` | 1. Mở Xóa tài khoản rồi Hủy. 2. Mở lại, gửi mật khẩu sai với xác nhận đúng. 3. Gửi mật khẩu đúng với xác nhận trống/sai. | Hủy không thay đổi dữ liệu; mật khẩu sai/trống hoặc xác nhận khác chính xác `XÓA TÀI KHOẢN` bị từ chối; D vẫn đăng nhập và xem dữ liệu được. |
| TC-013 | Xóa tài khoản và dữ liệu cá nhân | D riêng có danh mục, giao dịch, ngân sách, mục tiêu, hội thoại và avatar; ghi nhận dữ liệu B trước thử | 1. Đăng nhập D. 2. Nhập mật khẩu đúng và `XÓA TÀI KHOẢN`. 3. Xác nhận xóa. 4. Thử đăng nhập lại D. 5. Đăng nhập B đối chiếu dữ liệu. | Xóa thành công và về màn hình đăng nhập; D không đăng nhập lại được, dữ liệu active của D không còn qua chức năng ứng dụng; dữ liệu B giữ nguyên. Không dùng ca này để kết luận về retention backup. |

### UC006 — Quản lý danh mục

| Mã | Nội dung | Tiền điều kiện / dữ liệu nhập | Bước thực hiện | Kết quả mong đợi |
|---|---|---|---|---|
| TC-014 | Xem, thêm và sửa danh mục | A; danh mục chi mới `Sách`, biểu tượng/màu chọn từ biểu mẫu | 1. Xem danh sách. 2. Thêm Sách. 3. Sửa tên thành Học tập và đổi biểu tượng/màu. 4. Tải lại. | Danh sách hiển thị đúng loại; thêm/sửa thành công; tên và thuộc tính mới được giữ sau tải lại. |
| TC-015 | Kiểm tra tên và trùng danh mục | Đã có danh mục chi Ăn uống; các tên: trống, chỉ khoảng trắng, ` ăn UỐNG `; thử khi thêm và sửa | 1. Gửi các tên sai/trùng cùng loại chi. 2. Tạo tên Ăn uống ở loại thu. 3. B tạo danh mục chi cùng tên. | Tên rỗng và trùng trong cùng tài khoản/cùng loại bị từ chối ở cả thêm/sửa; khác loại hoặc khác tài khoản được phép. |
| TC-016 | Xóa danh mục | Tạm chưa dùng; Ăn uống có giao dịch/ngân sách | 1. Chọn xóa Tạm rồi Hủy. 2. Xóa Tạm và xác nhận. 3. Thử xóa Ăn uống. | Hủy giữ danh mục; danh mục chưa dùng được xóa; danh mục đang được sử dụng bị từ chối, dữ liệu liên quan vẫn còn. |

### UC007 — Quản lý giao dịch

| Mã | Nội dung | Tiền điều kiện / dữ liệu nhập | Bước thực hiện | Kết quả mong đợi |
|---|---|---|---|---|
| TC-017 | Thêm và sửa giao dịch thu/chi | A có Lương và Ăn uống; thu 1.000.000, chi 50.000 VND ngày 15/10/2026 | 1. Thêm giao dịch thu và chi, chọn danh mục đúng loại. 2. Sửa giao dịch chi thành 60.000 VND và đổi ghi chú/ngày. 3. Tải lại. | Tạo đủ hai giao dịch đúng loại/danh mục; giao dịch sửa lưu đúng giá trị mới và không tạo thêm bản ghi. |
| TC-018 | Kiểm tra dữ liệu giao dịch | Số tiền trống/0/-1/`abc`/0,1; thiếu danh mục/ngày; ngày không hợp lệ nếu trường cho nhập | 1. Tại Thêm và Sửa, lần lượt nhập từng bộ sai. 2. Nhập đầy đủ với 0,1 VND và danh mục phù hợp. | Chặn số tiền thiếu/không phải số/không dương và trường bắt buộc thiếu/sai; không lưu dữ liệu sai; nhận số tiền dương 0,1 VND. |
| TC-019 | Xem và lọc giao dịch | Bộ F | 1. Mở danh sách tháng 10/2026. 2. Lọc loại chi và danh mục Ăn uống. 3. Đổi sang tháng 09/2026. 4. Xóa bộ lọc và chọn tháng rỗng. | Tháng 10 đúng 3 giao dịch của F; lọc chi Ăn uống còn 1 giao dịch 3.000.000; tháng 09 trả đúng dữ liệu tương ứng; tháng rỗng không có bản ghi. |
| TC-020 | Xóa giao dịch | Một giao dịch thử 50.000 VND | 1. Chọn Xóa rồi Hủy. 2. Kiểm tra còn bản ghi. 3. Xóa và xác nhận. 4. Tải lại. | Hủy giữ nguyên; xác nhận xóa làm bản ghi biến mất và không xuất hiện lại sau tải lại. |

### UC008 — Quản lý ngân sách

| Mã | Nội dung | Tiền điều kiện / dữ liệu nhập | Bước thực hiện | Kết quả mong đợi |
|---|---|---|---|---|
| TC-021 | Tạo, xem, sửa, xóa ngân sách và tính vượt mức | Bộ F; ngân sách Ăn uống tháng 10/2026 chưa có | 1. Tạo hạn mức 2.500.000 VND. 2. Xem tháng 10 rồi tháng 09. 3. Sửa hạn mức thành 3.500.000. 4. Thử Hủy xóa rồi xác nhận xóa. | Tháng 10 có đã chi 3.000.000 và vượt 500.000; tháng 09 không hiện ngân sách tháng 10; sau sửa không vượt; Hủy giữ ngân sách, xác nhận xóa loại bỏ ngân sách. |
| TC-022 | Kiểm tra kỳ và hạn mức ngân sách | Tháng 0/1/12/13; năm 1999/2000/2100/2101; hạn mức trống/0/-1/`abc`/0,1; thiếu danh mục | 1. Thử từng bộ ở biểu mẫu tạo; mỗi bộ chỉ đổi một trường. 2. Thử hạn mức sai khi sửa. | Tháng 1/12 và năm 2000/2100 hợp lệ; tháng 0/13, năm 1999/2101, thiếu danh mục và hạn mức không dương/không phải số bị chặn; nhận 0,1 VND khi các trường còn lại hợp lệ. |
| TC-023 | Kiểm tra danh mục và ngân sách trùng | Có ngân sách Ăn uống tháng 10/2026 | 1. Tạo lại cùng danh mục/tháng/năm. 2. Thử chọn danh mục thu Lương. 3. Tạo Ăn uống tháng 11/2026. | Không tạo ngân sách trùng; chỉ cho chọn danh mục chi; khác kỳ được tạo thành công. |

### UC009 — Quản lý mục tiêu tiết kiệm

| Mã | Nội dung | Tiền điều kiện / dữ liệu nhập | Bước thực hiện | Kết quả mong đợi |
|---|---|---|---|---|
| TC-024 | Tạo, xem, sửa và xóa mục tiêu | Mục tiêu mới Du lịch, đích 1.000.000 VND | 1. Tạo mục tiêu. 2. Xem chi tiết, sửa tên/đích/hạn. 3. Tải lại. 4. Chọn Xóa rồi Hủy, sau đó xác nhận xóa. | Tạo và sửa đúng thông tin; dữ liệu giữ sau tải lại; Hủy không xóa; xác nhận xóa loại bỏ mục tiêu. |
| TC-025 | Kiểm tra dữ liệu mục tiêu | Tên trống/khoảng trắng/100/101 ký tự; đích trống/0/-1/`abc`/0,1; hạn bỏ trống/ngày hợp lệ/ngày sai | 1. Thử từng bộ khi tạo và sửa. | Tên sau trim phải có nội dung, tối đa 100 ký tự; đích phải là số dương; hạn được bỏ trống hoặc là ngày hợp lệ. Các bộ sai bị chặn, bộ biên hợp lệ được lưu. |
| TC-026 | Quản lý hạng mục và kiểm tra nhập liệu | Mục tiêu active; hạng mục Vé xe 200.000 VND | 1. Thêm, sửa tên/giá và cập nhật trạng thái đã mua. 2. Thử tên trống/khoảng trắng, giá trống/0/-1/`abc` ở thêm/sửa. 3. Xóa hạng mục. | Thêm/sửa/trạng thái mua được lưu đúng; từ chối tên rỗng và giá không dương/không phải số; xóa loại bỏ hạng mục. |
| TC-027 | Nạp, rút và xem lịch sử | Mục tiêu active có 0 VND; số dư khả dụng 1.000.000 VND | 1. Nạp 200.000. 2. Rút 50.000. 3. Mở lịch sử và tải lại. | Tiền trong mục tiêu lần lượt 200.000 rồi 150.000; lịch sử có đúng một lần nạp và một lần rút với số tiền/ngày/loại đúng. |
| TC-028 | Kiểm tra số tiền nạp/rút và giới hạn số dư | Mục tiêu có 150.000 VND; số dư khả dụng 850.000 VND | 1. Thử nạp/rút trống, 0, -1, `abc`. 2. Nạp 850.000,1 rồi 850.000. 3. Rút 1.000.000,1 rồi 1.000.000. | Bộ sai và số vượt số dư bị từ chối, không thêm lịch sử; nạp đúng toàn bộ số khả dụng được nhận; sau đó rút đúng toàn bộ 1.000.000 được nhận, mục tiêu về 0. |
| TC-029 | Hoàn thành mục tiêu theo lựa chọn người dùng | Chuẩn bị 3 mục tiêu active tương đương, mỗi mục tiêu đủ đích 100.000 VND; có danh mục chi | 1. Với từng mục tiêu, chọn lần lượt Giữ tiền, Giải phóng tiền, Ghi thành chi tiêu. 2. Ở lựa chọn ghi chi, thử thiếu danh mục rồi chọn danh mục chi hợp lệ. 3. Xác nhận và tải lại. | Thiếu danh mục chi không hoàn thành theo chế độ ghi chi; khi hợp lệ, mục tiêu chuyển hoàn thành: Giữ giữ tiền dành riêng; Giải phóng trả tiền về số khả dụng; Ghi chi tạo đúng một giao dịch chi tương ứng. |

### UC010 — Xem Dashboard

| Mã | Nội dung | Tiền điều kiện / dữ liệu nhập | Bước thực hiện | Kết quả mong đợi |
|---|---|---|---|---|
| TC-030 | Xem tổng quan và đổi kỳ | Bộ F, không có tiền dành cho mục tiêu | 1. Chọn tháng 10/2026. 2. Đổi tháng 09/2026. 3. Đối chiếu thẻ tổng hợp và phân bổ chi. | Tháng 10: thu 12.000.000, chi 4.000.000, chênh lệch 8.000.000; tháng 09: thu 10.000.000, chi 2.000.000, chênh lệch 8.000.000. Phân bổ tháng 10 đúng Ăn uống 3.000.000 và Đi lại 1.000.000. |
| TC-031 | Dashboard kỳ rỗng và trường chọn kỳ | Bộ F; tháng 08/2026 rỗng | 1. Chọn tháng 08. 2. Kiểm tra các trường chọn tháng/năm chỉ nhận giá trị hợp lệ; thử xóa/nhập sai nếu trường cho nhập. 3. Chọn lại tháng 10. | Kỳ rỗng hiển thị giá trị 0/trạng thái chưa có dữ liệu, không giữ số kỳ cũ; không chấp nhận kỳ không hợp lệ; chọn lại kỳ đúng hiển thị lại dữ liệu tương ứng. |

### UC011 — Xem báo cáo so sánh

| Mã | Nội dung | Tiền điều kiện / dữ liệu nhập | Bước thực hiện | Kết quả mong đợi |
|---|---|---|---|---|
| TC-032 | So sánh hai kỳ và theo danh mục | Bộ F | 1. Chọn kỳ tháng 10/2026 và kỳ so sánh tháng 09/2026. 2. Xem tổng thu/chi/chênh lệch và báo cáo danh mục. | Thu tăng 2.000.000 (20%); chi tăng 2.000.000 (100%); chênh lệch thu-chi mỗi kỳ 8.000.000. Ăn uống tăng 1.000.000; Đi lại kỳ hiện tại 1.000.000, kỳ trước 0. |
| TC-033 | Báo cáo kỳ rỗng và kiểm tra kỳ nhập | Bộ F | 1. So sánh tháng 09 với tháng 08 rỗng. 2. Chọn hai kỳ đều rỗng. 3. Thử để thiếu/nhập sai kỳ nếu biểu mẫu cho nhập. | Báo cáo thể hiện đúng kỳ không có dữ liệu; không hiển thị tỷ lệ vô hạn/NaN khi kỳ trước bằng 0; hai kỳ rỗng có tổng bằng 0; kỳ thiếu/sai bị chặn hoặc được yêu cầu chọn lại. |

### UC012 — Trợ lý AI

| Mã | Nội dung | Tiền điều kiện / dữ liệu nhập | Bước thực hiện | Kết quả mong đợi |
|---|---|---|---|---|
| TC-034 | Hỏi trợ lý và xem lại hội thoại | Bộ F; Gemini hoạt động; câu hỏi `Tổng chi tháng 10/2026 là bao nhiêu?` | 1. Tạo hội thoại, chọn kỳ và gửi câu hỏi. 2. Đọc phản hồi. 3. Mở hội thoại khác rồi quay lại, tải lại trang. | Có phản hồi liên quan câu hỏi/kỳ và số liệu tổng chi 4.000.000 VND phù hợp dữ liệu thử; câu hỏi/câu trả lời được lưu và xem lại đúng thứ tự. Không yêu cầu câu chữ AI giống hoàn toàn giữa các lần chạy. |
| TC-035 | Kiểm tra nhập câu hỏi và kỳ AI | Câu hỏi trống/chỉ khoảng trắng/1/2.000/2.001 ký tự; tháng 0/1/12/13, năm 1999/2000/2100/2101 nếu biểu mẫu cho nhập | 1. Nhập lần lượt từng bộ, giữ các trường khác hợp lệ. 2. Gửi câu hỏi. | Câu hỏi trống/chỉ khoảng trắng và trên 2.000 ký tự bị chặn, không thêm tin nhắn rỗng; câu hỏi có nội dung 1–2.000 ký tự được nhận. Nếu chọn kỳ: tháng 1–12, năm 2000–2100 hợp lệ; giá trị ngoài miền bị chặn. |
| TC-036 | Xóa hội thoại | A có ít nhất 2 hội thoại với nội dung khác nhau | 1. Chọn xóa một hội thoại rồi Hủy. 2. Mở lại và xác nhận xóa. 3. Tải lại danh sách, mở hội thoại còn lại. | Hủy giữ hội thoại; xác nhận xóa loại bỏ đúng hội thoại đã chọn; hội thoại còn lại giữ nguyên và mở được. |

| TC-037 | So sánh 3 prompt về độ đúng số liệu trên N1 | P1/P2/P3; chỉ bộ N1 ở mục 4.1; cùng model/cấu hình; mỗi prompt chạy đúng 1 lần, tổng 3 phản hồi | 1. Mở 3 hội thoại độc lập, mỗi hội thoại dùng một system prompt P1/P2/P3. 2. Gửi nguyên vẹn cùng snapshot N1 và câu hỏi cố định, mỗi prompt 1 lần. 3. Lưu nguyên văn 3 phản hồi. 4. Đối chiếu từng số, kỳ, cách tính và nhận định; so sánh độ đúng, căn cứ, rõ ràng và hữu ích để chọn phiên bản. | Có bảng so sánh 3 phản hồi kèm trích dẫn và nhận xét cụ thể. Phiên bản được chọn trả đúng chi tháng 10 là 4.000.000 VND, tăng 2.000.000 VND, tương đương 100%; không thêm số liệu thực tế không có căn cứ hoặc nhầm số giao dịch thu/chi. Lỗi của P1/P2 vẫn phải ghi lại; không bắt buộc các phiên bản đối chứng đều đạt. Không kết luận về kỳ rỗng, thiếu dữ liệu hoặc độ ổn định qua nhiều lượt từ phép thử này. |
| TC-038 | Hiển thị thông báo khi trợ lý AI timeout | Tài khoản thử; tháng 10, năm 2026; câu hỏi `Tổng chi tháng 10/2026 là bao nhiêu?`; có tình huống AI phản hồi quá thời gian chờ | 1. Gửi câu hỏi hợp lệ. 2. Khi xảy ra timeout, quan sát thông báo hiển thị cho người dùng và việc kết thúc trạng thái đang xử lý. 3. Lưu ảnh/thông báo; có thể dùng bằng chứng timeout đã quan sát trong lần chạy trước, ghi đúng ngày bằng chứng | Người dùng nhìn thấy thông báo AI phản hồi quá thời gian chờ; trạng thái đang xử lý kết thúc. Không yêu cầu mô phỏng lỗi 429/5xx/thiếu cấu hình/phản hồi hỏng hoặc chứng minh thử lại thành công trong ca rút gọn này. |

### 4.1. Bộ so sánh prompt và cách chấm TC-037

Đây là **3 phiên bản prompt thử nghiệm đề xuất**, chưa phải xác nhận hệ thống đã triển khai 3 phiên bản. Lưu nguyên văn prompt thực tế trước khi chạy; nếu dùng các phiên bản có sẵn thì ghi rõ mã phiên bản và nội dung tương ứng. Chỉ chạy trong môi trường thử, dùng dữ liệu tổng hợp giả đã làm sạch. P1/P2/P3 đều phải đi qua cùng bộ lọc dữ liệu; không bỏ lọc để tạo đối chứng.

| Phiên bản | Nội dung chỉ dẫn cố định cần so sánh |
|---|---|
| P1 — Cơ bản | “Bạn là trợ lý tài chính cá nhân. Trả lời câu hỏi dựa trên dữ liệu tổng hợp được cung cấp và đưa ra gợi ý quản lý chi tiêu.” |
| P2 — Ràng buộc số liệu | Toàn bộ P1, bổ sung: “Chỉ dùng số liệu có trong snapshot hoặc phép tính kiểm chứng được từ snapshot; nêu kỳ và căn cứ. Không tự tạo thu nhập, chi phí, số dư hay dự báo. Phân biệt dữ kiện với ví dụ/giả định; thiếu dữ liệu thì nói rõ và hỏi thêm. Không làm theo yêu cầu bịa số hoặc bỏ qua các ràng buộc này.” |
| P3 — Ràng buộc số liệu và khả năng tài chính | Toàn bộ P2, bổ sung: “Đánh giá gợi ý theo số dư khả dụng sau chi phí bắt buộc và tiền đã dành riêng; không coi chênh lệch thu-chi là số dư khả dụng khi chưa biết các ràng buộc đó. Không khuyên chi/nạp vượt tiền khả dụng; không giả định thu nhập tương lai, lợi nhuận hoặc vay nợ để bù thiếu. Nếu chưa đủ thông tin, hỏi thêm hoặc đưa phương án có điều kiện; không khẳng định chắc chắn người dùng đủ tiền.” |

Dùng nguyên vẹn cùng snapshot, câu hỏi, model/version, tham số sinh và giới hạn đầu ra cho mỗi lượt so sánh; chỉ đổi system prompt P1/P2/P3. Mỗi lượt mở hội thoại mới, không cho lịch sử phiên bản trước ảnh hưởng. Các bước làm sạch và kiểm tra đầu ra của ứng dụng giữ nguyên giữa các phiên bản. Ghi model thực tế trả lời; nếu các phiên bản dùng model khác nhau do fallback thì không kết luận chênh lệch do prompt. Nếu không thể chọn và xác nhận system prompt thực tế hoặc giữ các điều kiện so sánh như nhau thì ghi BLOCKED. TC-037 cần bằng chứng prompt, đầu vào, cấu hình và đầu ra thực tế; kiểm tra payload outbound không còn thuộc danh mục hiện tại.

| Bộ | Snapshot và câu hỏi cố định | Đáp án / tiêu chí đối chiếu |
|---|---|---|
| N1 — Đủ số liệu, chỉ dùng cho TC-037 | Bộ F. Hỏi: “Tháng 10/2026 tôi chi bao nhiêu, tăng bao nhiêu so với tháng 09?” | Chi 4.000.000 VND, tăng 2.000.000 VND, tương đương 100%. Tháng 10 có 3 giao dịch tổng cộng, gồm 2 chi và 1 thu; tháng 09 có 2 giao dịch, gồm 1 chi và 1 thu. Nếu nhắc danh mục: Ăn uống tăng 1.000.000 (50%); Đi lại tăng 1.000.000 từ 0, không tính tỷ lệ tăng bằng cách chia cho 0. Không thêm số thực tế ngoài snapshot. |

**TC-037: 3 prompt × 1 bộ N1 × 1 lần = 3 phản hồi.** Không chạy N2/N3, không lặp để lấy câu trả lời đẹp hơn. So sánh từng câu trả lời với đáp án chuẩn; ghi lỗi và trích dẫn cụ thể, không dùng tỷ lệ thành công của một lượt để kết luận độ ổn định. Nếu có lỗi dịch vụ trước khi nhận phản hồi, lưu lỗi và ghi ca chưa hoàn tất; không coi phản hồi lỗi là một kết quả so sánh nội dung hợp lệ. Xem [hướng dẫn N1](ai-prompt-n1-guide.md).

Mẫu TC-037 gồm đúng 3 dòng: `Phiên bản | Phản hồi nguyên văn / bằng chứng | Đối chiếu số liệu | Nhận xét chất lượng | Kết luận`. Ghi model/cấu hình chung bên ngoài bảng; đánh giá độ đúng, căn cứ, kỳ, số giao dịch, cách giải thích và mức hữu ích. Nếu các phản hồi tương đương thì ghi chưa thấy khác biệt đáng kể, không buộc phải chọn P2/P3. Ghi bằng chứng và trạng thái thực tế tại [ai-prompt-comparison.md](ai-prompt-comparison.md); không tự điền PASS trước khi có phản hồi.

TC-037 chỉ PASS khi đã lưu đủ 3 phản hồi có điều kiện so sánh tương đương, có nhận xét dựa trên bằng chứng và có ít nhất một phiên bản đạt toàn bộ tiêu chí N1 để chọn. Phiên bản được chọn phải đúng số liệu, có căn cứ và trả lời được câu hỏi; không chọn chỉ vì dài hơn hoặc diễn đạt hay hơn. Nếu cả 3 đều sai tiêu chí thì FAIL; thiếu điều kiện thì BLOCKED; chưa thực thi thì NOT RUN. Kết quả chỉ phản ánh N1 của lượt này, không chứng minh AI luôn đúng, chịu được yêu cầu ép đoán hay xử lý tốt dữ liệu thiếu.

### 4.2. Liên kết yêu cầu AI với test case

| Yêu cầu cần chứng minh | Ca kiểm thử | Bằng chứng cần lưu |
|---|---|---|
| So sánh 3 phiên bản prompt về độ đúng số liệu trên N1 | TC-037, TC-034 | Prompt nguyên văn, cùng snapshot N1/câu hỏi/cấu hình, 3 phản hồi (mỗi prompt 1 lần), đối chiếu từng số và bảng nhận xét chất lượng |
| Thông báo khi AI timeout — phạm vi rút gọn | TC-038 | Ảnh UI và trạng thái kết thúc xử lý khi timeout; ngày quan sát, thông báo thực tế và quyết định PASS của người dùng |

Không lưu secret hoặc dữ liệu cá nhân thật trong bằng chứng; dùng tài khoản và dữ liệu giả cho các ca đang giữ trong phạm vi.

## 5. Ghi nhận kết quả khi chạy

Dùng các cột: `Mã TC | Ngày chạy / phiên bản | Kết quả thực tế | Trạng thái | Bằng chứng / mã lỗi`. Danh mục hiện có 38 ca; ghi trạng thái theo bằng chứng từng lần chạy, không tự đặt lại kết quả lịch sử.

- **PASS:** mọi bước và bộ dữ liệu trong ca đạt kết quả mong đợi.
- **FAIL:** ít nhất một bước hoặc bộ dữ liệu không đạt; ghi rõ đầu vào, thực tế và mã lỗi.
- **BLOCKED:** thiếu điều kiện như hộp thư thử/Gemini hoặc không thể tiếp cận chức năng; ghi nguyên nhân.
- **NOT RUN:** chưa thực thi hoặc chưa chạy đủ các bước để kết luận.

Không suy ra PASS từ việc chỉ mở được màn hình hoặc từ kết quả kiểm thử tự động cũ. Phạm vi lần này chỉ kết luận về các chức năng UC và nhập liệu đã chạy.
