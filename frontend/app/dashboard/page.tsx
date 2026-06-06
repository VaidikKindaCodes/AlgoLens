"use client";

import { PageHeader } from "@/components/shared/page-header";
import { Card } from "@/components/ui/card";
import { CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useRouter } from "next/navigation";
import { BarChart3, Clock, FileText, Play, Save, Zap } from "lucide-react";
import { useDashboardSummary } from "@/hooks/use-dashboard";

export default function DashboardPage() {
  const router = useRouter();
  const { data } = useDashboardSummary();

  const stats = [
    { label: "Problems Analyzed", value: data?.problems_analyzed ?? 0, icon: FileText },
    { label: "AI Sessions", value: data?.ai_sessions ?? 0, icon: BarChart3 },
    { label: "Code Runs", value: data?.code_runs ?? 0, icon: Play },
    { label: "Saved Workspaces", value: data?.saved_workspaces ?? 0, icon: Save },
  ];

  return (
    <div className="min-w-0 space-y-6">
      <PageHeader
        title="Dashboard"
        description="Welcome back! Here's your AlgoLens overview."
      />

      <div className="grid min-w-0 gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {stats.map((stat) => {
          const Icon = stat.icon;
          return (
            <Card key={stat.label}>
              <CardContent className="flex items-center justify-between gap-3 p-4">
                <div>
                  <p className="text-xs text-muted-foreground">{stat.label}</p>
                  <p className="text-2xl font-semibold tracking-[-0.03em]">{stat.value}</p>
                </div>
                <Icon className="size-8 text-primary/50" />
              </CardContent>
            </Card>
          );
        })}
      </div>

      <div className="min-w-0 space-y-3">
        <h2 className="text-lg font-semibold tracking-[-0.02em]">Quick Actions</h2>
        <div className="grid min-w-0 gap-3 sm:grid-cols-2 xl:grid-cols-3">
          <Button
            onClick={() => router.push("/workspace")}
            className="h-20 items-start justify-center gap-2 px-4 text-left"
          >
            <Zap className="size-5" />
            Start Coding
          </Button>
          <Button
            variant="outline"
            className="h-20 items-start justify-center gap-2 px-4 text-left"
          >
            <FileText className="size-5" />
            Analyze Problem
          </Button>
          <Button
            variant="outline"
            className="h-20 items-start justify-center gap-2 px-4 text-left"
          >
            <Clock className="size-5" />
            View History
          </Button>
        </div>
      </div>

      <div className="min-w-0 space-y-3">
        <h2 className="text-lg font-semibold tracking-[-0.02em]">Recent Activity</h2>
        <div className="space-y-3">
          {data?.recent_history?.length ? (
            data.recent_history.map((item) => (
              <Card key={`${item.type}-${item.id}`}>
                <CardContent className="flex items-start justify-between gap-3 p-4">
                  <div className="min-w-0">
                    <p className="font-medium">{item.title}</p>
                    <p className="text-sm text-muted-foreground">
                      {item.summary || item.language || "No details available"}
                    </p>
                  </div>
                  <div className="shrink-0 text-right text-xs text-muted-foreground">
                    <p className="uppercase tracking-wide">{item.type.replace("_", " ")}</p>
                    <p>{new Date(item.created_at).toLocaleString()}</p>
                  </div>
                </CardContent>
              </Card>
            ))
          ) : (
            <Card className="p-6 text-center text-muted-foreground">
              <p>No recent activity yet. Start coding to see your activity here.</p>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}
