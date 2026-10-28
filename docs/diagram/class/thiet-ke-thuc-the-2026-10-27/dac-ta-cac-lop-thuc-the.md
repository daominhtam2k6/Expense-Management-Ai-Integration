## 4.3. Đặc tả các lớp thực thể

Mô hình gồm chín lớp thực thể: User, Category, Transaction, Budget, SavingGoal, GoalTransaction, GoalItem, AIConversation và AIMessage. Các phương thức được lựa chọn theo chức năng của từng lớp và được đặc tả ở mức thiết kế giả định; tên, tham số và kiểu trả về không bắt buộc trùng với mã nguồn hiện tại.

Các thao tác cấp lớp như create(), register(), login(), recoverPassword(), deposit() và withdraw() không yêu cầu một đối tượng nhận đã tồn tại; các thao tác còn lại làm việc với đối tượng hiện tại. Trên sơ đồ UML, phương thức cấp lớp được gạch chân. Dấu (...) chỉ lược tham số trên hình; bảng dưới đây ghi chữ ký đầy đủ.

Tên thuộc tính dùng camelCase; dấu ? chỉ giá trị có thể rỗng, dấu / chỉ thuộc tính dẫn xuất. Decimal là kiểu số tiền với độ chính xác lưu trữ (14,2). CategoryType và TransactionType gồm income, expense; GoalStatus gồm active, completed; GoalTransactionType gồm deposit, withdraw; MessageRole gồm user, assistant. AIMessageOutput là cấu trúc đầu ra, không bổ sung vào danh sách lớp thực thể.

Tầng ứng dụng phối hợp xác thực, kiểm tra quyền, truy vấn và lưu dữ liệu. Các ràng buộc bao gồm nghiệp vụ và lưu trữ, không đồng nghĩa toàn bộ đều là CHECK trong cơ sở dữ liệu. Với phương thức thay đổi dữ liệu, thao tác chỉ thành công khi lưu hoàn tất; lỗi kiểm tra hoặc lỗi lưu phải giữ nguyên trạng thái đã lưu trước đó. void biểu thị không trả giá trị; trường hợp không hợp lệ được thông báo bằng lỗi.

Trong phạm vi đặc tả này, updateAccount() cập nhật hồ sơ; recoverPassword() khởi tạo yêu cầu khôi phục; isTargetReached() chỉ kiểm tra đã đạt số tiền mục tiêu; create() của AIConversation tạo hội thoại mới. Thông tin status, completionAmount và completionMode vẫn được giữ đầy đủ trong mô hình dữ liệu dù phương thức kiểm tra tiến độ không sửa các trường này.

### 4.3.1. Lớp User

Lớp User biểu diễn tài khoản của người sử dụng, lưu thông tin đăng nhập, hồ sơ, ảnh đại diện và dữ liệu phục vụ khôi phục mật khẩu.

**a) Thuộc tính**

*Bảng 4.2. Thuộc tính lớp User*

| Tên | Kiểu dữ liệu | Ràng buộc | Ý nghĩa |
|---|---|---|---|
| id | String | PK; UUID sinh tự động | Mã người sử dụng. |
| username | String | Bắt buộc; 3–50 ký tự; không trùng sau chuẩn hóa | Tên đăng nhập. |
| email | String | Bắt buộc; đúng định dạng; không trùng sau chuẩn hóa | Email đăng ký và khôi phục mật khẩu. |
| displayName | String? | Có thể rỗng; tối đa 80 ký tự | Tên hiển thị. |
| passwordHash | String | Bắt buộc; lưu giá trị đã băm | Thông tin kiểm tra mật khẩu; không lưu mật khẩu rõ. |
| avatarUrl | String? | Có thể rỗng | Đường dẫn ảnh đại diện. |
| createdAt | DateTime | Mặc định thời điểm tạo | Thời điểm tạo tài khoản. |
| resetTokenHash | String? | Có thể rỗng; chỉ lưu giá trị đã băm | Mã khôi phục mật khẩu đã băm. |
| resetTokenExpiry | DateTime? | Có thể rỗng | Thời điểm hết hạn mã khôi phục. |
| usernameNormalized | String | Bắt buộc; duy nhất | Khóa so sánh username sau NFKC, trim và case-fold. |
| emailNormalized | String | Bắt buộc; duy nhất | Khóa so sánh email sau NFKC, trim và case-fold. |

**b) Các phương thức**

**Phương thức 1: register()**

*Bảng 4.3. Đặc tả phương thức User.register()*

| Mục | Nội dung |
|---|---|
| Tên | register(username: String, email: String, password: String): User |
| Mô tả | Đăng ký tài khoản mới. |
| Tham số đầu vào | username: tên đăng nhập; email: email đăng ký; password: mật khẩu. |
| Kết quả đầu ra | Đối tượng User mới. |
| Điều kiện bắt đầu | Tên đăng nhập và email hợp lệ, chưa được sử dụng; mật khẩu có ít nhất 6 ký tự. |
| Luồng xử lý | B1. Chuẩn hóa username, email và kiểm tra trùng.<br>B2. Băm mật khẩu, tạo UUID và xác lập thời điểm tạo.<br>B3. Khởi tạo User cùng các khóa chuẩn hóa; phối hợp tầng ứng dụng lưu tài khoản. |
| Điều kiện kết thúc | Tài khoản được tạo duy nhất; không lưu mật khẩu rõ. |

