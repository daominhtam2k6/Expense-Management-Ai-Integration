import { PiggyBank, ReceiptText, ShieldCheck, Target, WalletCards } from "lucide-react";
import { Outlet } from "react-router-dom";
import { ThemeToggle } from "../ThemeToggle";

const capabilities = [
  { icon: ReceiptText, title: "Ghi chép rõ ràng", copy: "Theo dõi các khoản thu và chi trong một nơi." },
  { icon: WalletCards, title: "Giữ đúng ngân sách", copy: "Biết danh mục nào cần chú ý trước khi vượt hạn mức." },
  { icon: Target, title: "Tiến gần mục tiêu", copy: "Theo dõi hành trình tiết kiệm bằng dữ liệu của chính bạn." },
];

export function AuthLayout() {
  return (
    <div className="auth-shell">
      <section className="auth-brand-panel" aria-label="Giới thiệu Sổ Chi Tiêu">
        <div className="auth-brand"><span className="brand__mark"><PiggyBank size={22} /></span><strong>Sổ Chi Tiêu</strong></div>
        <div className="auth-brand-copy">
          <h1>Tài chính rõ ràng bắt đầu từ những ghi chép nhỏ.</h1>
          <p>Một không gian riêng để bạn hiểu dòng tiền, chủ động ngân sách và bền bỉ với mục tiêu.</p>
        </div>
        <div className="auth-capability-list">
          {capabilities.map(({ icon: Icon, title, copy }) => (
            <div className="auth-capability" key={title}>
              <span><Icon size={19} /></span>
              <div><strong>{title}</strong><p>{copy}</p></div>
            </div>
          ))}
        </div>
        <p className="auth-privacy-note"><ShieldCheck size={17} /> Dữ liệu được tách biệt theo từng tài khoản.</p>
      </section>

      <main className="auth-workspace">
        <div className="auth-theme"><ThemeToggle /></div>
        <div className="auth-form-frame"><Outlet /></div>
      </main>
    </div>
  );
}
