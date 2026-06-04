"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { ChevronsLeft, ChevronsRight, CircleHelp, Plus } from "lucide-react";
import { BrandMark } from "@/components/shared/brand-mark";
import { Button } from "@/components/ui/button";
import { navigationItems } from "@/components/layout/navigation";
import { cn } from "@/lib/utils";

export function Sidebar({
  collapsed,
  onToggleCollapse,
}: {
  collapsed: boolean;
  onToggleCollapse: () => void;
}) {
  const pathname = usePathname();

  return (
    <aside
      className={cn(
        "sticky top-0 z-30 hidden h-dvh shrink-0 flex-col border-r border-border bg-card transition-[width] duration-200 lg:flex",
        collapsed ? "w-16" : "w-60",
      )}
    >
      <div
        className={cn(
          "flex h-16 items-center border-b border-border",
          collapsed ? "relative justify-center px-2" : "justify-between px-3",
        )}
      >
        <Link href="/dashboard" className="focus-ring rounded-lg">
          <BrandMark compact={collapsed} />
        </Link>

        <Button
          type="button"
          variant="ghost"
          size="icon"
          className={cn(
            "hidden lg:inline-flex",
            collapsed && "absolute right-1 top-1/2 -translate-y-1/2",
          )}
          onClick={onToggleCollapse}
          aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}
        >
          {collapsed ? <ChevronsRight /> : <ChevronsLeft />}
        </Button>
      </div>

      <div className={cn("px-3 pb-4 pt-3", collapsed && "px-2")}>
        <Button
          asChild
          className={cn(
            "w-full shadow-sm",
            collapsed ? "justify-center px-0" : "justify-start",
          )}
          title="New workspace"
        >
          <Link href="/workspace">
            <Plus />
            <span className={collapsed ? "sr-only" : ""}>New workspace</span>
          </Link>
        </Button>
      </div>

      <nav className={cn("flex-1 space-y-1 overflow-y-auto px-3 py-1", collapsed && "px-2")}>
        {navigationItems.map((item) => {
          const active = pathname === item.href || pathname.startsWith(`${item.href}/`);
          const Icon = item.icon;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "focus-ring flex h-9 items-center rounded-md text-sm font-medium text-muted-foreground transition-colors hover:bg-muted hover:text-foreground",
                collapsed ? "justify-center px-0" : "gap-3 px-3",
                active && "bg-accent text-accent-foreground",
              )}
            >
              <Icon className="size-4 shrink-0" />
              <span className={collapsed ? "sr-only" : ""}>{item.label}</span>
            </Link>
          );
        })}
      </nav>

      <div className={cn("border-t border-border p-3", collapsed && "px-2")}>
        <a
          href="https://github.com"
          target="_blank"
          rel="noreferrer"
          className={cn(
            "focus-ring flex items-center rounded-md py-2 text-sm text-muted-foreground transition-colors hover:bg-muted hover:text-foreground",
            collapsed ? "justify-center px-0" : "gap-3 px-3",
          )}
          title="Documentation"
        >
          <CircleHelp className="size-4 shrink-0" />
          <span className={collapsed ? "sr-only" : ""}>Documentation</span>
        </a>
      </div>
    </aside>
  );
}
