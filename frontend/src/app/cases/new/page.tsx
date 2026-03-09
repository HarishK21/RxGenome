"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Dna, ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { createCase } from "@/lib/api";

export default function NewCasePage() {
  const router = useRouter();
  const [name, setName] = useState("");
  const [medication, setMedication] = useState("");

  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) return;
    setLoading(true);
    try {
      const c = await createCase({
        name,
        condition: "breast_cancer_risk",

        medication_name: medication || undefined,
      });
      router.push(`/cases/${c.id}/upload`);
    } catch {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <nav className="border-b">
        <div className="max-w-4xl mx-auto px-6 h-16 flex items-center gap-4">
          <Link href="/" className="flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors">
            <ArrowLeft className="w-4 h-4" />
            Back
          </Link>
          <div className="flex items-center gap-2">
            <Dna className="w-5 h-5 text-primary" />
            <span className="font-semibold">RxGenome</span>
          </div>
        </div>
      </nav>

      <main className="max-w-2xl mx-auto px-6 py-12">
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Create New Case</h1>
          <p className="text-muted-foreground">
            Set up a precision medicine case for genomic risk analysis and
            pharmacogenomic review.
          </p>
        </div>

        <form onSubmit={handleSubmit}>
          <Card className="mb-6">
            <CardHeader>
              <CardTitle>Case Details</CardTitle>
              <CardDescription>Basic information about this analysis</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label htmlFor="name">Case Name</Label>
                <Input
                  id="name"
                  placeholder="e.g., Patient Genomics Review — March 2026"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  required
                />
              </div>
              <div>
                <Label htmlFor="condition">Condition</Label>
                <Input
                  id="condition"
                  value="Breast Cancer Risk Assessment"
                  disabled
                  className="bg-muted"
                />
                <p className="text-xs text-muted-foreground mt-1">
                  Disease risk prediction based on genomic feature analysis
                </p>
              </div>
              <div>
                <Label htmlFor="medication">Medication (optional)</Label>
                <Input
                  id="medication"
                  placeholder="e.g., tamoxifen, clopidogrel"
                  value={medication}
                  onChange={(e) => setMedication(e.target.value)}
                />
                <p className="text-xs text-muted-foreground mt-1">
                  Enter a medication to check for pharmacogenomic interactions
                </p>
              </div>
            </CardContent>
          </Card>


          <Button
            type="submit"
            disabled={!name.trim() || loading}
            className="w-full gradient-primary text-white border-0 h-12 text-base font-medium"
          >
            {loading ? "Creating..." : "Create Case & Continue"}
          </Button>
        </form>
      </main>
    </div>
  );
}
