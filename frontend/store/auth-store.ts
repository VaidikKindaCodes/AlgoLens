"use client";

import { create } from "zustand";
import { createJSONStorage, persist } from "zustand/middleware";
import type { TokenResponse, User } from "@/types/auth";

interface AuthState {
  user: User | null;
  accessToken: string | null;
  refreshToken: string | null;
  expiresAt: number | null;
  rememberSession: boolean;
  hydrated: boolean;
  setSession: (session: TokenResponse, remember?: boolean) => void;
  setUser: (user: User) => void;
  clearSession: () => void;
  setHydrated: (hydrated: boolean) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      accessToken: null,
      refreshToken: null,
      expiresAt: null,
      rememberSession: false,
      hydrated: false,
      setSession: (session, remember) =>
        set((state) => ({
          user: session.user,
          accessToken: session.access_token,
          refreshToken: session.refresh_token,
          expiresAt: Date.now() + session.expires_in * 1000,
          rememberSession: remember ?? state.rememberSession,
        })),
      setUser: (user) => set({ user }),
      clearSession: () =>
        set({
          user: null,
          accessToken: null,
          refreshToken: null,
          expiresAt: null,
          rememberSession: false,
        }),
      setHydrated: (hydrated) => set({ hydrated }),
    }),
    {
      name: "algolens-auth",
      storage: createJSONStorage(() => localStorage),
      partialize: ({
        user,
        accessToken,
        refreshToken,
        expiresAt,
        rememberSession,
      }) =>
        rememberSession
          ? { user, accessToken, refreshToken, expiresAt, rememberSession }
          : {
              user: null,
              accessToken: null,
              refreshToken: null,
              expiresAt: null,
              rememberSession: false,
            },
      onRehydrateStorage: () => (state) => state?.setHydrated(true),
    },
  ),
);
