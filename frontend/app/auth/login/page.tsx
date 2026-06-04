"use client";

import { useState, useCallback } from "react";
import { useMutation } from "@tanstack/react-query";
import { toast } from "sonner";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { BrandMark } from "@/components/shared/brand-mark";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { authService } from "@/services/auth.service";
import { useAuthStore } from "@/store/auth-store";
import type { LoginRequest } from "@/types/auth";

export default function LoginPage() {
  const router = useRouter();
  const { setSession } = useAuthStore();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const loginMutation = useMutation({
    mutationFn: async (payload: LoginRequest) => {
      return authService.login(payload);
    },
    onSuccess: (data) => {
      setSession(data, true);
      toast.success("Logged in successfully!");
      router.push("/dashboard");
    },

    onError: (error) => {
      toast.error("Invalid email or password");
      console.error(error);
    },
  });

  const handleLogin = useCallback(
    (e: React.FormEvent) => {
      e.preventDefault();

      if (!email || !password) {
        toast.error("Please fill in all fields");
        return;
      }

      loginMutation.mutate({ email, password });
    },
    [email, password, loginMutation],
  );

  return (
    <div className="min-h-[100svh] bg-background px-4 py-10">
      <div className="mx-auto flex min-h-[calc(100svh-5rem)] w-full max-w-md items-center">
        <Card className="w-full p-6 sm:p-8">
          <div className="mb-8 text-center">
            <BrandMark className="mx-auto mb-4 justify-center" />
            <h1 className="text-2xl font-semibold tracking-[-0.03em]">Welcome Back</h1>
            <p className="mt-1 text-sm text-muted-foreground">
            Sign in to your AlgoLens account
            </p>
          </div>

          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                disabled={loginMutation.isPending}
                className="mt-1"
              />
            </div>

            <div>
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                disabled={loginMutation.isPending}
                className="mt-1"
              />
            </div>

            <Button
              type="submit"
              className="w-full"
              disabled={loginMutation.isPending}
            >
              {loginMutation.isPending ? "Signing in..." : "Sign in"}
            </Button>
          </form>

          <div className="mt-6 text-center text-sm">
            <span className="text-muted-foreground">Don&apos;t have an account? </span>
            <Link
              href="/auth/register"
              className="font-medium text-primary hover:underline"
            >
              Sign up
            </Link>
          </div>
        </Card>
      </div>
    </div>
  );
}
