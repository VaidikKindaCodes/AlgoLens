"use client";

import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { useWorkspaceStore } from "@/store/workspace-store";
import type { ExecutionResult } from "@/types/workspace";

function getStatusBadgeVariant(status: ExecutionResult["status"]) {
  switch (status) {
    case "accepted":
      return "default";
    case "runtime_error":
    case "time_limit":
    case "compile_error":
    case "error":
      return "destructive";
    default:
      return "secondary";
  }
}

function getStatusLabel(status: ExecutionResult["status"]) {
  switch (status) {
    case "accepted":
      return "✓ Accepted";
    case "runtime_error":
      return "✗ Runtime Error";
    case "time_limit":
      return "✗ Time Limit";
    case "compile_error":
      return "✗ Compile Error";
    case "error":
      return "✗ Error";
    default:
      return "Unknown";
  }
}

export function ConsolePanel({
  isLoading = false,
}: {
  isLoading?: boolean;
}) {
  const { result } = useWorkspaceStore();

  if (isLoading) {
    return (
      <Card className="flex h-full min-w-0 flex-col gap-2 p-3">
        <Skeleton className="h-6 w-32" />
        <Skeleton className="flex-1" />
      </Card>
    );
  }

  if (!result) {
    return (
      <Card className="flex h-full min-w-0 items-center justify-center p-3 text-muted-foreground">
        <p>Run your code to see the output</p>
      </Card>
    );
  }

  return (
    <Card className="flex h-full min-w-0 flex-col gap-3 overflow-hidden p-3">
      <div className="flex items-center justify-between gap-2">
        <Badge variant={getStatusBadgeVariant(result.status)}>
          {getStatusLabel(result.status)}
        </Badge>

        <div className="flex flex-wrap gap-x-4 gap-y-1 text-xs text-muted-foreground">
          {result.execution_time_ms !== null &&
            result.execution_time_ms !== undefined && (
              <span>
                Runtime: {result.execution_time_ms.toFixed(2)}ms
              </span>
            )}

          {result.memory_usage_bytes !== null &&
            result.memory_usage_bytes !== undefined && (
              <span>
                Memory: {(result.memory_usage_bytes / 1024).toFixed(2)}KB
              </span>
            )}
        </div>
      </div>

      <div className="flex min-h-0 flex-1 flex-col gap-2 overflow-hidden">
        {result.output && (
          <div className="flex-1 overflow-auto">
            <p className="mb-1 text-xs font-semibold">Output:</p>
            <pre className="bg-muted rounded p-2 text-xs font-mono whitespace-pre-wrap break-words overflow-auto">
              {result.output}
            </pre>
          </div>
        )}

        {result.error && (
          <div className="flex-1 overflow-auto">
            <p className="mb-1 text-xs font-semibold text-destructive">
              Error:
            </p>
            <pre className="bg-destructive/10 rounded p-2 text-xs font-mono text-destructive whitespace-pre-wrap break-words overflow-auto">
              {result.error}
            </pre>
          </div>
        )}

        {!result.output && !result.error && (
          <p className="text-xs text-muted-foreground">No output</p>
        )}
      </div>
    </Card>
  );
}