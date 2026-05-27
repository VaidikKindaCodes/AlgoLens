import { apiRequest } from "@/lib/api-client";
import type { PaginatedResponse } from "@/types/api";
import type {
  DashboardSummary,
  HistoryFilters,
  HistoryItem,
} from "@/types/history";

export const historyService = {
  list(filters: HistoryFilters = {}) {
    return apiRequest<PaginatedResponse<HistoryItem>>({
      method: "GET",
      url: "/workspace/history",
      params: {
        search: filters.search || undefined,
        type: filters.type === "all" ? undefined : filters.type,
        page: filters.page ?? 1,
        page_size: filters.page_size ?? 10,
      },
    });
  },

  getDashboard() {
    return apiRequest<DashboardSummary>({
      method: "GET",
      url: "/workspace/summary",
    });
  },
};
