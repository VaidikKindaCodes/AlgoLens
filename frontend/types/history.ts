import type { AiActionType } from "@/types/ai";

export interface HistoryItem {
  id: string;
  type: AiActionType;
  title: string;
  summary?: string;
  language?: string;
  created_at: string;
}

export interface HistoryFilters {
  search?: string;
  type?: AiActionType | "all";
  page?: number;
  page_size?: number;
}

export interface DashboardSummary {
  problems_analyzed: number;
  ai_sessions: number;
  code_runs: number;
  saved_workspaces: number;
  recent_history: HistoryItem[];
}
