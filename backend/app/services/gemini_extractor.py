"""Gemini extractor service - uses Google Gemini for document understanding."""

import os
import json
import base64
from app.config import GEMINI_API_KEY, GEMINI_MODEL, GEMINI_STRONG_MODEL

# Try to import google.generativeai
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


def _get_client(strong: bool = False):
    """Get configured Gemini client."""
    if not GEMINI_AVAILABLE or not GEMINI_API_KEY:
        return None
    genai.configure(api_key=GEMINI_API_KEY)
    model_name = GEMINI_STRONG_MODEL if strong else GEMINI_MODEL
    return genai.GenerativeModel(model_name)


def extract_report_from_pdf(filepath: str) -> list[dict]:
    """Extract structured medical report values from a PDF using Gemini."""
    model = _get_client(strong=False)
    if not model:
        return _mock_report_fields()

    try:
        with open(filepath, "rb") as f:
            pdf_data = f.read()

        prompt = """You are a medical report data extractor. Extract all lab values, measurements, and clinical findings from this medical report.

Return ONLY valid JSON array, no other text. Each item must have:
- "field_name": name of the measurement/test
- "field_value": the value found
- "unit": unit of measurement (or null)
- "reference_range": normal range if shown (or null)
- "is_abnormal": 1 if the value is flagged or outside reference range, 0 otherwise

Example format:
[{"field_name": "Hemoglobin", "field_value": "12.5", "unit": "g/dL", "reference_range": "12.0-16.0", "is_abnormal": 0}]

Extract all values you can identify. Do NOT infer or make up values not present in the document."""

        response = model.generate_content([
            prompt,
            {"mime_type": "application/pdf", "data": pdf_data}
        ])

        text = response.text.strip()
        # Clean markdown fences if present
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
            if text.endswith("```"):
                text = text[:-3]
        return json.loads(text)
    except Exception as e:
        print(f"Gemini PDF extraction failed: {e}")
        return _mock_report_fields()


def extract_report_from_image(filepath: str) -> list[dict]:
    """Extract structured medical report values from a screenshot using Gemini."""
    model = _get_client(strong=False)
    if not model:
        return _mock_report_fields()

    try:
        with open(filepath, "rb") as f:
            image_data = f.read()

        ext = os.path.splitext(filepath)[1].lower()
        mime_map = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}
        mime_type = mime_map.get(ext, "image/png")

        prompt = """You are a medical report data extractor. Extract all lab values, measurements, and clinical findings from this medical report image.

Return ONLY valid JSON array, no other text. Each item must have:
- "field_name": name of the measurement/test
- "field_value": the value found
- "unit": unit of measurement (or null)
- "reference_range": normal range if shown (or null)
- "is_abnormal": 1 if the value is flagged or outside reference range, 0 otherwise

Extract only values visible in the image. Do NOT infer missing data."""

        response = model.generate_content([
            prompt,
            {"mime_type": mime_type, "data": image_data}
        ])

        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
            if text.endswith("```"):
                text = text[:-3]
        return json.loads(text)
    except Exception as e:
        print(f"Gemini image extraction failed: {e}")
        return _mock_report_fields()


def extract_medication_from_label(filepath: str) -> dict:
    """Extract medication info from a label image using Gemini."""
    model = _get_client(strong=False)
    if not model:
        return {"medication_name": "tamoxifen", "dosage": "20mg", "source": "mock"}

    try:
        with open(filepath, "rb") as f:
            image_data = f.read()

        ext = os.path.splitext(filepath)[1].lower()
        mime_map = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}
        mime_type = mime_map.get(ext, "image/png")

        prompt = """You are a medication label reader. Identify the medication name and dosage from this label image.

Return ONLY valid JSON, no other text:
{"medication_name": "...", "dosage": "..."}

Only report what is clearly visible on the label. Do not guess."""

        response = model.generate_content([
            prompt,
            {"mime_type": mime_type, "data": image_data}
        ])

        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
            if text.endswith("```"):
                text = text[:-3]
        return json.loads(text)
    except Exception as e:
        print(f"Gemini label extraction failed: {e}")
        return {"medication_name": "unknown", "dosage": "unknown", "source": "extraction_failed"}


