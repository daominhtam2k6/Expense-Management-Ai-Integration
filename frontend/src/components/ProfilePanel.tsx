import { Camera, ImagePlus, Trash2, UserRound } from "lucide-react";
import type { ChangeEvent, FormEvent } from "react";
import { useEffect, useMemo, useRef, useState } from "react";
import { useAuth } from "../auth/AuthContext";
import { SidePanel } from "./SidePanel";

interface ProfilePanelProps {
  open: boolean;
  onClose: () => void;
}

const AVATAR_MAX_BYTES = 2 * 1024 * 1024;
const AVATAR_TYPES = ["image/jpeg", "image/png", "image/webp"];

export function ProfilePanel({ open, onClose }: ProfilePanelProps) {
  const { user, updateProfile, uploadAvatar, deleteAvatar } = useAuth();
  const [displayName, setDisplayName] = useState("");
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [saving, setSaving] = useState(false);
  const [avatarBusy, setAvatarBusy] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (!open || !user) return;
    setDisplayName(user.display_name ?? "");
    setUsername(user.username);
    setEmail(user.email);
    setError("");
    setSuccess("");
  }, [open, user?.id]);

  const dirty = useMemo(() => Boolean(user) && (
    displayName.trim() !== (user?.display_name ?? "")
    || username.trim() !== user?.username
    || email.trim().toLocaleLowerCase("vi") !== user?.email.toLocaleLowerCase("vi")
  ), [displayName, email, user, username]);

  const saveProfile = async (event: FormEvent) => {
    event.preventDefault();
    if (!user || !dirty || saving) return;
    setSaving(true);
    setError("");
    setSuccess("");
    try {
      await updateProfile({
        display_name: displayName.trim() || null,
        username: username.trim(),
        email: email.trim(),
      });
      setSuccess("Thông tin cá nhân đã được cập nhật.");
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Chưa thể lưu thông tin cá nhân.");
    } finally {
      setSaving(false);
    }
  };

  const chooseAvatar = () => fileInputRef.current?.click();

  const changeAvatar = async (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    event.target.value = "";
    if (!file) return;
    setError("");
    setSuccess("");
    if (!AVATAR_TYPES.includes(file.type)) {
      setError("Ảnh đại diện phải là tệp PNG, JPEG hoặc WebP.");
      return;
    }
    if (file.size > AVATAR_MAX_BYTES) {
      setError("Ảnh đại diện không được vượt quá 2 MB.");
      return;
    }
    setAvatarBusy(true);
    try {
      await uploadAvatar(file);
      setSuccess("Ảnh đại diện đã được cập nhật.");
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Chưa thể tải ảnh đại diện.");
    } finally {
      setAvatarBusy(false);
    }
  };

  const removeAvatar = async () => {
    if (!user?.avatar_url || avatarBusy) return;
    setAvatarBusy(true);
    setError("");
    setSuccess("");
    try {
      await deleteAvatar();
      setSuccess("Ảnh đại diện đã được xóa.");
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Chưa thể xóa ảnh đại diện.");
    } finally {
      setAvatarBusy(false);
    }
  };

  const footer = (
    <>
      <button className="button button--secondary" type="button" onClick={onClose}>Đóng</button>
      <button
        className="button button--primary"
        type="submit"
        form="profile-form"
        disabled={!dirty || saving || avatarBusy}
      >
        {saving ? "Đang lưu…" : "Lưu thay đổi"}
      </button>
    </>
  );

  return (
    <SidePanel
      open={open}
      onClose={onClose}
      title="Thông tin cá nhân"
      description="Cập nhật cách tên và ảnh của bạn xuất hiện trong Sổ Chi Tiêu."
      footer={footer}
    >
      {user && (
        <form id="profile-form" className="form-stack profile-form" onSubmit={saveProfile}>
          <section className="profile-avatar-editor" aria-labelledby="profile-avatar-title">
            <ProfileAvatar
              avatarUrl={user.avatar_url}
              label={displayName.trim() || username.trim() || user.username}
              size="large"
            />
            <div>
              <strong id="profile-avatar-title">Ảnh đại diện</strong>
              <p>PNG, JPEG hoặc WebP · tối đa 2 MB</p>
              <div className="profile-avatar-actions">
                <button className="button button--secondary" type="button" onClick={chooseAvatar} disabled={avatarBusy}>
                  {user.avatar_url ? <Camera size={16} /> : <ImagePlus size={16} />}
                  {avatarBusy ? "Đang xử lý…" : user.avatar_url ? "Đổi ảnh" : "Tải ảnh lên"}
                </button>
                {user.avatar_url && (
                  <button className="profile-avatar-remove" type="button" onClick={removeAvatar} disabled={avatarBusy}>
                    <Trash2 size={16} /> Xóa ảnh
                  </button>
                )}
              </div>
              <input
                ref={fileInputRef}
                className="sr-only"
                type="file"
                accept="image/png,image/jpeg,image/webp"
                onChange={changeAvatar}
                tabIndex={-1}
              />
            </div>
          </section>

          <div className="profile-section-heading">
            <UserRound size={18} />
            <div><strong>Thông tin hiển thị</strong><small>Username và email vẫn được dùng để đăng nhập.</small></div>
          </div>

          <label className="field">
            <span>Tên hiển thị</span>
            <input
              data-panel-initial-focus
              value={displayName}
              onChange={(event) => { setDisplayName(event.target.value); setSuccess(""); }}
              maxLength={80}
              autoComplete="name"
              placeholder="Ví dụ: Minh Đỗ"
            />
            <small>Tên này xuất hiện trong khu vực tài khoản; có thể để trống.</small>
          </label>

          <label className="field">
            <span>Tên đăng nhập</span>
            <input
              value={username}
              onChange={(event) => { setUsername(event.target.value); setSuccess(""); }}
              minLength={3}
              maxLength={50}
              autoComplete="username"
              required
            />
            <small>Dùng tên này hoặc email để đăng nhập.</small>
          </label>

          <label className="field">
            <span>Email</span>
            <input
              type="email"
              value={email}
              onChange={(event) => { setEmail(event.target.value); setSuccess(""); }}
              maxLength={254}
              autoComplete="email"
              required
            />
            <small>Email mới sẽ được dùng cho lần đăng nhập và khôi phục mật khẩu tiếp theo.</small>
          </label>

          {error && <div className="profile-form-message profile-form-message--error" role="alert">{error}</div>}
          {success && <div className="profile-form-message profile-form-message--success" role="status">{success}</div>}
        </form>
      )}
    </SidePanel>
  );
}

export function ProfileAvatar({
  avatarUrl,
  label,
  size = "default",
}: {
  avatarUrl: string | null;
  label: string;
  size?: "default" | "compact" | "large";
}) {
  const [imageFailed, setImageFailed] = useState(false);
  useEffect(() => setImageFailed(false), [avatarUrl]);
  const initial = label.trim().charAt(0).toLocaleUpperCase("vi") || "?";

  return (
    <span className={`avatar profile-avatar profile-avatar--${size}`} aria-hidden="true">
      <span>{initial}</span>
      {avatarUrl && !imageFailed && <img src={avatarUrl} alt="" onError={() => setImageFailed(true)} />}
    </span>
  );
}
