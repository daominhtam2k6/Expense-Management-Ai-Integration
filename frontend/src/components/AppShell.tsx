import {
  BarChart3,
  Bot,
  ChevronDown,
  Grid2X2,
  LogOut,
  PiggyBank,
  ReceiptText,
  Tags,
  Target,
  WalletCards,
} from "lucide-react";
import { NavLink, Outlet } from "react-router-dom";

const navItems = [
  { to: "/dashboard", label: "Tổng quan", icon: Grid2X2 },
  { to: "/transactions", label: "Giao dịch", icon: ReceiptText, disabled: true },
  { to: "/categories", label: "Danh mục", icon: Tags },
  { to: "/budgets", label: "Ngân sách", icon: WalletCards },
  { to: "/goals", label: "Mục tiêu", icon: Target, disabled: true },
  { to: "/reports", label: "Báo cáo", icon: BarChart3, disabled: true },
  { to: "/assistant", label: "Trợ lý AI", icon: Bot, disabled: true },
];

export function AppShell() {
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
          <button type="button" className="account-card">
            <span className="avatar">A</span>
            <span className="account-copy">
              <strong>admin</strong>
              <small>admin@domain.com</small>
            </span>
            <ChevronDown size={16} />
          </button>
          <button type="button" className="logout-button">
            <LogOut size={20} />
            <span>Đăng xuất</span>
          </button>
        </div>
      </aside>

      <main className="main-content">
        <Outlet />
      </main>
    </div>
  );
}
