import hashlib
import secrets
from collections import defaultdict
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import (
    UserRegister,
    UserOut,
    Token,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    MessageResponse,
)
from app.core.security import hash_password, verify_password, create_access_token
from app.core.deps import get_current_user
from app.core.email import send_reset_password_email

router = APIRouter(prefix="/auth", tags=["auth"])

RESET_TOKEN_EXPIRE_MINUTES = 15

# Rate limit đơn giản trong bộ nhớ: tối đa 3 lần yêu cầu / email / giờ.
# Đủ dùng cho quy mô đồ án; nếu deploy thật lâu dài nên thay bằng Redis.
_reset_request_log: dict[str, list[datetime]] = defaultdict(list)
RESET_RATE_LIMIT_MAX = 3
RESET_RATE_LIMIT_WINDOW = timedelta(hours=1)


def _hash_token(raw_token: str) -> str:
    return hashlib.sha256(raw_token.encode()).hexdigest()


def _is_rate_limited(email: str) -> bool:
    now = datetime.now(timezone.utc)
    recent = [t for t in _reset_request_log[email] if now - t < RESET_RATE_LIMIT_WINDOW]
    _reset_request_log[email] = recent
    return len(recent) >= RESET_RATE_LIMIT_MAX

@router.post("/register", response_model=UserOut)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    username = payload.username.strip()
    email = str(payload.email).strip().lower()
    if len(username) < 3:
        raise HTTPException(status_code=400, detail="Tên đăng nhập phải có ít nhất 3 ký tự.")

    existing_username = db.query(User).filter(User.username == username).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Tên đăng nhập đã tồn tại.")

    existing_email = db.query(User).filter(func.lower(User.email) == email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email đã được sử dụng.")

    user = User(
        username=username,
        email=email,
        password_hash=hash_password(payload.password),
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail="Tên đăng nhập hoặc email đã được sử dụng.") from exc
    db.refresh(user)
    return user

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    identifier = form_data.username.strip()
    user = db.query(User).filter(User.username == identifier).first()
    if not user:
        user = db.query(User).filter(func.lower(User.email) == identifier.lower()).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tên đăng nhập, email hoặc mật khẩu không đúng.",
        )
    token = create_access_token({"sub": user.id})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/forgot-password", response_model=MessageResponse)
def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    email = str(payload.email).strip().lower()
    generic_response = MessageResponse(
        message="Nếu email tồn tại trong hệ thống, một liên kết đặt lại mật khẩu đã được gửi."
    )

    if _is_rate_limited(email):
        # Vẫn trả về thông báo chung, chỉ không gửi email nữa
        return generic_response

    user = db.query(User).filter(func.lower(User.email) == email).first()
    if not user:
        # Không tiết lộ email có tồn tại hay không (chống user enumeration)
        return generic_response

    raw_token = secrets.token_urlsafe(32)
    user.reset_token_hash = _hash_token(raw_token)
    user.reset_token_expiry = datetime.now(timezone.utc) + timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES)
    db.commit()

    _reset_request_log[email].append(datetime.now(timezone.utc))
    send_reset_password_email(email, raw_token)

    return generic_response

@router.post("/reset-password", response_model=MessageResponse)
def reset_password(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    token_hash = _hash_token(payload.token)
    user = db.query(User).filter(User.reset_token_hash == token_hash).first()

    if not user or not user.reset_token_expiry:
        raise HTTPException(status_code=400, detail="Liên kết đặt lại mật khẩu không hợp lệ.")

    expiry = user.reset_token_expiry
    if expiry.tzinfo is None:
        expiry = expiry.replace(tzinfo=timezone.utc)

    if expiry < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Liên kết đặt lại mật khẩu đã hết hạn.")

    user.password_hash = hash_password(payload.new_password)

    # Vô hiệu hóa token ngay sau khi dùng — đảm bảo chỉ dùng được một lần
    user.reset_token_hash = None
    user.reset_token_expiry = None
    db.commit()

    return MessageResponse(message="Đặt lại mật khẩu thành công. Vui lòng đăng nhập lại.")
