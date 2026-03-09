# RxGenome - BACSA Hacks 2026 Presentation Script

**Estimated Time:** 2-3 minutes
**Tips:** 
- Keep a steady pace.
- Emphasize the bolded words.
- Click through the UI as you speak the corresponding lines.

---

### 1. Introduction & The Problem (0:00 - 0:30)

"Hi everyone, we are excited to present **RxGenome**.

At this hackathon, we were challenged to find solutions at the intersection of technology and biology. We decided to tackle both **Disease Detection** and **Health Improvement**. 

Today, personalized medicine is broken. Genomic data, unstructured lab reports, and medication histories are completely siloed. Patients don't understand their raw data, and doctors simply don't have the time to synthesize thousands of genomic variants against complex pharmacological guidelines during a 15-minute consultation.

To solve this, we built **RxGenome**—a precision-medicine interpretation assistant."

### 2. The Solution & Case Creation (0:30 - 1:00)

*(Action: Have the RxGenome "Create Case" page open on screen)*

"Our platform allows patients or clinicians to upload their combined health profile. 

*(Action: Type in a dummy name and condition, and enter 'Tamoxifen' as the medication)*

As we create a new case, we input the patient's basic information and current medications—in this case, **Tamoxifen**, a common breast cancer drug. 

*(Action: Click 'Create Case & Continue'. On the upload screen, drag and drop a dummy genome CSV and a medical report image)*

Next, we upload the raw genomic variant data alongside an unstructured image of a recent medical lab report. When we hit 'Continue to Analysis', our **FastAPI** backend orchestrates a complex, four-stage analytical pipeline."

*(Action: Click 'Continue to Analysis' to show the processing loader)*

### 3. Disease Detection - Machine Learning (1:00 - 1:30)

*(Action: Once the Results page loads, point to the Disease Risk Score and the Features tab)*

"For **Disease Detection**, we trained an **XGBoost machine learning classifier** on genomic dataset features. 

But in healthcare, black-box AI is unacceptable. That's why RxGenome provides **Explainable AI**. If you look at the 'Features' tab, we map statistical anomalies back to standard biological gene symbols—like BRCA1 or TP53—so clinicians know exactly *why* a risk probability was assigned."

### 4. Health Improvement - Pharmacogenomics (1:30 - 2:00)

*(Action: Click on the 'PGx' tab)*

"For **Health Improvement**, we implemented a Pharmacogenomic—or **PGx**—rules engine. 

RxGenome automatically cross-references the patient's genomic profile against FDA and CPIC guidelines. Here, the system has successfully flagged a **High Caution** interaction: our patient is a poor metabolizer of the CYP2D6 enzyme, which drastically reduces the efficacy of their Tamoxifen prescription. By catching this, we directly prevent adverse drug events and improve patient outcomes."

### 5. Multimodal AI & Conclusion (2:00 - 2:30)

*(Action: Click on the 'Report' tab, then the 'Doctor Note' tab)*

"Finally, we integrated **Google Gemini 2.0**. It acts as our multimodal OCR agent, physically 'reading' the unstructured lab report image we uploaded to extract and flag abnormal medical biomarkers. 

Gemini then synthesizes the ML disease risk, the PGx medication alerts, and the lab arrays into an empathic, 8th-grade reading level summary for the patient, alongside a structured discussion note for the doctor.

Built with Next.js, FastAPI, XGBoost, and Gemini, **RxGenome** transforms raw biology into actionable, life-saving insights. Thank you."
