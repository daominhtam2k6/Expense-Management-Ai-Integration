import {
  BarChart3,
  Bot,
  Grid2X2,
  LogOut,
  MoreHorizontal,
  PiggyBank,
  ReceiptText,
  Tags,
  Target,
  WalletCards,
} from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { NavLink, Outlet, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";

const navItems = [
  { to: "/dashboard", label: "Tổng quan", icon: Grid2X2 },
  { to: "/transactions", label: "Giao dịch", icon: ReceiptText },
  { to: "/categories", label: "Danh mục", icon: Tags },
  { to: "/budgets", label: "Ngân sách", icon: WalletCards },
  { to: "/goals", label: "Mục tiêu", icon: Target },
  { to: "/reports", label: "Báo cáo", icon: BarChart3 },
  { to: "/assistant", label: "Trợ lý AI", icon: Bot },
];

export function AppShell() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const navRef = useRef<HTMLElement>(null);
  const [mobileMoreOpen, setMobileMoreOpen] = useState(false);
  const initial = user?.username.trim().charAt(0).toLocaleUpperCase("vi") || "?";

  useEffect(() => {
    navRef.current?.querySelector<HTMLElement>(".nav-item.is-active")?.scrollIntoView({
      block: "nearest",
      inline: "center",
    });
    setMobileMoreOpen(false);
  }, [location.pathname]);

  useEffect(() => {
    if (!mobileMoreOpen) return;
    const closeOnEscape = (event: globalThis.KeyboardEvent) => {
      if (event.key === "Escape") setMobileMoreOpen(false);
    };
    window.addEventListener("keydown", closeOnEscape);
    return () => window.removeEventListener("keydown", closeOnEscape);
  }, [mobileMoreOpen]);

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

        <nav ref={navRef} className="primary-nav" aria-label="Điều hướng chính">
          {navItems.map(({ to, label, icon: Icon }) => (
            <NavLink key={to} to={to} className={({ isActive }) => `nav-item${isActive ? " is-active" : ""}`}>
              <Icon size={21} />
              <span>{label}</span>
            </NavLink>
          ))}
          <button
            className={`nav-item mobile-more-button${mobileMoreOpen ? " is-active" : ""}`}
            type="button"
            onClick={() => setMobileMoreOpen((open) => !open)}
            aria-expanded={mobileMoreOpen}
            aria-controls="mobile-more-menu"
          >
            <MoreHorizontal size={21} />
            <span>Thêm</span>
          </button>
        </nav>

        {mobileMoreOpen && (
          <>
            <button className="mobile-more-scrim" type="button" onClick={() => setMobileMoreOpen(false)} aria-label="Đóng menu thêm" />
            <div id="mobile-more-menu" className="mobile-more-menu" role="menu" aria-label="Các trang khác">
              {navItems.slice(2, 5).map(({ to, label, icon: Icon }) => (
                <NavLink key={to} to={to} role="menuitem"><Icon size={19} /><span>{label}</span></NavLink>
              ))}
            </div>
          </>
        )}

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
