"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { CircleHelp, Plus } from "lucide-react";
import { BrandMark } from "@/components/shared/brand-mark";
import { Button } from "@/components/ui/button";
import { navigationItems } from "@/components/layout/navigation";
import { cn } from "@/lib/utils";

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="fixed inset-y-0 left-0 z-30 hidden w-60 flex-col border-r border-border bg-card lg:flex">
      <div className="flex h-16 items-center px-5">
        <Link href="/dashboard" className="focus-ring rounded-lg">
          <BrandMark />
        </Link>
      </div>

      <div className="px-3 pb-4">
        <Button asChild className="w-full justify-start shadow-sm">
          <Link href="/workspace">
            <Plus />
            New workspace
          </Link>
        </Button>
      </div>

      <nav className="flex-1 space-y-1 px-3">
        {navigationItems.map((item) => {
          const active = pathname === item.href || pathname.startsWith(`${item.href}/`);
          const Icon = item.icon;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "focus-ring flex h-9 items-center gap-3 rounded-md px-3 text-sm font-medium text-muted-foreground transition-colors hover:bg-muted hover:text-foreground",
                active && "bg-accent text-accent-foreground",
              )}
            >
              <Icon className="size-4" />
              {item.label}
            </Link>
          );
        })}
      </nav>

      <div className="border-t border-border p-3">
        <a
          href="https://github.com"
          target="_blank"
          rel="noreferrer"
          className="focus-ring flex items-center gap-3 rounded-md px-3 py-2 text-sm text-muted-foreground hover:bg-muted hover:text-foreground"
        >
          <CircleHelp className="size-4" />
          Documentation
        </a>
      </div>
    </aside>
  );
}
