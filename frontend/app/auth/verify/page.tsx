"use client";

import { useCallback, useEffect, useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { toast } from "sonner";
import { useRouter, useSearchParams } from "next/navigation";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { BrandMark } from "@/components/shared/brand-mark";
import Link from "next/link";
import { authService } from "@/services/auth.service";
import { useAuthStore } from "@/store/auth-store";

export default function VerifyPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [email, setEmail] = useState("");
  const [code, setCode] = useState("");

  const { setSession } = useAuthStore();

  useEffect(() => {
    const paramEmail = searchParams.get("email");
    if (paramEmail) {
      setEmail(paramEmail);
    }
  }, [searchParams]);

  const verifyMutation = useMutation({
    mutationFn: async () => {
      return authService.verifyOtp({ email, code });
    },
    onSuccess: (data) => {
      setSession(data, true);
      toast.success("Email verified successfully.");
      router.push("/dashboard");
    },
    onError: (error) => {
      toast.error("Verification failed. Please check your code and try again.");
      console.error(error);
    },
  });

  const resendMutation = useMutation({
    mutationFn: async () => {
      return authService.resendOtp({ email });
    },
    onSuccess: () => {
      toast.success("Verification code resent. Check your email.");
    },
    onError: (error) => {
      toast.error("Unable to resend verification code.");
      console.error(error);
    },
  });

  const handleVerify = useCallback(
    (event: React.FormEvent) => {
      event.preventDefault();
      if (!email || !code) {
        toast.error("Please enter your email and verification code.");
        return;
      }
      verifyMutation.mutate();
    },
    [email, code, verifyMutation],
  );

  return (
    <div className="min-h-screen bg-background px-4 py-10">
      <div className="mx-auto flex min-h-[calc(100vh-5rem)] w-full max-w-md items-center">
        <Card className="w-full p-6 sm:p-8">
          <div className="mb-8 text-center">
            <BrandMark className="mx-auto mb-4 justify-center" />
            <h1 className="text-2xl font-semibold tracking-[-0.03em]">Verify Your Email</h1>
            <p className="mt-1 text-sm text-muted-foreground">
              Enter the 6-digit code sent to your email to complete signup.
            </p>
          </div>

          <form onSubmit={handleVerify} className="space-y-4">
            <div>
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                disabled={verifyMutation.isPending || Boolean(searchParams.get("email"))}
                className="mt-1"
              />
            </div>

            <div>
              <Label htmlFor="code">Verification Code</Label>
              <Input
                id="code"
                type="text"
                inputMode="numeric"
                placeholder="123456"
                value={code}
                onChange={(e) => setCode(e.target.value)}
                disabled={verifyMutation.isPending}
                className="mt-1"
              />
            </div>

            <Button type="submit" className="w-full" disabled={verifyMutation.isPending}>
              {verifyMutation.isPending ? "Verifying..." : "Verify Email"}
            </Button>
          </form>

          <div className="mt-6 flex items-center justify-between text-sm">
            <Button
              type="button"
              variant="secondary"
              size="sm"
              className="w-full"
              onClick={() => resendMutation.mutate()}
              disabled={resendMutation.isPending || !email}
            >
              {resendMutation.isPending ? "Resending..." : "Resend Code"}
            </Button>
          </div>

          <div className="mt-6 text-center text-sm">
            <span className="text-muted-foreground">Already verified? </span>
            <Link href="/auth/login" className="font-medium text-primary hover:underline">
              Sign in
            </Link>
          </div>
        </Card>
      </div>
    </div>
  );
}
