import { apiRequest } from "@/lib/api-client";
import type { PaginatedResponse } from "@/types/api";
import type {
  ExecutionResult,
  RunCodeRequest,
  WorkspaceRecord,
  WorkspaceSaveRequest,
} from "@/types/workspace";

export const workspaceService = {
  run(payload: RunCodeRequest) {
    return apiRequest<ExecutionResult>({
      method: "POST",
      url: "/workspace/run",
      data: payload,
      timeout: 60_000,
    });
  },

  save(payload: WorkspaceSaveRequest) {
    return apiRequest<WorkspaceRecord>({
      method: "POST",
      url: "/workspace",
      data: payload,
    });
  },

  getHistory(page = 1, pageSize = 10) {
    return apiRequest<PaginatedResponse<WorkspaceRecord>>({
      method: "GET",
      url: "/workspace/history",
      params: { page, page_size: pageSize },
    });
  },
};
