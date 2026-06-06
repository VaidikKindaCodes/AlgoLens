import { apiRequest } from "@/lib/api-client";
import type {
  LoginRequest,
  RegisterRequest,
  TokenResponse,
  User,
} from "@/types/auth";

function toUsername(name: string) {
  const username = name
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "_")
    .replace(/^_+|_+$/g, "")
    .slice(0, 32);

  return username.length >= 3 ? username : `${username || "user"}_algolens`;
}

export const authService = {
  login(payload: LoginRequest) {
    return apiRequest<TokenResponse>({
      method: "POST",
      url: "/auth/login",
      data: payload,
    });
  },

  async register(payload: RegisterRequest) {
    await apiRequest<User>({
      method: "POST",
      url: "/auth/register",
      data: {
        email: payload.email,
        username: toUsername(payload.name),
        password: payload.password,
      },
    });

    return this.login({ email: payload.email, password: payload.password });
  },

  me() {
    return apiRequest<User>({ method: "GET", url: "/auth/me" });
  },

  logout(refreshToken: string) {
    return apiRequest<{ message: string }>({
      method: "POST",
      url: "/auth/logout",
      data: { refresh_token: refreshToken },
    });
  },
};
