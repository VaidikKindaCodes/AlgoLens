"use client";

import { useMutation } from "@tanstack/react-query";
import { workspaceService } from "@/services/workspace.service";

export function useRunCode() {
  return useMutation({ mutationFn: workspaceService.run });
}

export function useSaveWorkspace() {
  return useMutation({ mutationFn: workspaceService.save });
}
