"use client";

import Link from "next/link";
import {
  Dna,
  Pill,
  FileText,
  BarChart3,
  Shield,
  ArrowRight,
  Sparkles,
  FlaskConical,
  Microscope,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

const features = [
  {
    icon: Dna,
    title: "Genomic Risk Analysis",
    description:
      "ML-powered disease risk prediction from SNP-style genomic data using XGBoost and feature importance.",
  },
  {
    icon: Pill,
    title: "Pharmacogenomic Cautions",
    description:
      "Evidence-based medication-gene interaction alerts with CYP enzyme metabolizer status mapping.",
  },
  {
    icon: FileText,
    title: "Report Understanding",
    description:
      "Gemini-powered extraction of lab values and clinical findings from PDFs and images.",
  },
  {
    icon: BarChart3,
    title: "Explainable Results",
    description:
      "Feature importance charts, biological context, and plain-English summaries of all findings.",
  },
  {
    icon: Shield,
    title: "Doctor Discussion Notes",
    description:
      "Auto-generated clinician-ready summaries with suggested discussion questions.",
  },
  {
    icon: Sparkles,
    title: "Gemini-Powered Insights",
    description:
      "Multimodal AI understanding of documents, labels, and complex medical data.",
  },
];

export default function LandingPage() {
  return (
    <div className="min-h-screen">
      {/* Navigation */}
      <nav className="fixed top-0 w-full z-50 glass border-b border-white/20">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg gradient-primary flex items-center justify-center">
              <Dna className="w-5 h-5 text-white" />
            </div>
            <span className="font-bold text-lg tracking-tight">RxGenome</span>
          </Link>
          <div className="flex items-center gap-3">
            <Link href="/demo">
              <Button variant="ghost" size="sm">
                Demo
              </Button>
            </Link>
            <Link href="/cases/new">
              <Button size="sm" className="gradient-primary text-white border-0 hover:opacity-90">
                Create Case
              </Button>
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="gradient-hero text-white pt-32 pb-24 px-6">
        <div className="max-w-4xl mx-auto text-center animate-fade-in">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white/10 text-sm mb-6 backdrop-blur-sm border border-white/10">
            <FlaskConical className="w-4 h-4" />
            Educational Precision Medicine Assistant
          </div>
          <h1 className="text-5xl md:text-6xl font-bold tracking-tight mb-6 leading-tight">
            Explainable Disease Risk &<br />
            Medication-Response Insights
          </h1>
          <p className="text-xl text-white/70 max-w-2xl mx-auto mb-10 leading-relaxed">
            Upload genomic data, medical reports, and medication info to receive
            AI-powered risk analysis, pharmacogenomic cautions, and plain-English
            explanations — all designed for informed doctor discussions.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link href="/demo">
              <Button
                size="lg"
                className="bg-white text-gray-900 hover:bg-white/90 gap-2 font-semibold px-8 h-12"
              >
                <Microscope className="w-5 h-5" />
                Try Demo Case
              </Button>
            </Link>
            <Link href="/cases/new">
              <Button
                size="lg"
                variant="outline"
                className="border-white/30 text-white hover:bg-white/10 gap-2 px-8 h-12"
              >
                Create Your Case
                <ArrowRight className="w-4 h-4" />
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Features grid */}
      <section className="py-24 px-6 bg-background">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16 animate-fade-in">
            <h2 className="text-3xl font-bold mb-4">How RxGenome Works</h2>
            <p className="text-muted-foreground text-lg max-w-xl mx-auto">
              From raw genomic data to actionable, explainable insights — powered
              by ML models and Google Gemini.
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 stagger-children">
            {features.map((feature) => (
              <Card
                key={feature.title}
                className="group hover:shadow-lg transition-all duration-300 border-border/50 hover:border-primary/20"
              >
                <CardContent className="pt-6">
                  <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center mb-4 group-hover:bg-primary/15 transition-colors">
                    <feature.icon className="w-6 h-6 text-primary" />
                  </div>
                  <h3 className="font-semibold text-lg mb-2">{feature.title}</h3>
                  <p className="text-muted-foreground text-sm leading-relaxed">
                    {feature.description}
                  </p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Pipeline overview */}
      <section className="py-24 px-6 bg-muted/30">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold mb-4">Analysis Pipeline</h2>
            <p className="text-muted-foreground text-lg">
              Understanding the difference between association and prediction
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center animate-fade-in">
              <div className="w-16 h-16 rounded-2xl gradient-primary text-white flex items-center justify-center text-xl font-bold mx-auto mb-4">
                1
              </div>
              <h3 className="font-semibold mb-2">GWAS Associations</h3>
              <p className="text-sm text-muted-foreground">
                Genome-wide studies identify SNP associations with disease traits —
                revealing biological mechanisms and susceptibility markers.
              </p>
            </div>
            <div className="text-center animate-fade-in" style={{ animationDelay: "0.2s" }}>
              <div className="w-16 h-16 rounded-2xl gradient-primary text-white flex items-center justify-center text-xl font-bold mx-auto mb-4">
                2
              </div>
              <h3 className="font-semibold mb-2">ML Risk Prediction</h3>
              <p className="text-sm text-muted-foreground">
                Machine learning predicts disease risk from combinations of genomic
                features using a trained feature matrix — each row a patient, each
                column a biological marker.
              </p>
            </div>
            <div className="text-center animate-fade-in" style={{ animationDelay: "0.4s" }}>
              <div className="w-16 h-16 rounded-2xl gradient-primary text-white flex items-center justify-center text-xl font-bold mx-auto mb-4">
                3
              </div>
              <h3 className="font-semibold mb-2">Explainable Insights</h3>
              <p className="text-sm text-muted-foreground">
                Feature importance connects model output back to biology. PGx rules
                add medication-gene cautions. Gemini explains everything in plain
                English.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Disclaimer + CTA */}
      <section className="py-16 px-6">
        <div className="max-w-3xl mx-auto text-center">
          <Card className="border-primary/20 bg-primary/5">
            <CardContent className="pt-6">
              <Shield className="w-8 h-8 text-primary mx-auto mb-3" />
              <h3 className="font-semibold mb-2">Educational Tool Only</h3>
              <p className="text-sm text-muted-foreground mb-6 leading-relaxed">
                RxGenome is an educational precision-medicine interpretation
                assistant, not a diagnostic device. All results should be discussed
                with a qualified healthcare provider. The application demonstrates
                how ML and AI can support informed medical discussions.
              </p>
              <div className="flex gap-3 justify-center">
                <Link href="/demo">
                  <Button className="gradient-primary text-white border-0">
                    Try Demo
                  </Button>
                </Link>
                <Link href="/cases/new">
                  <Button variant="outline">Create Case</Button>
                </Link>
              </div>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t py-8 px-6">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between text-sm text-muted-foreground">
          <div className="flex items-center gap-2 mb-4 md:mb-0">
            <Dna className="w-4 h-4 text-primary" />
            <span>RxGenome — BACSA Hacks 2026</span>
          </div>
          <p>Educational precision-medicine interpretation assistant</p>
        </div>
      </footer>
    </div>
  );
}
