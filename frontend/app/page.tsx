import Link from "next/link";
import { ArrowRight, BarChart3, Code2, ShieldCheck, Sparkles, Zap } from "lucide-react";
import { BrandMark } from "@/components/shared/brand-mark";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

export default function HomePage() {
  return (
    <div className="min-h-[100svh] bg-background">
      <div className="mx-auto flex min-h-[100svh] w-full max-w-7xl flex-col px-4 py-6 sm:px-6 lg:px-8">
        <header className="flex items-center justify-between gap-4 py-2">
          <BrandMark />
          <div className="flex items-center gap-2">
            <Button variant="ghost" asChild className="hidden sm:inline-flex">
              <Link href="/auth/login">Sign in</Link>
            </Button>
            <Button asChild>
              <Link href="/auth/register">
                Get started
                <ArrowRight className="size-4" />
              </Link>
            </Button>
          </div>
        </header>

        <main className="grid flex-1 items-center gap-12 py-10 lg:grid-cols-[1.15fr_0.85fr] lg:py-16">
          <section className="space-y-8">
            <div className="space-y-4">
              <div className="inline-flex items-center gap-2 rounded-full border border-border bg-card px-3 py-1 text-xs font-medium text-muted-foreground shadow-sm">
                <Sparkles className="size-3.5 text-primary" />
                AI-assisted competitive programming workspace
              </div>
              <div className="space-y-4">
                <h1 className="max-w-2xl text-4xl font-semibold tracking-[-0.04em] sm:text-5xl lg:text-6xl">
                  Analyze problems, write code, and review solutions in one focused workspace.
                </h1>
                <p className="max-w-2xl text-base leading-7 text-muted-foreground sm:text-lg">
                  AlgoLens brings problem analysis, editor tools, execution feedback, and AI review
                  into a clean dashboard that feels built for daily practice.
                </p>
              </div>
            </div>

            <div className="flex flex-wrap items-center gap-3">
              <Button size="lg" asChild>
                <Link href="/workspace">
                  Open workspace
                  <ArrowRight className="size-4" />
                </Link>
              </Button>
              <Button size="lg" variant="outline" asChild>
                <Link href="/dashboard">View dashboard</Link>
              </Button>
            </div>

            <div className="grid gap-3 sm:grid-cols-3">
              {[
                {
                  icon: Code2,
                  title: "Workspace-first",
                  description: "Keep problem statement, editor, and execution output in view.",
                },
                {
                  icon: BarChart3,
                  title: "Analysis tools",
                  description: "Move from raw statement to strategy without leaving the app.",
                },
                {
                  icon: ShieldCheck,
                  title: "Polished UI",
                  description: "Responsive layouts and consistent spacing across every route.",
                },
              ].map((item) => {
                const Icon = item.icon;
                return (
                  <Card key={item.title} className="border-border/70 bg-card/80">
                    <CardContent className="p-4">
                      <Icon className="size-5 text-primary" />
                      <h2 className="mt-3 text-sm font-semibold">{item.title}</h2>
                      <p className="mt-1 text-sm leading-6 text-muted-foreground">
                        {item.description}
                      </p>
                    </CardContent>
                  </Card>
                );
              })}
            </div>
          </section>

          <aside className="space-y-4">
            <Card className="border-border/70 bg-card/90 shadow-sm">
              <CardContent className="space-y-5 p-6">
                <div className="flex items-center gap-3">
                  <span className="flex size-10 items-center justify-center rounded-xl bg-primary/10 text-primary">
                    <Zap className="size-5" />
                  </span>
                  <div>
                    <p className="text-sm font-semibold">Start in seconds</p>
                    <p className="text-sm text-muted-foreground">
                      Jump to the route that matches your next step.
                    </p>
                  </div>
                </div>

                <div className="grid gap-3">
                  <Button variant="outline" className="justify-start" asChild>
                    <Link href="/auth/login">Sign in to an existing account</Link>
                  </Button>
                  <Button variant="outline" className="justify-start" asChild>
                    <Link href="/history">Review past work</Link>
                  </Button>
                  <Button variant="outline" className="justify-start" asChild>
                    <Link href="/settings">Adjust your preferences</Link>
                  </Button>
                </div>
              </CardContent>
            </Card>
          </aside>
        </main>
      </div>
    </div>
  );
}