**Phương thức 2: login()**

*Bảng 4.4. Đặc tả phương thức User.login()*

| Mục | Nội dung |
|---|---|
| Tên | login(identifier: String, password: String): String |
| Mô tả | Xác thực thông tin đăng nhập và cấp token truy cập. |
| Tham số đầu vào | identifier: tên đăng nhập hoặc email; password: mật khẩu. |
| Kết quả đầu ra | Chuỗi token truy cập khi xác thực thành công. |
| Điều kiện bắt đầu | Có tài khoản phù hợp với thông tin đăng nhập. |
| Luồng xử lý | B1. Chuẩn hóa identifier và xác định tài khoản.<br>B2. Kiểm tra password với passwordHash.<br>B3. Nếu hợp lệ, yêu cầu tầng xác thực tạo token; nếu không, báo lỗi đăng nhập. |
| Điều kiện kết thúc | Trả token gắn với đúng tài khoản; không trả passwordHash. |

**Phương thức 3: logout()**

*Bảng 4.5. Đặc tả phương thức User.logout()*

| Mục | Nội dung |
|---|---|
| Tên | logout(accessToken: String): void |
| Mô tả | Kết thúc phiên truy cập hiện tại. |
| Tham số đầu vào | accessToken: token của phiên cần kết thúc. |
| Kết quả đầu ra | void. |
| Điều kiện bắt đầu | Người sử dụng đang có phiên truy cập. |
| Luồng xử lý | B1. Xác định phiên gắn với accessToken.<br>B2. Yêu cầu tầng xác thực kết thúc phiên theo cơ chế quản lý phiên được lựa chọn.<br>B3. Yêu cầu giao diện xóa token và thông tin phiên đang giữ. |
| Điều kiện kết thúc | Phiên hiện tại kết thúc; dữ liệu tài khoản và tài chính không bị xóa. |

**Phương thức 4: recoverPassword()**

*Bảng 4.6. Đặc tả phương thức User.recoverPassword()*

| Mục | Nội dung |
|---|---|
| Tên | recoverPassword(email: String): void |
| Mô tả | Khởi tạo yêu cầu khôi phục mật khẩu qua email. |
| Tham số đầu vào | email: địa chỉ email nhận hướng dẫn khôi phục. |
| Kết quả đầu ra | void. |
| Điều kiện bắt đầu | Email đúng định dạng; dịch vụ gửi email đã được cấu hình. |
| Luồng xử lý | B1. Chuẩn hóa email và kiểm tra tài khoản tương ứng.<br>B2. Với tài khoản hợp lệ, tạo mã khôi phục; chỉ lưu resetTokenHash và resetTokenExpiry, thay thế mã cũ.<br>B3. Gửi liên kết khôi phục qua tầng gửi email; trả thông báo chung cho yêu cầu. |
| Điều kiện kết thúc | Nếu có tài khoản, mã khôi phục mới có thời hạn; mật khẩu chưa bị thay đổi. Phương thức này chỉ khởi tạo yêu cầu khôi phục. |

**Phương thức 5: updateAccount()**

*Bảng 4.7. Đặc tả phương thức User.updateAccount()*

| Mục | Nội dung |
|---|---|
| Tên | updateAccount(username: String, email: String, displayName: String?, avatarUrl: String?): void |
| Mô tả | Cập nhật thông tin tài khoản và hồ sơ. |
| Tham số đầu vào | username: tên đăng nhập; email: email; displayName: tên hiển thị; avatarUrl: đường dẫn ảnh đã được kiểm tra. |
| Kết quả đầu ra | void. |
| Điều kiện bắt đầu | Tài khoản tồn tại, đúng quyền; tên đăng nhập và email mới không trùng tài khoản khác. |
| Luồng xử lý | B1. Kiểm tra và chuẩn hóa thông tin đầu vào.<br>B2. Cập nhật username, email, displayName, avatarUrl và các khóa chuẩn hóa.<br>B3. Nếu email thay đổi, xóa mã khôi phục và thời hạn cũ; phối hợp lưu thay đổi. |
| Điều kiện kết thúc | Hồ sơ được cập nhật nhất quán; không thay đổi mật khẩu. Giá trị null ở trường tùy chọn biểu thị xóa giá trị hiện tại. |

### 4.3.2. Lớp Category

Lớp Category biểu diễn danh mục thu nhập hoặc chi tiêu, dùng để phân loại giao dịch và xác định danh mục áp dụng ngân sách.

**a) Thuộc tính**

*Bảng 4.8. Thuộc tính lớp Category*

| Tên | Kiểu dữ liệu | Ràng buộc | Ý nghĩa |
|---|---|---|---|
| id | String | PK; UUID sinh tự động | Mã danh mục. |
| userId | String | FK → User.id; bắt buộc | Người sở hữu danh mục. |
| name | String | Bắt buộc; không chỉ gồm khoảng trắng | Tên danh mục. |
| type | CategoryType | income hoặc expense | Loại thu nhập hoặc chi tiêu. |
| color | String | Bắt buộc; mặc định #D9A441 | Màu hiển thị. |
| icon | String | Bắt buộc; mặc định circle-dollar-sign | Biểu tượng hiển thị. |
| nameNormalized | String | Bắt buộc; duy nhất trong (userId, type) | Tên chuẩn hóa để kiểm tra trùng. |

