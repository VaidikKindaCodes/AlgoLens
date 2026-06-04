"use client";

import React, { useEffect, useState } from "react";
import {
  createAICredential,
  listAICredentials,
  deleteAICredential,
  getDefaultAICredential,
  type AICredentialSummary,
} from "@/lib/ai-client";
import { useSettingsStore } from "@/store/settings-store";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

function getErrorMessage(error: unknown, fallback: string) {
  if (typeof error === "object" && error !== null) {
    const response = error as {
      response?: { data?: { detail?: string } };
      message?: string;
    };

    return response.response?.data?.detail || response.message || fallback;
  }

  return fallback;
}

export default function AICredentialsForm() {
  const [provider, setProvider] = useState<string>(
    useSettingsStore.getState().provider,
  );
  const [model, setModel] = useState<string>(
    useSettingsStore.getState().model || "",
  );
  const [apiKey, setApiKey] = useState<string>("");
  const [setDefault, setSetDefault] = useState<boolean>(false);
  const [creds, setCreds] = useState<AICredentialSummary[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const apiKeyRef = React.useRef<HTMLInputElement | null>(null);

  useEffect(() => {
    let focusTimeout: ReturnType<typeof setTimeout> | undefined;
    void loadCredentials();

    return () => {
      if (focusTimeout) {
        clearTimeout(focusTimeout);
      }
    };

    async function loadCredentials() {
      setLoading(true);
      try {
        const data = await listAICredentials();
        setCreds(data);
        const def = await getDefaultAICredential().catch(() => null);
        if (def) {
          setProvider(def.provider);
          setModel(def.model_name || "");
        }
        if (data.length === 0) {
          focusTimeout = setTimeout(() => apiKeyRef.current?.focus(), 100);
        }
      } catch (error: unknown) {
        setError(getErrorMessage(error, "Unable to load credentials"));
      } finally {
        setLoading(false);
      }
    }
  }, []);

  async function refreshCredentials() {
    setLoading(true);
    try {
      const data = await listAICredentials();
      setCreds(data);
      const def = await getDefaultAICredential().catch(() => null);
      if (def) {
        setProvider(def.provider);
        setModel(def.model_name || "");
      }
    } catch (error: unknown) {
      setError(getErrorMessage(error, "Unable to load credentials"));
    } finally {
      setLoading(false);
    }
  }

  async function onSave(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await createAICredential({
        provider,
        api_key: apiKey,
        model_name: model || null,
        set_default: setDefault,
      });
      setApiKey("");
      setSetDefault(false);
      await refreshCredentials();
    } catch (error: unknown) {
      setError(getErrorMessage(error, "Save failed"));
    } finally {
      setLoading(false);
    }
  }

  async function onDelete(id: number) {
    setLoading(true);
    setError(null);
    try {
      await deleteAICredential(id);
      await refreshCredentials();
    } catch (error: unknown) {
      setError(getErrorMessage(error, "Delete failed"));
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="mx-auto flex w-full max-w-3xl min-w-0 flex-col gap-4">
      <Card>
        <CardHeader>
          <CardTitle>AI Credentials</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <form onSubmit={onSave} className="space-y-4">
            <div className="grid gap-4 sm:grid-cols-2">
              <div className="space-y-1.5">
                <Label htmlFor="provider">Provider</Label>
                <Select value={provider} onValueChange={setProvider}>
                  <SelectTrigger id="provider">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="openai">OpenAI</SelectItem>
                    <SelectItem value="anthropic">Anthropic</SelectItem>
                    <SelectItem value="gemini">Gemini</SelectItem>
                    <SelectItem value="huggingface">Hugging Face</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-1.5">
                <Label htmlFor="model">Model (optional)</Label>
                <Input
                  id="model"
                  value={model}
                  onChange={(e) => setModel(e.target.value)}
                  placeholder="default"
                />
              </div>
            </div>

            <div className="space-y-1.5">
              <Label htmlFor="api-key">API Key</Label>
              <Input
                id="api-key"
                ref={apiKeyRef}
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                type="password"
                autoComplete="off"
              />
            </div>

            <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
              <label className="flex items-center gap-2 text-sm text-muted-foreground">
                <input
                  type="checkbox"
                  checked={setDefault}
                  onChange={(e) => setSetDefault(e.target.checked)}
                  className="size-4 rounded border-border text-primary focus:ring-primary"
                />
                Set as default
              </label>
              <Button type="submit" disabled={loading} className="w-full sm:w-auto">
                Save Credential
              </Button>
            </div>
          </form>

          {error && <p className="text-sm text-destructive">{error}</p>}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Saved Credentials</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          {loading && <p className="text-sm text-muted-foreground">Loading...</p>}

          {!loading && creds.length === 0 && (
            <p className="text-sm text-muted-foreground">No saved credentials yet.</p>
          )}

          <ul className="space-y-2">
            {creds.map((c) => (
              <li
                key={c.id}
                className="flex items-center justify-between gap-3 rounded-lg border border-border bg-muted/30 px-3 py-2"
              >
                <div className="min-w-0">
                  <div className="flex flex-wrap items-center gap-2">
                    <p className="truncate text-sm font-medium">{c.provider}</p>
                    {c.is_default && (
                      <span className="rounded-full bg-accent px-2 py-0.5 text-[11px] font-medium text-accent-foreground">
                        Default
                      </span>
                    )}
                  </div>
                  <p className="truncate text-xs text-muted-foreground">
                    {c.model_name || "No model"}
                  </p>
                </div>
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={() => onDelete(c.id)}
                  disabled={loading}
                  className="shrink-0"
                >
                  Delete
                </Button>
              </li>
            ))}
          </ul>
        </CardContent>
      </Card>
    </div>
  );
}
