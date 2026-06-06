"use client";

import { useState, useCallback } from "react";
import { useMutation } from "@tanstack/react-query";
import { toast } from "sonner";
import { PageHeader } from "@/components/shared/page-header";
import { Card } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { useRouter } from "next/navigation";
import { problemService } from "@/services/problem.service";
import { useWorkspaceStore } from "@/store/workspace-store";
import { Zap } from "lucide-react";
import type { AiResponse } from "@/types/ai";
import type { Problem } from "@/types/workspace";

export default function AnalysePage() {
  const router = useRouter();
  const { setProblem, setLanguage } = useWorkspaceStore();

  const [problemText, setProblemText] = useState("");
  const [analysis, setAnalysis] = useState<AiResponse | null>(null);

  const analyzeMutation = useMutation({
    mutationFn: async (problem: Problem) => {
      return problemService.analyze({ problem });
    },
    onSuccess: (data) => {
      setAnalysis(data);
      toast.success("Problem analyzed successfully!");
    },
    onError: () => {
      toast.error("Failed to analyze problem. Please try again.");
    },
  });

  const handleAnalyze = useCallback(() => {
    if (!problemText.trim()) {
      toast.error("Please paste a problem statement");
      return;
    }

    const problem: Problem = {
      title: "Problem",
      statement: problemText,
      constraints: [],
      examples: [],
    };

    analyzeMutation.mutate(problem);
  }, [problemText, analyzeMutation]);

  const handleOpenInWorkspace = useCallback(() => {
    if (!problemText.trim() || !analysis) {
      toast.error("Please analyze a problem first");
      return;
    }

    const problem: Problem = {
      title: "Problem",
      statement: problemText,
      constraints: [],
      examples: [],
    };

    setProblem(problem);
    setLanguage("cpp");
    router.push("/workspace");
  }, [problemText, analysis, setProblem, setLanguage, router]);

  return (
    <div className="space-y-6">
      <PageHeader
        title="Problem Analysis"
        description="Paste a problem statement to get insights and recommendations."
      />

      <div className="grid gap-6 lg:grid-cols-2">
        <Card className="p-6">
          <h2 className="text-lg font-semibold mb-4">Problem Statement</h2>
          <div className="space-y-3">
            <Textarea
              value={problemText}
              onChange={(e) => setProblemText(e.target.value)}
              placeholder="Paste the complete problem statement here..."
              className="min-h-64 resize-none font-mono text-sm"
            />
            <div className="flex flex-col gap-2 sm:flex-row">
              <Button
                onClick={handleAnalyze}
                disabled={analyzeMutation.isPending || !problemText.trim()}
                className="gap-2 sm:flex-1"
              >
                <Zap className="w-4 h-4" />
                {analyzeMutation.isPending ? "Analyzing..." : "Analyze"}
              </Button>
              <Button
                variant="outline"
                onClick={() => setProblemText("")}
                disabled={analyzeMutation.isPending}
                className="sm:w-auto"
              >
                Clear
              </Button>
            </div>
          </div>
        </Card>

        <Card className="p-6">
          <h2 className="text-lg font-semibold mb-4">Analysis Results</h2>
          <div className="space-y-3">
            {analyzeMutation.isPending ? (
              <div className="space-y-2">
                <Skeleton className="h-4 w-full" />
                <Skeleton className="h-4 w-5/6" />
                <Skeleton className="h-4 w-4/6" />
                <Skeleton className="h-32 w-full" />
              </div>
            ) : analysis ? (
              <div className="space-y-3">
                <div className="flex items-center gap-2 mb-2">
                  <Badge>Analysis</Badge>
                  {analysis.model && (
                    <Badge variant="secondary" className="text-xs">
                      {analysis.model}
                    </Badge>
                  )}
                </div>
                <div className="max-h-64 overflow-y-auto rounded-lg bg-muted p-4">
                  <p className="text-sm whitespace-pre-wrap text-foreground">
                    {analysis.content}
                  </p>
                </div>
                <Button
                  onClick={handleOpenInWorkspace}
                  className="w-full"
                >
                  Start Coding in Workspace
                </Button>
              </div>
            ) : (
              <div className="text-center py-8 text-muted-foreground">
                <p>Analyze a problem to see insights here</p>
              </div>
            )}
          </div>
        </Card>
      </div>
    </div>
  );
}