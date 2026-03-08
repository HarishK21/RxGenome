"use client";

import { useState, useCallback } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import {
  Dna,
  ArrowLeft,
  ArrowRight,
  FileText,
  Pill,
  Upload,
  CheckCircle2,
  X,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { uploadFile, addMedication } from "@/lib/api";

export default function UploadPage() {
  const params = useParams();
  const router = useRouter();
  const caseId = params.id as string;

  const [genomeFile, setGenomeFile] = useState<File | null>(null);
  const [reportFile, setReportFile] = useState<File | null>(null);
  const [medLabelFile, setMedLabelFile] = useState<File | null>(null);
  const [medicationName, setMedicationName] = useState("");
  const [uploading, setUploading] = useState(false);
  const [uploaded, setUploaded] = useState<Record<string, boolean>>({});

  const handleFileChange =
    (setter: (f: File | null) => void) =>
    (e: React.ChangeEvent<HTMLInputElement>) => {
      if (e.target.files?.[0]) setter(e.target.files[0]);
    };

  const handleContinue = async () => {
    setUploading(true);
    try {
      if (genomeFile) {
        await uploadFile(caseId, "genome", genomeFile);
        setUploaded((prev) => ({ ...prev, genome: true }));
      }
      if (reportFile) {
        await uploadFile(caseId, "report", reportFile);
        setUploaded((prev) => ({ ...prev, report: true }));
      }
      if (medLabelFile) {
        await uploadFile(caseId, "medication_label", medLabelFile);
        setUploaded((prev) => ({ ...prev, medication_label: true }));
      }
      if (medicationName.trim()) {
        await addMedication(caseId, medicationName);
        setUploaded((prev) => ({ ...prev, medication: true }));
      }
      router.push(`/cases/${caseId}/processing`);
    } catch (err) {
      console.error(err);
      setUploading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <nav className="border-b">
        <div className="max-w-4xl mx-auto px-6 h-16 flex items-center gap-4">
          <Link
            href="/cases/new"
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

      <main className="max-w-3xl mx-auto px-6 py-12">
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Upload Data</h1>
          <p className="text-muted-foreground">
            Provide genomic data, medical reports, and medication information for
            analysis.
          </p>
        </div>

        <div className="space-y-6 stagger-children">
          {/* Genome upload */}
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle className="flex items-center gap-2">
                    <Dna className="w-5 h-5 text-primary" />
                    Genomic Data
                  </CardTitle>
                  <CardDescription>
                    Upload SNP/genomic data as CSV or TSV
                  </CardDescription>
                </div>
                {uploaded.genome && (
                  <Badge className="bg-emerald-100 text-emerald-700">
                    <CheckCircle2 className="w-3 h-3 mr-1" /> Uploaded
                  </Badge>
                )}
              </div>
            </CardHeader>
            <CardContent>
              <div className="border-2 border-dashed rounded-lg p-6 text-center hover:border-primary/40 transition-colors">
                <Upload className="w-8 h-8 text-muted-foreground mx-auto mb-2" />
                <div className="text-sm text-muted-foreground mb-3">
                  {genomeFile ? (
                    <span className="text-foreground font-medium flex items-center justify-center gap-2">
                      {genomeFile.name}
                      <button onClick={() => setGenomeFile(null)}>
                        <X className="w-4 h-4 text-muted-foreground hover:text-destructive" />
                      </button>
                    </span>
                  ) : (
                    "Drop CSV/TSV file or click to browse"
                  )}
                </div>
                <Input
                  type="file"
                  accept=".csv,.tsv,.txt,.vcf"
                  onChange={handleFileChange(setGenomeFile)}
                  className="max-w-xs mx-auto"
                />
              </div>
              <p className="text-xs text-muted-foreground mt-2">
                Accepts CSV, TSV, or VCF formats. Each row = sample, each column
                = genomic feature.
              </p>
            </CardContent>
          </Card>

          {/* Report upload */}
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle className="flex items-center gap-2">
                    <FileText className="w-5 h-5 text-primary" />
                    Medical Report
                  </CardTitle>
                  <CardDescription>
                    Upload a lab report PDF or screenshot
                  </CardDescription>
                </div>
                {uploaded.report && (
                  <Badge className="bg-emerald-100 text-emerald-700">
                    <CheckCircle2 className="w-3 h-3 mr-1" /> Uploaded
                  </Badge>
                )}
              </div>
            </CardHeader>
            <CardContent>
              <div className="border-2 border-dashed rounded-lg p-6 text-center hover:border-primary/40 transition-colors">
                <FileText className="w-8 h-8 text-muted-foreground mx-auto mb-2" />
                <div className="text-sm text-muted-foreground mb-3">
                  {reportFile ? (
                    <span className="text-foreground font-medium flex items-center justify-center gap-2">
                      {reportFile.name}
                      <button onClick={() => setReportFile(null)}>
                        <X className="w-4 h-4 text-muted-foreground hover:text-destructive" />
                      </button>
                    </span>
                  ) : (
                    "Drop PDF or image file"
                  )}
                </div>
                <Input
                  type="file"
                  accept=".pdf,.png,.jpg,.jpeg,.webp"
                  onChange={handleFileChange(setReportFile)}
                  className="max-w-xs mx-auto"
                />
              </div>
            </CardContent>
          </Card>

          {/* Medication */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Pill className="w-5 h-5 text-primary" />
                Medication
              </CardTitle>
              <CardDescription>
                Enter medication name or upload a label image
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label>Medication Name</Label>
                <Input
                  placeholder="e.g., tamoxifen, clopidogrel"
                  value={medicationName}
                  onChange={(e) => setMedicationName(e.target.value)}
                />
              </div>
              <div className="border-2 border-dashed rounded-lg p-4 text-center hover:border-primary/40 transition-colors">
                <div className="text-sm text-muted-foreground mb-2">
                  {medLabelFile
                    ? medLabelFile.name
                    : "Or upload a medication label image"}
                </div>
                <Input
                  type="file"
                  accept=".png,.jpg,.jpeg,.webp"
                  onChange={handleFileChange(setMedLabelFile)}
                  className="max-w-xs mx-auto"
                />
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="mt-8 flex gap-4">
          <Button
            onClick={handleContinue}
            disabled={uploading}
            className="flex-1 gradient-primary text-white border-0 h-12"
          >
            {uploading ? "Uploading..." : "Continue to Analysis"}
            <ArrowRight className="w-4 h-4 ml-2" />
          </Button>
        </div>
      </main>
    </div>
  );
}
