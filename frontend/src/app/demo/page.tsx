"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import {
  Dna,
  ArrowLeft,
  User,
  AlertTriangle,
  CheckCircle2,
  Loader2,
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
import { getDemoPersonas, runDemo, type DemoPersona } from "@/lib/api";
import { useEffect } from "react";

export default function DemoPage() {
  const router = useRouter();
  const [personas, setPersonas] = useState<DemoPersona[]>([]);
  const [loading, setLoading] = useState<string | null>(null);

  useEffect(() => {
    getDemoPersonas().then(setPersonas).catch(console.error);
  }, []);

  const handleRun = async (personaId: string) => {
    setLoading(personaId);
    try {
      const result = await runDemo(personaId);
      router.push(`/cases/${result.case_id}/results`);
    } catch (err) {
      console.error(err);
      setLoading(null);
    }
  };

  const riskBadgeVariant = (level: string) => {
    switch (level) {
      case "high":
        return "destructive" as const;
      case "moderate":
        return "secondary" as const;
      default:
        return "outline" as const;
    }
  };

  const riskIcon = (level: string) => {
    switch (level) {
      case "high":
        return <AlertTriangle className="w-3.5 h-3.5" />;
      case "moderate":
        return <AlertTriangle className="w-3.5 h-3.5" />;
      default:
        return <CheckCircle2 className="w-3.5 h-3.5" />;
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <nav className="border-b">
        <div className="max-w-5xl mx-auto px-6 h-16 flex items-center gap-4">
          <Link
            href="/"
            className="flex items-center gap-2 text-muted-foreground hover:text-foreground"
          >
            <ArrowLeft className="w-4 h-4" /> Back
          </Link>
          <div className="flex items-center gap-2">
            <Dna className="w-5 h-5 text-primary" />
            <span className="font-semibold">RxGenome</span>
          </div>
        </div>
      </nav>

      <main className="max-w-5xl mx-auto px-6 py-12">
        <div className="mb-10 text-center">
          <h1 className="text-3xl font-bold mb-3">Demo Cases</h1>
          <p className="text-muted-foreground max-w-xl mx-auto">
            Select a pre-seeded persona to see RxGenome in action. Each demo
            includes genomic data, medication info, and a complete analysis
            pipeline.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-6 stagger-children">
          {personas.map((persona) => (
            <Card
              key={persona.id}
              className="group hover:shadow-lg transition-all duration-300 hover:border-primary/20"
            >
              <CardHeader>
                <div className="flex items-center justify-between mb-2">
                  <div className="w-10 h-10 rounded-full gradient-primary text-white flex items-center justify-center">
                    <User className="w-5 h-5" />
                  </div>
                  <Badge variant={riskBadgeVariant(persona.risk_level)} className="gap-1">
                    {riskIcon(persona.risk_level)}
                    {persona.risk_level} risk
                  </Badge>
                </div>
                <CardTitle className="text-lg">{persona.name}</CardTitle>
                <CardDescription className="text-sm leading-relaxed">
                  {persona.description}
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="space-y-2 text-sm">
                  {persona.medication && (
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Medication</span>
                      <span className="font-medium capitalize">
                        {persona.medication}
                      </span>
                    </div>
                  )}
                  {persona.genotype && (
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Genotype</span>
                      <span className="font-mono text-xs bg-muted px-2 py-0.5 rounded">
                        {persona.genotype}
                      </span>
                    </div>
                  )}
                </div>
                <Button
                  onClick={() => handleRun(persona.id)}
                  disabled={loading !== null}
                  className="w-full gradient-primary text-white border-0"
                >
                  {loading === persona.id ? (
                    <>
                      <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                      Running...
                    </>
                  ) : (
                    "Run Demo Analysis"
                  )}
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>

        {personas.length === 0 && (
          <div className="text-center py-12">
            <Loader2 className="w-8 h-8 text-primary animate-spin mx-auto mb-3" />
            <p className="text-muted-foreground">Loading demo personas...</p>
          </div>
        )}
      </main>
    </div>
  );
}
