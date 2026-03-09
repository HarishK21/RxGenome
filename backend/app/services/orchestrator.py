"""Orchestrator - runs the full analysis pipeline in order."""

import os
from sqlalchemy.orm import Session
from app.models.database import Case, Upload, Prediction, Medication, PGxFinding, ReportField, Summary
from app.services import genome_parser, disease_model, medication_normalizer, pgx_engine, gemini_extractor
from app.config import UPLOAD_DIR


def run_pipeline(case_id: str, db: Session) -> dict:
    """
    Run the full analysis pipeline for a case.
    Stages: parse_genome → extract_report → normalize_medication → run_model → check_pgx → generate_summaries
    """
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise ValueError(f"Case {case_id} not found")

    stages = {}

    # Clear prior analysis records in case of double-fire or re-run
    db.query(ReportField).filter(ReportField.case_id == case_id).delete()
    db.query(Prediction).filter(Prediction.case_id == case_id).delete()
    db.query(PGxFinding).filter(PGxFinding.case_id == case_id).delete()
    db.query(Summary).filter(Summary.case_id == case_id).delete()
    db.commit()

    # Stage 1: Parse genome
    stages["parse_genome"] = {"status": "running"}
    try:
        genome_upload = db.query(Upload).filter(
            Upload.case_id == case_id, Upload.upload_type == "genome"
        ).first()
        if genome_upload:
            genome_data = genome_parser.parse_genome_file(genome_upload.filepath)
        else:
            raise ValueError("No genome file uploaded for this case")
        stages["parse_genome"] = {"status": "completed"}
    except Exception as e:
        stages["parse_genome"] = {"status": "error", "message": str(e)}
        genome_data = {"features": {}} # fallback empty features so pipeline doesn't crash completely

    # Stage 2: Extract report
    stages["extract_report"] = {"status": "running"}
    report_fields_data = []
    try:
        report_upload = db.query(Upload).filter(
            Upload.case_id == case_id, Upload.upload_type == "report"
        ).first()
        if report_upload:
            ext = os.path.splitext(report_upload.filepath)[1].lower()
            if ext == ".pdf":
                report_fields_data = gemini_extractor.extract_report_from_pdf(report_upload.filepath)
            else:
                report_fields_data = gemini_extractor.extract_report_from_image(report_upload.filepath)
        stages["extract_report"] = {"status": "completed"}
    except Exception as e:
        stages["extract_report"] = {"status": "error", "message": str(e)}
        report_fields_data = []

    # Save report fields
    for rf in report_fields_data:
        db_rf = ReportField(
            case_id=case_id,
            field_name=rf.get("field_name", ""),
            field_value=str(rf.get("field_value", "")),
            unit=rf.get("unit"),
            reference_range=rf.get("reference_range"),
            is_abnormal=rf.get("is_abnormal", 0),
            source="upload" if report_upload else "unknown",
        )
        db.add(db_rf)

    # Stage 3: Normalize medication
    stages["normalize_medication"] = {"status": "running"}
    med_info = None
    try:
        med = db.query(Medication).filter(Medication.case_id == case_id).first()
        raw_name = med.raw_name if med else "tamoxifen"
        
        med_result = medication_normalizer.normalize_medication(raw_name)
        if med:
            med.canonical_name = med_result["canonical_name"]
        else:
            med = Medication(case_id=case_id, raw_name="tamoxifen", canonical_name=med_result["canonical_name"], source="hardcoded")
            db.add(med)
            
        med_info = med_result
        stages["normalize_medication"] = {"status": "completed"}
    except Exception as e:
        stages["normalize_medication"] = {"status": "error", "message": str(e)}

    # Stage 4: Run disease model
    stages["run_model"] = {"status": "running"}
    try:
        prediction_result = disease_model.predict(genome_data["features"])
        db_pred = Prediction(
            case_id=case_id,
            model_name=prediction_result["model_name"],
            risk_score=prediction_result["risk_score"],
            risk_tier=prediction_result["risk_tier"],
            accuracy=prediction_result["accuracy"],
            roc_auc=prediction_result["roc_auc"],
            feature_importance=prediction_result["feature_importance"],
        )
        db.add(db_pred)
        stages["run_model"] = {"status": "completed"}
    except Exception as e:
        stages["run_model"] = {"status": "error", "message": str(e)}
        prediction_result = {
            "model_name": "xgboost", "risk_score": 0.5, "risk_tier": "moderate",
            "accuracy": 0.0, "roc_auc": 0.0, "feature_importance": [],
        }

    # Stage 5: Check PGx rules
    stages["check_pgx"] = {"status": "running"}
    pgx_result = {"found": False}
    try:
        if med_info and med_info.get("has_pgx_rule"):
            # Look for genotype from case metadata

            genotype = None
            pgx_result = pgx_engine.lookup_pgx(med_info["canonical_name"], genotype)
            db_pgx = PGxFinding(
                case_id=case_id,
                medication=pgx_result["medication"],
                gene=pgx_result.get("gene", ""),
                genotype=pgx_result.get("genotype", ""),
                phenotype=pgx_result.get("phenotype", ""),
                caution_level=pgx_result.get("caution_level", "unknown"),
                summary=pgx_result.get("summary", ""),
                discussion_points=pgx_result.get("discussion_points", []),
                evidence=pgx_result.get("evidence", ""),
            )
            db.add(db_pgx)
        stages["check_pgx"] = {"status": "completed"}
    except Exception as e:
        stages["check_pgx"] = {"status": "error", "message": str(e)}

    # Stage 6: Generate summaries
    stages["generate_summaries"] = {"status": "running"}
    try:
        patient_summary = gemini_extractor.generate_patient_summary(
            prediction_result, pgx_result, report_fields_data
        )
        clinician_summary = gemini_extractor.generate_clinician_summary(
            prediction_result, pgx_result, report_fields_data
        )
        doctor_note = gemini_extractor.generate_doctor_note(
            prediction_result, pgx_result, report_fields_data
        )

        for stype, content in [
            ("patient", patient_summary),
            ("clinician", clinician_summary),
            ("doctor_note", doctor_note),
        ]:
            db_sum = Summary(case_id=case_id, summary_type=stype, content=content)
            db.add(db_sum)

        stages["generate_summaries"] = {"status": "completed"}
    except Exception as e:
        stages["generate_summaries"] = {"status": "error", "message": str(e)}

    # Update case status
    has_errors = any(s["status"] == "error" for s in stages.values())
    case.status = "completed" if not has_errors else "completed_with_errors"
    db.commit()

    return {
        "case_id": case_id,
        "status": case.status,
        "stages": stages,
    }
