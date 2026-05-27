import { apiRequest } from "@/lib/api-client";
import type { AiRequest, AiResponse } from "@/types/ai";

export const problemService = {
  analyze(payload: AiRequest) {
    return apiRequest<AiResponse>({
      method: "POST",
      url: "/problems/analyze",
      data: payload,
      timeout: 60_000,
    });
  },

  generateHint(payload: AiRequest) {
    return apiRequest<AiResponse>({
      method: "POST",
      url: "/problems/hints",
      data: payload,
      timeout: 60_000,
    });
  },

  generateSolution(payload: AiRequest) {
    return apiRequest<AiResponse>({
      method: "POST",
      url: "/problems/solution",
      data: payload,
      timeout: 90_000,
    });
  },

  generateTestCases(payload: AiRequest) {
    return apiRequest<AiResponse>({
      method: "POST",
      url: "/problems/testcases",
      data: payload,
      timeout: 60_000,
    });
  },
};
