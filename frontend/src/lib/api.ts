import type {
  Budget,
  BudgetPayload,
  Category,
  CategoryPayload,
  DashboardData,
  AuthToken,
  MessageResponse,
  RegisterPayload,
  User,
} from "../types";

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "/api";
export const TOKEN_KEY = "access_token";
export const AUTH_UNAUTHORIZED_EVENT = "auth:unauthorized";

export class ApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const token = localStorage.getItem(TOKEN_KEY);
  const response = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...init?.headers,
    },
  });

  if (!response.ok) {
    const body = await response.json().catch(() => null) as { detail?: unknown } | null;
    const validationMessage = Array.isArray(body?.detail)
      ? body.detail.find((item): item is { msg: string } => Boolean(item) && typeof item === "object" && "msg" in item && typeof item.msg === "string")?.msg
      : undefined;
    const message = typeof body?.detail === "string"
      ? body.detail
      : validationMessage
        ? validationMessage
        : response.status === 401
          ? "Phiên đăng nhập không hợp lệ hoặc đã hết hạn."
          : "Không thể kết nối với máy chủ. Vui lòng thử lại.";
    if (response.status === 401 && token && path !== "/auth/login") {
      window.dispatchEvent(new Event(AUTH_UNAUTHORIZED_EVENT));
    }
    throw new ApiError(message, response.status);
  }

  if (response.status === 204) return undefined as T;
  return response.json() as Promise<T>;
}

const asNumber = (value: number) => {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : 0;
};

const normalizeDashboard = (data: DashboardData): DashboardData => ({
  ...data,
  summary: {
    income: asNumber(data.summary.income),
    expense: asNumber(data.summary.expense),
    net: asNumber(data.summary.net),
    available_balance: asNumber(data.summary.available_balance),
  },
  spending_by_category: data.spending_by_category.map((item) => ({
    ...item,
    amount: asNumber(item.amount),
    percentage: asNumber(item.percentage),
  })),
  trend: data.trend.map((item) => ({
    ...item,
    income: asNumber(item.income),
    expense: asNumber(item.expense),
  })),
  budgets: data.budgets.map((item) => ({
    ...item,
    limit_amount: asNumber(item.limit_amount),
    spent: asNumber(item.spent),
    remaining: asNumber(item.remaining),
    usage_percentage: asNumber(item.usage_percentage),
  })),
  goals: data.goals.map((item) => ({
    ...item,
    target_amount: asNumber(item.target_amount),
    current_amount: asNumber(item.current_amount),
    progress_percentage: asNumber(item.progress_percentage),
  })),
  recent_transactions: data.recent_transactions.map((item) => ({
    ...item,
    amount: asNumber(item.amount),
  })),
});

export const api = {
  login: (identifier: string, password: string) => {
    const body = new URLSearchParams({ username: identifier, password });
    return request<AuthToken>("/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body,
    });
  },
  register: (payload: RegisterPayload) =>
    request<User>("/auth/register", { method: "POST", body: JSON.stringify(payload) }),
  getMe: (signal?: AbortSignal) => request<User>("/auth/me", { signal }),
  forgotPassword: (email: string) =>
    request<MessageResponse>("/auth/forgot-password", { method: "POST", body: JSON.stringify({ email }) }),
  resetPassword: (token: string, newPassword: string) =>
    request<MessageResponse>("/auth/reset-password", { method: "POST", body: JSON.stringify({ token, new_password: newPassword }) }),
  getDashboard: (month: number, year: number, signal?: AbortSignal) =>
    request<DashboardData>(`/dashboard/?month=${month}&year=${year}`, { signal }).then(normalizeDashboard),
  listCategories: (signal?: AbortSignal) => request<Category[]>("/categories/", { signal }),
  createCategory: (payload: CategoryPayload) =>
    request<Category>("/categories/", { method: "POST", body: JSON.stringify(payload) }),
  updateCategory: (id: string, payload: Partial<CategoryPayload>) =>
    request<Category>(`/categories/${id}`, { method: "PUT", body: JSON.stringify(payload) }),
  deleteCategory: (id: string) => request<{ message: string }>(`/categories/${id}`, { method: "DELETE" }),
  listBudgets: (month: number, year: number, signal?: AbortSignal) => request<Budget[]>(`/budgets/?month=${month}&year=${year}`, { signal }),
  createBudget: (payload: BudgetPayload) =>
    request<Budget>("/budgets/", { method: "POST", body: JSON.stringify(payload) }),
  updateBudget: (id: string, limitAmount: number) =>
    request<Budget>(`/budgets/${id}`, { method: "PUT", body: JSON.stringify({ limit_amount: limitAmount }) }),
  deleteBudget: (id: string) => request<{ message: string }>(`/budgets/${id}`, { method: "DELETE" }),
};