**b) Các phương thức**

**Phương thức 1: create()**

*Bảng 4.9. Đặc tả phương thức Category.create()*

| Mục | Nội dung |
|---|---|
| Tên | create(userId: String, name: String, type: CategoryType, color: String, icon: String): Category |
| Mô tả | Tạo danh mục thu nhập hoặc chi tiêu. |
| Tham số đầu vào | userId: người sở hữu; name: tên; type: loại; color: màu; icon: biểu tượng. |
| Kết quả đầu ra | Đối tượng Category mới. |
| Điều kiện bắt đầu | Người sử dụng tồn tại, đúng quyền; tên không trống và chưa trùng trong cùng người sở hữu, loại danh mục. |
| Luồng xử lý | B1. Kiểm tra tên, loại, màu và biểu tượng.<br>B2. Chuẩn hóa tên, tạo UUID và gắn userId.<br>B3. Khởi tạo danh mục và phối hợp lưu dữ liệu. |
| Điều kiện kết thúc | Danh mục mới có khóa chuẩn hóa và thuộc đúng người sử dụng. |

**Phương thức 2: update()**

*Bảng 4.10. Đặc tả phương thức Category.update()*

| Mục | Nội dung |
|---|---|
| Tên | update(name: String, color: String, icon: String): void |
| Mô tả | Chỉnh sửa thông tin hiển thị của danh mục. |
| Tham số đầu vào | name: tên mới; color: màu mới; icon: biểu tượng mới. |
| Kết quả đầu ra | void. |
| Điều kiện bắt đầu | Danh mục tồn tại, đúng quyền; tên mới không trùng danh mục khác cùng loại. |
| Luồng xử lý | B1. Kiểm tra và chuẩn hóa name.<br>B2. Cập nhật name, nameNormalized, color và icon.<br>B3. Giữ nguyên id, userId và type; phối hợp lưu thay đổi. |
| Điều kiện kết thúc | Thông tin hiển thị được cập nhật; các tham chiếu từ giao dịch và ngân sách được giữ nguyên. |

**Phương thức 3: delete()**

*Bảng 4.11. Đặc tả phương thức Category.delete()*

| Mục | Nội dung |
|---|---|
| Tên | delete(): void |
| Mô tả | Xóa danh mục không còn được sử dụng. |
| Tham số đầu vào | Không có; thao tác trên danh mục hiện tại. |
| Kết quả đầu ra | void. |
| Điều kiện bắt đầu | Danh mục tồn tại, đúng quyền. |
| Luồng xử lý | B1. Kiểm tra giao dịch và ngân sách đang tham chiếu danh mục.<br>B2. Nếu còn tham chiếu, báo lỗi và dừng.<br>B3. Nếu không còn tham chiếu, yêu cầu tầng ứng dụng xóa danh mục. |
| Điều kiện kết thúc | Danh mục được xóa khi hợp lệ; không xóa dây chuyền các giao dịch hoặc ngân sách. |

### 4.3.3. Lớp Transaction

Lớp Transaction biểu diễn một khoản thu hoặc chi, ghi nhận số tiền, danh mục, ngày phát sinh và ghi chú; đây là dữ liệu đầu vào cho thống kê tài chính.

**a) Thuộc tính**

*Bảng 4.12. Thuộc tính lớp Transaction*

| Tên | Kiểu dữ liệu | Ràng buộc | Ý nghĩa |
|---|---|---|---|
| id | String | PK; UUID sinh tự động | Mã giao dịch. |
| userId | String | FK → User.id; bắt buộc | Người sở hữu giao dịch. |
| categoryId | String | FK → Category.id; bắt buộc; cùng chủ sở hữu | Danh mục phân loại giao dịch. |
| amount | Decimal | Bắt buộc; > 0; độ chính xác (14,2) | Số tiền thu hoặc chi. |
| type | TransactionType | income hoặc expense; khớp loại danh mục | Loại giao dịch. |
| transactionDate | Date | Bắt buộc; không lớn hơn ngày hiện tại | Ngày phát sinh; ánh xạ txn_date trong mã nguồn. |
| note | String? | Có thể rỗng | Ghi chú giao dịch. |

**b) Các phương thức**

**Phương thức 1: create()**

*Bảng 4.13. Đặc tả phương thức Transaction.create()*

| Mục | Nội dung |
|---|---|
| Tên | create(userId: String, category: Category, amount: Decimal, transactionDate: Date, note: String?): Transaction |
| Mô tả | Ghi nhận khoản thu hoặc chi mới. |
| Tham số đầu vào | userId: người sở hữu; category: danh mục; amount: số tiền; transactionDate: ngày phát sinh; note: ghi chú tùy chọn. |
| Kết quả đầu ra | Đối tượng Transaction mới. |
| Điều kiện bắt đầu | Danh mục thuộc userId; amount > 0; ngày không ở tương lai. |
| Luồng xử lý | B1. Kiểm tra quyền sở hữu danh mục, số tiền và ngày.<br>B2. Tạo UUID, gắn userId và categoryId; xác định type theo category.type.<br>B3. Gán số tiền, ngày, ghi chú và phối hợp lưu giao dịch. |
| Điều kiện kết thúc | Khoản thu/chi được ghi nhận đúng loại và đúng chủ sở hữu. |

