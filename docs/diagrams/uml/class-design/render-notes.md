# Class Diagram thiết kế hướng đối tượng

- Trạng thái: **thiết kế bám sát hiện trạng**. Thuộc tính, khóa và quan hệ lấy từ Model/CSDL hiện tại; phương thức được tổ chức theo trách nhiệm thiết kế lớp và các thao tác Backend đã có.
- Nguồn: requirements đã duyệt, 9 thực thể nghiệp vụ, Model ORM và các thao tác được đặc tả trong ORD.
- Entity chứa trạng thái cùng hành vi tự nhiên; thao tác use case/CRUD liên đối tượng nằm ở lớp `«control»`. Sơ đồ không trình bày Schema để giữ mức tổng quan.
- Khóa được ghi trực tiếp bằng `{PK}` và `{FK}`; không đặt khối chú thích trong hình.
- Font ảnh: Arial 16; PNG/SVG render bằng PlantUML local; chèn Word ở chiều rộng tối đa 16 cm.
