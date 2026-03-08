# RxGenome Implementation Plan

## Overview
RxGenome is an educational precision-medicine interpretation assistant that combines disease detection from genomic/SNP-style data, medical report visualization, pharmacogenomic medication caution summaries, and Gemini-powered multimodal document understanding.

## Architecture

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│  Next.js     │───▶│  FastAPI      │───▶│  ML Models  │
│  Frontend    │◀───│  Backend     │◀───│  (sklearn/  │
│  (TypeScript)│    │  (Python)    │    │   XGBoost)  │
└─────────────┘    └──────┬───────┘    └─────────────┘
                          │
                   ┌──────┴───────┐
                   │  Gemini API  │
                   │  (extraction │
                   │   & summary) │
                   └──────────────┘
```

## Tech Stack
- **Frontend**: Next.js App Router, TypeScript, Tailwind CSS, shadcn/ui, Recharts
- **Backend**: FastAPI, Python, Pydantic, SQLAlchemy
- **Database**: SQLite (local fallback, easy demo)
- **ML**: pandas, scikit-learn, XGBoost
- **AI**: Google Gemini API

## Phases

### Phase 1: Project Setup & Structure
- Initialize Next.js frontend
- Initialize FastAPI backend
- Create ML pipeline directory
- Setup configs and env files

### Phase 2: ML Pipeline
- Seed demo data (Breast Cancer Wisconsin style)
- Train Logistic Regression baseline
- Train RandomForest baseline
- Train XGBoost final model
- Save model artifacts and metrics

### Phase 3: Backend API
- Database models (SQLAlchemy + SQLite)
- Case management endpoints
- Genome parser service
- PGx rule engine
- Disease model inference service
- Gemini extraction/summary service
- Orchestrator pipeline

### Phase 4: Frontend
- App shell and layout
- Landing page
- Case creation flow
- Upload page
- Processing/progress page
- Results dashboard
- Doctor note export
- Demo page with pre-seeded personas

### Phase 5: Integration & Polish
- End-to-end flow testing
- Demo data seeding
- UI polish
- README and docs

## Verification Plan
1. ML pipeline: Run training script, verify model artifacts and metrics JSON are produced
2. Backend: Start FastAPI server, hit /health endpoint, create a case via API
3. Frontend: Start Next.js dev server, navigate through pages
4. Integration: Run demo flow end-to-end through the UI
5. Browser validation: Visually verify landing page, results dashboard
