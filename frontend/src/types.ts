export type CategoryType = "income" | "expense";
export type CategoryIconKey =
  | "circle-dollar-sign"
  | "wallet"
  | "utensils"
  | "shopping-bag"
  | "house"
  | "car"
  | "bus"
  | "fuel"
  | "smartphone"
  | "receipt"
  | "heart-pulse"
  | "graduation-cap"
  | "gamepad-2"
  | "dog"
  | "baby"
  | "dumbbell"
  | "plane"
  | "gift"
  | "piggy-bank"
  | "banknote"
  | "briefcase-business"
  | "trending-up"
  | "hand-coins"
  | "badge-dollar-sign";

export interface User {
  id: string;
  username: string;
  email: string;
  avatar_url: string | null;
}

export interface AuthToken {
  access_token: string;
  token_type: string;
}

export interface RegisterPayload {
  username: string;
  email: string;
  password: string;
}

export interface MessageResponse {
  message: string;
}

export interface Category {
  id: string;
  name: string;
  type: CategoryType;
  color: string;
  icon: CategoryIconKey;
}

export interface Budget {
  id: string;
  category_id: string;
  month: number;
  year: number;
  limit_amount: number;
  spent: number;
  is_over: boolean;
}

export interface CategoryPayload {
  name: string;
  type: CategoryType;
  color: string;
  icon: CategoryIconKey;
}

export interface BudgetPayload {
  category_id: string;
  month: number;
  year: number;
  limit_amount: number;
}

export type GoalStatus = "active" | "completed";
export type GoalCompleteMode = "keep" | "release" | "spend";

export interface GoalItem {
  id: string;
  name: string;
  cost: number;
  is_purchased: boolean;
}

export interface Goal {
  id: string;
  name: string;
  target_amount: number;
  deadline: string | null;
  status: GoalStatus;
  current_amount: number;
  items: GoalItem[];
}

export interface GoalPayload {
  name: string;
  target_amount: number;
  deadline: string | null;
}

export interface GoalTransaction {
  id: string;
  amount: number;
  type: "deposit" | "withdraw";
  txn_date: string;
  note: string | null;
}

export interface GoalCompletePayload {
  mode: GoalCompleteMode;
  category_id?: string;
  note?: string | null;
}

export interface Transaction {
  id: string;
  category_id: string;
  amount: number;
  type: CategoryType;
  txn_date: string;
  note: string | null;
}

export interface TransactionPayload {
  category_id: string;
  amount: number;
  txn_date: string;
  note: string | null;
}

export interface TransactionFilters {
  category_id?: string;
  type?: CategoryType;
  from_date?: string;
  to_date?: string;
  keyword?: string;
}

export interface DashboardSummary {
  income: number;
  expense: number;
  net: number;
  available_balance: number;
}

export interface DashboardCategorySpending {
  category_id: string;
  category_name: string;
  color: string;
  icon: CategoryIconKey;
  amount: number;
  percentage: number;
}

export interface DashboardTrendPoint {
  month: number;
  year: number;
  income: number;
  expense: number;
}

export interface DashboardBudget {
  id: string;
  category_id: string;
  category_name: string;
  color: string;
  icon: CategoryIconKey;
  limit_amount: number;
  spent: number;
  remaining: number;
  usage_percentage: number;
  is_over: boolean;
  status: "safe" | "warning" | "over";
}

export interface DashboardGoal {
  id: string;
  name: string;
  target_amount: number;
  current_amount: number;
  progress_percentage: number;
  deadline: string | null;
  status: string;
}

export interface DashboardRecentTransaction {
  id: string;
  category_id: string;
  category_name: string;
  category_color: string;
  category_icon: CategoryIconKey;
  amount: number;
  type: CategoryType;
  txn_date: string;
  note: string | null;
}

export interface DashboardData {
  month: number;
  year: number;
  summary: DashboardSummary;
  spending_by_category: DashboardCategorySpending[];
  trend: DashboardTrendPoint[];
  budgets: DashboardBudget[];
  goals: DashboardGoal[];
  recent_transactions: DashboardRecentTransaction[];
}
