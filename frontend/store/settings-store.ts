"use client";

import { create } from "zustand";
import { createJSONStorage, persist } from "zustand/middleware";

export type AiProvider = "openai" | "anthropic" | "gemini" | "huggingface";
export type EditorFontSize = 13 | 14 | 15 | 16 | 18;

interface SettingsState {
  provider: AiProvider;
  model: string;
  editorFontSize: EditorFontSize;
  wordWrap: boolean;
  minimap: boolean;
  setProvider: (provider: AiProvider) => void;
  setModel: (model: string) => void;
  setEditorFontSize: (size: EditorFontSize) => void;
  setWordWrap: (enabled: boolean) => void;
  setMinimap: (enabled: boolean) => void;
}

export const useSettingsStore = create<SettingsState>()(
  persist(
    (set) => ({
      provider: "openai",
      model: "default",
      editorFontSize: 14,
      wordWrap: false,
      minimap: true,
      setProvider: (provider) => set({ provider, model: "default" }),
      setModel: (model) => set({ model }),
      setEditorFontSize: (editorFontSize) => set({ editorFontSize }),
      setWordWrap: (wordWrap) => set({ wordWrap }),
      setMinimap: (minimap) => set({ minimap }),
    }),
    {
      name: "algolens-settings",
      storage: createJSONStorage(() => localStorage),
    },
  ),
);
