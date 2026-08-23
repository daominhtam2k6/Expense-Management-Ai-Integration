import { CircleDollarSign } from "lucide-react";
import type { Category } from "../types";

export function CategoryAvatar({ category, size = "md" }: { category: Category; size?: "sm" | "md" | "lg" }) {
  return (
    <span
      className={`category-avatar category-avatar--${size}`}
      style={{ "--category-color": category.color } as React.CSSProperties}
      aria-hidden="true"
    >
      <CircleDollarSign />
    </span>
  );
}