**Phương thức 2: update()**

*Bảng 4.14. Đặc tả phương thức Transaction.update()*

| Mục | Nội dung |
|---|---|
| Tên | update(category: Category, amount: Decimal, transactionDate: Date, note: String?): void |
| Mô tả | Chỉnh sửa khoản thu hoặc chi hiện có. |
| Tham số đầu vào | category: danh mục mới; amount: số tiền; transactionDate: ngày; note: ghi chú tùy chọn. |
| Kết quả đầu ra | void. |
| Điều kiện bắt đầu | Giao dịch tồn tại, đúng quyền; danh mục cùng người sở hữu; số tiền và ngày hợp lệ. |
| Luồng xử lý | B1. Kiểm tra dữ liệu thay thế.<br>B2. Cập nhật categoryId, amount, transactionDate, note và đồng bộ type theo danh mục.<br>B3. Giữ nguyên id và userId; phối hợp lưu thay đổi. |
| Điều kiện kết thúc | Giao dịch được cập nhật; số liệu tổng hợp về sau sử dụng giá trị mới. |

**Phương thức 3: delete()**

*Bảng 4.15. Đặc tả phương thức Transaction.delete()*

| Mục | Nội dung |
|---|---|
| Tên | delete(): void |
| Mô tả | Xóa giao dịch hiện tại. |
| Tham số đầu vào | Không có. |
| Kết quả đầu ra | void. |
| Điều kiện bắt đầu | Giao dịch tồn tại và thuộc người sử dụng đang thao tác. |
| Luồng xử lý | B1. Kiểm tra quyền thao tác trên giao dịch.<br>B2. Yêu cầu tầng ứng dụng xóa bản ghi.<br>B3. Khi hiển thị lại, tổng hợp tài chính dựa trên dữ liệu còn lại. |
| Điều kiện kết thúc | Giao dịch không còn được tính vào thu/chi; danh mục liên quan vẫn được giữ. |

### 4.3.4. Lớp Budget

Lớp Budget biểu diễn hạn mức chi tiêu cho một danh mục trong tháng và năm xác định, hỗ trợ đánh giá số tiền còn lại và tình trạng vượt ngân sách.

**a) Thuộc tính**

*Bảng 4.16. Thuộc tính lớp Budget*

| Tên | Kiểu dữ liệu | Ràng buộc | Ý nghĩa |
|---|---|---|---|
| id | String | PK; UUID sinh tự động | Mã ngân sách. |
| userId | String | FK → User.id; bắt buộc | Người sở hữu ngân sách. |
| categoryId | String | FK → Category.id; danh mục expense cùng chủ sở hữu | Danh mục áp dụng hạn mức. |
| month | Integer | Bắt buộc; 1–12 | Tháng áp dụng. |
| year | Integer | Bắt buộc; 2000–2100 | Năm áp dụng. |
| limitAmount | Decimal | Bắt buộc; > 0; độ chính xác (14,2) | Hạn mức chi tiêu. |

Mỗi bộ (userId, categoryId, month, year) chỉ có một ngân sách theo quy tắc nghiệp vụ.

**b) Các phương thức**

**Phương thức 1: create()**

*Bảng 4.17. Đặc tả phương thức Budget.create()*

| Mục | Nội dung |
|---|---|
| Tên | create(userId: String, category: Category, month: Integer, year: Integer, limitAmount: Decimal): Budget |
| Mô tả | Tạo hạn mức chi tiêu cho một danh mục trong kỳ. |
| Tham số đầu vào | userId: người sở hữu; category: danh mục chi; month, year: kỳ áp dụng; limitAmount: hạn mức. |
| Kết quả đầu ra | Đối tượng Budget mới. |
| Điều kiện bắt đầu | Danh mục expense thuộc userId; tháng 1–12, năm 2000–2100; hạn mức > 0; chưa có ngân sách cùng danh mục và kỳ. |
| Luồng xử lý | B1. Kiểm tra danh mục, kỳ và hạn mức.<br>B2. Kiểm tra trùng theo userId, categoryId, month, year.<br>B3. Tạo UUID, khởi tạo Budget và phối hợp lưu dữ liệu. |
| Điều kiện kết thúc | Có một ngân sách hợp lệ cho danh mục và kỳ đã chọn. |

**Phương thức 2: update()**

*Bảng 4.18. Đặc tả phương thức Budget.update()*

| Mục | Nội dung |
|---|---|
| Tên | update(limitAmount: Decimal): void |
| Mô tả | Thay đổi hạn mức của ngân sách. |
| Tham số đầu vào | limitAmount: hạn mức chi tiêu mới. |
| Kết quả đầu ra | void. |
| Điều kiện bắt đầu | Ngân sách tồn tại, đúng quyền; hạn mức mới > 0. |
| Luồng xử lý | B1. Kiểm tra hạn mức mới.<br>B2. Cập nhật limitAmount; giữ nguyên danh mục và kỳ.<br>B3. Phối hợp lưu thay đổi. |
| Điều kiện kết thúc | Hạn mức mới được áp dụng khi tính số còn lại và tình trạng vượt ngân sách. |

