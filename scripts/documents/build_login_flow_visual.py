from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PROJECT_ROOT = Path(__file__).resolve().parents[2]


OUT = (PROJECT_ROOT / ".tools/document-assets/screenflow_db_media/LoginFlow_Visual.png")
W, H = 1800, 1420


def font(size: int, bold: bool = False):
    name = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype(f"C:/Windows/Fonts/{name}", size)


def rounded(draw, box, radius=22, fill="#ffffff", outline="#c9d8e8", width=3):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def text(draw, xy, value, size, color="#162b4d", bold=False, anchor="la"):
    draw.text(xy, value, font=font(size, bold), fill=color, anchor=anchor)


def wrapped(draw, box, value, size, color="#65758b", bold=False, spacing=5, align="left"):
    x1, y1, x2, _ = box
    words = value.split()
    lines, line = [], ""
    for word in words:
        candidate = f"{line} {word}".strip()
        if draw.textbbox((0, 0), candidate, font=font(size, bold))[2] <= x2 - x1:
            line = candidate
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    for i, ln in enumerate(lines):
        if align == "center":
            text(draw, ((x1 + x2) / 2, y1 + i * (size + spacing)), ln, size, color, bold, "ma")
        else:
            text(draw, (x1, y1 + i * (size + spacing)), ln, size, color, bold)


def arrow(draw, start, end, color="#1769c2", width=5):
    draw.line([start, end], fill=color, width=width)
    x, y = end
    if abs(end[0] - start[0]) >= abs(end[1] - start[1]):
        sign = 1 if end[0] > start[0] else -1
        pts = [(x, y), (x - sign * 18, y - 11), (x - sign * 18, y + 11)]
    else:
        sign = 1 if end[1] > start[1] else -1
        pts = [(x, y), (x - 11, y - sign * 18), (x + 11, y - sign * 18)]
    draw.polygon(pts, fill=color)


def poly_arrow(draw, points, color="#1769c2", width=5):
    draw.line(points, fill=color, width=width, joint="curve")
    arrow(draw, points[-2], points[-1], color, width)


