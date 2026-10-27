"""Build readable screen-flow diagrams from real browser captures."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

PROJECT_ROOT = Path(__file__).resolve().parents[2]

ROOT = (PROJECT_ROOT / ".tools/document-assets")
SRC = (PROJECT_ROOT / ".tools/document-assets/screenflows_v3/screens")
OUT = (PROJECT_ROOT / ".tools/document-assets/screenflows_v3/diagrams")
W, CARD_W, CARD_H = 1800, 760, 480
LEFT, RIGHT, TOP, ROW_GAP = 90, 950, 155, 75

FLOWS = [
    ("01_login", "LUỒNG ĐĂNG NHẬP", "Xác thực tài khoản và xử lý hai kết quả", [
        ("login_empty", "1", "Màn hình đăng nhập", "Nhập tài khoản hoặc chọn lối phụ"),
        ("login_filled", "2", "Nhập thông tin", "Điền tên đăng nhập/email và mật khẩu"),
        ("login_error", "3", "Thông tin không hợp lệ", "Hiển thị lỗi và cho phép thử lại"),
        ("dashboard", "4", "Đăng nhập thành công", "Chuyển đến Dashboard"),
    ], ["Nhập thông tin", "Sai → quay lại", "Đúng → Dashboard"]),
    ("02_register", "LUỒNG ĐĂNG KÝ", "Tạo tài khoản mới và quay về đăng nhập", [
        ("register_empty", "1", "Mở đăng ký", "Từ Đăng nhập chọn Tạo tài khoản"),
        ("register_error", "2", "Kiểm tra dữ liệu", "Thiếu hoặc không khớp → báo lỗi"),
        ("register_filled", "3", "Sửa thông tin", "Nhập đủ username, email và mật khẩu"),
        ("register_success", "4", "Tạo thành công", "Chuyển về Đăng nhập và báo thành công"),
    ], ["Nhấn Tạo tài khoản", "Sửa dữ liệu", "Hợp lệ"]),
    ("03_password_recovery", "LUỒNG KHÔI PHỤC MẬT KHẨU", "Yêu cầu liên kết, đặt mật khẩu và xử lý token", [
        ("forgot_form", "1", "Nhập email", "Mở Quên mật khẩu từ màn hình đăng nhập"),
        ("forgot_sent", "2", "Đã tiếp nhận yêu cầu", "Thông báo kiểm tra hộp thư"),
        ("reset_form", "3", "Đặt mật khẩu mới", "Mở liên kết có token và nhập mật khẩu"),
        ("reset_error", "4", "Token không hợp lệ", "Hiển thị lỗi và yêu cầu liên kết mới"),
        ("reset_success", "5", "Đặt lại thành công", "Quay về Đăng nhập với thông báo"),
    ], ["Gửi liên kết", "Mở liên kết", "Token sai", "Token đúng"]),
    ("04_dashboard", "LUỒNG DASHBOARD", "Điểm vào sau đăng nhập và điều hướng nghiệp vụ", [
        ("dashboard_empty", "1", "Dashboard chưa có dữ liệu", "Hiển thị trạng thái ban đầu"),
        ("dashboard", "2", "Dashboard có dữ liệu", "Tổng hợp thu, chi, ngân sách và mục tiêu"),
    ], ["Có giao dịch"]),
    ("05_transaction_create", "LUỒNG TẠO GIAO DỊCH", "Nhập, kiểm tra và lưu khoản thu/chi", [
        ("transactions", "1", "Mở Giao dịch", "Xem danh sách và biểu mẫu"),
        ("transaction_form", "2", "Biểu mẫu tạo", "Chọn loại, danh mục, ngày và ghi chú"),
        ("transaction_error", "3", "Dữ liệu chưa hợp lệ", "Hiển thị lỗi ngay trong biểu mẫu"),
        ("transaction_filled", "4", "Hoàn thiện dữ liệu", "Sửa các trường theo thông báo"),
        ("transaction_saved", "5", "Lưu thành công", "Giao dịch xuất hiện trong danh sách"),
    ], ["Thêm giao dịch", "Thiếu dữ liệu", "Sửa", "Lưu"]),
    ("06_transaction_filter", "LUỒNG TÌM KIẾM GIAO DỊCH", "Lọc danh sách và xử lý khi không có kết quả", [
        ("transactions", "1", "Danh sách giao dịch", "Mở khu vực tìm kiếm và bộ lọc"),
        ("transaction_filtered", "2", "Có kết quả", "Danh sách chỉ giữ bản ghi phù hợp"),
        ("transaction_no_results", "3", "Không có kết quả", "Hiển thị trạng thái rỗng"),
        ("transactions", "4", "Xóa bộ lọc", "Trở lại danh sách đầy đủ"),
    ], ["Nhập điều kiện", "Điều kiện khác", "Đặt lại"]),
    ("07_transaction_edit_delete", "LUỒNG SỬA VÀ XÓA GIAO DỊCH", "Cập nhật bản ghi hoặc xác nhận xóa", [
        ("transaction_edit", "1", "Mở chỉnh sửa", "Chọn giao dịch và Chỉnh sửa"),
        ("transaction_updated", "2", "Cập nhật thành công", "Danh sách phản ánh dữ liệu mới"),
        ("transaction_delete_menu", "3", "Chọn Xóa giao dịch", "Hệ thống yêu cầu xác nhận"),
        ("transaction_deleted", "4", "Xóa thành công", "Bản ghi được loại khỏi danh sách"),
    ], ["Lưu thay đổi", "Mở thao tác", "Xác nhận"]),
    ("08_category_create", "LUỒNG TẠO DANH MỤC", "Chọn loại, biểu tượng, màu và lưu", [
        ("categories", "1", "Danh sách danh mục", "Chọn Thêm danh mục"),
        ("category_form", "2", "Biểu mẫu tạo", "Nhập tên, loại, icon và màu"),
        ("category_error", "3", "Thiếu tên", "Hiển thị lỗi kiểm tra dữ liệu"),
        ("category_filled", "4", "Hoàn thiện dữ liệu", "Nhập tên và lựa chọn hợp lệ"),
        ("category_saved", "5", "Tạo thành công", "Danh mục mới xuất hiện"),
    ], ["Thêm danh mục", "Thiếu dữ liệu", "Sửa", "Tạo"]),
    ("09_category_edit_delete", "LUỒNG SỬA VÀ XÓA DANH MỤC", "Cập nhật danh mục và bảo vệ dữ liệu đang tham chiếu", [
        ("category_edit", "1", "Chỉnh sửa danh mục", "Loại danh mục được giữ cố định"),
        ("category_updated", "2", "Cập nhật thành công", "Tên và giao diện được cập nhật"),
        ("category_delete_menu", "3", "Chọn Xóa", "Yêu cầu xác nhận trước khi xóa"),
        ("category_delete_error", "4", "Không thể xóa", "Danh mục đang có giao dịch tham chiếu"),
        ("category_deleted", "5", "Xóa thành công", "Danh mục không được tham chiếu đã bị xóa"),
    ], ["Lưu", "Chọn thao tác", "Đang được dùng", "Không được dùng"]),
    ("10_budget_create", "LUỒNG ĐẶT NGÂN SÁCH", "Thiết lập hạn mức theo danh mục và kỳ", [
        ("budgets_empty", "1", "Mở Ngân sách", "Chọn Đặt ngân sách"),
        ("budget_form", "2", "Biểu mẫu ngân sách", "Chọn danh mục và nhập hạn mức"),
        ("budget_error", "3", "Dữ liệu chưa hợp lệ", "Hiển thị lỗi trong bảng thao tác"),
        ("budget_filled", "4", "Hoàn thiện hạn mức", "Nhập giá trị lớn hơn 0"),
        ("budget_saved", "5", "Lưu thành công", "Tiến độ ngân sách được hiển thị"),
    ], ["Đặt ngân sách", "Thiếu dữ liệu", "Sửa", "Lưu"]),
    ("11_budget_edit_delete", "LUỒNG SỬA VÀ XÓA NGÂN SÁCH", "Điều chỉnh hạn mức hoặc loại bỏ ngân sách", [
        ("budget_edit", "1", "Mở chỉnh sửa", "Danh mục và kỳ hiện tại được giữ"),
        ("budget_updated", "2", "Cập nhật hạn mức", "Tỷ lệ sử dụng được tính lại"),
        ("budget_delete", "3", "Chọn Xóa", "Yêu cầu xác nhận xóa hạn mức"),
        ("budget_deleted", "4", "Xóa thành công", "Danh mục trở về trạng thái chưa đặt"),
    ], ["Lưu thay đổi", "Mở lại", "Xác nhận"]),
    ("12_goal_create", "LUỒNG TẠO MỤC TIÊU", "Đặt tên, số tiền cần đạt và thời hạn", [
        ("goals", "1", "Danh sách mục tiêu", "Chọn Thêm mục tiêu"),
        ("goal_form", "2", "Biểu mẫu mục tiêu", "Nhập thông tin kế hoạch"),
        ("goal_error", "3", "Dữ liệu chưa hợp lệ", "Hiển thị lỗi trong biểu mẫu"),
        ("goal_filled", "4", "Hoàn thiện dữ liệu", "Nhập tên và số tiền hợp lệ"),
        ("goal_saved", "5", "Tạo thành công", "Mục tiêu mới xuất hiện"),
    ], ["Thêm mục tiêu", "Thiếu dữ liệu", "Sửa", "Tạo"]),
    ("13_goal_edit_delete", "LUỒNG SỬA VÀ XÓA MỤC TIÊU", "Điều chỉnh kế hoạch hoặc xóa mục tiêu chưa có lịch sử tiền", [
        ("goal_detail_empty", "1", "Chi tiết mục tiêu", "Mở mục tiêu cần thao tác"),
        ("goal_edit", "2", "Chỉnh sửa", "Thay đổi số tiền hoặc thời hạn"),
        ("goal_updated", "3", "Cập nhật thành công", "Danh sách phản ánh kế hoạch mới"),
        ("goal_deleted", "4", "Xóa thành công", "Mục tiêu chưa có lịch sử được loại bỏ"),
    ], ["Sửa", "Lưu", "Xóa và xác nhận"]),
    ("14_goal_items", "LUỒNG HẠNG MỤC CON", "Chia nhỏ kế hoạch, đánh dấu và xóa hạng mục", [
        ("goal_detail", "1", "Chi tiết mục tiêu", "Mở Kế hoạch chi tiết"),
        ("item_form", "2", "Nhập hạng mục", "Tên và chi phí dự kiến"),
        ("item_saved", "3", "Thêm thành công", "Hạng mục xuất hiện trong kế hoạch"),
        ("item_checked", "4", "Đánh dấu hoàn tất", "Cập nhật trạng thái đã mua"),
        ("item_deleted", "5", "Xóa hạng mục", "Hạng mục được loại khỏi kế hoạch"),
    ], ["Mở kế hoạch", "Thêm", "Đánh dấu", "Xóa"]),
    ("15_goal_deposit", "LUỒNG NẠP TIỀN MỤC TIÊU", "Kiểm tra số dư khả dụng trước khi dành tiền", [
        ("deposit_form", "1", "Mở Nạp tiền", "Nhập số tiền muốn dành riêng"),
        ("deposit_error", "2", "Vượt số dư", "Hiển thị lỗi và giữ biểu mẫu"),
        ("deposit_filled", "3", "Sửa số tiền", "Nhập giá trị trong giới hạn"),
        ("deposit_success", "4", "Nạp thành công", "Tiến độ và lịch sử được cập nhật"),
    ], ["Nạp", "Sửa", "Hợp lệ"]),
    ("16_goal_withdraw", "LUỒNG RÚT TIỀN MỤC TIÊU", "Không cho rút vượt số tiền đang có", [
        ("withdraw_form", "1", "Mở Rút tiền", "Nhập số tiền muốn giải phóng"),
        ("withdraw_error", "2", "Vượt số tiền hiện có", "Hiển thị lỗi và giữ biểu mẫu"),
        ("withdraw_success", "3", "Rút thành công", "Tiền trở lại số dư khả dụng"),
    ], ["Rút", "Sửa và xác nhận"]),
    ("17_goal_complete", "LUỒNG HOÀN THÀNH MỤC TIÊU", "Chọn cách xử lý khoản tiền đã dành", [
        ("goal_ready", "1", "Mục tiêu đạt 100%", "Mở hành động hoàn thành"),
        ("complete_keep", "2A", "Giữ nguyên tiền", "Đánh dấu hoàn thành và giữ tiền"),
        ("complete_spend", "2B", "Ghi nhận đã sử dụng", "Tạo giao dịch chi tương ứng"),
        ("complete_release", "2C", "Chuyển về số dư", "Giải phóng tiền về số dư khả dụng"),
        ("complete_success", "3", "Hoàn thành", "Mục tiêu chuyển sang tab Đã hoàn thành"),
    ], ["Chọn xử lý", "Hoặc", "Hoặc", "Xác nhận"]),
    ("18_reports", "LUỒNG BÁO CÁO", "So sánh kỳ và truy ngược giao dịch bằng chứng", [
        ("reports", "1", "Mở Báo cáo", "Chọn kỳ và xem biến động"),
        ("reports_to_transactions", "2", "Xem giao dịch", "Đi đến danh sách đã lọc theo danh mục"),
    ], ["Xem giao dịch"]),
    ("19_assistant", "LUỒNG TRỢ LÝ AI", "Gửi câu hỏi và nhận phân tích có dữ liệu đối chiếu", [
        ("assistant", "1", "Mở Trợ lý AI", "Chọn kỳ dữ liệu và cuộc trò chuyện"),
        ("assistant_question", "2", "Nhập câu hỏi", "Gửi câu hỏi về tài chính cá nhân"),
        ("assistant_answer", "3", "Nhận câu trả lời", "Hiển thị phân tích và evidence"),
    ], ["Nhập câu hỏi", "Gửi"]),
    ("20_profile", "LUỒNG HỒ SƠ VÀ ẢNH ĐẠI DIỆN", "Cập nhật thông tin, kiểm tra tệp và quản lý avatar", [
        ("profile", "1", "Mở hồ sơ", "Nhấn avatar trong AppShell"),
        ("profile_success", "2", "Lưu thông tin", "Hiển thị thông báo cập nhật thành công"),
        ("avatar_error", "3", "Tệp không hợp lệ", "Hiển thị lỗi định dạng ảnh"),
        ("avatar_success", "4", "Tải ảnh thành công", "Avatar mới được hiển thị"),
        ("avatar_deleted", "5", "Xóa ảnh", "Quay về avatar chữ cái"),
    ], ["Lưu", "Chọn tệp sai", "Chọn PNG/JPEG/WebP", "Xóa ảnh"]),
    ("21_logout", "LUỒNG ĐĂNG XUẤT", "Kết thúc phiên và quay về vùng công khai", [
        ("dashboard", "1", "Đang ở AppShell", "Người dùng đã xác thực"),
        ("logout", "2", "Đăng xuất", "Token bị xóa và chuyển về Đăng nhập"),
    ], ["Nhấn Đăng xuất"]),
]


def font(size, bold=False):
    return ImageFont.truetype(f"C:/Windows/Fonts/{'arialbd.ttf' if bold else 'arial.ttf'}", size)


def rr(d, box, radius=22, fill="#fff", outline="#bed2e6", width=3):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def text(d, xy, value, size, color="#17324f", bold=False, anchor="la"):
    d.text(xy, value, font=font(size, bold), fill=color, anchor=anchor)


def wrap(d, value, max_width, size, bold=False):
    lines, line = [], ""
    for word in value.split():
        candidate = f"{line} {word}".strip()
        if d.textbbox((0, 0), candidate, font=font(size, bold))[2] <= max_width:
            line = candidate
        else:
            lines.append(line); line = word
    if line: lines.append(line)
    return lines


def card(canvas, d, node, x, y):
    shot, step, title, subtitle = node
    accent = "#1570d8"
    rr(d, (x, y, x + CARD_W, y + CARD_H), 24, "#f8fbfe", accent, 3)
    d.ellipse((x + 22, y + 18, x + 82, y + 78), fill=accent)
    text(d, (x + 52, y + 48), step, 24 if len(step) == 1 else 19, "white", True, "mm")
    text(d, (x + 100, y + 22), title, 23, "#17324f", True)
    for i, line in enumerate(wrap(d, subtitle, CARD_W - 125, 15)):
        text(d, (x + 100, y + 57 + i * 19), line, 15, "#64768b")
    img = Image.open(SRC / f"{shot}.png").convert("RGB")
    max_w, max_h = CARD_W - 34, CARD_H - 118
    scale = min(max_w / img.width, max_h / img.height)
    img = img.resize((round(img.width * scale), round(img.height * scale)), Image.Resampling.LANCZOS)
    ix, iy = x + (CARD_W - img.width) // 2, y + CARD_H - 18 - img.height
    rr(d, (ix - 7, iy - 7, ix + img.width + 7, iy + img.height + 7), 12, "#eaf1f6", "#b9cada", 2)
    canvas.paste(img, (ix, iy))
    return (x, y, x + CARD_W, y + CARD_H)


def arrow(d, start, end, label):
    low = label.lower()
    color = "#e52d45" if any(k in low for k in ("sai", "thiếu", "lỗi", "không", "vượt")) else "#07966f" if any(k in low for k in ("đúng", "hợp lệ", "lưu", "tạo", "thành công", "xác nhận")) else "#1769c2"
    d.line((start, end), fill=color, width=6)
    x1, y1 = start; x2, y2 = end
    if abs(x2 - x1) >= abs(y2 - y1):
        s = 1 if x2 > x1 else -1; head = [(x2,y2),(x2-s*20,y2-12),(x2-s*20,y2+12)]
    else:
        s = 1 if y2 > y1 else -1; head = [(x2,y2),(x2-12,y2-s*20),(x2+12,y2-s*20)]
    d.polygon(head, fill=color)
    mx, my = (x1+x2)//2, (y1+y2)//2
    width = max(120, d.textbbox((0,0), label, font=font(14, True))[2] + 34)
    rr(d, (mx-width//2, my-20, mx+width//2, my+20), 18, "white", color, 2)
    text(d, (mx,my), label, 14, color, True, "mm")


def path_arrow(d, points, label, label_at=None, color="#1769c2"):
    d.line(points, fill=color, width=6, joint="curve")
    x1, y1 = points[-2]; x2, y2 = points[-1]
    if abs(x2-x1) >= abs(y2-y1):
        s=1 if x2>x1 else -1; head=[(x2,y2),(x2-s*20,y2-12),(x2-s*20,y2+12)]
    else:
        s=1 if y2>y1 else -1; head=[(x2,y2),(x2-12,y2-s*20),(x2+12,y2-s*20)]
    d.polygon(head,fill=color)
    mx,my=label_at or ((points[0][0]+points[-1][0])//2,(points[0][1]+points[-1][1])//2)
    width=max(120,d.textbbox((0,0),label,font=font(14,True))[2]+34)
    rr(d,(mx-width//2,my-20,mx+width//2,my+20),18,"white",color,2); text(d,(mx,my),label,14,color,True,"mm")


def build_login():
    flow=FLOWS[0]; height=1355
    canvas=Image.new("RGB",(W,height),"white"); d=ImageDraw.Draw(canvas)
    text(d,(60,40),flow[1],34,"#123d4a",True); text(d,(60,88),flow[2],18,"#687b8f"); d.line((60,125,W-60,125),fill="#dce6ee",width=2)
    boxes=[card(canvas,d,flow[3][0],LEFT,TOP),card(canvas,d,flow[3][1],RIGHT,TOP),card(canvas,d,flow[3][3],LEFT,710),card(canvas,d,flow[3][2],RIGHT,710)]
    arrow(d,(850,395),(945,395),"Nhập thông tin")
    path_arrow(d,[(1330,635),(1330,680),(1330,705)],"Sai",(1395,670),"#e52d45")
    path_arrow(d,[(1250,635),(1250,670),(470,670),(470,705)],"Đúng → Dashboard",(850,670),"#07966f")
    path_arrow(d,[(1710,950),(1750,950),(1750,395),(1715,395)],"Thử lại",(1750,670),"#e52d45")
    rr(d,(120,650,405,692),18,"#f4efff","#7357d8",2); text(d,(262,671),"Tạo tài khoản → Luồng 02",14,"#6546c7",True,"mm")
    rr(d,(535,650,850,692),18,"#f4efff","#7357d8",2); text(d,(692,671),"Quên mật khẩu → Luồng 03",14,"#6546c7",True,"mm")
    rr(d,(60,height-58,W-60,height-20),12,"#f4f8fb","#d6e2eb",1); text(d,(82,height-39),"Xanh dương: điều hướng  •  Xanh lá: thành công  •  Đỏ: lỗi/quay lại",14,"#5f7185",anchor="lm")
    canvas.save((PROJECT_ROOT / ".tools/document-assets/screenflows_v3/diagrams/01_login.png"),dpi=(180,180))


def build_complete():
    flow=FLOWS[16]; height=1900
    canvas=Image.new("RGB",(W,height),"white"); d=ImageDraw.Draw(canvas)
    text(d,(60,40),flow[1],34,"#123d4a",True); text(d,(60,88),flow[2],18,"#687b8f"); d.line((60,125,W-60,125),fill="#dce6ee",width=2)
    ready=card(canvas,d,flow[3][0],520,TOP)
    keep=card(canvas,d,flow[3][1],LEFT,710); spend=card(canvas,d,flow[3][2],RIGHT,710); release=card(canvas,d,flow[3][3],LEFT,1265); done=card(canvas,d,flow[3][4],RIGHT,1265)
    path_arrow(d,[(900,635),(900,675),(470,675),(470,705)],"Giữ nguyên",(680,675),"#1769c2")
    path_arrow(d,[(900,635),(900,675),(1330,675),(1330,705)],"Ghi nhận chi",(1120,675),"#1769c2")
    path_arrow(d,[(900,635),(900,1225),(470,1225),(470,1260)],"Chuyển về số dư",(680,1225),"#1769c2")
    d.line([(850,950),(900,950),(900,1510)],fill="#07966f",width=6)
    d.line([(950,950),(900,950)],fill="#07966f",width=6)
    d.line([(850,1510),(945,1510)],fill="#07966f",width=6)
    d.polygon([(945,1510),(925,1498),(925,1522)],fill="#07966f")
    rr(d,(835,1230,965,1270),18,"white","#07966f",2); text(d,(900,1250),"Xác nhận",14,"#07966f",True,"mm")
    rr(d,(60,height-58,W-60,height-20),12,"#f4f8fb","#d6e2eb",1); text(d,(82,height-39),"Ba lựa chọn xử lý đều dẫn đến trạng thái Đã hoàn thành",14,"#5f7185",anchor="lm")
    canvas.save((PROJECT_ROOT / ".tools/document-assets/screenflows_v3/diagrams/17_goal_complete.png"),dpi=(180,180))


def build(flow):
    slug, title, subtitle, nodes, labels = flow
    rows = (len(nodes) + 1) // 2
    height = TOP + rows * CARD_H + (rows - 1) * ROW_GAP + 105
    canvas = Image.new("RGB", (W, height), "white"); d = ImageDraw.Draw(canvas)
    text(d, (60, 40), title, 34, "#123d4a", True)
    text(d, (60, 88), subtitle, 18, "#687b8f")
    d.line((60,125,W-60,125), fill="#dce6ee", width=2)
    boxes=[]
    for i,node in enumerate(nodes):
        row=i//2; even=row%2==0; col=i%2
        x=(LEFT if col==0 else RIGHT) if even else (RIGHT if col==0 else LEFT)
        y=TOP+row*(CARD_H+ROW_GAP)
        boxes.append(card(canvas,d,node,x,y))
    for i,label in enumerate(labels):
        a,b=boxes[i],boxes[i+1]
        if a[1]==b[1]:
            start=(a[2],(a[1]+a[3])//2) if b[0]>a[0] else (a[0],(a[1]+a[3])//2)
            end=(b[0]-5,(b[1]+b[3])//2) if b[0]>a[0] else (b[2]+5,(b[1]+b[3])//2)
        else:
            start=((a[0]+a[2])//2,a[3]); end=((b[0]+b[2])//2,b[1]-5)
        arrow(d,start,end,label)
    rr(d,(60,height-58,W-60,height-20),12,"#f4f8fb","#d6e2eb",1)
    text(d,(82,height-39),"Xanh dương: điều hướng  •  Xanh lá: lưu/thành công  •  Đỏ: lỗi hoặc điều kiện không đạt",14,"#5f7185",anchor="lm")
    canvas.save(OUT/f"{slug}.png",dpi=(180,180))


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    for flow in FLOWS: build(flow)
    build_login()
    build_complete()
    print(f"{len(FLOWS)} diagrams -> {OUT}")


if __name__ == "__main__": main()
