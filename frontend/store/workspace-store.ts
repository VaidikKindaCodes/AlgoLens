"use client";

import { create } from "zustand";
import { createJSONStorage, persist } from "zustand/middleware";
import { DEFAULT_CODE } from "@/lib/constants";
import type {
  ExecutionResult,
  LanguageId,
  Problem,
} from "@/types/workspace";

interface WorkspaceState {
  problem: Problem;
  language: LanguageId;
  codeByLanguage: Record<LanguageId, string>;
  customInput: string;
  result: ExecutionResult | null;
  isDirty: boolean;
  setProblem: (problem: Partial<Problem>) => void;
  setLanguage: (language: LanguageId) => void;
  setCode: (code: string) => void;
  setCustomInput: (input: string) => void;
  setResult: (result: ExecutionResult | null) => void;
  markSaved: () => void;
  reset: () => void;
}

const emptyProblem: Problem = {
  title: "",
  statement: "",
  constraints: [],
  examples: [],
};

export const useWorkspaceStore = create<WorkspaceState>()(
  persist(
    (set) => ({
      problem: emptyProblem,
      language: "cpp",
      codeByLanguage: DEFAULT_CODE,
      customInput: "",
      result: null,
      isDirty: false,
      setProblem: (problem) =>
        set((state) => ({
          problem: { ...state.problem, ...problem },
          isDirty: true,
        })),
      setLanguage: (language) => set({ language }),
      setCode: (code) =>
        set((state) => ({
          codeByLanguage: { ...state.codeByLanguage, [state.language]: code },
          isDirty: true,
        })),
      setCustomInput: (customInput) => set({ customInput, isDirty: true }),
      setResult: (result) => set({ result }),
      markSaved: () => set({ isDirty: false }),
      reset: () =>
        set({
          problem: emptyProblem,
          language: "cpp",
          codeByLanguage: DEFAULT_CODE,
          customInput: "",
          result: null,
          isDirty: false,
        }),
    }),
    {
      name: "algolens-workspace",
      storage: createJSONStorage(() => localStorage),
      partialize: ({
        problem,
        language,
        codeByLanguage,
        customInput,
        isDirty,
      }) => ({ problem, language, codeByLanguage, customInput, isDirty }),
    },
  ),
);
