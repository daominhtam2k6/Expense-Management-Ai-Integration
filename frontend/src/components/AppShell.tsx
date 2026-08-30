import {
  BarChart3,
  Bot,
  Grid2X2,
  LogOut,
  PiggyBank,
  ReceiptText,
  Tags,
  Target,
  WalletCards,
} from "lucide-react";
import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";

const navItems = [
  { to: "/dashboard", label: "Tổng quan", icon: Grid2X2 },
  { to: "/transactions", label: "Giao dịch", icon: ReceiptText },
  { to: "/categories", label: "Danh mục", icon: Tags },
  { to: "/budgets", label: "Ngân sách", icon: WalletCards },
  { to: "/goals", label: "Mục tiêu", icon: Target },
  { to: "/reports", label: "Báo cáo", icon: BarChart3, disabled: true },
  { to: "/assistant", label: "Trợ lý AI", icon: Bot, disabled: true },
];

export function AppShell() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const initial = user?.username.trim().charAt(0).toLocaleUpperCase("vi") || "?";

  const handleLogout = () => {
    sessionStorage.setItem("auth_notice", "Bạn đã đăng xuất an toàn.");
    logout();
    navigate("/login", { replace: true });
  };

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <span className="brand__mark"><PiggyBank size={22} /></span>
          <span>Sổ Chi Tiêu</span>
        </div>

        <nav className="primary-nav" aria-label="Điều hướng chính">
          {navItems.map(({ to, label, icon: Icon, disabled }) =>
            disabled ? (
              <span key={to} className="nav-item is-disabled" title="Sẽ có trong giai đoạn tiếp theo">
                <Icon size={21} />
                <span>{label}</span>
              </span>
            ) : (
              <NavLink key={to} to={to} className={({ isActive }) => `nav-item${isActive ? " is-active" : ""}`}>
                <Icon size={21} />
                <span>{label}</span>
              </NavLink>
            ),
          )}
        </nav>

        <div className="sidebar__account">
          <div className="account-card">
            <span className="avatar">{initial}</span>
            <span className="account-copy">
              <strong>{user?.username}</strong>
              <small>{user?.email}</small>
            </span>
          </div>
          <button type="button" className="logout-button" onClick={handleLogout}>
            <LogOut size={20} />
            <span>Đăng xuất</span>
          </button>
        </div>
        <button type="button" className="compact-logout" onClick={handleLogout} aria-label="Đăng xuất" title="Đăng xuất"><LogOut size={20} /></button>
      </aside>

      <main className="main-content">
        <Outlet />
      </main>
    </div>
  );
}
