from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

PROJECT_ROOT = Path(__file__).resolve().parents[2]


ROOT = (PROJECT_ROOT / ".tools/document-assets")
SRC = (PROJECT_ROOT / ".tools/document-assets/screenflow_source_screens/New folder")
OUT = (PROJECT_ROOT / ".tools/document-assets/screenflow_db_media/detailed")
W = 1800


def f(size, bold=False):
    return ImageFont.truetype(f"C:/Windows/Fonts/{'arialbd.ttf' if bold else 'arial.ttf'}", size)


def rr(d, box, radius=20, fill="white", outline="#cbd9e6", width=3):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def txt(d, xy, value, size, color="#17324f", bold=False, anchor="la"):
    d.text(xy, value, font=f(size, bold), fill=color, anchor=anchor)


def fit_text(d, value, max_width, size, bold=False):
    words, lines, line = value.split(), [], ""
    for word in words:
        candidate = f"{line} {word}".strip()
        if d.textbbox((0, 0), candidate, font=f(size, bold))[2] <= max_width:
            line = candidate
        else:
            lines.append(line); line = word
    if line: lines.append(line)
    return lines


def screenshot_card(canvas, draw, x, y, w, h, step, title, subtitle, filename, accent="#1570d8"):
    rr(draw, (x, y, x+w, y+h), 24, "#f8fbfe", accent, 3)
    draw.ellipse((x+20, y+18, x+78, y+76), fill=accent)
    txt(draw, (x+49, y+47), str(step), 26, "white", True, "mm")
    txt(draw, (x+94, y+24), title, 23, "#17324f", True)
    for i, line in enumerate(fit_text(draw, subtitle, w-120, 15)):
        txt(draw, (x+94, y+59+i*19), line, 15, "#66788d")
    image = Image.open(SRC / filename).convert("RGB")
    max_w, max_h = w-34, h-118
    scale = min(max_w/image.width, max_h/image.height)
    image = image.resize((int(image.width*scale), int(image.height*scale)), Image.Resampling.LANCZOS)
    ix, iy = x+(w-image.width)//2, y+h-18-image.height
    rr(draw, (ix-7, iy-7, ix+image.width+7, iy+image.height+7), 12, "#eaf1f6", "#b9cada", 2)
    canvas.paste(image, (ix, iy))
    return (x, y, x+w, y+h)


def arrow(d, points, color="#1769c2", label=None, label_xy=None):
    d.line(points, fill=color, width=6, joint="curve")
    x1, y1 = points[-2]; x2, y2 = points[-1]
    if abs(x2-x1) >= abs(y2-y1):
        s = 1 if x2 > x1 else -1
        head = [(x2,y2),(x2-s*20,y2-12),(x2-s*20,y2+12)]
    else:
        s = 1 if y2 > y1 else -1
        head = [(x2,y2),(x2-12,y2-s*20),(x2+12,y2-s*20)]
    d.polygon(head, fill=color)
    if label and label_xy:
        rr(d, (label_xy[0]-75,label_xy[1]-20,label_xy[0]+75,label_xy[1]+20), 18, "white", color, 2)
        txt(d, label_xy, label, 15, color, True, "mm")


def header(d, title, subtitle, height):
    txt(d, (60, 42), title, 34, "#123d4a", True)
    txt(d, (60, 88), subtitle, 18, "#687b8f")
    d.line((60, 122, W-60, 122), fill="#dce6ee", width=2)
    rr(d, (60,height-55,W-60,height-20), 12, "#f4f8fb", "#d6e2eb", 1)
    txt(d, (82,height-37), "Mũi tên xanh: luồng chính   •   Xanh lá: thành công   •   Đỏ: lỗi/quay lại", 14, "#5f7185", anchor="lm")


def save_auth():
    h=1350; im=Image.new("RGB",(W,h),"white"); d=ImageDraw.Draw(im)
    header(d,"LUỒNG XÁC THỰC NGƯỜI DÙNG","Đăng nhập, xử lý lỗi và các lối sang đăng ký/khôi phục mật khẩu",h)
    cw,ch,gap=390,445,36; xs=[60+i*(cw+gap) for i in range(4)]
    screenshot_card(im,d,xs[0],155,cw,ch,1,"Mở đăng nhập","Truy cập /login.","login.png")
    screenshot_card(im,d,xs[1],155,cw,ch,2,"Nhập thông tin","Điền tài khoản và mật khẩu.","login fill.png")
    screenshot_card(im,d,xs[2],155,cw,ch,3,"Xác thực","Nhấn Đăng nhập; backend kiểm tra.","login fill.png")
    screenshot_card(im,d,80,785,620,470,4,"Dashboard","Thông tin hợp lệ → /dashboard.","dashboard.png","#07966f")
    screenshot_card(im,d,1100,785,620,470,5,"Thông báo lỗi","Thông tin sai → hiển thị lỗi.","login error.png","#e52d45")
    for i in range(2): arrow(d,[(xs[i]+cw,378),(xs[i+1]-5,378)])
    diamond=[(1320,640),(1425,710),(1320,780),(1215,710)]
    d.polygon(diamond,fill="#fff8dc",outline="#efad27",width=4)
    txt(d,(1320,698),"Hợp lệ?",20,"#27425c",True,"mm")
    arrow(d,[(xs[2]+cw,378),(1700,378),(1700,640),(1425,640),(1425,675)])
    arrow(d,[(1215,710),(630,710),(630,785)],"#07966f","Có",(900,710))
    arrow(d,[(1425,710),(1450,710),(1450,785)],"#e52d45","Không",(1570,710))
    arrow(d,[(1410,1255),(1410,1290),(250,1290),(250,600)],"#e52d45","Thử lại",(850,1290))
    # Secondary routes from login.
    screenshot_card(im,d,60,625,330,145,"A","Đăng ký","Lối phụ: tạo tài khoản mới.","register.png","#7357d8")
    screenshot_card(im,d,410,625,330,145,"B","Quên mật khẩu","Lối phụ: gửi yêu cầu đặt lại.","reset password.png","#7357d8")
    im.save((PROJECT_ROOT / ".tools/document-assets/screenflow_db_media/detailed/01_Authentication_Flow.png"),dpi=(180,180))