def browser(draw, box, kind):
    x1, y1, x2, y2 = box
    rounded(draw, box, 16, "#eff4f7", "#b9cadb", 3)
    rounded(draw, (x1 + 12, y1 + 12, x2 - 12, y2 - 12), 12, "#ffffff", "#d9e3ec", 2)
    draw.rectangle((x1 + 13, y1 + 13, x2 - 13, y1 + 48), fill="#edf2f6")
    for i, c in enumerate(("#ef6b68", "#f2b94b", "#52bb75")):
        draw.ellipse((x1 + 26 + i * 18, y1 + 26, x1 + 34 + i * 18, y1 + 34), fill=c)
    rounded(draw, (x1 + 90, y1 + 21, x2 - 26, y1 + 41), 8, "#ffffff", "#dde6ee", 1)
    text(draw, (x1 + 102, y1 + 31), "sochitieu.app/login", 11, "#75869a", anchor="lm")
    cx = (x1 + x2) / 2
    if kind in ("login", "filled"):
        draw.ellipse((cx - 28, y1 + 70, cx + 28, y1 + 126), fill="#dcf6ee")
        text(draw, (cx, y1 + 98), "₫", 30, "#087e68", True, "mm")
        text(draw, (cx, y1 + 142), "SỔ CHI TIÊU", 22, "#123d3a", True, "ma")
        text(draw, (cx, y1 + 174), "Chào mừng bạn trở lại", 17, "#253b52", True, "ma")
        rounded(draw, (x1 + 42, y1 + 202, x2 - 42, y1 + 244), 8, "#ffffff", "#cad7e2", 2)
        rounded(draw, (x1 + 42, y1 + 254, x2 - 42, y1 + 296), 8, "#ffffff", "#cad7e2", 2)
        text(draw, (x1 + 55, y1 + 223), "minh@email.com" if kind == "filled" else "Tên đăng nhập hoặc email", 14, "#32465b" if kind == "filled" else "#8391a1", anchor="lm")
        text(draw, (x1 + 55, y1 + 275), "••••••••" if kind == "filled" else "Mật khẩu", 14, "#32465b" if kind == "filled" else "#8391a1", anchor="lm")
        rounded(draw, (x1 + 42, y1 + 314, x2 - 42, y1 + 360), 9, "#087e68", "#087e68", 1)
        text(draw, (cx, y1 + 337), "Đăng nhập", 15, "#ffffff", True, "mm")
        text(draw, (cx, y1 + 378), "Quên mật khẩu?", 13, "#087e68", True, "ma")
    elif kind == "checking":
        draw.ellipse((cx - 48, y1 + 95, cx + 48, y1 + 191), fill="#dcf6ee")
        text(draw, (cx, y1 + 143), "↻", 55, "#087e68", True, "mm")
        text(draw, (cx, y1 + 225), "Đang đăng nhập…", 21, "#19364d", True, "ma")
        text(draw, (cx, y1 + 262), "Vui lòng chờ trong giây lát", 14, "#718095", anchor="ma")
        rounded(draw, (x1 + 56, y1 + 298, x2 - 56, y1 + 312), 7, "#dbe5ec", "#dbe5ec", 1)
        rounded(draw, (x1 + 56, y1 + 298, x1 + 175, y1 + 312), 7, "#087e68", "#087e68", 1)
    elif kind == "error":
        draw.ellipse((cx - 44, y1 + 78, cx + 44, y1 + 166), fill="#ffe4e7")
        text(draw, (cx, y1 + 122), "!", 48, "#e52d45", True, "mm")
        text(draw, (cx, y1 + 208), "Đăng nhập thất bại", 21, "#d9233d", True, "ma")
        wrapped(draw, (x1 + 45, y1 + 242, x2 - 45, y2), "Tên đăng nhập hoặc mật khẩu không đúng. Vui lòng kiểm tra lại.", 15, align="center")
        rounded(draw, (x1 + 70, y1 + 320, x2 - 70, y1 + 368), 9, "#e52d45", "#e52d45", 1)
        text(draw, (cx, y1 + 344), "Thử lại", 15, "#ffffff", True, "mm")
    elif kind == "dashboard":
        draw.rectangle((x1 + 13, y1 + 49, x1 + 100, y2 - 13), fill="#073b43")
        text(draw, (x1 + 56, y1 + 75), "SỔ", 15, "#66e3bf", True, "ma")
        for i, label in enumerate(("Tổng quan", "Giao dịch", "Danh mục", "Ngân sách", "Mục tiêu", "Báo cáo", "Trợ lý AI")):
            yy = y1 + 112 + i * 34
            if i == 0:
                rounded(draw, (x1 + 23, yy - 12, x1 + 90, yy + 15), 6, "#087e68", "#087e68", 1)
            text(draw, (x1 + 31, yy), label, 10, "#ffffff", i == 0, "lm")
        text(draw, (x1 + 125, y1 + 82), "Tổng quan", 23, "#18354b", True)
        cards = [("Thu nhập", "12.500.000 ₫", "#e0f7ef"), ("Chi tiêu", "6.240.000 ₫", "#ffe8e8"), ("Còn lại", "6.260.000 ₫", "#e7f0ff")]
        for i, (lab, val, c) in enumerate(cards):
            bx = x1 + 125 + i * 142
            rounded(draw, (bx, y1 + 115, bx + 128, y1 + 180), 9, c, c, 1)
            text(draw, (bx + 10, y1 + 136), lab, 10, "#617389")
            text(draw, (bx + 10, y1 + 162), val, 13, "#17384d", True)
        rounded(draw, (x1 + 125, y1 + 200, x2 - 28, y2 - 30), 10, "#ffffff", "#d8e2e8", 2)
        text(draw, (x1 + 145, y1 + 228), "Xu hướng thu / chi", 14, "#17384d", True)
        for i, h in enumerate((42, 75, 58, 105, 82, 122, 96)):
            bx = x1 + 160 + i * 43
            draw.rectangle((bx, y2 - 57 - h, bx + 20, y2 - 57), fill="#087e68")


