const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

export interface Case {
  id: string;
  name: string;
  condition: string;
  status: string;
  created_at: string;
  updated_at: string;
}


export interface FeatureImportance {
  feature: string;
  importance: number;
  value?: number;
  biological_context?: string;
}

export interface Prediction {
  model_name: string;
  risk_score: number;
  risk_tier: string;
  accuracy: number;
  roc_auc: number;
  feature_importance: FeatureImportance[];
}

export interface PGxFinding {
  medication: string;
  gene: string;
  genotype: string;
  phenotype: string;
  caution_level: string;
  summary: string;
  discussion_points: string[];
  evidence: string;
}

export interface ReportField {
  field_name: string;
  field_value: string;
  unit: string | null;
  reference_range: string | null;
  is_abnormal: number;
}

export interface Summary {
  summary_type: string;
  content: string;
}

export interface Medication {
  raw_name: string;
  canonical_name: string | null;
  source: string;
}

export interface UploadInfo {
  id: string;
  case_id: string;
  upload_type: string;
  filename: string;
  mime_type: string | null;
  file_size: number | null;
  created_at: string;
}

export interface FullResults {
  case: Case;
  prediction: Prediction | null;
  medications: Medication[];
  pgx_findings: PGxFinding[];
  report_fields: ReportField[];
  summaries: Summary[];
}

export interface AnalysisResult {
  case_id: string;
  status: string;
  stages: Record<string, { status: string; message?: string }>;
}

// --- API functions ---

export async function createCase(data: {
  name: string;
  condition?: string;
  medication_name?: string;
}): Promise<Case> {
  const res = await fetch(`${API_URL}/cases`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function getCase(id: string): Promise<Case> {
  const res = await fetch(`${API_URL}/cases/${id}`);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function listCases(): Promise<Case[]> {
  const res = await fetch(`${API_URL}/cases`);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function uploadFile(
  caseId: string,
  uploadType: string,
  file: File
): Promise<{ id: string; filename: string }> {
  const formData = new FormData();
  formData.append("upload_type", uploadType);
  formData.append("file", file);
  const res = await fetch(`${API_URL}/cases/${caseId}/upload`, {
    method: "POST",
    body: formData,
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function getUploads(caseId: string): Promise<UploadInfo[]> {
  const res = await fetch(`${API_URL}/cases/${caseId}/uploads`);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function addMedication(
  caseId: string,
  name: string
): Promise<{ raw_name: string; status: string }> {
  const formData = new FormData();
  formData.append("name", name);
  const res = await fetch(`${API_URL}/cases/${caseId}/medication`, {
    method: "POST",
    body: formData,
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function runAnalysis(caseId: string): Promise<AnalysisResult> {
  const res = await fetch(`${API_URL}/cases/${caseId}/analyze`, {
    method: "POST",
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function getResults(caseId: string): Promise<FullResults> {
  const res = await fetch(`${API_URL}/cases/${caseId}/results`);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

