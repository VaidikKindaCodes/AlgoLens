"use client";

import { keepPreviousData, useQuery } from "@tanstack/react-query";
import { historyService } from "@/services/history.service";
import type { HistoryFilters } from "@/types/history";

export function useHistory(filters: HistoryFilters) {
  return useQuery({
    queryKey: ["history", filters],
    queryFn: () => historyService.list(filters),
    placeholderData: keepPreviousData,
  });
}
