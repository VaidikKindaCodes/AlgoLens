"use client";

import { useState } from "react";
import { FileText } from "lucide-react";
import { PageHeader } from "@/components/shared/page-header";
import { SearchInput } from "@/components/shared/search-input";
import { Card } from "@/components/ui/card";
import { CardContent } from "@/components/ui/card";
import { useHistory } from "@/hooks/use-history";

export default function HistoryPage() {
  const [query, setQuery] = useState("");
  const { data } = useHistory({
    search: query.trim() || undefined,
    page: 1,
    page_size: 20,
  });

  return (
    <div className="space-y-6">
      <PageHeader
        title="History"
        description="View all your previous analyses and solutions."
      />

      <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
        <SearchInput value={query} onChange={setQuery} placeholder="Search queries..." />
      </div>

      <div className="space-y-3">
        {data?.items?.length ? (
          data.items.map((item) => (
            <Card key={`${item.type}-${item.id}`}>
              <CardContent className="flex items-start justify-between gap-3 p-4">
                <div className="min-w-0">
                  <p className="font-medium">{item.title}</p>
                  <p className="text-sm text-muted-foreground">
                    {item.summary || item.language || "No details available"}
                  </p>
                </div>
                <div className="shrink-0 text-right text-xs text-muted-foreground">
                  <p className="uppercase tracking-wide">{item.type.replace("_", " ")}</p>
                  <p>{new Date(item.created_at).toLocaleString()}</p>
                </div>
              </CardContent>
            </Card>
          ))
        ) : (
          <Card>
            <CardContent className="flex items-center gap-3 p-6 text-muted-foreground">
              <FileText className="size-5" />
              <p>No history yet. Run code or save workspaces to see them here.</p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
