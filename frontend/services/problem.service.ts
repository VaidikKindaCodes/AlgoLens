import { apiRequest } from "@/lib/api-client";
import type {
  AiResponse,
  AnalyzeRequest,
  HintRequest,
  SolutionRequest,
  TestCasesRequest,
} from "@/types/ai";

export const problemService = {
  analyze(payload: AnalyzeRequest) {
    return apiRequest<AiResponse>({
      method: "POST",
      url: "/problems/analyze",
      data: payload,
      timeout: 60_000,
    });
  },

  generateHint(payload: HintRequest) {
    return apiRequest<AiResponse>({
      method: "POST",
      url: "/problems/hints",
      data: payload,
      timeout: 60_000,
    });
  },

  generateSolution(payload: SolutionRequest) {
    return apiRequest<AiResponse>({
      method: "POST",
      url: "/problems/solution",
      data: payload,
      timeout: 90_000,
    });
  },

  generateTestCases(payload: TestCasesRequest) {
    return apiRequest<AiResponse>({
      method: "POST",
      url: "/problems/testcases",
      data: payload,
      timeout: 60_000,
    });
  },
};