"use client";

import { useEffect } from "react";
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

  useEffect(() => {
    if (hydrated && !accessToken) {
      router.replace(`/login?next=${encodeURIComponent(pathname)}`);
    }
  }, [accessToken, hydrated, pathname, router]);

  if (!hydrated) {
    return <div className="min-h-screen bg-background" />;
  }

  return (
    <div className="min-h-screen bg-background">
      <Sidebar />
      <TopNavigation />
      <main
        className={cn(
          "min-h-screen pt-16 lg:pl-60",
          fullBleed ? "h-screen overflow-hidden" : "px-4 py-6 sm:px-6 lg:px-8 lg:py-8",
        )}
      >
        {children}
      </main>
    </div>
  );
}
