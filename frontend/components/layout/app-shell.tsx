"use client";

import { useEffect, useState } from "react";
import { usePathname, useRouter } from "next/navigation";
import { Sidebar } from "@/components/layout/sidebar";
import { TopNavigation } from "@/components/layout/top-navigation";
import { useAuthStore } from "@/store/auth-store";
import { cn } from "@/lib/utils";

export function AppShell({
  children,
  fullBleed = false,
}: {
  children: React.ReactNode;
  fullBleed?: boolean;
}) {
  const router = useRouter();
  const pathname = usePathname();
  const hydrated = useAuthStore((state) => state.hydrated);
  const accessToken = useAuthStore((state) => state.accessToken);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(() => {
    if (typeof window === "undefined") {
      return false;
    }

    return window.localStorage.getItem("algolens-sidebar-collapsed") === "true";
  });

  useEffect(() => {
    window.localStorage.setItem(
      "algolens-sidebar-collapsed",
      String(sidebarCollapsed),
    );
  }, [sidebarCollapsed]);

  useEffect(() => {
    if (hydrated && !accessToken) {
      router.replace(`/login?next=${encodeURIComponent(pathname)}`);
    }
  }, [accessToken, hydrated, pathname, router]);

  // Keep auth in sync across tabs/windows by reacting to localStorage changes
  useEffect(() => {
    const handler = (event: StorageEvent) => {
      if (event.key !== "algolens-auth") return;

      if (!event.newValue) {
        useAuthStore.getState().clearSession();
        return;
      }

      try {
        const parsed = JSON.parse(event.newValue as string);
        const saved = parsed?.state ?? parsed;
        useAuthStore.setState({
          user: saved.user ?? null,
          accessToken: saved.accessToken ?? null,
          refreshToken: saved.refreshToken ?? null,
          expiresAt: saved.expiresAt ?? null,
          rememberSession: saved.rememberSession ?? true,
          hydrated: true,
        });
      } catch (err) {
        // ignore
      }
    };

    window.addEventListener("storage", handler);
    return () => window.removeEventListener("storage", handler);
  }, []);

  if (!hydrated) {
    return <div className="min-h-screen bg-background" />;
  }

  return (
    <div className="min-h-screen bg-background lg:flex">
      <Sidebar
        collapsed={sidebarCollapsed}
        onToggleCollapse={() => setSidebarCollapsed((value) => !value)}
      />
      <div className="flex min-w-0 flex-1 flex-col">
        <TopNavigation />
        <main
          className={cn(
            "flex-1 min-h-0 min-w-0",
            fullBleed
              ? "overflow-hidden"
              : "px-4 py-6 sm:px-6 lg:px-8 lg:py-8",
          )}
        >
          {children}
        </main>
      </div>
    </div>
  );
}
