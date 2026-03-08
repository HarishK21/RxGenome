"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import {
  Dna,
  ArrowLeft,
  AlertTriangle,
  CheckCircle2,
  Shield,
  BarChart3,
  Pill,
  FileText,
  Stethoscope,
  Download,
  Copy,
  TrendingUp,
  Info,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip as RechartsTooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";
import { getResults, type FullResults } from "@/lib/api";

/* ---- helper ---- */
function riskColor(tier: string) {
  switch (tier) {
    case "high":
      return "text-rose-600";
    case "moderate":
      return "text-amber-600";
    default:
      return "text-emerald-600";
  }
}
function riskBg(tier: string) {
  switch (tier) {
    case "high":
      return "bg-rose-50 border-rose-200";
    case "moderate":
      return "bg-amber-50 border-amber-200";
    default:
      return "bg-emerald-50 border-emerald-200";
  }
}
function cautionBg(level: string) {
  switch (level) {
    case "high":
      return "bg-rose-50 border-rose-200";
    case "moderate":
      return "bg-amber-50 border-amber-200";
    default:
      return "bg-emerald-50 border-emerald-200";
  }
}

function cautionBadgeVariant(level: string) {
  switch (level) {
    case "high":
      return "destructive" as const;
    case "moderate":
      return "secondary" as const;
    default:
      return "outline" as const;
  }
}

const barColors = [
  "#7c3aed",
  "#6d28d9",
  "#5b21b6",
  "#4c1d95",
  "#8b5cf6",
  "#a78bfa",
  "#c4b5fd",
  "#ddd6fe",
  "#ede9fe",
  "#f5f3ff",
];

