import type { LucideIcon } from "lucide-react";
import { Inbox } from "lucide-react";
import { cn } from "@/lib/utils";

export function EmptyState({
  title,
  description,
  icon: Icon = Inbox,
  action,
  className,
}: {
  title: string;
  description: string;
  icon?: LucideIcon;
  action?: React.ReactNode;
  className?: string;
}) {
  return (
    <div
      className={cn(
        "flex min-h-56 flex-col items-center justify-center rounded-xl border border-dashed border-border bg-card/50 px-6 py-10 text-center",
        className,
      )}
    >
      <div className="mb-4 flex size-10 items-center justify-center rounded-lg border border-border bg-card shadow-sm">
        <Icon className="size-5 text-muted-foreground" />
      </div>
      <h3 className="text-sm font-semibold">{title}</h3>
      <p className="mt-1 max-w-sm text-sm leading-6 text-muted-foreground">
        {description}
      </p>
      {action && <div className="mt-5">{action}</div>}
    </div>
  );
}
