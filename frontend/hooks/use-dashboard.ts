"use client";

import { useQuery } from "@tanstack/react-query";
import { historyService } from "@/services/history.service";

export function useDashboardSummary() {
  return useQuery({
    queryKey: ["dashboard", "summary"],
    queryFn: historyService.getDashboard,
  });
}
