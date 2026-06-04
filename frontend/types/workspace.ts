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
  custom_input: string;
}

export interface ExecutionResult {
  id: number;
  language: string;
  code: string;
  custom_input: string;

  output: string;
  error: string;

  execution_time_ms: number | null;
  memory_usage_bytes: number | null;

  status: "accepted" | "error" | "runtime_error" | "compile_error" | "time_limit";

  created_at: string;
}

export interface WorkspaceSaveRequest {
  title : string;
  language: LanguageId;
  code: string;
  custom_input: string;
}

export interface WorkspaceRecord extends WorkspaceSaveRequest {
  id: string;
  updated_at: string;
}
