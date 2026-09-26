import unittest
import hashlib
from datetime import datetime, timedelta, timezone
from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import patch

from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.security import decode_access_token, hash_password, verify_password
from app.core.normalization import canonicalize_identity, normalize_identity
from app.database import Base
from app.models.user import User
from app.routers.auth import (
    change_password,
    delete_avatar,
    forgot_password,
    login,
    register,
    reset_password,
    update_profile,
    upload_avatar,
)
from app.schemas.user import (
    ChangePasswordRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    UserProfileUpdate,
    UserRegister,
)


class AuthApiTest(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        session = sessionmaker(bind=self.engine)
        self.db = session()
        self.user = User(
            id="user-1",
            username="minh",
            email="minh@example.com",
            password_hash=hash_password("secret123"),
        )
        self.db.add(self.user)
        self.db.commit()

    def tearDown(self):
        self.db.close()
        self.engine.dispose()

    def test_registration_requires_email(self):
        with self.assertRaises(ValidationError):
            UserRegister(username="new-user", password="secret123")

    def test_registration_rejects_duplicate_email_case_insensitively(self):
        payload = UserRegister(username="another", email="MINH@example.com", password="secret123")
        with self.assertRaises(HTTPException) as context:
            register(payload=payload, db=self.db)
        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(context.exception.detail, "Email đã được sử dụng.")

    def test_login_accepts_username(self):
        token = login(
            form_data=SimpleNamespace(username="minh", password="secret123"),
            db=self.db,
        )
        self.assertEqual(decode_access_token(token["access_token"])["sub"], self.user.id)

    def test_identity_normalization_uses_nfkc_trim_and_casefold(self):
        self.assertEqual(canonicalize_identity("  Ｍinh  "), "Minh")
        self.assertEqual(normalize_identity("  ＭINH  "), "minh")
        self.assertEqual(normalize_identity("Straße"), normalize_identity("STRASSE"))

    def test_login_accepts_username_case_insensitively(self):
        token = login(
            form_data=SimpleNamespace(username="  ＭINH  ", password="secret123"),
            db=self.db,
        )
        self.assertEqual(decode_access_token(token["access_token"])["sub"], self.user.id)

    def test_login_accepts_email_case_insensitively(self):
        token = login(
            form_data=SimpleNamespace(username="MINH@EXAMPLE.COM", password="secret123"),
            db=self.db,
        )
        self.assertEqual(decode_access_token(token["access_token"])["sub"], self.user.id)

    def test_registration_rejects_normalized_username_duplicate(self):
        payload = UserRegister(username="  ＭINH  ", email="fresh@example.com", password="secret123")
        with self.assertRaises(HTTPException) as context:
            register(payload=payload, db=self.db)
        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(context.exception.detail, "Tên đăng nhập đã tồn tại.")

    def test_profile_updates_display_name_username_and_email(self):
        result = update_profile(
            payload=UserProfileUpdate(
                display_name="  Minh Đỗ  ",
                username="minh-moi",
                email="MINH.MOI@example.com",
            ),
            db=self.db,
            current_user=self.user,
        )

        self.assertEqual(result.display_name, "Minh Đỗ")
        self.assertEqual(result.username, "minh-moi")
        self.assertEqual(result.email, "minh.moi@example.com")

    def test_profile_rejects_another_users_email(self):
        self.db.add(
            User(
                id="user-2",
                username="another",
                email="another@example.com",
                password_hash=hash_password("secret123"),
            )
        )
        self.db.commit()

        with self.assertRaises(HTTPException) as context:
            update_profile(
                payload=UserProfileUpdate(
                    display_name="Minh",
                    username="minh",
                    email="ANOTHER@example.com",
                ),
                db=self.db,
                current_user=self.user,
            )
        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(context.exception.detail, "Email đã được sử dụng.")

    def test_profile_rejects_normalized_username_collision(self):
        self.db.add(
            User(
                id="user-2",
                username="Other",
                email="other@example.com",
                password_hash=hash_password("secret123"),
            )
        )
        self.db.commit()

        with self.assertRaises(HTTPException) as context:
            update_profile(
                payload=UserProfileUpdate(
                    display_name="Minh",
                    username="  ＯTHER  ",
                    email=self.user.email,
                ),
                db=self.db,
                current_user=self.user,
            )
        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(context.exception.detail, "Tên đăng nhập đã tồn tại.")

    def test_authenticated_user_can_change_password(self):
        result = change_password(
            payload=ChangePasswordRequest(
                current_password="secret123",
                new_password="new-secret",
            ),
            db=self.db,
            current_user=self.user,
        )

        self.assertEqual(result.message, "Đổi mật khẩu thành công.")
        self.assertTrue(verify_password("new-secret", self.user.password_hash))
        self.assertFalse(verify_password("secret123", self.user.password_hash))

    def test_change_password_rejects_wrong_current_password(self):
        original_hash = self.user.password_hash
        with self.assertRaises(HTTPException) as context:
            change_password(
                payload=ChangePasswordRequest(
                    current_password="wrong-password",
                    new_password="new-secret",
                ),
                db=self.db,
                current_user=self.user,
            )

        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(context.exception.detail, "Mật khẩu hiện tại không đúng.")
        self.assertEqual(self.user.password_hash, original_hash)

    def test_change_password_request_has_stable_vietnamese_validation(self):
        cases = (
            ({"current_password": "", "new_password": "new-secret"}, "Mật khẩu hiện tại không được để trống."),
            ({"current_password": "secret123", "new_password": "short"}, "Mật khẩu mới phải có ít nhất 6 ký tự."),
        )
        for payload, expected_message in cases:
            with self.subTest(payload=payload), self.assertRaises(ValidationError) as context:
                ChangePasswordRequest(**payload)
            self.assertIn(expected_message, str(context.exception))

    def test_avatar_upload_and_delete(self):
        with TemporaryDirectory() as directory, patch(
            "app.routers.auth.AVATAR_DIRECTORY", Path(directory)
        ):
            image = SimpleNamespace(
                content_type="image/png",
                file=BytesIO(b"\x89PNG\r\n\x1a\nprofile-image"),
            )
            result = upload_avatar(file=image, db=self.db, current_user=self.user)
            saved_file = Path(directory) / Path(result.avatar_url).name
            self.assertTrue(saved_file.is_file())

            result = delete_avatar(db=self.db, current_user=self.user)
            self.assertIsNone(result.avatar_url)
            self.assertFalse(saved_file.exists())

    def test_forgot_password_does_not_reveal_unknown_email(self):
        result = forgot_password(
            payload=ForgotPasswordRequest(email="unknown@example.com"),
            db=self.db,
        )
        self.assertIn("Nếu email tồn tại", result.message)

    def test_reset_token_is_single_use(self):
        raw_token = "single-use-token"
        self.user.reset_token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
        self.user.reset_token_expiry = datetime.now(timezone.utc) + timedelta(minutes=15)
        self.db.commit()

        result = reset_password(
            payload=ResetPasswordRequest(token=raw_token, new_password="new-secret"),
            db=self.db,
        )
        self.assertIn("thành công", result.message)
        self.assertTrue(verify_password("new-secret", self.user.password_hash))

        with self.assertRaises(HTTPException) as context:
            reset_password(
                payload=ResetPasswordRequest(token=raw_token, new_password="another-secret"),
                db=self.db,
            )
        self.assertEqual(context.exception.status_code, 400)


if __name__ == "__main__":
    unittest.main()
