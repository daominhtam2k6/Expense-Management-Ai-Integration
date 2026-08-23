export type CategoryType = "income" | "expense";

export interface Category {
  id: string;
  name: string;
  type: CategoryType;
  color: string;
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
}

export interface BudgetPayload {
  category_id: string;
  month: number;
  year: number;
  limit_amount: number;
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
