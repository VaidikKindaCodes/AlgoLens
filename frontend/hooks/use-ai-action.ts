"use client";

import { useMutation } from "@tanstack/react-query";
import { aiService } from "@/services/ai.service";
import { problemService } from "@/services/problem.service";
import type { AiActionType, AiRequest } from "@/types/ai";

const handlers: Record<AiActionType, (payload: AiRequest) => Promise<unknown>> = {
  analysis: problemService.analyze,
  hint: problemService.generateHint,
  solution: problemService.generateSolution,
  review: aiService.reviewCode,
  test_cases: problemService.generateTestCases,
};

export function useAiAction() {
  return useMutation({
    mutationFn: ({
      action,
      payload,
    }: {
      action: AiActionType;
      payload: AiRequest;
    }) => handlers[action](payload),
  });
}
