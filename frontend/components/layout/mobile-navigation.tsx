"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Menu, Plus } from "lucide-react";
import { useState } from "react";
import { BrandMark } from "@/components/shared/brand-mark";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { navigationItems } from "@/components/layout/navigation";
import { cn } from "@/lib/utils";

export function MobileNavigation() {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="ghost" size="icon" className="lg:hidden" aria-label="Open navigation">
          <Menu />
        </Button>
      </DialogTrigger>
      <DialogContent
        className="fixed left-0 top-0 flex h-[100svh] w-[min(20rem,85vw)] translate-x-0 translate-y-0 flex-col overflow-hidden rounded-none rounded-r-xl border-y-0 border-l-0 p-0"
        showCloseButton={false}
      >
        <DialogTitle className="sr-only">Navigation</DialogTitle>
        <div className="flex h-16 items-center border-b border-border px-5">
          <BrandMark />
        </div>
        <div className="p-3">
          <Button asChild className="w-full justify-start" onClick={() => setOpen(false)}>
            <Link href="/workspace">
              <Plus />
              New workspace
            </Link>
          </Button>
        </div>
        <nav className="flex-1 space-y-1 overflow-y-auto px-3 pb-3">
          {navigationItems.map((item) => {
            const Icon = item.icon;
            const active = pathname === item.href || pathname.startsWith(`${item.href}/`);
            return (
              <Link
                key={item.href}
                href={item.href}
                onClick={() => setOpen(false)}
                className={cn(
                  "flex h-10 items-center gap-3 rounded-md px-3 text-sm font-medium text-muted-foreground transition-colors hover:bg-muted hover:text-foreground",
                  active && "bg-accent text-accent-foreground",
                )}
              >
                <Icon className="size-4" />
                {item.label}
              </Link>
            );
          })}
        </nav>
      </DialogContent>
    </Dialog>
  );
}
