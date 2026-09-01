import os
import requests
from dotenv import load_dotenv


load_dotenv()

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
RENDER_EXTERNAL_HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME", "").strip()
FRONTEND_URL = os.getenv("FRONTEND_URL") or (
    f"https://{RENDER_EXTERNAL_HOSTNAME}"
    if RENDER_EXTERNAL_HOSTNAME
    else "http://127.0.0.1:8000"
)
RESEND_FROM_EMAIL = os.getenv(
    "RESEND_FROM_EMAIL",
    "Expense Management AI <onboarding@resend.dev>",
).strip()
RESEND_API_URL = "https://api.resend.com/emails"


def send_reset_password_email(to_email: str, reset_token: str) -> bool:
    """Gửi email chứa link đặt lại mật khẩu. Trả về True nếu gửi thành công."""
    reset_link = f"{FRONTEND_URL}/reset-password?token={reset_token}"

    payload = {
        "from": RESEND_FROM_EMAIL,
        "to": [to_email],
        "subject": "Yêu cầu đặt lại mật khẩu",
        "html": f"""
            <p>Bạn (hoặc ai đó) vừa yêu cầu đặt lại mật khẩu cho tài khoản này.</p>
            <p><a href="{reset_link}">Nhấn vào đây để đặt lại mật khẩu</a></p>
            <p>Link có hiệu lực trong 15 phút. Nếu không phải bạn yêu cầu, hãy bỏ qua email này.</p>
        """,
    }
    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(RESEND_API_URL, json=payload, headers=headers, timeout=10)
        return response.status_code == 200
    except requests.RequestException:
        return False
