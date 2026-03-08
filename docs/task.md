# RxGenome Build Checklist

## Phase 1: Project Setup
- [x] Create repo structure (frontend/, backend/, ml/, data/, docs/, scripts/)
- [x] Initialize Next.js frontend with TypeScript + Tailwind
- [x] Setup shadcn/ui
- [x] Initialize FastAPI backend with dependencies
- [x] Create .env.example files
- [x] Create README.md

## Phase 2: ML Pipeline
- [x] Create seeded demo dataset (Breast Cancer Wisconsin style)
- [x] Train Logistic Regression baseline
- [x] Train RandomForest baseline
- [x] Train XGBoost final model
- [x] Save model artifacts, feature order, metrics JSON
- [x] Create PGx rules JSON

## Phase 3: Backend API
- [x] Database models (SQLAlchemy + SQLite)
- [x] Case CRUD endpoints
- [x] Upload service
- [x] Genome parser service
- [x] Medication normalizer
- [x] Disease model inference
- [x] PGx rule engine
- [x] Gemini extractor service
- [x] Explanation composer (via Gemini service)
- [x] Orchestrator pipeline
- [x] Export service (doctor note page)

## Phase 4: Frontend
- [x] App shell / layout / navigation
- [x] Landing page (/)
- [x] Create case page (/cases/new)
- [x] Upload page (/cases/[id]/upload)
- [x] Processing page (/cases/[id]/processing) 
- [x] Results dashboard (/cases/[id]/results)
- [x] Doctor note page (/cases/[id]/doctor-note)
- [x] Demo page (/demo)
- [x] Feature importance chart (Recharts)
- [x] Lab value table with abnormal highlighting
- [x] PGx findings panel with discussion points

## Phase 5: Integration & Polish
- [x] End-to-end flow testing
- [x] Demo data seeding (3 personas)
- [x] Layout fix (Tabs component)
- [x] Final README with run instructions
- [x] .gitignore
