"use client";

import { useState, useCallback } from "react";
import { useMutation } from "@tanstack/react-query";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { EditorPanel } from "@/components/workspace/editor-panel";
import { InputPanel } from "@/components/workspace/input-panel";
import { ConsolePanel } from "@/components/workspace/console-panel";
import { ProblemPanel } from "@/components/workspace/problem-panel";
import { AISidebar } from "@/components/workspace/ai-sidebar";
import { useWorkspaceStore } from "@/store/workspace-store";
import { workspaceService } from "@/services/workspace.service";
import { Play, Save } from "lucide-react";
import { Separator } from "@/components/ui/separator";

export default function WorkspacePage() {
  const {
    problem,
    language,
    codeByLanguage,
    customInput,
    setResult,
    markSaved,
    isDirty,
  } = useWorkspaceStore();

  const [showProblem, setShowProblem] = useState(true);

  const runMutation = useMutation({
    mutationFn: () =>
      workspaceService.run({
        language,
        code: codeByLanguage[language],
        custom_input: customInput,
      }),
    onSuccess: (data) => {
      setResult(data);
      if (data.status === "accepted") {
        toast.success("Code executed successfully");
      } else {
        toast.error(`Execution failed: ${data.status}`);
      }
    },
    onError: (error) => {
      toast.error("Failed to run code");
      console.error(error);
    },
  });

  const saveMutation = useMutation({
    mutationFn: () =>
      workspaceService.save({
        title: problem.title,
        language,
        code: codeByLanguage[language],
        custom_input: customInput,
      }),
    onSuccess: () => {
      markSaved();
      toast.success("Workspace saved");
    },
    onError: (error) => {
      toast.error("Failed to save workspace");
      console.error(error);
    },
  });

  const handleRun = useCallback(() => {
    if (!codeByLanguage[language].trim()) {
      toast.error("Please write some code");
      return;
    }
    runMutation.mutate();
  }, [codeByLanguage, language, runMutation]);

  const handleSave = useCallback(() => {
    saveMutation.mutate();
  }, [saveMutation]);

  return (
    <div className="flex min-h-[calc(100svh-4rem)] min-w-0 flex-col gap-4">
      <div className="flex min-w-0 flex-col gap-3 rounded-xl border border-border bg-card/90 p-3 shadow-sm sm:flex-row sm:items-center sm:justify-between">
        <div className="flex flex-wrap items-center gap-2">
          <Button
            size="sm"
            onClick={() => setShowProblem(!showProblem)}
            variant={showProblem ? "default" : "outline"}
          >
            {showProblem ? "Hide" : "Show"} Problem
          </Button>
          <Separator orientation="vertical" className="hidden h-6 sm:block" />
          {isDirty && (
            <span className="text-xs text-amber-600 dark:text-amber-500 font-medium">
              Unsaved changes
            </span>
          )}
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <Button
            size="sm"
            variant="outline"
            onClick={handleSave}
            disabled={saveMutation.isPending}
            className="gap-2"
          >
            <Save className="w-4 h-4" />
            {saveMutation.isPending ? "Saving..." : "Save"}
          </Button>
          <Button
            size="sm"
            onClick={handleRun}
            disabled={runMutation.isPending}
            className="gap-2"
          >
            <Play className="w-4 h-4" />
            {runMutation.isPending ? "Running..." : "Run"}
          </Button>
        </div>
      </div>

      <div className="grid flex-1 min-h-0 min-w-0 gap-4 xl:grid-cols-[minmax(0,1.05fr)_minmax(0,0.95fr)_minmax(0,0.9fr)]">
        <div className="flex min-h-0 min-w-0 flex-col gap-4">
          {showProblem && (
            <div className="min-h-[18rem] flex-1 overflow-hidden rounded-xl border border-border bg-card">
              <ProblemPanel />
            </div>
          )}
          <div className={showProblem ? "min-h-[24rem] flex-1 overflow-hidden rounded-xl border border-border bg-card" : "min-h-[42rem] overflow-hidden rounded-xl border border-border bg-card"}>
            <EditorPanel />
          </div>
        </div>

        <div className="flex min-h-0 min-w-0 flex-col gap-4">
          <div className="min-h-[14rem] flex-1 overflow-hidden rounded-xl border border-border bg-card">
            <InputPanel />
          </div>
          <div className="min-h-[14rem] flex-1 overflow-hidden rounded-xl border border-border bg-card">
            <ConsolePanel isLoading={runMutation.isPending} />
          </div>
        </div>

        <div className="min-h-[32rem] min-w-0 overflow-hidden rounded-xl border border-border bg-card">
          <AISidebar />
        </div>
      </div>
    </div>
  );
}
