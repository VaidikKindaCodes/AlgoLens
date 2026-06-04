"use client";

import { useState, useCallback } from "react";
import { useMutation } from "@tanstack/react-query";
import { toast } from "sonner";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  AnalysisCard,
  HintsCard,
  ReviewCard,
  SolutionCard,
} from "./ai-cards";
import { useWorkspaceStore } from "@/store/workspace-store";
import { problemService } from "@/services/problem.service";
import { aiService } from "@/services/ai.service";
import type { AiResponse } from "@/types/ai";

export function AISidebar() {
  const { problem, language, codeByLanguage } = useWorkspaceStore();

  const [analysis, setAnalysis] = useState<AiResponse | null>(null);
  const [hints, setHints] = useState<AiResponse | null>(null);
  const [hints1, setHints1] = useState<AiResponse | null>(null);
  const [hints2, setHints2] = useState<AiResponse | null>(null);
  const [review, setReview] = useState<AiResponse | null>(null);
  const [solution, setSolution] = useState<AiResponse | null>(null);
  const [hintLevel, setHintLevel] = useState(0);

  const analyzeMutation = useMutation({
    mutationFn: () =>
      problemService.analyze({
        problem_statement: problem.statement,
      }),
    onSuccess: (data) => {
      setAnalysis(data);
      toast.success("Problem analyzed");
    },
    onError: (error) => {
      toast.error("Failed to analyze problem");
      console.error(error);
    },
  });

  const hintMutation = useMutation({
    mutationFn: (level: number) =>
      problemService.generateHint({
        problem_statement: problem.statement,
        level: level,
      }),
    onSuccess: (data) => {
      if (hintLevel === 1) setHints1(data);
      else if (hintLevel === 2) setHints2(data);
      else setHints(data);
      toast.success(`Hint level ${hintLevel} generated`);
    },
    onError: (error) => {
      toast.error("Failed to generate hint");
      console.error(error);
    },
  });

  const reviewMutation = useMutation({
    mutationFn: () =>
      aiService.reviewCode({
        problem,
        language,
        code: codeByLanguage[language],
      }),
    onSuccess: (data) => {
      setReview(data);
      toast.success("Code reviewed");
    },
    onError: (error) => {
      toast.error("Failed to review code");
      console.error(error);
    },
  });

  const solutionMutation = useMutation({
    mutationFn: () =>
      problemService.generateSolution({
        problem_statement: problem.statement,
        language,
      }),
    onSuccess: (data) => {
      setSolution(data);
      toast.success("Solution generated");
    },
    onError: (error) => {
      toast.error("Failed to generate solution");
      console.error(error);
    },
  });

  const handleAnalyze = useCallback(() => {
    if (!problem.statement) {
      toast.error("Please enter a problem statement");
      return;
    }
    analyzeMutation.mutate();
  }, [problem.statement, analyzeMutation]);

  const handleHint = useCallback(
    (level: number) => {
      if (!problem.statement) {
        toast.error("Please enter a problem statement");
        return;
      }
      setHintLevel(level);
      hintMutation.mutate(level);
    },
    [problem.statement, hintMutation],
  );

  const handleReview = useCallback(() => {
    if (!codeByLanguage[language]) {
      toast.error("Please write some code");
      return;
    }
    reviewMutation.mutate();
  }, [codeByLanguage, language, reviewMutation]);

  const handleSolution = useCallback(() => {
    if (!problem.statement) {
      toast.error("Please enter a problem statement");
      return;
    }
    solutionMutation.mutate();
  }, [problem.statement, solutionMutation]);

  const hasContent = problem.statement || codeByLanguage[language];

  if (!hasContent) {
    return (
      <div className="flex h-full items-center justify-center p-4 text-center text-sm text-muted-foreground">
        <p>Enter a problem statement or code to get started with AI features</p>
      </div>
    );
  }

  return (
    <Tabs defaultValue="analysis" className="flex h-full min-w-0 flex-col">
      <TabsList className="grid w-full shrink-0 grid-cols-2 rounded-b-none border-b sm:grid-cols-4">
        <TabsTrigger value="analysis" className="min-w-0 text-xs">
          Analyze
        </TabsTrigger>
        <TabsTrigger value="hints" className="min-w-0 text-xs">
          Hints
        </TabsTrigger>
        <TabsTrigger value="review" className="min-w-0 text-xs">
          Review
        </TabsTrigger>
        <TabsTrigger value="solution" className="min-w-0 text-xs">
          Solution
        </TabsTrigger>
      </TabsList>

      <div className="min-h-0 flex-1 overflow-y-auto">
        <TabsContent value="analysis" className="p-3">
          <AnalysisCard
            response={analysis}
            isLoading={analyzeMutation.isPending}
            onAction={handleAnalyze}
            actionLabel={
              analyzeMutation.isPending ? "Analyzing..." : "Analyze Problem"
            }
          />
        </TabsContent>

        <TabsContent value="hints" className="space-y-2 p-3">
          <HintsCard
            response={hints}
            isLoading={hintMutation.isPending && hintLevel === 0}
            onAction={() => handleHint(0)}
            actionLabel="Get Initial Hint"
          />
          <HintsCard
            response={hints1}
            isLoading={hintMutation.isPending && hintLevel === 1}
            onAction={() => handleHint(1)}
            actionLabel="Get Hint Level 2"
          />
          <HintsCard
            response={hints2}
            isLoading={hintMutation.isPending && hintLevel === 2}
            onAction={() => handleHint(2)}
            actionLabel="Get Hint Level 3"
          />
        </TabsContent>

        <TabsContent value="review" className="p-3">
          <ReviewCard
            response={review}
            isLoading={reviewMutation.isPending}
            onAction={handleReview}
            actionLabel={
              reviewMutation.isPending ? "Reviewing..." : "Review My Code"
            }
          />
        </TabsContent>

        <TabsContent value="solution" className="p-3">
          <SolutionCard
            response={solution}
            isLoading={solutionMutation.isPending}
            onAction={handleSolution}
            actionLabel={
              solutionMutation.isPending ? "Generating..." : "Generate Solution"
            }
          />
        </TabsContent>
      </div>
    </Tabs>
  );
}