def simple_flow(filename, title, subtitle, nodes, links, height=780):
    im=Image.new("RGB",(W,height),"white"); d=ImageDraw.Draw(im); header(d,title,subtitle,height)
    boxes=[]
    for node in nodes:
        boxes.append(screenshot_card(im,d,*node))
    for link in links:
        a,b,color,label=link
        ba,bb=boxes[a],boxes[b]
        start=(ba[2],(ba[1]+ba[3])//2); end=(bb[0]-5,(bb[1]+bb[3])//2)
        arrow(d,[start,end],color,label,((start[0]+end[0])//2,start[1]-27) if label else None)
    im.save(OUT/filename,dpi=(180,180))


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    save_auth()
    y,w,h=165,400,520
    simple_flow("02_Transactions_Flow.png","LUỒNG QUẢN LÝ GIAO DỊCH","Xem danh sách, lọc/tìm kiếm và tạo giao dịch",[
        (55,y,w,h,1,"Dashboard","Chọn Giao dịch.","dashboard.png"),(480,y,w,h,2,"Danh sách giao dịch","Xem và quản lý dữ liệu.","transactions.png"),(905,y,w,h,3,"Lọc giao dịch","Chọn loại, danh mục, thời gian.","Search transactions.png"),(1330,y,w,h,4,"Tạo giao dịch","Nhập dữ liệu và lưu.","Create transaction.png")],[(0,1,"#1769c2",None),(1,2,"#1769c2","Tìm kiếm"),(2,3,"#07966f","Thêm mới")])
    simple_flow("03_Categories_Flow.png","LUỒNG QUẢN LÝ DANH MỤC","Xem danh mục thu/chi và tạo danh mục mới",[
        (120,y,480,h,1,"Danh mục","Mở /categories.","Categories.png"),(660,y,480,h,2,"Thêm danh mục","Chọn loại, tên, icon và màu.","Create category.png"),(1200,y,480,h,3,"Lưu kết quả","Danh mục mới xuất hiện trong danh sách.","Categories.png")],[(0,1,"#1769c2","Thêm mới"),(1,2,"#07966f","Lưu")])
    simple_flow("04_Budgets_Flow.png","LUỒNG QUẢN LÝ NGÂN SÁCH","Theo dõi hạn mức và đặt ngân sách theo danh mục",[
        (120,y,480,h,1,"Ngân sách","Mở /budgets.","budgets.png"),(660,y,480,h,2,"Đặt ngân sách","Chọn danh mục và hạn mức.","create buget.png"),(1200,y,480,h,3,"Theo dõi sử dụng","Cập nhật tiến độ chi tiêu theo kỳ.","budgets.png")],[(0,1,"#1769c2","Đặt ngân sách"),(1,2,"#07966f","Lưu")])
    simple_flow("05_Goals_Flow.png","LUỒNG QUẢN LÝ MỤC TIÊU TIẾT KIỆM","Tạo mục tiêu, xem chi tiết và nạp tiền",[
        (55,y,w,h,1,"Danh sách mục tiêu","Mở /goals.","Goal saving.png"),(480,y,w,h,2,"Tạo mục tiêu","Nhập tên và số tiền đích.","Create goal saving.png"),(905,y,w,h,3,"Chi tiết mục tiêu","Quản lý hạng mục và lịch sử.","Details goal saving.png"),(1330,y,w,h,4,"Nạp tiền","Nhập số tiền và xác nhận.","send money to goal saving.png")],[(0,1,"#1769c2","Tạo mới"),(1,2,"#07966f","Lưu"),(2,3,"#1769c2","Nạp tiền")])
    simple_flow("06_Reports_Flow.png","LUỒNG BÁO CÁO VÀ ĐỐI CHIẾU","So sánh kỳ và mở giao dịch làm bằng chứng",[
        (190,y,600,h,1,"Báo cáo","Chọn kỳ, xem so sánh và phân bổ.","Reports.png"),(1010,y,600,h,2,"Giao dịch đã lọc","Mở chi tiết dữ liệu từ báo cáo.","Search transactions.png")],[(0,1,"#1769c2","Xem chi tiết")])
    simple_flow("07_Assistant_Flow.png","LUỒNG TRỢ LÝ AI","Đặt câu hỏi và nhận câu trả lời có dữ liệu đối chiếu",[
        (190,y,600,h,1,"Trợ lý AI","Chọn hội thoại và nhập câu hỏi.","Ai chatbot.png"),(1010,y,600,h,2,"Câu trả lời AI","Hiển thị phân tích và evidence.","AI answer.png")],[(0,1,"#07966f","Gửi câu hỏi")])
    simple_flow("08_Profile_Flow.png","LUỒNG QUẢN LÝ HỒ SƠ","Mở SidePanel, cập nhật thông tin và lưu thay đổi",[
        (190,y,600,h,1,"Mở hồ sơ","Nhấn avatar trong AppShell.","dashboard.png"),(1010,y,600,h,2,"Cập nhật hồ sơ","Sửa thông tin hoặc ảnh đại diện.","Profile.png")],[(0,1,"#1769c2","Nhấn avatar")])
    print(OUT)


if __name__ == "__main__":
    main()
