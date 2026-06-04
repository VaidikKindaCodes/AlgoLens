import type { LanguageId, Problem } from "@/types/workspace";

export type AiActionType =
  | "analysis"
  | "hint"
  | "solution"
  | "review"
  | "test_cases"
  | "workspace"
  | "code_run";

export interface AiRequest {
  problem: Problem;
  language?: LanguageId;
  code?: string;
  hint_level?: number;
}
export interface AnalyzeRequest {
  problem_statement: string;
}

export interface HintRequest {
  problem_statement: string;
  level: number;
}

export interface SolutionRequest {
  problem_statement: string;
  language: LanguageId;
}

export interface ReviewRequest {
  problem_statement: string;
  code: string;
  language: LanguageId;
}
export interface TestCasesRequest {
  problem_statement: string;
  count: number;
}
export interface AiResponse {
  id: string;
  type: AiActionType;
  content: string;
  created_at: string;
  model?: string;
}
