"use client";

import { useCallback } from "react";
import Editor from "@monaco-editor/react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { LANGUAGES, DEFAULT_CODE } from "@/lib/constants";
import { useWorkspaceStore } from "@/store/workspace-store";
import type { LanguageId } from "@/types/workspace";

export function EditorPanel() {
  const { language, setLanguage, codeByLanguage, setCode } =
    useWorkspaceStore();

  const currentLanguage = LANGUAGES.find((l) => l.id === language);
  const currentCode = codeByLanguage[language];

  const handleLanguageChange = useCallback(
    (value: string) => {
      setLanguage(value as LanguageId);
    },
    [setLanguage],
  );

  const handleCodeChange = useCallback(
    (value: string | undefined) => {
      if (value !== undefined) {
        setCode(value);
      }
    },
    [setCode],
  );

  const handleReset = useCallback(() => {
    setCode(DEFAULT_CODE[language]);
  }, [language, setCode]);

  return (
    <div className="flex h-full min-w-0 flex-col gap-3">
      <Card className="min-w-0 p-3">
        <div className="flex items-center justify-between gap-2">
          <Select value={language} onValueChange={handleLanguageChange}>
            <SelectTrigger className="w-full sm:w-40">
              <SelectValue placeholder="Select language" />
            </SelectTrigger>
            <SelectContent>
              {LANGUAGES.map((lang) => (
                <SelectItem key={lang.id} value={lang.id}>
                  {lang.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>

          <Button
            variant="outline"
            size="sm"
            onClick={handleReset}
            className="text-xs"
          >
            Reset
          </Button>
        </div>
      </Card>

      <Card className="min-h-[24rem] min-w-0 flex-1 overflow-hidden">
        <Editor
          language={currentLanguage?.monacoId || "cpp"}
          value={currentCode}
          onChange={handleCodeChange}
          theme="vs-dark"
          options={{
            minimap: { enabled: true },
            fontSize: 14,
            wordWrap: "on",
            formatOnPaste: true,
            formatOnType: true,
            scrollBeyondLastLine: false,
            fontFamily: "Monaco, 'Courier New', monospace",
            automaticLayout: true,
          }}
          className="h-full w-full min-w-0"
        />
      </Card>
    </div>
  );
}
