import type { LanguageId, Problem } from "@/types/workspace";

export type AiActionType =
  | "analysis"
  | "hint"
  | "solution"
  | "review"
  | "test_cases";

export interface AiRequest {
  problem: Problem;
  language?: LanguageId;
  code?: string;
  hint_level?: number;
}

export interface AiResponse {
  id: string;
  type: AiActionType;
  content: string;
  created_at: string;
  model?: string;
}