def card(draw, box, number, title_value, subtitle, kind, accent="#1670dc", tint="#f8fbff"):
    x1, y1, x2, y2 = box
    rounded(draw, box, 24, tint, accent, 3)
    draw.ellipse((x1 + 20, y1 + 20, x1 + 78, y1 + 78), fill=accent)
    text(draw, (x1 + 49, y1 + 49), str(number), 27, "#ffffff", True, "mm")
    text(draw, (x1 + 95, y1 + 31), title_value, 24, "#153153", True)
    wrapped(draw, (x1 + 95, y1 + 66, x2 - 18, y1 + 115), subtitle, 15)
    browser(draw, (x1 + 20, y1 + 125, x2 - 20, y2 - 22), kind)


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    im = Image.new("RGB", (W, H), "#ffffff")
    d = ImageDraw.Draw(im)
    text(d, (60, 46), "LUỒNG ĐĂNG NHẬP — HỆ THỐNG SỔ CHI TIÊU", 34, "#123d4a", True)
    text(d, (60, 94), "Minh họa theo giao diện và hành vi triển khai thực tế", 18, "#687b8f")
    top_y, card_w, gap = 145, 400, 34
    xs = [60 + i * (card_w + gap) for i in range(4)]
    cards = [
        (1, "Mở ứng dụng", "Người dùng truy cập hệ thống.", "login"),
        (2, "Màn hình đăng nhập", "Hệ thống hiển thị biểu mẫu xác thực.", "login"),
        (3, "Nhập thông tin", "Nhập tên đăng nhập/email và mật khẩu.", "filled"),
        (4, "Kiểm tra thông tin", "Backend xác thực tài khoản và mật khẩu.", "checking"),
    ]
    for x, (n, t, s, k) in zip(xs, cards):
        card(d, (x, top_y, x + card_w, top_y + 575), n, t, s, k)
    for i in range(3):
        arrow(d, (xs[i] + card_w, top_y + 330), (xs[i + 1] - 8, top_y + 330))

    diamond = [(900, 770), (1015, 855), (900, 940), (785, 855)]
    d.polygon(diamond, fill="#fff8dc", outline="#eead28", width=4)
    text(d, (900, 836), "Thông tin", 21, "#26415c", True, "mm")
    text(d, (900, 868), "hợp lệ?", 21, "#26415c", True, "mm")
    poly_arrow(d, [(1594, 720), (1594, 760), (1015, 760), (1015, 812)], "#1769c2")

    card(d, (100, 885, 760, 1310), 5, "Dashboard", "Đăng nhập thành công, hiển thị trang tổng quan.", "dashboard", "#07966f", "#f5fffb")
    card(d, (1120, 885, 1700, 1310), 6, "Thông báo lỗi", "Hiển thị lỗi khi thông tin không hợp lệ.", "error", "#eb2945", "#fff7f8")
    text(d, (690, 814), "Có", 21, "#07966f", True, "mm")
    poly_arrow(d, [(785, 855), (650, 855), (650, 885)], "#07966f")
    text(d, (1092, 814), "Không", 21, "#e52d45", True, "mm")
    poly_arrow(d, [(1015, 855), (1410, 855), (1410, 885)], "#e52d45")
    poly_arrow(d, [(1410, 1310), (1410, 1360), (280, 1360), (280, 720)], "#e52d45")
    rounded(d, (675, 1333, 1015, 1387), 22, "#ffe9ed", "#ffc1ca", 2)
    text(d, (845, 1360), "Quay lại màn hình đăng nhập", 17, "#c6293f", True, "mm")

    rounded(d, (60, 1392, 1740, 1414), 8, "#f5f8fb", "#d6e1ea", 1)
    text(d, (84, 1403), "CHÚ THÍCH", 13, "#203a57", True, "lm")
    d.line((260, 1403, 325, 1403), fill="#1769c2", width=5); arrow(d, (290, 1403), (325, 1403), "#1769c2", 5)
    text(d, (340, 1403), "Luồng xử lý", 12, "#5f7185", anchor="lm")
    d.line((520, 1403, 585, 1403), fill="#07966f", width=5); arrow(d, (550, 1403), (585, 1403), "#07966f", 5)
    text(d, (600, 1403), "Đăng nhập thành công", 12, "#5f7185", anchor="lm")
    d.line((850, 1403, 915, 1403), fill="#e52d45", width=5); arrow(d, (880, 1403), (915, 1403), "#e52d45", 5)
    text(d, (930, 1403), "Lỗi / quay lại", 12, "#5f7185", anchor="lm")
    im.save(OUT, quality=96, dpi=(180, 180))
    print(OUT)


if __name__ == "__main__":
    main()
