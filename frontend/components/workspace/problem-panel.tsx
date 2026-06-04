"use client";

import { useCallback } from "react";
import { Card } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { useWorkspaceStore } from "@/store/workspace-store";

export function ProblemPanel() {
  const { problem, setProblem } = useWorkspaceStore();

  const handleTitleChange = useCallback(
    (value: string) => {
      setProblem({ title: value });
    },
    [setProblem],
  );

  const handleStatementChange = useCallback(
    (value: string) => {
      setProblem({ statement: value });
    },
    [setProblem],
  );

  const handleConstraintsChange = useCallback(
    (value: string) => {
      const constraints = value
        .split("\n")
        .map((c) => c.trim())
        .filter((c) => c.length > 0);
      setProblem({ constraints });
    },
    [setProblem],
  );

  const handleClear = useCallback(() => {
    setProblem({
      title: "",
      statement: "",
      constraints: [],
      examples: [],
    });
  }, [setProblem]);

  return (
    <div className="h-full space-y-3 overflow-y-auto pb-3 pr-1">
      <Card className="space-y-2 p-3">
        <div>
          <Label className="text-xs font-semibold">Problem Title</Label>
          <Input
            value={problem.title}
            onChange={(e) => handleTitleChange(e.target.value)}
            placeholder="Enter problem title..."
            className="text-sm"
          />
        </div>

        <div>
          <Label className="text-xs font-semibold">Problem Statement</Label>
          <Textarea
            value={problem.statement}
            onChange={(e) => handleStatementChange(e.target.value)}
            placeholder="Paste the problem statement here..."
            className="min-h-32 text-xs resize-none"
          />
        </div>

        <div>
          <Label className="text-xs font-semibold">Constraints</Label>
          <Textarea
            value={problem.constraints.join("\n")}
            onChange={(e) => handleConstraintsChange(e.target.value)}
            placeholder="Enter constraints (one per line)..."
            className="min-h-20 text-xs resize-none"
          />
        </div>

        <Button
          variant="outline"
          size="sm"
          onClick={handleClear}
          className="w-full text-xs"
        >
          Clear Problem
        </Button>
      </Card>
    </div>
  );
}
