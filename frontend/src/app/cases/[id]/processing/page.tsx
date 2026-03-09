"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { Dna, CheckCircle2, Loader2, AlertCircle, XCircle } from "lucide-react";
import { Progress } from "@/components/ui/progress";
import { runAnalysis, type AnalysisResult } from "@/lib/api";

const stages = [
  { key: "parse_genome", label: "Parsing Genomic Data", icon: "🧬" },
  { key: "extract_report", label: "Extracting Report Values", icon: "📋" },
  { key: "normalize_medication", label: "Normalizing Medication", icon: "💊" },
  { key: "run_model", label: "Running Disease Model", icon: "🤖" },
  { key: "check_pgx", label: "Checking PGx Rules", icon: "⚗️" },
  { key: "generate_summaries", label: "Generating AI Summaries", icon: "✨" },
];

export default function ProcessingPage() {
  const params = useParams();
  const router = useRouter();
  const caseId = params.id as string;
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [currentStage, setCurrentStage] = useState(0);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;

    // Animate stages while waiting
    const interval = setInterval(() => {
      if (mounted && !result) {
        setCurrentStage((prev) => Math.min(prev + 1, stages.length - 1));
      }
    }, 1500);

    // Run analysis
    runAnalysis(caseId)
      .then((res) => {
        if (mounted) {
          setResult(res);
          setCurrentStage(stages.length);
          setTimeout(() => {
            router.push(`/cases/${caseId}/results`);
          }, 1500);
        }
      })
      .catch((err) => {
        if (mounted) setError(err.message);
      });

    return () => {
      mounted = false;
      clearInterval(interval);
    };
  }, [caseId, router]);

  const progressPercent = result
    ? 100
    : Math.round(((currentStage + 1) / stages.length) * 85);

  return (
    <div className="min-h-screen bg-background flex items-center justify-center px-6">
      <div className="max-w-lg w-full">
        <div className="text-center mb-8 animate-fade-in">
          <div className="w-16 h-16 rounded-2xl gradient-primary text-white flex items-center justify-center mx-auto mb-4 animate-pulse-glow">
            <Dna className="w-8 h-8" />
          </div>
          <h1 className="text-2xl font-bold mb-2">
            {result ? "Analysis Complete" : "Running Analysis"}
          </h1>
          <p className="text-muted-foreground">
            {result
              ? "Redirecting to results..."
              : "Processing your case through the pipeline"}
          </p>
        </div>

        <div className="mb-8">
          <Progress value={progressPercent} className="h-2 mb-2" />
          <p className="text-xs text-muted-foreground text-right">
            {progressPercent}%
          </p>
        </div>

        {error && (
          <div className="mb-6 p-4 rounded-lg bg-destructive/10 text-destructive flex items-start gap-3">
            <AlertCircle className="w-5 h-5 mt-0.5 shrink-0" />
            <div>
              <p className="font-medium">Analysis Error</p>
              <p className="text-sm mt-1">{error}</p>
              <Link
                href={`/cases/${caseId}/upload`}
                className="text-sm underline mt-2 inline-block"
              >
                Go back and try again
              </Link>
            </div>
          </div>
        )}

        <div className="space-y-3">
          {stages.map((stage, i) => {
            const stageResult = result?.stages?.[stage.key];
            let status: "pending" | "running" | "completed" | "error" = "pending";
            if (stageResult) {
              status = (stageResult.status as any) as "pending" | "running" | "completed" | "error";
            } else if (i < currentStage) {
              status = "completed";
            } else if (i === currentStage && !result) {
              status = "running";
            }

            return (
              <div
                key={stage.key}
                className={`flex items-center gap-3 p-3 rounded-lg transition-all duration-300 ${status === "running"
                  ? "bg-primary/5 border border-primary/20"
                  : status === "completed"
                    ? "bg-muted/50"
                    : status === "error"
                      ? "bg-destructive/5 border border-destructive/20"
                      : "opacity-50"
                  }`}
              >
                <span className="text-lg">{stage.icon}</span>
                <span className="flex-1 text-sm font-medium">{stage.label}</span>
                {status === "running" && (
                  <Loader2 className="w-4 h-4 text-primary animate-spin" />
                )}
                {status === "completed" && (
                  <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                )}
                {status === "error" && (
                  <XCircle className="w-4 h-4 text-destructive" />
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