**Phương thức 3: delete()**

*Bảng 4.19. Đặc tả phương thức Budget.delete()*

| Mục | Nội dung |
|---|---|
| Tên | delete(): void |
| Mô tả | Xóa thiết lập ngân sách hiện tại. |
| Tham số đầu vào | Không có. |
| Kết quả đầu ra | void. |
| Điều kiện bắt đầu | Ngân sách tồn tại và thuộc người sử dụng đang thao tác. |
| Luồng xử lý | B1. Kiểm tra quyền sở hữu.<br>B2. Yêu cầu tầng ứng dụng xóa ngân sách. |
| Điều kiện kết thúc | Hạn mức được gỡ bỏ; không xóa danh mục hoặc giao dịch chi tiêu. |

**Phương thức 4: calculateRemaining()**

*Bảng 4.20. Đặc tả phương thức Budget.calculateRemaining()*

| Mục | Nội dung |
|---|---|
| Tên | calculateRemaining(transactions: List<Transaction>): Decimal |
| Mô tả | Tính lượng ngân sách còn lại trong kỳ. |
| Tham số đầu vào | transactions: tập giao dịch dùng để tổng hợp. |
| Kết quả đầu ra | limitAmount trừ tổng chi phù hợp; có thể âm. |
| Điều kiện bắt đầu | Có đầy đủ giao dịch của phạm vi cần tính; ngân sách đã xác định chủ sở hữu, danh mục và kỳ. |
| Luồng xử lý | B1. Lọc giao dịch expense cùng userId, categoryId, tháng và năm.<br>B2. Tính tổng amount; không có giao dịch thì tổng bằng 0.<br>B3. Trả limitAmount trừ tổng chi. |
| Điều kiện kết thúc | Kết quả âm thể hiện đã vượt hạn mức; không ghi thêm dữ liệu. |

**Phương thức 5: isOverBudget()**

*Bảng 4.21. Đặc tả phương thức Budget.isOverBudget()*

| Mục | Nội dung |
|---|---|
| Tên | isOverBudget(transactions: List<Transaction>): Boolean |
| Mô tả | Kiểm tra tổng chi có vượt hạn mức hay không. |
| Tham số đầu vào | transactions: tập giao dịch dùng để tính mức sử dụng. |
| Kết quả đầu ra | true khi tổng chi > limitAmount; ngược lại false. |
| Điều kiện bắt đầu | Có đủ dữ liệu như calculateRemaining(). |
| Luồng xử lý | B1. Tính calculateRemaining(transactions).<br>B2. Trả true nếu kết quả < 0; các trường hợp còn lại trả false. |
| Điều kiện kết thúc | Chi bằng đúng hạn mức chưa được coi là vượt ngân sách; không thay đổi dữ liệu. |

### 4.3.5. Lớp SavingGoal

Lớp SavingGoal biểu diễn kế hoạch tiết kiệm, lưu số tiền cần đạt, thời hạn, trạng thái và thông tin hoàn thành. Số tiền đang dành cho mục tiêu được tính từ lịch sử nạp/rút.

**a) Thuộc tính**

*Bảng 4.22. Thuộc tính lớp SavingGoal*

| Tên | Kiểu dữ liệu | Ràng buộc | Ý nghĩa |
|---|---|---|---|
| id | String | PK; UUID sinh tự động | Mã mục tiêu. |
| userId | String | FK → User.id; bắt buộc | Người sở hữu mục tiêu. |
| name | String | Bắt buộc; không trống; tối đa 100 ký tự | Tên mục tiêu. |
| targetAmount | Decimal | Bắt buộc; > 0; độ chính xác (14,2) | Số tiền cần đạt. |
| deadline | Date? | Có thể rỗng | Thời hạn dự kiến. |
| status | GoalStatus | active hoặc completed; mặc định active | Trạng thái mục tiêu. |
| completionAmount | Decimal? | Có thể rỗng; được xác lập khi hoàn thành | Số tiền tại thời điểm hoàn thành. |
| completionMode | String? | keep, release hoặc spend; rỗng khi chưa hoàn thành | Cách xử lý tiền lúc hoàn thành. |

**b) Các phương thức**

**Phương thức 1: create()**

*Bảng 4.23. Đặc tả phương thức SavingGoal.create()*

| Mục | Nội dung |
|---|---|
| Tên | create(userId: String, name: String, targetAmount: Decimal, deadline: Date?): SavingGoal |
| Mô tả | Tạo kế hoạch tiết kiệm mới. |
| Tham số đầu vào | userId: người sở hữu; name: tên mục tiêu; targetAmount: số tiền cần đạt; deadline: hạn dự kiến tùy chọn. |
| Kết quả đầu ra | Đối tượng SavingGoal mới. |
| Điều kiện bắt đầu | Người sử dụng tồn tại; tên không trống, tối đa 100 ký tự; targetAmount > 0. |
| Luồng xử lý | B1. Kiểm tra thông tin mục tiêu.<br>B2. Tạo UUID, gắn userId, đặt status = active; thông tin hoàn thành ban đầu rỗng.<br>B3. Phối hợp lưu mục tiêu; số tiền hiện tại ban đầu bằng 0. |
| Điều kiện kết thúc | Mục tiêu được tạo, chưa phát sinh lịch sử tiền. |

