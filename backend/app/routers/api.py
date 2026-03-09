"""API routes for RxGenome."""

import os
import uuid
import shutil
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models.database import Case, Upload, Medication, Prediction, PGxFinding, ReportField, Summary
from app.models.schemas import (
    CaseCreate, CaseResponse, FullResultsResponse,
    PredictionResponse, MedicationResponse, PGxFindingResponse,
    ReportFieldResponse, SummaryResponse, UploadResponse,
)
from app.services import orchestrator
from app.config import UPLOAD_DIR

router = APIRouter()


# --- Case endpoints ---
@router.post("/cases", response_model=CaseResponse)
def create_case(case_data: CaseCreate, db: Session = Depends(get_db)):
    """Create a new case."""
    case = Case(
        name=case_data.name,
        condition=case_data.condition,
        status="created",
    )
    db.add(case)
    db.flush()

    # If medication provided, add it
    if case_data.medication_name:
        med = Medication(
            case_id=case.id,
            raw_name=case_data.medication_name,
            source="text_input",
        )
        db.add(med)

    db.commit()
    db.refresh(case)
    return case


@router.get("/cases/{case_id}", response_model=CaseResponse)
def get_case(case_id: str, db: Session = Depends(get_db)):
    """Get case details."""
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case


@router.get("/cases", response_model=list[CaseResponse])
def list_cases(db: Session = Depends(get_db)):
    """List all cases."""
    return db.query(Case).order_by(Case.created_at.desc()).all()


# --- Upload endpoints ---
@router.post("/cases/{case_id}/upload")
def upload_file(
    case_id: str,
    upload_type: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """Upload a file (genome, report, medication_label)."""
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    allowed_types = {
        "genome": [".csv", ".tsv", ".vcf", ".txt"],
        "report": [".pdf", ".png", ".jpg", ".jpeg", ".webp"],
        "medication_label": [".png", ".jpg", ".jpeg", ".webp"],
    }

    if upload_type not in allowed_types:
        raise HTTPException(status_code=400, detail=f"Invalid upload type: {upload_type}")

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed_types[upload_type]:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type {ext} for {upload_type}. Allowed: {allowed_types[upload_type]}"
        )

    # Save file
    file_id = str(uuid.uuid4())
    save_dir = os.path.join(UPLOAD_DIR, case_id)
    os.makedirs(save_dir, exist_ok=True)
    filepath = os.path.join(save_dir, f"{file_id}{ext}")

    with open(filepath, "wb") as f:
        shutil.copyfileobj(file.file, f)

    file_size = os.path.getsize(filepath)

    upload = Upload(
        case_id=case_id,
        upload_type=upload_type,
        filename=file.filename,
        filepath=filepath,
        mime_type=file.content_type,
        file_size=file_size,
    )
    db.add(upload)
    case.status = "uploading"
    db.commit()
    db.refresh(upload)

    return {"id": upload.id, "filename": upload.filename, "upload_type": upload_type, "file_size": file_size}


@router.get("/cases/{case_id}/uploads", response_model=list[UploadResponse])
def get_uploads(case_id: str, db: Session = Depends(get_db)):
    """Get all uploads for a case."""
    return db.query(Upload).filter(Upload.case_id == case_id).all()


# --- Medication endpoints ---
@router.post("/cases/{case_id}/medication")
def add_medication(
    case_id: str,
    name: str = Form(...),
    db: Session = Depends(get_db),
):
    """Add a medication to a case."""
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    med = Medication(case_id=case_id, raw_name=name, source="text_input")
    db.add(med)
    db.commit()
    return {"raw_name": name, "status": "added"}


# --- Analysis endpoints ---
@router.post("/cases/{case_id}/analyze")
def run_analysis(case_id: str, db: Session = Depends(get_db)):
    """Run the full analysis pipeline for a case."""
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    case.status = "processing"
    db.commit()

    try:
        result = orchestrator.run_pipeline(case_id, db)
        return result
    except Exception as e:
        case.status = "error"
        db.commit()
        raise HTTPException(status_code=500, detail=str(e))


# --- Results endpoints ---
@router.get("/cases/{case_id}/results", response_model=FullResultsResponse)
def get_results(case_id: str, db: Session = Depends(get_db)):
    """Get full results for a case."""
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    prediction = db.query(Prediction).filter(Prediction.case_id == case_id).first()
    medications = db.query(Medication).filter(Medication.case_id == case_id).all()
    pgx_findings = db.query(PGxFinding).filter(PGxFinding.case_id == case_id).all()
    report_fields = db.query(ReportField).filter(ReportField.case_id == case_id).all()
    summaries = db.query(Summary).filter(Summary.case_id == case_id).all()

    return FullResultsResponse(
        case=case,
        prediction=prediction,
        medications=medications,
        pgx_findings=pgx_findings,
        report_fields=report_fields,
        summaries=summaries,
    )



# --- Health check ---
@router.get("/health")
def health_check():
    return {"status": "healthy", "service": "rxgenome-api"}