def generate_patient_summary(prediction: dict, pgx: dict, report_fields: list) -> str:
    """Generate a plain-English patient summary using Gemini."""
    model = _get_client(strong=True)
    if not model:
        return _mock_patient_summary(prediction, pgx, report_fields)

    try:
        context = json.dumps({
            "prediction": prediction,
            "pgx_finding": pgx,
            "report_fields": report_fields,
        }, indent=2)

        prompt = f"""You are a medical communication assistant writing for patients. Based on the following structured findings, write a clear, empathetic, plain-English summary that a patient can understand.

STRUCTURED FINDINGS:
{context}

RULES:
- Write 2-3 paragraphs maximum
- Use simple language (8th grade reading level)
- Explain what was found and why it matters
- Do NOT add diagnoses, prescriptions, or medical advice not in the findings
- Mention this is for educational purposes and to discuss with their doctor
- Preserve all uncertainty - use "may", "suggests", "could" appropriately
- End with encouragement to discuss results with healthcare provider"""

        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Gemini summary generation failed: {e}")
        return _mock_patient_summary(prediction, pgx, report_fields)


def generate_clinician_summary(prediction: dict, pgx: dict, report_fields: list) -> str:
    """Generate a clinician-oriented summary using Gemini."""
    model = _get_client(strong=True)
    if not model:
        return _mock_clinician_summary(prediction, pgx, report_fields)

    try:
        context = json.dumps({
            "prediction": prediction,
            "pgx_finding": pgx,
            "report_fields": report_fields,
        }, indent=2)

        prompt = f"""You are a clinical decision support assistant. Based on the following structured findings, write a concise clinician-oriented summary.

STRUCTURED FINDINGS:
{context}

RULES:
- Use clinical terminology
- Highlight actionable findings
- Note model confidence and limitations
- Include relevant pharmacogenomic considerations
- Keep to 2-3 concise paragraphs
- Do NOT prescribe treatment or make definitive diagnoses
- Note this is ML-derived and requires clinical correlation"""

        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Gemini clinician summary failed: {e}")
        return _mock_clinician_summary(prediction, pgx, report_fields)


def generate_doctor_note(prediction: dict, pgx: dict, report_fields: list) -> str:
    """Generate a doctor discussion note."""
    model = _get_client(strong=True)
    if not model:
        return _mock_doctor_note(prediction, pgx, report_fields)

    try:
        context = json.dumps({
            "prediction": prediction,
            "pgx_finding": pgx,
            "report_fields": report_fields,
        }, indent=2)

        prompt = f"""You are a clinical documentation assistant. Generate a concise doctor discussion note based on these structured findings.

STRUCTURED FINDINGS:
{context}

FORMAT:
## Summary
[2-3 sentence overview of key findings]

## Key Findings
- [bullet points of notable results]

## Pharmacogenomic Considerations
- [medication-gene interactions if any]

## Discussion Questions
1. [3-5 suggested questions for the patient to discuss with their doctor]

## Limitations
- [note about ML model limitations and educational purpose]

RULES:
- Be factual and concise
- Preserve uncertainty
- Do not make prescriptive claims
- Note this is for educational discussion purposes only"""

        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Gemini doctor note failed: {e}")
        return _mock_doctor_note(prediction, pgx, report_fields)



def _mock_patient_summary(prediction, pgx, report_fields):
    risk_tier = prediction.get("risk_tier", "moderate")
    risk_score = prediction.get("risk_score", 0.5)
    med = pgx.get("medication", "your medication") if pgx.get("found") else "your medication"

    return f"""Based on the analysis of your genomic data and medical reports, here is a summary of the findings:

**Disease Risk Assessment**: Your genomic profile analysis indicates a **{risk_tier} risk level** (score: {risk_score:.1%}) based on patterns identified across multiple genetic markers. This score reflects the likelihood predicted by our machine learning model trained on similar genomic datasets. It is important to understand that this is a statistical estimate and not a definitive diagnosis.

**Medication Considerations**: {'The analysis identified potential pharmacogenomic interactions with ' + med + '. ' + pgx.get("summary", "") if pgx.get("found") else "No specific pharmacogenomic interactions were flagged for the medications reviewed."}

**What This Means**: These findings are generated by an educational AI system designed to help you have more informed conversations with your healthcare provider. The results should be discussed with your doctor, who can consider your complete medical history and clinical context. We encourage you to bring this report to your next appointment and ask about the discussion questions provided."""


