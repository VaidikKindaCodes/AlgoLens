import { apiRequest } from "./api-client";

export interface AICredentialSummary {
  id: number;
  provider: string;
  model_name: string | null;
  is_default: boolean;
}

export async function createAICredential(payload: {
  provider: string;
  api_key: string;
  model_name?: string | null;
  set_default?: boolean;
}) {
  return apiRequest<AICredentialSummary>({
    url: "/ai-credentials/",
    method: "POST",
    data: payload,
  });
}

export async function listAICredentials() {
  return apiRequest<AICredentialSummary[]>({
    url: "/ai-credentials/",
    method: "GET",
  });
}

export async function deleteAICredential(id: number) {
  return apiRequest<void>({ url: `/ai-credentials/${id}`, method: "DELETE" });
}

export async function getDefaultAICredential() {
  return apiRequest<AICredentialSummary>({
    url: "/ai-credentials/default",
    method: "GET",
  });
}