**Phương thức 2: update()**

*Bảng 4.24. Đặc tả phương thức SavingGoal.update()*

| Mục | Nội dung |
|---|---|
| Tên | update(name: String, targetAmount: Decimal, deadline: Date?): void |
| Mô tả | Chỉnh sửa thông tin của mục tiêu tiết kiệm. |
| Tham số đầu vào | name: tên; targetAmount: số tiền cần đạt; deadline: hạn dự kiến hoặc null để bỏ thời hạn. |
| Kết quả đầu ra | void. |
| Điều kiện bắt đầu | Mục tiêu tồn tại, đúng quyền; tên và số tiền mới hợp lệ. |
| Luồng xử lý | B1. Kiểm tra tên, targetAmount và thời hạn.<br>B2. Cập nhật name, targetAmount và deadline.<br>B3. Giữ nguyên lịch sử nạp/rút và phối hợp lưu thay đổi. |
| Điều kiện kết thúc | Thông tin kế hoạch được cập nhật; không tự tạo khoản nạp, rút hoặc chi. |

**Phương thức 3: delete()**

*Bảng 4.25. Đặc tả phương thức SavingGoal.delete()*

| Mục | Nội dung |
|---|---|
| Tên | delete(): void |
| Mô tả | Xóa mục tiêu chưa có lịch sử tiền. |
| Tham số đầu vào | Không có. |
| Kết quả đầu ra | void. |
| Điều kiện bắt đầu | Mục tiêu tồn tại và thuộc người sử dụng đang thao tác. |
| Luồng xử lý | B1. Kiểm tra các GoalTransaction của mục tiêu.<br>B2. Nếu đã có lịch sử nạp/rút, báo lỗi và dừng.<br>B3. Nếu không có, xóa các GoalItem thuộc mục tiêu và xóa mục tiêu trong cùng giao dịch dữ liệu. |
| Điều kiện kết thúc | Mục tiêu và hạng mục được xóa khi hợp lệ; nhật ký tài chính đã phát sinh được bảo toàn. |

**Phương thức 4: calculateCurrentAmount()**

*Bảng 4.26. Đặc tả phương thức SavingGoal.calculateCurrentAmount()*

| Mục | Nội dung |
|---|---|
| Tên | calculateCurrentAmount(transactions: List<GoalTransaction>): Decimal |
| Mô tả | Tính lượng tiền đang dành cho mục tiêu. |
| Tham số đầu vào | transactions: tập lịch sử nạp/rút được cung cấp. |
| Kết quả đầu ra | Tổng deposit trừ tổng withdraw của mục tiêu hiện tại. |
| Điều kiện bắt đầu | Lịch sử tiền được cung cấp đầy đủ. |
| Luồng xử lý | B1. Chọn các bản ghi có goalId bằng id của mục tiêu.<br>B2. Tính tổng amount của deposit và tổng amount của withdraw.<br>B3. Trả hiệu hai tổng; không có lịch sử thì trả 0. |
| Điều kiện kết thúc | Không tạo cột currentAmount riêng và không làm thay đổi số liệu thu/chi. |

**Phương thức 5: isTargetReached()**

*Bảng 4.27. Đặc tả phương thức SavingGoal.isTargetReached()*

| Mục | Nội dung |
|---|---|
| Tên | isTargetReached(transactions: List<GoalTransaction>): Boolean |
| Mô tả | Kiểm tra số tiền tiết kiệm hiện tại đã đạt mức cần thiết hay chưa. |
| Tham số đầu vào | transactions: lịch sử tiền dùng để tính tiến độ. |
| Kết quả đầu ra | true nếu số tiền hiện tại ≥ targetAmount; ngược lại false. |
| Điều kiện bắt đầu | Mục tiêu có targetAmount hợp lệ; lịch sử tiền đầy đủ. |
| Luồng xử lý | B1. Tính calculateCurrentAmount(transactions).<br>B2. So sánh kết quả với targetAmount và trả giá trị Boolean. |
| Điều kiện kết thúc | Chỉ trả kết quả kiểm tra; không đổi status, không ghi completionAmount hoặc completionMode và không tự xử lý tiền. |

### 4.3.6. Lớp GoalTransaction

Lớp GoalTransaction biểu diễn một lần nạp hoặc rút tiền của mục tiêu. Các bản ghi tạo thành nhật ký riêng để xác định số tiền đang dành cho mục tiêu.

**a) Thuộc tính**

*Bảng 4.28. Thuộc tính lớp GoalTransaction*

| Tên | Kiểu dữ liệu | Ràng buộc | Ý nghĩa |
|---|---|---|---|
| id | String | PK; UUID sinh tự động | Mã giao dịch mục tiêu. |
| goalId | String | FK → SavingGoal.id; bắt buộc | Mục tiêu liên quan. |
| amount | Decimal | Bắt buộc; > 0; độ chính xác (14,2) | Số tiền nạp hoặc rút, luôn lưu giá trị dương. |
| type | GoalTransactionType | deposit hoặc withdraw | Loại biến động tiền mục tiêu. |
| transactionDate | Date | Bắt buộc; không lớn hơn ngày hiện tại | Ngày nạp/rút do người sử dụng hoặc nghiệp vụ cung cấp; ánh xạ txn_date. |
| note | String? | Có thể rỗng | Ghi chú biến động. |

