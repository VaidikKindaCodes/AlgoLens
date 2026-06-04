"use client";

import { useCallback } from "react";
import { Card } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { useWorkspaceStore } from "@/store/workspace-store";

export function InputPanel() {
  const { customInput, setCustomInput } = useWorkspaceStore();

  const handleInputChange = useCallback(
    (value: string) => {
      setCustomInput(value);
    },
    [setCustomInput],
  );

  return (
    <div className="flex h-full min-w-0 flex-col gap-2">
      <Card className="flex min-h-0 min-w-0 flex-1 flex-col overflow-hidden p-3">
        <Label className="text-xs font-semibold mb-2">Custom Input</Label>
        <Textarea
          value={customInput}
          onChange={(e) => handleInputChange(e.target.value)}
          placeholder="Paste your test input here..."
          className="min-h-0 flex-1 resize-none font-mono text-sm"
        />
      </Card>
    </div>
  );
}
