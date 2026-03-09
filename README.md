<div align="center">
  
# 🧬 RxGenome
**Explainable Disease Risk & Pharmacogenomic Insights**

*Built for the BACSA Hacks 2026 Open Challenge (Disease Detection & Health Improvement)*

</div>

<br />

## 🎯 The Vision

At the intersection of technology and biology, **RxGenome** empowers patients and healthcare providers by turning raw, complex medical data into actionable biological insights. 

Built in 24 hours for **BACSA Hacks**, RxGenome tackles the Open Challenge by addressing both **Disease Detection** and **Health Improvement**. It serves as a precision-medicine interpretation assistant—combining machine learning for genomic risk prediction, multimodal AI for report understanding, and evidence-based pharmacogenomic (PGx) rules to flag dangerous medication interactions.

> ⚠️ **Educational Tool Only** — RxGenome is a demonstration of applied health-tech and is not a diagnostic device. All results should be discussed with a qualified healthcare provider.

<img width="2559" height="1307" alt="image" src="https://github.com/user-attachments/assets/70735e88-2821-43df-9d31-dcf0704b1dab" />

---

## ✨ Key Features

### 🧬 Explainable Disease Detection
- **Machine Learning Analysis:** Utilizes a trained XGBoost classifier over genomic/SNP-style feature matrices to accurately predict disease risk probability.
- **Biological Context:** Instead of black-box predictions, RxGenome provides an explainable Feature Importance chart, mapping statistical anomalies back to standard HGNC gene symbols (e.g., `BRCA1`, `TP53`, `PIK3CA`).

<img width="2539" height="1303" alt="image" src="https://github.com/user-attachments/assets/8f970596-8878-4b79-9eb7-01eec6c940b9" />

### 💊 Health Improvement via Pharmacogenomics (PGx)
- **Medication Safety:** Cross-references a patient's prescription data against FDA and CPIC guidelines.
- **Metabolizer Alerts:** Flags severe gene-drug interactions (e.g., *CYP2D6* poor metabolizers taking Tamoxifen), generating specific discussion points to prevent adverse drug events.

<img width="1228" height="676" alt="image" src="https://github.com/user-attachments/assets/8f9e73cb-f3ca-4beb-bc94-1342f4f7220f" />

### 📋 Multimodal Report Understanding
- **AI-Powered Extraction:** Integrates Google Gemini (2.0 Flash / 2.5 Pro) to physically read unstructured medical PDFs and lab report images.
- **Smart Formatting:** Automatically extracts vital lab values, identifies units and reference ranges, and flags abnormal biomarkers.

<img width="1376" height="1110" alt="image" src="https://github.com/user-attachments/assets/d8e661e8-c0f8-44f7-9d26-74a4a85ef9da" />

### 🩺 Clinician & Patient Summaries
- **Patient-Friendly Breakdowns:** Dynamically generates an empathetic, 8th-grade reading level summary of the patient's risk profile and PGx alerts.
- **Doctor Discussion Notes:** Auto-generates structured clinical notes, pulling together all extracted lab anomalies, model ROC-AUC confidences, and PGx cautions—equipping patients for their next appointment.

<img width="1387" height="1130" alt="image" src="https://github.com/user-attachments/assets/b6856f28-481a-44b6-a65f-3a9764caf21c" />


---

## 🛠️ The Tech Stack

RxGenome leverages a modern, decoupled architecture designed for speed, accuracy, and responsive UX.

| Layer | Technology |
|-------|-------------|
| **Frontend UI** | Next.js (React), TypeScript, Tailwind CSS, shadcn/ui, Recharts |
| **Backend API** | FastAPI (Python), SQLAlchemy, Pydantic |
| **Database** | SQLite |
| **Machine Learning** | XGBoost, scikit-learn, pandas |
| **Generative AI** | Google Gemini API |

---

## 🔬 How It Works

1. **Input Data:** The user uploads a unified case containing their genomic variant file (CSV/VCF), unstructured lab reports (PDF/Images), and current medication profiles.
2. **Orchestration Pipeline:** The FastAPI backend securely routes the data through four stages:
   - *Genomic Parsing*
   - *Gemini OCR Document Extraction*
   - *Medication Normalization*
   - *XGBoost Risk Prediction*
3. **PGx Evaluation:** The rule engine evaluates the identified genomic variants against the canonical medication sequence.
4. **Synthesis:** Gemini synthesizes the structured output of the ML model, the PGx rules, and the lab arrays into tailored conversational summaries.
5. **Insights Dashboard:** The React frontend renders a beautiful, interactive matrix of the patient's holistic health profile.

<img width="1237" height="1190" alt="image" src="https://github.com/user-attachments/assets/fba0e3c2-9b08-4f10-8070-66cc8a6c995f" />


---


