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
import type { RegisterRequest } from "@/types/auth";

export default function RegisterPage() {
  const router = useRouter();
  const { setSession } = useAuthStore();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const registerMutation = useMutation({
    mutationFn: async (payload: RegisterRequest) => {
      return authService.register(payload);
    },
    onSuccess: (data) => {
      setSession(data);
      toast.success("Account created successfully! Please add your AI key in Settings.");
      router.push("/settings");
    },
    onError: (error) => {
      toast.error("Registration failed. Please try again.");
      console.error(error);
    },
  });

  const handleRegister = useCallback(
    (e: React.FormEvent) => {
      console.log("hello hello ");
      e.preventDefault();
      if (!name || !email || !password || !confirmPassword) {
        toast.error("Please fill in all fields");
        return;
      }

      if (password !== confirmPassword) {
        toast.error("Passwords do not match");
        return;
      }

      if (password.length < 6) {
        toast.error("Password must be at least 6 characters");
        return;
      }
      console.log("registering")
      registerMutation.mutate({ name, email, password });
    },
    [name, email, password, confirmPassword, registerMutation],
  );

  return (
    <div className="min-h-[100svh] bg-background px-4 py-10">
      <div className="mx-auto flex min-h-[calc(100svh-5rem)] w-full max-w-md items-center">
        <Card className="w-full p-6 sm:p-8">
          <div className="mb-8 text-center">
            <BrandMark className="mx-auto mb-4 justify-center" />
            <h1 className="text-2xl font-semibold tracking-[-0.03em]">Create Account</h1>
            <p className="mt-1 text-sm text-muted-foreground">
            Join AlgoLens and start solving problems
            </p>
          </div>

          <form  onSubmit={handleRegister} className="space-y-4">
            <div>
              <Label htmlFor="name">Full Name</Label>
              <Input
                id="name"
                type="text"
                placeholder="John Doe"
                value={name}
                onChange={(e) => setName(e.target.value)}
                disabled={registerMutation.isPending}
                className="mt-1"
              />
            </div>

            <div>
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                disabled={registerMutation.isPending}
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
                disabled={registerMutation.isPending}
                className="mt-1"
              />
            </div>

            <div>
              <Label htmlFor="confirm-password">Confirm Password</Label>
              <Input
                id="confirm-password"
                type="password"
                placeholder="••••••••"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                disabled={registerMutation.isPending}
                className="mt-1"
              />
            </div>

            <Button
              type="submit"
              className="w-full"
              onClick={() => console.log("BUTTON CLICKED")}
              // disabled={registerMutation.isPending}
            >
              {registerMutation.isPending ? "Creating account..." : "Sign up"}
            </Button>
          </form>

          <div className="mt-6 text-center text-sm">
            <span className="text-muted-foreground">Already have an account? </span>
            <Link
              href="/auth/login"
              className="font-medium text-primary hover:underline"
            >
              Sign in
            </Link>
          </div>
        </Card>
      </div>
    </div>
  );
}
