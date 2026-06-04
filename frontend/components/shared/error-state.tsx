import { AlertCircle, RotateCcw } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export function ErrorState({
  title = "Unable to load this data",
  description = "Check that the AlgoLens API is running, then try again.",
  onRetry,
  compact = false,
  className,
}: {
  title?: string;
  description?: string;
  onRetry?: () => void;
  compact?: boolean;
  className?: string;
}) {
  return (
    <div
      className={cn(
        "flex flex-col items-center justify-center rounded-xl border border-destructive/20 bg-destructive/[0.035] px-6 text-center",
        compact ? "min-h-36 py-6" : "min-h-56 py-10",
        className,
      )}
    >
      <AlertCircle className="mb-3 size-5 text-destructive" />
      <h3 className="text-sm font-semibold">{title}</h3>
      <p className="mt-1 max-w-md text-sm text-muted-foreground">{description}</p>
      {onRetry && (
        <Button variant="outline" size="sm" onClick={onRetry} className="mt-4">
          <RotateCcw className="size-3.5" />
          Try again
        </Button>
      )}
    </div>
  );
}
