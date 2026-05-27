import axios, {
  AxiosError,
  type AxiosRequestConfig,
  type InternalAxiosRequestConfig,
} from "axios";
import type { TokenResponse } from "@/types/auth";
import { useAuthStore } from "@/store/auth-store";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

interface RetryableRequest extends InternalAxiosRequestConfig {
  _retry?: boolean;
}

export const apiClient = axios.create({
  baseURL: API_URL,
  timeout: 30_000,
  headers: { "Content-Type": "application/json" },
});

let refreshPromise: Promise<string> | null = null;

async function refreshAccessToken() {
  const refreshToken = useAuthStore.getState().refreshToken;
  if (!refreshToken) throw new Error("No refresh token available");

  if (!refreshPromise) {
    refreshPromise = axios
      .post<TokenResponse>(`${API_URL}/auth/refresh`, {
        refresh_token: refreshToken,
      })
      .then(({ data }) => {
        useAuthStore.getState().setSession(data);
        return data.access_token;
      })
      .finally(() => {
        refreshPromise = null;
      });
  }

  return refreshPromise;
}

apiClient.interceptors.request.use((config) => {
  const token = useAuthStore.getState().accessToken;
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const request = error.config as RetryableRequest | undefined;
    const isAuthRoute = request?.url?.includes("/auth/");

    if (error.response?.status !== 401 || !request || request._retry || isAuthRoute) {
      return Promise.reject(error);
    }

    request._retry = true;
    try {
      const token = await refreshAccessToken();
      request.headers.Authorization = `Bearer ${token}`;
      return apiClient(request);
    } catch (refreshError) {
      useAuthStore.getState().clearSession();
      if (typeof window !== "undefined") window.location.assign("/login");
      return Promise.reject(refreshError);
    }
  },
);

export function getApiErrorMessage(error: unknown) {
  if (!axios.isAxiosError(error)) return "Something went wrong. Please try again.";

  const detail = error.response?.data?.detail;
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) {
    return detail.map((item) => item.msg).join(". ");
  }
  if (error.code === "ECONNABORTED") return "The request timed out. Please try again.";
  if (!error.response) return "Unable to reach the AlgoLens API.";

  return "The server could not complete this request.";
}

export async function apiRequest<T>(config: AxiosRequestConfig) {
  const response = await apiClient.request<T>(config);
  return response.data;
}