**b) Các phương thức**

**Phương thức 1: deposit()**

*Bảng 4.29. Đặc tả phương thức GoalTransaction.deposit()*

| Mục | Nội dung |
|---|---|
| Tên | deposit(goal: SavingGoal, amount: Decimal, transactionDate: Date, note: String?): GoalTransaction |
| Mô tả | Tạo bản ghi nạp tiền vào mục tiêu. |
| Tham số đầu vào | goal: mục tiêu; amount: số tiền; transactionDate: ngày ghi nhận; note: ghi chú tùy chọn. |
| Kết quả đầu ra | Đối tượng GoalTransaction có type = deposit. |
| Điều kiện bắt đầu | Mục tiêu tồn tại, đúng quyền và active; amount > 0, không vượt số dư khả dụng; ngày hợp lệ, không ở tương lai. |
| Luồng xử lý | B1. Kiểm tra trạng thái mục tiêu, số tiền, ngày và số dư khả dụng do tầng ứng dụng cung cấp.<br>B2. Tạo UUID, gắn goalId, amount, transactionDate, note và type = deposit.<br>B3. Phối hợp lưu nhật ký nạp tiền. |
| Điều kiện kết thúc | Tiền dành riêng cho mục tiêu tăng theo bản ghi mới; không tạo giao dịch chi. |

**Phương thức 2: withdraw()**

*Bảng 4.30. Đặc tả phương thức GoalTransaction.withdraw()*

| Mục | Nội dung |
|---|---|
| Tên | withdraw(goal: SavingGoal, amount: Decimal, transactionDate: Date, note: String?): GoalTransaction |
| Mô tả | Tạo bản ghi rút tiền khỏi mục tiêu. |
| Tham số đầu vào | goal: mục tiêu; amount: số tiền; transactionDate: ngày ghi nhận; note: ghi chú tùy chọn. |
| Kết quả đầu ra | Đối tượng GoalTransaction có type = withdraw. |
| Điều kiện bắt đầu | Mục tiêu tồn tại, đúng quyền; amount > 0, không vượt số tiền hiện tại; ngày hợp lệ, không ở tương lai. |
| Luồng xử lý | B1. Kiểm tra số tiền, ngày và số tiền đang dành riêng cho mục tiêu.<br>B2. Tạo UUID, gắn goalId và dữ liệu giao dịch; đặt type = withdraw.<br>B3. Phối hợp lưu nhật ký rút tiền. |
| Điều kiện kết thúc | Tiền dành riêng giảm tương ứng; thao tác rút không tạo khoản thu mới. |

### 4.3.7. Lớp GoalItem

Lớp GoalItem biểu diễn một hạng mục trong mục tiêu tiết kiệm, gồm tên, chi phí dự kiến và trạng thái đã mua.

**a) Thuộc tính**

*Bảng 4.31. Thuộc tính lớp GoalItem*

| Tên | Kiểu dữ liệu | Ràng buộc | Ý nghĩa |
|---|---|---|---|
| id | String | PK; UUID sinh tự động | Mã hạng mục. |
| goalId | String | FK → SavingGoal.id; bắt buộc | Mục tiêu chứa hạng mục. |
| name | String | Bắt buộc; không trống | Tên hạng mục. |
| cost | Decimal | Bắt buộc; > 0; độ chính xác (14,2) | Chi phí của hạng mục. |
| isPurchased | Boolean | Bắt buộc; mặc định false | Trạng thái đã mua. |

**b) Các phương thức**

**Phương thức 1: updateStatus()**

*Bảng 4.32. Đặc tả phương thức GoalItem.updateStatus()*

| Mục | Nội dung |
|---|---|
| Tên | updateStatus(isPurchased: Boolean): void |
| Mô tả | Cập nhật trạng thái đã mua của hạng mục. |
| Tham số đầu vào | isPurchased: true nếu đã mua, false nếu chưa mua. |
| Kết quả đầu ra | void. |
| Điều kiện bắt đầu | Hạng mục tồn tại, thuộc đúng mục tiêu và đúng quyền sở hữu. |
| Luồng xử lý | B1. Kiểm tra quan hệ với mục tiêu và quyền thao tác.<br>B2. Gán isPurchased mới và phối hợp lưu thay đổi. |
| Điều kiện kết thúc | Trạng thái được cập nhật; tên và chi phí giữ nguyên; không tự tạo khoản chi hoặc rút tiền. |

### 4.3.8. Lớp AIConversation

Lớp AIConversation biểu diễn cuộc hội thoại của người sử dụng với trợ lý AI, tổ chức các tin nhắn và lưu thời điểm hoạt động gần nhất.

**a) Thuộc tính**

*Bảng 4.33. Thuộc tính lớp AIConversation*