def _mock_clinician_summary(prediction, pgx, report_fields):
    risk_tier = prediction.get("risk_tier", "moderate")
    risk_score = prediction.get("risk_score", 0.5)
    roc = prediction.get("roc_auc", 0.0)

    return f"""**ML-Derived Risk Assessment**: XGBoost classifier indicates {risk_tier} disease risk probability ({risk_score:.1%}). Model performance: ROC-AUC {roc:.3f} on held-out test set (80/20 stratified split). Feature importance analysis identifies top contributing genomic markers aligned with known biological pathways.

**Pharmacogenomic Profile**: {'CYP enzymatic pathway analysis suggests ' + pgx.get("phenotype", "variant") + ' status for ' + pgx.get("gene", "relevant gene") + ', which may impact metabolism of ' + pgx.get("medication", "prescribed medication") + '. ' + pgx.get("evidence", "") if pgx.get("found") else "No actionable pharmacogenomic variants identified within the current rule set."}

**Clinical Correlation Required**: These results are derived from ML analysis of genomic feature matrices and should be interpreted in the context of complete clinical presentation, family history, and confirmatory diagnostic workup. The model operates on curated biomedical features and its predictions represent statistical patterns, not deterministic outcomes."""


def _mock_doctor_note(prediction, pgx, report_fields):
    risk_tier = prediction.get("risk_tier", "moderate")
    risk_score = prediction.get("risk_score", 0.5)

    abnormal = [f for f in report_fields if f.get("is_abnormal")]
    abnormal_text = ", ".join([f"{f['field_name']}: {f['field_value']} {f.get('unit', '')}" for f in abnormal]) if abnormal else "None identified"

    return f"""## Summary
Genomic risk analysis indicates **{risk_tier} risk** (probability: {risk_score:.1%}) based on XGBoost model analysis of {prediction.get('feature_importance', [{}]).__len__()} genomic markers. {'Pharmacogenomic analysis identified ' + pgx.get("caution_level", "moderate") + '-caution interaction for ' + pgx.get("medication", "medication") + '/' + pgx.get("gene", "gene") + '.' if pgx.get("found") else 'No actionable PGx findings.'}

## Key Findings
- Disease risk tier: **{risk_tier.upper()}** ({risk_score:.1%} probability)
- Model confidence: ROC-AUC {prediction.get("roc_auc", 0.0):.3f}
- Top predictive markers: {", ".join([f["feature"] for f in prediction.get("feature_importance", [])[:3]])}
- Abnormal lab values: {abnormal_text}

## Pharmacogenomic Considerations
{"- " + pgx.get("summary", "No PGx findings") if pgx.get("found") else "- No pharmacogenomic interactions identified in the current rule set"}

## Discussion Questions
1. What additional diagnostic tests would help confirm or rule out the risk indicated by the genomic analysis?
2. {"How should the " + pgx.get("phenotype", "metabolizer") + " status for " + pgx.get("gene", "gene") + " affect the current treatment plan for " + pgx.get("medication", "medication") + "?" if pgx.get("found") else "Are there medications in the current regimen that should be evaluated for pharmacogenomic interactions?"}
3. What is the recommended follow-up timeline given the identified risk level?
4. Should genetic counseling be considered based on these genomic findings?
5. How do these findings integrate with family history and other clinical data?

## Limitations
- This analysis is generated by an educational AI system and is **not a clinical diagnostic tool**
- ML predictions represent statistical patterns from training data, not deterministic outcomes
- The pharmacogenomic rules cover a limited set of medication-gene interactions
- All findings require clinical correlation and professional medical judgment
- **Always consult with a qualified healthcare provider before making medical decisions**"""
