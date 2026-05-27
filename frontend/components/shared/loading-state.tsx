import { Skeleton } from "@/components/ui/skeleton";

export function PageLoadingState() {
  return (
    <div className="space-y-7">
      <div className="space-y-2">
        <Skeleton className="h-8 w-52" />
        <Skeleton className="h-4 w-80 max-w-full" />
      </div>
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {Array.from({ length: 4 }).map((_, index) => (
          <Skeleton key={index} className="h-28 rounded-xl" />
        ))}
      </div>
      <div className="grid gap-4 xl:grid-cols-3">
        <Skeleton className="h-80 rounded-xl xl:col-span-2" />
        <Skeleton className="h-80 rounded-xl" />
      </div>
    </div>
  );
}

export function InlineLoader({ label = "Loading" }: { label?: string }) {
  return (
    <span className="inline-flex items-center gap-2 text-sm text-muted-foreground">
      <span className="size-3.5 animate-spin rounded-full border-2 border-current border-r-transparent" />
      {label}
    </span>
  );
}
