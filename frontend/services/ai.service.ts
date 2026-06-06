import { apiRequest } from "@/lib/api-client";
import type { AiRequest, AiResponse } from "@/types/ai";

export const aiService = {
  reviewCode(payload: AiRequest) {
    return apiRequest<AiResponse>({
      method: "POST",
      url: "/code/review",
      data: payload,
      timeout: 60_000,
    });
  },

  stressTest(payload: AiRequest) {
    return apiRequest<AiResponse>({
      method: "POST",
      url: "/code/stress-test",
      data: payload,
      timeout: 90_000,
    });
  },
};
