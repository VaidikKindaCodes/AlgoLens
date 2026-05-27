import { Aperture } from "lucide-react";
import { cn } from "@/lib/utils";

export function BrandMark({
  compact = false,
  className,
}: {
  compact?: boolean;
  className?: string;
}) {
  return (
    <div className={cn("flex items-center gap-2.5", className)}>
      <span className="flex size-8 items-center justify-center rounded-lg bg-primary text-primary-foreground shadow-sm">
        <Aperture className="size-4.5" strokeWidth={2.3} />
      </span>
      {!compact && (
        <span className="text-[15px] font-semibold tracking-[-0.02em]">
          AlgoLens
        </span>
      )}
    </div>
  );
}