export default function ResultsPage() {
  const params = useParams();
  const caseId = params.id as string;
  const [results, setResults] = useState<FullResults | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getResults(caseId)
      .then(setResults)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [caseId]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <Dna className="w-10 h-10 text-primary animate-pulse mx-auto mb-3" />
          <p className="text-muted-foreground">Loading results...</p>
        </div>
      </div>
    );
  }

  if (!results) {
    return (
      <div className="min-h-screen flex items-center justify-center px-6">
        <Card className="max-w-md w-full">
          <CardContent className="pt-6 text-center">
            <AlertTriangle className="w-10 h-10 text-amber-500 mx-auto mb-3" />
            <h2 className="font-semibold text-lg">No Results Found</h2>
            <p className="text-sm text-muted-foreground mt-1 mb-4">
              The analysis may not have completed yet.
            </p>
            <Link href={`/cases/${caseId}/processing`}>
              <Button>Run Analysis</Button>
            </Link>
          </CardContent>
        </Card>
      </div>
    );
  }

  const { prediction, pgx_findings, report_fields, summaries } = results;
  const patientSummary = summaries.find((s) => s.summary_type === "patient");
  const clinicianSummary = summaries.find((s) => s.summary_type === "clinician");
  const doctorNote = summaries.find((s) => s.summary_type === "doctor_note");

  const featureChartData = (prediction?.feature_importance || [])
    .slice(0, 8)
    .map((f) => ({
      name: f.feature.replace("SNP_", "").replace(/_/g, " "),
      value: +(f.importance * 100).toFixed(1),
      fullName: f.feature,
      bio: f.biological_context,
    }));

  return (
    <div className="min-h-screen bg-background">
      {/* Nav */}
      <nav className="border-b sticky top-0 bg-background/80 backdrop-blur-sm z-40 no-print">
        <div className="max-w-6xl mx-auto px-6 h-14 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link
              href="/"
              className="flex items-center gap-2 text-muted-foreground hover:text-foreground"
            >
              <ArrowLeft className="w-4 h-4" />
            </Link>
            <div className="flex items-center gap-2">
              <Dna className="w-5 h-5 text-primary" />
              <span className="font-semibold">RxGenome Results</span>
            </div>
          </div>
          <div className="flex gap-2">
            <Link href={`/cases/${caseId}/doctor-note`}>
              <Button variant="outline" size="sm" className="gap-1">
                <Download className="w-3.5 h-3.5" />
                Doctor Note
              </Button>
            </Link>
          </div>
        </div>
      </nav>

      <main className="max-w-6xl mx-auto px-6 py-8 space-y-8">
        {/* A. Hero Summary */}
        <div className="animate-fade-in">
          <Card
            className={`border-2 ${riskBg(
              prediction?.risk_tier || "moderate"
            )} overflow-hidden`}
          >
            <CardContent className="pt-6">
              <div className="grid md:grid-cols-3 gap-6">
                {/* Risk Score */}
                <div className="text-center">
                  <p className="text-sm font-medium text-muted-foreground mb-1">
                    Disease Risk Score
                  </p>
                  <p
                    className={`text-5xl font-bold ${riskColor(
                      prediction?.risk_tier || "moderate"
                    )}`}
                  >
                    {((prediction?.risk_score || 0) * 100).toFixed(1)}%
                  </p>
                  <Badge
                    variant={cautionBadgeVariant(
                      prediction?.risk_tier || "moderate"
                    )}
                    className="mt-2 uppercase text-xs"
                  >
                    {prediction?.risk_tier} Risk
                  </Badge>
                </div>

                {/* Model Info */}
                <div className="text-center">
                  <p className="text-sm font-medium text-muted-foreground mb-1">
                    Model Performance
                  </p>
                  <p className="text-4xl font-bold text-primary">
                    {((prediction?.roc_auc || 0) * 100).toFixed(1)}%
                  </p>
                  <p className="text-xs text-muted-foreground mt-1">
                    ROC-AUC ({prediction?.model_name || "XGBoost"})
                  </p>
                </div>

                {/* PGx */}
                <div className="text-center">
                  <p className="text-sm font-medium text-muted-foreground mb-1">
                    Medication Caution
                  </p>
                  {pgx_findings.length > 0 ? (
                    <>
                      <p
                        className={`text-3xl font-bold ${riskColor(
                          pgx_findings[0].caution_level
                        )}`}
                      >
                        {pgx_findings[0].caution_level.toUpperCase()}
                      </p>
                      <p className="text-xs text-muted-foreground mt-1">
                        {pgx_findings[0].medication} / {pgx_findings[0].gene}
                      </p>
                    </>
                  ) : (
                    <p className="text-2xl font-bold text-emerald-600">
                      No Alerts
                    </p>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Main content tabs */}
        <Tabs defaultValue="overview" className="animate-fade-in">
          <TabsList className="flex w-full justify-start gap-0 no-print">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="features">Features</TabsTrigger>
            <TabsTrigger value="pgx">PGx</TabsTrigger>
            <TabsTrigger value="report">Report</TabsTrigger>
            <TabsTrigger value="doctor">Doctor Note</TabsTrigger>
          </TabsList>

          {/* B. Overview Tab */}
          <TabsContent value="overview" className="mt-6 space-y-6">
            {/* Disease Risk Panel */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <BarChart3 className="w-5 h-5 text-primary" />
                  Disease Risk Analysis
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span className="text-muted-foreground">Model</span>
                      <span className="font-medium uppercase">
                        {prediction?.model_name}
                      </span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-muted-foreground">
                        Risk Probability
                      </span>
                      <span className="font-medium">
                        {((prediction?.risk_score || 0) * 100).toFixed(2)}%
                      </span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-muted-foreground">Accuracy</span>
                      <span className="font-medium">
                        {((prediction?.accuracy || 0) * 100).toFixed(1)}%
                      </span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-muted-foreground">ROC-AUC</span>
                      <span className="font-medium">
                        {((prediction?.roc_auc || 0) * 100).toFixed(1)}%
                      </span>
                    </div>
                  </div>
                  <div className="p-4 bg-muted/50 rounded-lg">
                    <div className="flex items-start gap-2 text-sm">
                      <Info className="w-4 h-4 text-primary mt-0.5 shrink-0" />
                      <p className="text-muted-foreground leading-relaxed">
                        <strong>ROC-AUC</strong> measures how well the model
                        distinguishes between risk groups. A score of{" "}
                        {((prediction?.roc_auc || 0) * 100).toFixed(0)}% means the
                        model correctly ranks a random positive case above a
                        negative one{" "}
                        {((prediction?.roc_auc || 0) * 100).toFixed(0)}% of the
                        time.
                      </p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Patient Summary */}
            {patientSummary && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Shield className="w-5 h-5 text-primary" />
                    Plain-English Summary
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="prose prose-sm max-w-none text-muted-foreground whitespace-pre-wrap leading-relaxed">
                    {patientSummary.content}
                  </div>
                </CardContent>
              </Card>
            )}
          </TabsContent>

          {/* C. Features Tab */}
          <TabsContent value="features" className="mt-6 space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <TrendingUp className="w-5 h-5 text-primary" />
                  What Drove This Result
                </CardTitle>
                <CardDescription>
                  Top contributing genomic features ranked by importance
                </CardDescription>
              </CardHeader>
              <CardContent>
                {featureChartData.length > 0 && (
                  <div className="h-80 mb-6">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart
                        data={featureChartData}
                        layout="vertical"
                        margin={{ left: 100, right: 20, top: 5, bottom: 5 }}
                      >
                        <XAxis type="number" tick={{ fontSize: 12 }} unit="%" />
                        <YAxis
                          type="category"
                          dataKey="name"
                          tick={{ fontSize: 11 }}
                          width={95}
                        />
                        <RechartsTooltip
                          content={({ active, payload }) => {
                            if (!active || !payload?.[0]) return null;
                            const d = payload[0].payload;
                            return (
                              <div className="bg-white border shadow-lg rounded-lg p-3 text-sm max-w-xs">
                                <p className="font-medium">{d.fullName}</p>
                                <p className="text-muted-foreground">{d.bio}</p>
                                <p className="font-semibold mt-1">
                                  Importance: {d.value}%
                                </p>
                              </div>
                            );
                          }}
                        />
                        <Bar dataKey="value" radius={[0, 4, 4, 0]}>
                          {featureChartData.map((_, i) => (
                            <Cell
                              key={i}
                              fill={barColors[i % barColors.length]}
                            />
                          ))}
                        </Bar>
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                )}

                {/* Feature details */}
                <div className="space-y-3">
                  {(prediction?.feature_importance || []).slice(0, 5).map((f, i) => (
                    <div
                      key={f.feature}
                      className="flex items-start gap-3 p-3 rounded-lg bg-muted/30"
                    >
                      <div className="w-7 h-7 rounded-lg gradient-primary text-white flex items-center justify-center text-xs font-bold shrink-0">
                        {i + 1}
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="font-medium text-sm">{f.feature}</p>
                        <p className="text-xs text-muted-foreground mt-0.5">
                          {f.biological_context}
                        </p>
                      </div>
                      <span className="text-sm font-semibold text-primary shrink-0">
                        {(f.importance * 100).toFixed(1)}%
                      </span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* D. PGx Tab */}
          <TabsContent value="pgx" className="mt-6 space-y-6">
            {pgx_findings.length > 0 ? (
              pgx_findings.map((pgx, i) => (
                <Card
                  key={i}
                  className={`border-2 ${cautionBg(pgx.caution_level)}`}
                >
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <CardTitle className="flex items-center gap-2">
                        <Pill className="w-5 h-5" />
                        {pgx.medication} / {pgx.gene}
                      </CardTitle>
                      <Badge variant={cautionBadgeVariant(pgx.caution_level)}>
                        {pgx.caution_level.toUpperCase()} CAUTION
                      </Badge>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="grid md:grid-cols-3 gap-4 text-sm">
                      <div>
                        <span className="text-muted-foreground">Genotype</span>
                        <p className="font-mono font-medium">{pgx.genotype}</p>
                      </div>
                      <div>
                        <span className="text-muted-foreground">Phenotype</span>
                        <p className="font-medium">{pgx.phenotype}</p>
                      </div>
                      <div>
                        <span className="text-muted-foreground">Evidence</span>
                        <p className="font-medium">{pgx.evidence}</p>
                      </div>
                    </div>
                    <Separator />
                    <div>
                      <h4 className="font-medium text-sm mb-2">Summary</h4>
                      <p className="text-sm text-muted-foreground leading-relaxed">
                        {pgx.summary}
                      </p>
                    </div>
                    <div>
                      <h4 className="font-medium text-sm mb-2">
                        Discussion Points
                      </h4>
                      <ul className="space-y-1.5">
                        {pgx.discussion_points.map((point, j) => (
                          <li
                            key={j}
                            className="flex items-start gap-2 text-sm text-muted-foreground"
                          >
                            <CheckCircle2 className="w-4 h-4 text-primary mt-0.5 shrink-0" />
                            {point}
                          </li>
                        ))}
                      </ul>
                    </div>
                  </CardContent>
                </Card>
              ))
            ) : (
              <Card>
                <CardContent className="pt-6 text-center py-12">
                  <Pill className="w-10 h-10 text-muted-foreground mx-auto mb-3" />
                  <h3 className="font-semibold">
                    No PGx Findings
                  </h3>
                  <p className="text-sm text-muted-foreground mt-1">
                    No pharmacogenomic interactions were identified for the
                    medications in this case.
                  </p>
                </CardContent>
              </Card>
            )}
          </TabsContent>

          {/* E. Report Tab */}
          <TabsContent value="report" className="mt-6 space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <FileText className="w-5 h-5 text-primary" />
                  Extracted Report Values
                </CardTitle>
                <CardDescription>
                  Lab values and clinical findings extracted from the uploaded
                  report
                </CardDescription>
              </CardHeader>
              <CardContent>
                {report_fields.length > 0 ? (
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm">
                      <thead>
                        <tr className="border-b">
                          <th className="text-left py-2 px-3 font-medium">
                            Test / Finding
                          </th>
                          <th className="text-left py-2 px-3 font-medium">
                            Value
                          </th>
                          <th className="text-left py-2 px-3 font-medium">
                            Unit
                          </th>
                          <th className="text-left py-2 px-3 font-medium">
                            Reference
                          </th>
                          <th className="text-left py-2 px-3 font-medium">
                            Status
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                        {report_fields.map((rf, i) => (
                          <tr
                            key={i}
                            className={`border-b last:border-0 ${
                              rf.is_abnormal
                                ? "bg-rose-50"
                                : i % 2 === 0
                                ? "bg-muted/20"
                                : ""
                            }`}
                          >
                            <td className="py-2.5 px-3 font-medium">
                              {rf.field_name}
                            </td>
                            <td
                              className={`py-2.5 px-3 font-mono ${
                                rf.is_abnormal
                                  ? "text-rose-600 font-semibold"
                                  : ""
                              }`}
                            >
                              {rf.field_value}
                            </td>
                            <td className="py-2.5 px-3 text-muted-foreground">
                              {rf.unit || "—"}
                            </td>
                            <td className="py-2.5 px-3 text-muted-foreground">
                              {rf.reference_range || "—"}
                            </td>
                            <td className="py-2.5 px-3">
                              {rf.is_abnormal ? (
                                <Badge variant="destructive" className="text-xs">
                                  <AlertTriangle className="w-3 h-3 mr-1" />
                                  Abnormal
                                </Badge>
                              ) : (
                                <Badge variant="outline" className="text-xs">
                                  Normal
                                </Badge>
                              )}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                ) : (
                  <p className="text-center text-muted-foreground py-8">
                    No report data extracted. Upload a medical report for
                    analysis.
                  </p>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* F. Doctor Note Tab */}
          <TabsContent value="doctor" className="mt-6 space-y-6">
            {doctorNote && (
              <Card>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle className="flex items-center gap-2">
                      <Stethoscope className="w-5 h-5 text-primary" />
                      Doctor Discussion Note
                    </CardTitle>
                    <div className="flex gap-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() =>
                          navigator.clipboard.writeText(doctorNote.content)
                        }
                      >
                        <Copy className="w-3.5 h-3.5 mr-1" /> Copy
                      </Button>
                      <Link href={`/cases/${caseId}/doctor-note`}>
                        <Button variant="outline" size="sm">
                          <Download className="w-3.5 h-3.5 mr-1" /> Export
                        </Button>
                      </Link>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="prose prose-sm max-w-none text-muted-foreground whitespace-pre-wrap leading-relaxed">
                    {doctorNote.content}
                  </div>
                </CardContent>
              </Card>
            )}

            {clinicianSummary && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Shield className="w-5 h-5 text-primary" />
                    Clinician Summary
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="prose prose-sm max-w-none text-muted-foreground whitespace-pre-wrap leading-relaxed">
                    {clinicianSummary.content}
                  </div>
                </CardContent>
              </Card>
            )}
          </TabsContent>
        </Tabs>

        {/* Educational disclaimer */}
        <Card className="border-primary/20 bg-primary/5 no-print">
          <CardContent className="pt-4 pb-4">
            <div className="flex items-start gap-3">
              <Info className="w-5 h-5 text-primary mt-0.5 shrink-0" />
              <div className="text-sm text-muted-foreground">
                <strong className="text-foreground">
                  Educational Tool — Not a Medical Device.
                </strong>{" "}
                RxGenome is an interpretation assistant for educational purposes.
                All results should be discussed with a qualified healthcare
                provider. ML predictions represent statistical patterns, not
                clinical diagnoses.
              </div>
            </div>
          </CardContent>
        </Card>
      </main>
    </div>
  );
}
