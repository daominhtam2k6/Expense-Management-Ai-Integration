import { render, screen, within } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { AssistantMessage } from "./AssistantMessage";
import { assistantPreview } from "../lib/assistantPreview";

describe("Assistant answer presentation", () => {
  it("renders the supplied financial answer as semantic Markdown without changing amounts", () => {
    const content = "## So sánh chi tiêu\n\n**Tổng chi:** 100.000 VNĐ, giảm -80,9%.\n\n* **Di chuyển:** 100.000 VNĐ\n* **Mua sắm:** 0 VNĐ\n\n*Lưu ý: dữ liệu còn ít.*";
    render(<AssistantMessage content={content} />);
    expect(screen.getByRole("heading", { name: "So sánh chi tiêu" })).toBeInTheDocument();
    expect(screen.getByText("Tổng chi:").tagName).toBe("STRONG");
    expect(screen.getAllByRole("listitem")).toHaveLength(2);
    expect(screen.getByText("Lưu ý: dữ liệu còn ít.").tagName).toBe("EM");
    expect(screen.getByText(/100.000 VNĐ, giảm -80,9%/)).toBeInTheDocument();
  });

  it("keeps tables and code in named keyboard-scrollable regions", () => {
    render(<AssistantMessage content={'| Nhóm | Số tiền |\n| --- | ---: |\n| Ăn uống | 115.000 VNĐ |\n\n```text\n100000 + 115000\n```'} />);
    const region = screen.getByRole("region", { name: "Bảng trong câu trả lời AI" });
    expect(region).toHaveAttribute("tabindex", "0");
    expect(within(region).getByRole("cell", { name: "115.000 VNĐ" })).toBeInTheDocument();
    expect(screen.getByLabelText("Đoạn mã trong câu trả lời AI")).toHaveAttribute("tabindex", "0");
  });

  it("blocks executable HTML, unsafe URLs and remote images while keeping safe links readable", () => {
    const { container } = render(<AssistantMessage content={'<script>alert(1)</script>\n\n<img src="https://evil.test/pixel" onerror="alert(1)">\n\n[Nguy hiểm](javascript:alert%281%29)\n\n[An toàn](https://example.com/report)\n\n![Biểu đồ](https://evil.test/chart.png)'} />);
    expect(container.querySelector("script, img")).toBeNull();
    expect(screen.getByText("Nguy hiểm").closest("a")).toBeNull();
    expect(screen.getByRole("link", { name: "An toàn" })).toHaveAttribute("href", "https://example.com/report");
    expect(screen.getByRole("link", { name: "An toàn" })).toHaveAttribute("rel", "noopener noreferrer");
    expect(screen.getByText("Biểu đồ")).toBeInTheDocument();
  });
});

describe("Assistant history previews", () => {
  it("removes formatting while preserving Vietnamese, signed amounts and percentages", () => {
    expect(assistantPreview("**Kết luận:** Chi 100.000 VNĐ, giảm -80,9%.\n\n* **Ăn uống:** 115.000 VNĐ"))
      .toBe("Kết luận: Chi 100.000 VNĐ, giảm -80,9%. Ăn uống: 115.000 VNĐ");
    expect(assistantPreview("[Báo cáo](/reports) và `100 * 2`" )).toBe("Báo cáo và 100 * 2");
  });

  it("handles empty and truncated Markdown without throwing or showing HTML", () => {
    expect(assistantPreview("")).toBe("");
    expect(assistantPreview("**Kết luận:** Tháng 10...")).toBe("Kết luận: Tháng 10...");
    expect(assistantPreview("<script>bad()</script>\n\n**Số dư:** 0 VNĐ")).toBe("Số dư: 0 VNĐ");
  });
});
