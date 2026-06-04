"use client";

import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { Button } from "@/components/ui/button";
import { AlertCircle, Lightbulb, Code2, CheckCircle2 } from "lucide-react";
import type { AiResponse } from "@/types/ai";

interface AiCardProps {
  response: AiResponse | null;
  isLoading: boolean;
  onAction?: () => void;
  actionLabel?: string;
}

export function AnalysisCard({
  response,
  isLoading,
  onAction,
  actionLabel = "Analyze",
}: AiCardProps) {
  return (
    <Card className="min-w-0 p-3">
      <div className="mb-2 flex items-center justify-between gap-2">
        <div className="flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4" />
          <h3 className="text-sm font-semibold">Problem Analysis</h3>
        </div>
        {response?.model && (
          <Badge variant="secondary" className="text-xs">
            {response.model}
          </Badge>
        )}
      </div>

      <div className="min-h-24 max-h-48 overflow-y-auto">
        {isLoading ? (
          <div className="space-y-2">
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-5/6" />
            <Skeleton className="h-4 w-4/6" />
          </div>
        ) : response ? (
          <p className="whitespace-pre-wrap text-xs text-muted-foreground">
            {response.content}
          </p>
        ) : (
          <p className="text-xs text-muted-foreground">
            Analyze the problem to get insights
          </p>
        )}
      </div>

      {onAction && (
        <Button
          size="sm"
          variant="outline"
          className="w-full mt-2 text-xs"
          onClick={onAction}
          disabled={isLoading}
        >
          {isLoading ? "Analyzing..." : actionLabel}
        </Button>
      )}
    </Card>
  );
}

export function HintsCard({
  response,
  isLoading,
  onAction,
  actionLabel = "Get Hint",
}: AiCardProps) {
  return (
    <Card className="min-w-0 p-3">
      <div className="mb-2 flex items-center justify-between gap-2">
        <div className="flex items-center gap-2">
          <Lightbulb className="w-4 h-4" />
          <h3 className="text-sm font-semibold">Hints</h3>
        </div>
        {response?.model && (
          <Badge variant="secondary" className="text-xs">
            {response.model}
          </Badge>
        )}
      </div>

      <div className="min-h-24 max-h-48 overflow-y-auto">
        {isLoading ? (
          <div className="space-y-2">
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-5/6" />
            <Skeleton className="h-4 w-4/6" />
          </div>
        ) : response ? (
          <p className="whitespace-pre-wrap text-xs text-muted-foreground">
            {response.content}
          </p>
        ) : (
          <p className="text-xs text-muted-foreground">
            Get step-by-step hints to solve the problem
          </p>
        )}
      </div>

      {onAction && (
        <Button
          size="sm"
          variant="outline"
          className="w-full mt-2 text-xs"
          onClick={onAction}
          disabled={isLoading}
        >
          {isLoading ? "Generating..." : actionLabel}
        </Button>
      )}
    </Card>
  );
}

export function ReviewCard({
  response,
  isLoading,
  onAction,
  actionLabel = "Review Code",
}: AiCardProps) {
  return (
    <Card className="min-w-0 p-3">
      <div className="mb-2 flex items-center justify-between gap-2">
        <div className="flex items-center gap-2">
          <Code2 className="w-4 h-4" />
          <h3 className="text-sm font-semibold">Code Review</h3>
        </div>
        {response?.model && (
          <Badge variant="secondary" className="text-xs">
            {response.model}
          </Badge>
        )}
      </div>

      <div className="min-h-24 max-h-48 overflow-y-auto">
        {isLoading ? (
          <div className="space-y-2">
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-5/6" />
            <Skeleton className="h-4 w-4/6" />
          </div>
        ) : response ? (
          <p className="whitespace-pre-wrap text-xs text-muted-foreground">
            {response.content}
          </p>
        ) : (
          <p className="text-xs text-muted-foreground">
            Get feedback on your code
          </p>
        )}
      </div>

      {onAction && (
        <Button
          size="sm"
          variant="outline"
          className="w-full mt-2 text-xs"
          onClick={onAction}
          disabled={isLoading}
        >
          {isLoading ? "Reviewing..." : actionLabel}
        </Button>
      )}
    </Card>
  );
}

export function SolutionCard({
  response,
  isLoading,
  onAction,
  actionLabel = "Generate Solution",
}: AiCardProps) {
  return (
    <Card className="min-w-0 p-3">
      <div className="mb-2 flex items-center justify-between gap-2">
        <div className="flex items-center gap-2">
          <AlertCircle className="w-4 h-4" />
          <h3 className="text-sm font-semibold">Solution</h3>
        </div>
        {response?.model && (
          <Badge variant="secondary" className="text-xs">
            {response.model}
          </Badge>
        )}
      </div>

      <div className="min-h-24 max-h-48 overflow-y-auto">
        {isLoading ? (
          <div className="space-y-2">
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-5/6" />
            <Skeleton className="h-4 w-4/6" />
          </div>
        ) : response ? (
          <pre className="overflow-auto rounded bg-muted p-2 font-mono text-xs text-muted-foreground whitespace-pre-wrap break-words">
            {response.content}
          </pre>
        ) : (
          <p className="text-xs text-muted-foreground">
            Generate a complete solution
          </p>
        )}
      </div>

      {onAction && (
        <Button
          size="sm"
          variant="outline"
          className="w-full mt-2 text-xs"
          onClick={onAction}
          disabled={isLoading}
        >
          {isLoading ? "Generating..." : actionLabel}
        </Button>
      )}
    </Card>
  );
}
