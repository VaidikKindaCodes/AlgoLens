// "use client";

// import { useState, useCallback } from "react";
// import { useMutation } from "@tanstack/react-query";
// import { toast } from "sonner";
// import { Button } from "@/components/ui/button";
// import { EditorPanel } from "@/components/workspace/editor-panel";
// import { InputPanel } from "@/components/workspace/input-panel";
// import { ConsolePanel } from "@/components/workspace/console-panel";
// import { ProblemPanel } from "@/components/workspace/problem-panel";
// import { AISidebar } from "@/components/workspace/ai-sidebar";
// import { useWorkspaceStore } from "@/store/workspace-store";
// import { workspaceService } from "@/services/workspace.service";
// import { Play, Save } from "lucide-react";
// import { Separator } from "@/components/ui/separator";

// export default function WorkspacePage() {
//   const {
//     problem,
//     language,
//     codeByLanguage,
//     customInput,
//     setResult,
//     markSaved,
//     isDirty,
//   } = useWorkspaceStore();

//   const [showProblem, setShowProblem] = useState(true);

//   const runMutation = useMutation({
//     mutationFn: () =>
//       workspaceService.run({
//         language,
//         code: codeByLanguage[language],
//         custom_input: customInput,
//       }),
//     onSuccess: (data) => {
//       setResult(data);
//       if (data.status === "accepted") {
//         toast.success("Code executed successfully");
//       } else {
//         toast.error(`Execution failed: ${data.status}`);
//       }
//     },
//     onError: (error) => {
//       toast.error("Failed to run code");
//       console.error(error);
//     },
//   });

//   const saveMutation = useMutation({
//     mutationFn: () =>
//       workspaceService.save({
//         title: problem.title,
//         language,
//         code: codeByLanguage[language],
//         custom_input: customInput,
//       }),
//     onSuccess: () => {
//       markSaved();
//       toast.success("Workspace saved");
//     },
//     onError: (error) => {
//       toast.error("Failed to save workspace");
//       console.error(error);
//     },
//   });

//   const handleRun = useCallback(() => {
//     if (!codeByLanguage[language].trim()) {
//       toast.error("Please write some code");
//       return;
//     }
//     runMutation.mutate();
//   }, [codeByLanguage, language, runMutation]);

//   const handleSave = useCallback(() => {
//     saveMutation.mutate();
//   }, [saveMutation]);

//   return (
//     <div className="flex min-h-[calc(100svh-4rem)] min-w-0 flex-col gap-4">
//       <div className="flex min-w-0 flex-col gap-3 rounded-xl border border-border bg-card/90 p-3 shadow-sm sm:flex-row sm:items-center sm:justify-between">
//         <div className="flex flex-wrap items-center gap-2">
//           <Button
//             size="sm"
//             onClick={() => setShowProblem(!showProblem)}
//             variant={showProblem ? "default" : "outline"}
//           >
//             {showProblem ? "Hide" : "Show"} Problem
//           </Button>
//           <Separator orientation="vertical" className="hidden h-6 sm:block" />
//           {isDirty && (
//             <span className="text-xs text-amber-600 dark:text-amber-500 font-medium">
//               Unsaved changes
//             </span>
//           )}
//         </div>

//         <div className="flex flex-wrap items-center gap-2">
//           <Button
//             size="sm"
//             variant="outline"
//             onClick={handleSave}
//             disabled={saveMutation.isPending}
//             className="gap-2"
//           >
//             <Save className="w-4 h-4" />
//             {saveMutation.isPending ? "Saving..." : "Save"}
//           </Button>
//           <Button
//             size="sm"
//             onClick={handleRun}
//             disabled={runMutation.isPending}
//             className="gap-2"
//           >
//             <Play className="w-4 h-4" />
//             {runMutation.isPending ? "Running..." : "Run"}
//           </Button>
//         </div>
//       </div>

//       <div className="grid flex-1 min-h-0 min-w-0 gap-4 xl:grid-cols-[minmax(0,1.05fr)_minmax(0,0.95fr)_minmax(0,0.9fr)]">
//         <div className="flex min-h-0 min-w-0 flex-col gap-4">
//           {showProblem && (
//             <div className="min-h-[18rem] flex-1 overflow-hidden rounded-xl border border-border bg-card">
//               <ProblemPanel />
//             </div>
//           )}
//           <div className={showProblem ? "min-h-[24rem] flex-1 overflow-hidden rounded-xl border border-border bg-card" : "min-h-[42rem] overflow-hidden rounded-xl border border-border bg-card"}>
//             <EditorPanel />
//           </div>
//         </div>

//         <div className="flex min-h-0 min-w-0 flex-col gap-4">
//           <div className="min-h-[14rem] flex-1 overflow-hidden rounded-xl border border-border bg-card">
//             <InputPanel />
//           </div>
//           <div className="min-h-[14rem] flex-1 overflow-hidden rounded-xl border border-border bg-card">
//             <ConsolePanel isLoading={runMutation.isPending} />
//           </div>
//         </div>

