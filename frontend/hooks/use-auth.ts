"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { authService } from "@/services/auth.service";
import { useAuthStore } from "@/store/auth-store";

export function useLogin() {
  const setSession = useAuthStore((state) => state.setSession);
  return useMutation({
    mutationFn: ({
      remember,
      ...credentials
    }: {
      email: string;
      password: string;
      remember: boolean;
    }) => authService.login(credentials),
    onSuccess: (session, variables) =>
      setSession(session, variables.remember),
  });
}

export function useRegister() {
  const setSession = useAuthStore((state) => state.setSession);
  return useMutation({
    mutationFn: authService.register,
    onSuccess: (session) => setSession(session, true),
  });
}

export function useCurrentUser() {
  const accessToken = useAuthStore((state) => state.accessToken);
  const setUser = useAuthStore((state) => state.setUser);
  return useQuery({
    queryKey: ["auth", "me"],
    queryFn: authService.me,
    enabled: Boolean(accessToken),
    staleTime: 5 * 60_000,
    select: (user) => {
      setUser(user);
      return user;
    },
  });
}

export function useLogout() {
  const queryClient = useQueryClient();
  const refreshToken = useAuthStore((state) => state.refreshToken);
  const clearSession = useAuthStore((state) => state.clearSession);

  return useMutation({
    mutationFn: () =>
      refreshToken
        ? authService.logout(refreshToken)
        : Promise.resolve({ message: "Logged out" }),
    onSettled: () => {
      clearSession();
      queryClient.clear();
    },
  });
}