| Tên | Kiểu dữ liệu | Ràng buộc | Ý nghĩa |
|---|---|---|---|
| id | String | PK; UUID sinh tự động | Mã hội thoại. |
| userId | String | FK → User.id; bắt buộc | Người sở hữu hội thoại. |
| title | String | Bắt buộc; tối đa 160 ký tự; mặc định “Cuộc trò chuyện mới” | Tiêu đề hội thoại. |
| createdAt | DateTime | Bắt buộc; mặc định thời điểm tạo | Thời điểm khởi tạo. |
| updatedAt | DateTime | Bắt buộc; cập nhật khi hội thoại phát sinh nội dung mới | Thời điểm hoạt động gần nhất. |

**b) Các phương thức**

**Phương thức 1: create()**

*Bảng 4.34. Đặc tả phương thức AIConversation.create()*

| Mục | Nội dung |
|---|---|
| Tên | create(userId: String, title: String): AIConversation |
| Mô tả | Tạo hội thoại AI mới. |
| Tham số đầu vào | userId: người sở hữu; title: tiêu đề. |
| Kết quả đầu ra | Đối tượng AIConversation mới. |
| Điều kiện bắt đầu | Người sử dụng tồn tại, đúng quyền; tiêu đề không trống và không quá 160 ký tự. |
| Luồng xử lý | B1. Kiểm tra và chuẩn hóa tiêu đề.<br>B2. Tạo UUID, gắn userId, xác lập createdAt và updatedAt.<br>B3. Phối hợp lưu hội thoại rỗng. |
| Điều kiện kết thúc | Hội thoại được tạo; chưa có tin nhắn và chưa phát sinh lời gọi đến Gemini. |

**Phương thức 2: delete()**

*Bảng 4.35. Đặc tả phương thức AIConversation.delete()*

| Mục | Nội dung |
|---|---|
| Tên | delete(): void |
| Mô tả | Xóa hội thoại cùng các tin nhắn thuộc hội thoại. |
| Tham số đầu vào | Không có. |
| Kết quả đầu ra | void. |
| Điều kiện bắt đầu | Hội thoại tồn tại và thuộc người sử dụng đang thao tác. |
| Luồng xử lý | B1. Kiểm tra quyền sở hữu hội thoại.<br>B2. Xóa các AIMessage có conversationId tương ứng.<br>B3. Xóa hội thoại và lưu toàn bộ trong cùng giao dịch dữ liệu. |
| Điều kiện kết thúc | Hội thoại và tin nhắn được xóa nhất quán; dữ liệu tài chính và hội thoại khác giữ nguyên. |

### 4.3.9. Lớp AIMessage

Lớp AIMessage biểu diễn một tin nhắn trong hội thoại, gồm vai trò, nội dung, kỳ dữ liệu và số liệu hỗ trợ câu trả lời.

**a) Thuộc tính**

*Bảng 4.36. Thuộc tính lớp AIMessage*

| Tên | Kiểu dữ liệu | Ràng buộc | Ý nghĩa |
|---|---|---|---|
| id | String | PK; UUID sinh tự động | Mã tin nhắn. |
| conversationId | String | FK → AIConversation.id; bắt buộc | Hội thoại chứa tin nhắn. |
| role | MessageRole | user hoặc assistant | Vai trò bên tạo nội dung. |
| content | Text | Bắt buộc; nội dung không trống theo nghiệp vụ | Nội dung câu hỏi hoặc câu trả lời. |
| contextMonth | Integer? | Có thể rỗng; nếu có: 1–12 | Tháng dữ liệu được phân tích. |
| contextYear | Integer? | Có thể rỗng; nếu có: 2000–2100 | Năm dữ liệu được phân tích. |
| evidenceJson | Text? | Có thể rỗng; nếu có phải là JSON hợp lệ | Số liệu hỗ trợ được lưu dưới dạng JSON. |
| /evidence | Map? | Thuộc tính dẫn xuất, chỉ đọc; không có cột lưu riêng | Dữ liệu giải mã từ evidenceJson. |
| createdAt | DateTime | Bắt buộc; mặc định thời điểm tạo | Thời điểm phát sinh tin nhắn. |

**b) Các phương thức**

**Phương thức 1: toOutput()**

*Bảng 4.37. Đặc tả phương thức AIMessage.toOutput()*

| Mục | Nội dung |
|---|---|
| Tên | toOutput(): AIMessageOutput |
| Mô tả | Chuyển tin nhắn thành cấu trúc dữ liệu đầu ra phục vụ hiển thị. |
| Tham số đầu vào | Không có; sử dụng các thuộc tính của tin nhắn hiện tại. |
| Kết quả đầu ra | AIMessageOutput gồm id, role, content, contextMonth, contextYear, evidence và createdAt. |
| Điều kiện bắt đầu | Tin nhắn tồn tại, đúng quyền; evidenceJson nếu có phải là JSON hợp lệ và đúng cấu trúc thiết kế. |
| Luồng xử lý | B1. Đọc thông tin nhận diện, nội dung, vai trò, kỳ dữ liệu và thời điểm tạo.<br>B2. Nếu evidenceJson có giá trị, giải mã thành evidence; nếu rỗng, gán evidence = null.<br>B3. Tạo và trả AIMessageOutput; dữ liệu không hợp lệ được báo lỗi trước khi trả đầu ra. |
| Điều kiện kết thúc | Không sửa dữ liệu lưu trữ, không thay đổi giao dịch tài chính và không tự gọi dịch vụ AI. |
