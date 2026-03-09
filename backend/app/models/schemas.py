"""Pydantic schemas for API request/response models."""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# --- Case schemas ---
class CaseCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    condition: str = "breast_cancer_risk"
    medication_name: Optional[str] = None
    genotype: Optional[str] = None
    notes: Optional[str] = None

class CaseResponse(BaseModel):
    id: str
    name: str
    condition: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CaseStatus(BaseModel):
    status: str
    stages: dict = {}

# --- Upload schemas ---
class UploadResponse(BaseModel):
    id: str
    case_id: str
    upload_type: str
    filename: str
    mime_type: Optional[str]
    file_size: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True

# --- Prediction schemas ---
class PredictionResponse(BaseModel):
    model_name: str
    risk_score: float
    risk_tier: str
    accuracy: float
    roc_auc: float
    feature_importance: List[dict]

    class Config:
        from_attributes = True

class FeatureImportance(BaseModel):
    feature: str
    importance: float
    biological_context: Optional[str] = None

# --- Medication schemas ---
class MedicationInput(BaseModel):
    name: str
    source: str = "text_input"

class MedicationResponse(BaseModel):
    raw_name: str
    canonical_name: Optional[str]
    source: str

    class Config:
        from_attributes = True

# --- PGx schemas ---
class PGxFindingResponse(BaseModel):
    medication: str
    gene: str
    genotype: str
    phenotype: str
    caution_level: str
    summary: str
    discussion_points: List[str]
    evidence: str

    class Config:
        from_attributes = True

# --- Report schemas ---
class ReportFieldResponse(BaseModel):
    field_name: str
    field_value: str
    unit: Optional[str]
    reference_range: Optional[str]
    is_abnormal: int

    class Config:
        from_attributes = True

# --- Summary schemas ---
class SummaryResponse(BaseModel):
    summary_type: str
    content: str

    class Config:
        from_attributes = True

# --- Full results ---
class FullResultsResponse(BaseModel):
    case: CaseResponse
    prediction: Optional[PredictionResponse] = None
    medications: List[MedicationResponse] = []
    pgx_findings: List[PGxFindingResponse] = []
    report_fields: List[ReportFieldResponse] = []
    summaries: List[SummaryResponse] = []

# --- Analysis request ---
class AnalysisRequest(BaseModel):
    case_id: str

class AnalysisStageUpdate(BaseModel):
    stage: str
    status: str  # pending, running, completed, error
    message: Optional[str] = None

