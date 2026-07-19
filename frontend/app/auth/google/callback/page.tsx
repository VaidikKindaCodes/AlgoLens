"use client";

import { useEffect, useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { toast } from "sonner";
import { useRouter, useSearchParams } from "next/navigation";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { BrandMark } from "@/components/shared/brand-mark";
import Link from "next/link";
import { authService } from "@/services/auth.service";
import { useAuthStore } from "@/store/auth-store";

export default function GoogleCallbackPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [initialized, setInitialized] = useState(false);

  const { setSession } = useAuthStore();

  const googleLoginMutation = useMutation({
    mutationFn: async (code: string) => {
      return authService.authenticateWithGoogle(code);
    },
    onSuccess: (data) => {
      setSession(data, true);
      toast.success("Signed in with Google successfully.");
      router.push("/dashboard");
    },
    onError: (error) => {
      toast.error("Google login failed. Please try again.");
      console.error(error);
      setInitialized(true);
    },
  });

  useEffect(() => {
    const code = searchParams.get("code");
    if (!code) {
      setInitialized(true);
      return;
    }
    googleLoginMutation.mutate(code);
  }, [googleLoginMutation, searchParams]);

  return (
    <div className="min-h-screen bg-background px-4 py-10">
      <div className="mx-auto flex min-h-[calc(100vh-5rem)] w-full max-w-md items-center">
        <Card className="w-full p-6 sm:p-8">
          <div className="mb-8 text-center">
            <BrandMark className="mx-auto mb-4 justify-center" />
            <h1 className="text-2xl font-semibold tracking-[-0.03em]">Signing in with Google</h1>
            <p className="mt-1 text-sm text-muted-foreground">
              Completing authentication. Please wait while we sign you in.
            </p>
          </div>

          {(googleLoginMutation.isLoading || !initialized) && (
            <div className="py-8 text-center text-sm text-muted-foreground">
              Redirecting to AlgoLens...
            </div>
          )}

          {initialized && !googleLoginMutation.isLoading && googleLoginMutation.isError && (
            <div className="space-y-4">
              <p className="text-sm text-destructive">
                Google login could not be completed. Please try again or use email/password.
              </p>
              <div className="flex flex-col gap-3">
                <Link href="/auth/login">
                  <Button className="w-full">Back to login</Button>
                </Link>
              </div>
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}
