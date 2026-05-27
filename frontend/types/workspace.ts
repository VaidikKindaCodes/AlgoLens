export type LanguageId = "cpp" | "python" | "java" | "javascript" | "go";

export interface LanguageOption {
  id: LanguageId;
  label: string;
  monacoId: string;
  extension: string;
}

export interface ProblemExample {
  input: string;
  output: string;
  explanation?: string;
}

export interface Problem {
  id?: string;
  title: string;
  statement: string;
  constraints: string[];
  examples: ProblemExample[];
  difficulty?: "Easy" | "Medium" | "Hard";
  source?: string;
}

export interface RunCodeRequest {
  language: LanguageId;
  code: string;
  input: string;
}

export interface ExecutionResult {
  status: "accepted" | "runtime_error" | "time_limit" | "compile_error";
  stdout: string;
  stderr?: string;
  runtime_ms?: number;
  memory_kb?: number;
}

export interface WorkspaceSaveRequest {
  problem: Problem;
  language: LanguageId;
  code: string;
  custom_input: string;
}

export interface WorkspaceRecord extends WorkspaceSaveRequest {
  id: string;
  updated_at: string;
}
