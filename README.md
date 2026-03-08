# RxGenome

**Explainable disease risk and medication-response insights from genetics and reports.**

An educational precision-medicine interpretation assistant that combines disease detection from genomic/SNP-style data, medical report visualization, pharmacogenomic medication caution summaries, and Gemini-powered multimodal document understanding.

> ⚠️ **Educational Tool Only** — RxGenome is not a diagnostic device. All results should be discussed with a qualified healthcare provider.

## Features

- 🧬 **Genomic Risk Analysis** — ML-powered disease risk prediction (XGBoost) from SNP-style feature matrices
- 💊 **Pharmacogenomic Cautions** — Evidence-based medication-gene interaction alerts (CYP2D6/tamoxifen, CYP2C19/clopidogrel)
- 📋 **Report Understanding** — Gemini-powered extraction of lab values from PDFs and images
- 📊 **Explainable Results** — Feature importance charts with biological context
- 🩺 **Doctor Discussion Notes** — Auto-generated clinician summaries with suggested discussion questions
- ✨ **Gemini Integration** — Plain-English explanations, document understanding, medication label reading

## Tech Stack

| Layer | Technologies |
|-------|-------------|
| **Frontend** | Next.js 16, TypeScript, Tailwind CSS v4, shadcn/ui, Recharts |
| **Backend** | FastAPI, Python, Pydantic, SQLAlchemy |
| **Database** | SQLite (local fallback) |
| **ML** | XGBoost, RandomForest, Logistic Regression, scikit-learn, pandas |
| **AI** | Google Gemini API (2.0 Flash + 2.5 Pro) |

## Quick Start

### Prerequisites
- Node.js 18+
- Python 3.10+
- (Optional) Gemini API key

### 1. Clone & Setup

```bash
git clone <this-repo>
cd BASCA2026
```

### 2. Train ML Models

```bash
py ml/train.py
```

This trains 3 models (Logistic Regression, RandomForest, XGBoost) and saves artifacts to `ml/artifacts/`.

### 3. Start Backend

```bash
cd backend
cp .env.example .env
# Edit .env to add your GEMINI_API_KEY (optional — demo works without it)
py -m uvicorn app.main:app --reload --port 8000
```

### 4. Start Frontend

```bash
cd frontend
cp .env.example .env.local
npm install
npm run dev
```

### 5. Open App

Visit [http://localhost:3000](http://localhost:3000)

**Quick Demo:** Click "Demo" → Select a persona → Results appear instantly.

## Demo Flow (2-3 minutes)

1. Open http://localhost:3000
2. Click **"Try Demo Case"** or navigate to **/demo**
3. Choose a persona (Sarah Chen = high risk, James Morrison = low risk)
4. Click **"Run Demo Analysis"**
5. View the results dashboard:
   - Disease risk score and tier
   - Feature importance chart with biological context
   - PGx medication caution (tamoxifen/CYP2D6)
   - Extracted lab values
   - Plain-English summary
   - Doctor discussion note
6. Click **"Doctor Note"** to export/print

## Project Structure

```
BASCA2026/
├── frontend/          # Next.js 16 + TypeScript + Tailwind + shadcn/ui
│   └── src/
│       ├── app/       # App Router pages
│       ├── components/# shadcn/ui components
│       └── lib/       # API client, utilities
├── backend/           # FastAPI + Python
│   └── app/
│       ├── models/    # SQLAlchemy + Pydantic
│       ├── routers/   # API routes
│       └── services/  # Business logic
├── ml/                # ML training pipeline
│   ├── train.py       # Training script
│   └── artifacts/     # Model files, metrics
├── data/
│   ├── demo/          # Seeded demo data
│   └── pgx_rules.json # PGx rule engine
└── docs/
    ├── plan.md        # Implementation plan
    └── task.md        # Build checklist
```

## ML Pipeline

| Model | Accuracy | ROC-AUC |
|-------|----------|---------|
| Logistic Regression | ~96% | ~99% |
| RandomForest | ~95% | ~99% |
| **XGBoost (final)** | **~95%** | **~99%** |

- Dataset: Breast Cancer Wisconsin (genomic-renamed features)
- Split: 80/20 stratified
- Features mapped to SNP-style genomic nomenclature (BRCA1, TP53, CHEK2, etc.)

## Gemini Integration

Gemini is used for:
1. **PDF/image extraction** — Structured extraction of lab values
2. **Medication label reading** — OCR + structured JSON
3. **Patient summary** — Plain-English explanation of findings
4. **Clinician summary** — Technical clinical interpretation
5. **Doctor note** — Discussion-ready document generation

Works without Gemini API key using built-in mock data for demos.

## BACSA Hacks 2026

Built for the BACSA Hacks Open Challenge and Gemini bonus track.

**Product Positioning:** An educational tool demonstrating how ML and AI can support informed medical discussions through explainable disease risk prediction and pharmacogenomic awareness.