//         <div className="min-h-[32rem] min-w-0 overflow-hidden rounded-xl border border-border bg-card">
//           <AISidebar />
//         </div>
//       </div>
//     </div>
//   );
// }
"use client";

import { useState, useCallback, useEffect } from "react";
import { useMutation } from "@tanstack/react-query";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { EditorPanel } from "@/components/workspace/editor-panel";
import { InputPanel } from "@/components/workspace/input-panel";
import { ConsolePanel } from "@/components/workspace/console-panel";
import { ProblemPanel } from "@/components/workspace/problem-panel";
import { AISidebar } from "@/components/workspace/ai-sidebar";
import { useWorkspaceStore } from "@/store/workspace-store";
import { workspaceService } from "@/services/workspace.service";
import { 
  Play, Save, Code2, Terminal, Sparkles, FileText, Keyboard, Maximize, Minimize 
} from "lucide-react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

export default function WorkspacePage() {
  const {
    problem,
    language,
    codeByLanguage,
    customInput,
    setResult,
    markSaved,
    isDirty,
  } = useWorkspaceStore();

  const [consoleTab, setConsoleTab] = useState("input");
  const [isFullscreen, setIsFullscreen] = useState(false);

  // Listen for native full-screen changes (e.g., if user presses Esc)
  useEffect(() => {
    const handleFullscreenChange = () => {
      setIsFullscreen(!!document.fullscreenElement);
    };
    document.addEventListener("fullscreenchange", handleFullscreenChange);
    return () => document.removeEventListener("fullscreenchange", handleFullscreenChange);
  }, []);

  const toggleFullscreen = () => {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch((err) => {
        toast.error(`Error attempting to enable fullscreen: ${err.message}`);
      });
    } else {
      if (document.exitFullscreen) {
        document.exitFullscreen();
      }
    }
  };

  const runMutation = useMutation({
    mutationFn: () =>
      workspaceService.run({
        language,
        code: codeByLanguage[language],
        custom_input: customInput,
      }),
    onSuccess: (data) => {
      setResult(data);
      setConsoleTab("output");
      if (data.status === "accepted") {
        toast.success("Code executed successfully");
      } else {
        toast.error(`Execution failed: ${data.status}`);
      }
    },
    onError: (error) => {
      toast.error("Failed to run code");
      console.error(error);
    },
  });

  const saveMutation = useMutation({
    mutationFn: () =>
      workspaceService.save({
        title: problem.title,
        language,
        code: codeByLanguage[language],
        custom_input: customInput,
      }),
    onSuccess: () => {
      markSaved();
      toast.success("Workspace saved");
    },
    onError: (error) => {
      toast.error("Failed to save workspace");
      console.error(error);
    },
  });

  const handleRun = useCallback(() => {
    if (!codeByLanguage[language]?.trim()) {
      toast.error("Please write some code");
      return;
    }
    setConsoleTab("output"); 
    runMutation.mutate();
  }, [codeByLanguage, language, runMutation]);

  const handleSave = useCallback(() => {
    saveMutation.mutate();
  }, [saveMutation]);

  return (
    <div 
      className={`flex w-full flex-col bg-zinc-950 p-3 text-zinc-200 antialiased selection:bg-zinc-700 transition-all ${
        isFullscreen ? "h-screen" : "h-[calc(100vh-4rem)]"
      }`}
    >
      
      {/* Top Navigation Bar */}
      <div className="flex items-center justify-between rounded-t-xl border border-zinc-800 bg-zinc-900/80 px-4 py-2.5 shadow-sm">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2">
            <div className="h-3 w-3 rounded-full bg-red-500/80" />
            <div className="h-3 w-3 rounded-full bg-amber-500/80" />
            <div className="h-3 w-3 rounded-full bg-emerald-500/80" />
          </div>
          <div className="h-4 w-px bg-zinc-800" />
          <span className="text-sm font-medium text-zinc-300">Workspace</span>
          {isDirty && (
            <span className="flex items-center gap-1.5 rounded-full border border-amber-500/20 bg-amber-500/10 px-2.5 py-0.5 text-[11px] font-medium text-amber-500/90 animate-pulse">
              ● Unsaved
            </span>
          )}
        </div>

        <div className="flex items-center gap-2">
          {/* Fullscreen Toggle Button */}
          <Button
            size="icon"
            variant="ghost"
            onClick={toggleFullscreen}
            className="h-8 w-8 text-zinc-400 hover:bg-zinc-800 hover:text-zinc-200 mr-2"
            title={isFullscreen ? "Exit Full Screen" : "Full Screen"}
          >
            {isFullscreen ? (
              <Minimize className="h-4 w-4" />
            ) : (
              <Maximize className="h-4 w-4" />
            )}
          </Button>

          <Button
            size="sm"
            variant="ghost"
            onClick={handleSave}
            disabled={saveMutation.isPending}
            className="h-8 gap-2 border border-zinc-800 text-xs font-medium text-zinc-400 hover:bg-zinc-800 hover:text-zinc-200"
          >
            <Save className="h-3.5 w-3.5" />
            {saveMutation.isPending ? "Saving..." : "Save"}
          </Button>
          <Button
            size="sm"
            onClick={handleRun}
            disabled={runMutation.isPending}
            className="h-8 gap-2 bg-emerald-600 text-xs font-semibold text-white shadow-md shadow-emerald-900/20 hover:bg-emerald-500"
          >
            <Play className="h-3.5 w-3.5 fill-current" />
            {runMutation.isPending ? "Running..." : "Run"}
          </Button>
        </div>
      </div>

      {/* Main Content Split */}
      <div className="mt-3 flex min-h-0 flex-1 w-full gap-3">
        
        {/* LEFT PANE: Description & AI (Tabbed) */}
        <div className="flex w-[45%] min-w-[300px] flex-col rounded-xl border border-zinc-800 bg-zinc-900/40 shadow-sm">
          <Tabs defaultValue="problem" className="flex h-full flex-col">
            <div className="flex shrink-0 items-center border-b border-zinc-800 bg-zinc-900/60 px-2 h-10">
              <TabsList className="h-auto bg-transparent p-0 gap-1">
                <TabsTrigger 
                  value="problem" 
                  className="gap-2 h-8 px-3 text-xs text-zinc-400 data-[state=active]:bg-zinc-800 data-[state=active]:text-white rounded-md"
                >
                  <FileText className="h-3.5 w-3.5" />
                  Description
                </TabsTrigger>
                <TabsTrigger 
                  value="ai" 
                  className="gap-2 h-8 px-3 text-xs text-zinc-400 data-[state=active]:bg-zinc-800 data-[state=active]:text-white rounded-md"
                >
                  <Sparkles className="h-3.5 w-3.5 text-purple-400" />
                  AI Assistant
                </TabsTrigger>
              </TabsList>
            </div>
            
            <div className="flex-1 min-h-0 overflow-hidden">
              <TabsContent value="problem" className="h-full m-0 p-4 overflow-y-auto">
                <ProblemPanel />
              </TabsContent>
              <TabsContent value="ai" className="h-full m-0 overflow-hidden">
                <AISidebar />
              </TabsContent>
            </div>
          </Tabs>
        </div>

        {/* RIGHT PANE: Code Editor & Console */}
        <div className="flex w-[55%] flex-col gap-3 min-w-[400px]">
          
          {/* Top Right: Editor */}
          <div className="flex flex-[3] flex-col overflow-hidden rounded-xl border border-zinc-800 bg-zinc-900/20 shadow-sm min-h-[300px]">
            <div className="flex h-10 shrink-0 items-center gap-2 border-b border-zinc-800/80 bg-zinc-900/60 px-4 text-xs font-medium text-zinc-400">
              <Code2 className="h-4 w-4 text-blue-400" />
              Code Editor
            </div>
            <div className="flex-1 min-h-0">
              <EditorPanel />
            </div>
          </div>

          {/* Bottom Right: Input & Console */}
          <div className="flex flex-[2] flex-col overflow-hidden rounded-xl border border-zinc-800 bg-zinc-900/60 shadow-sm min-h-[200px]">
            <Tabs value={consoleTab} onValueChange={setConsoleTab} className="flex h-full flex-col">
              <div className="flex h-10 shrink-0 items-center border-b border-zinc-800 bg-zinc-900/40 px-2">
                <TabsList className="h-auto bg-transparent p-0 gap-1">
                  <TabsTrigger 
                    value="input" 
                    className="gap-2 h-8 px-3 text-xs text-zinc-400 data-[state=active]:bg-zinc-800 data-[state=active]:text-white rounded-md"
                  >
                    <Keyboard className="h-3.5 w-3.5" />
                    Custom Input
                  </TabsTrigger>
                  <TabsTrigger 
                    value="output" 
                    className="gap-2 h-8 px-3 text-xs text-zinc-400 data-[state=active]:bg-zinc-800 data-[state=active]:text-white rounded-md"
                  >
                    <Terminal className="h-3.5 w-3.5" />
                    Console
                  </TabsTrigger>
                </TabsList>
              </div>
              
              <div className="flex-1 min-h-0 bg-zinc-950/40">
                <TabsContent value="input" className="h-full m-0 p-3 overflow-y-auto">
                  <InputPanel />
                </TabsContent>
                <TabsContent value="output" className="h-full m-0 p-3 overflow-y-auto">
                  <ConsolePanel isLoading={runMutation.isPending} />
                </TabsContent>
              </div>
            </Tabs>
          </div>

        </div>
      </div>
    </div>
  );
}