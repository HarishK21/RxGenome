"""Disease model inference service."""

import os
import json
import joblib
import numpy as np
from app.config import ML_ARTIFACT_DIR

# Biological context for features (for explainability)
FEATURE_BIO_CONTEXT = {
    "SNP_BRCA1_radius": "BRCA1 gene variant — associated with DNA repair and tumor suppression",
    "SNP_TP53_texture": "TP53 gene variant — key tumor suppressor, 'guardian of the genome'",
    "SNP_CHEK2_perimeter": "CHEK2 gene variant — DNA damage checkpoint kinase",
    "SNP_ATM_area": "ATM gene variant — DNA double-strand break repair signaling",
    "SNP_PALB2_smoothness": "PALB2 gene variant — partner of BRCA2 in DNA repair",
    "SNP_CDH1_compactness": "CDH1 gene variant — cell adhesion molecule, lobular carcinoma risk",
    "SNP_PTEN_concavity": "PTEN gene variant — phosphatase and tumor suppressor",
    "SNP_STK11_concave_pts": "STK11 gene variant — serine/threonine kinase, Peutz-Jeghers syndrome",
    "SNP_BRCA2_radius_w": "BRCA2 gene variant — homologous recombination DNA repair",
    "SNP_ERBB2_texture_w": "ERBB2/HER2 gene variant — growth factor receptor",
    "SNP_PIK3CA_perim_w": "PIK3CA gene variant — PI3K signaling pathway",
    "SNP_ESR1_concav_w": "ESR1 gene variant — estrogen receptor alpha",
    "SNP_PGR_cp_w": "PGR gene variant — progesterone receptor",
}


def load_model(model_name: str = "xgboost"):
    """Load a trained model artifact."""
    model_files = {
        "xgboost": "xgboost_final.joblib",
        "random_forest": "random_forest.joblib",
        "logistic_regression": "logistic_regression.joblib",
    }
    filename = model_files.get(model_name, "xgboost_final.joblib")
    path = os.path.join(ML_ARTIFACT_DIR, filename)
    return joblib.load(path)


def load_metrics():
    """Load model evaluation metrics."""
    path = os.path.join(ML_ARTIFACT_DIR, "metrics.json")
    with open(path) as f:
        return json.load(f)


def load_feature_importance():
    """Load precomputed feature importance."""
    path = os.path.join(ML_ARTIFACT_DIR, "feature_importance.json")
    with open(path) as f:
        return json.load(f)


def load_feature_order():
    """Load feature order."""
    path = os.path.join(ML_ARTIFACT_DIR, "feature_order.json")
    with open(path) as f:
        return json.load(f)


def predict(features: dict, model_name: str = "xgboost") -> dict:
    """
    Run disease risk prediction on a feature vector.
    Returns risk score, tier, and top contributing features.
    """
    model = load_model(model_name)
    feature_order = load_feature_order()
    metrics = load_metrics()

    # Build input vector in correct order
    X = np.array([[features.get(f, 0.0) for f in feature_order]])

    # Get risk probability
    proba = model.predict_proba(X)[0]
    # In our encoding: 0=malignant, 1=benign
    # Risk score = probability of malignant (class 0)
    risk_score = float(proba[0])

    # Determine risk tier
    if risk_score >= 0.7:
        risk_tier = "high"
    elif risk_score >= 0.3:
        risk_tier = "moderate"
    else:
        risk_tier = "low"

    # Get feature importance with biological context
    feature_imp = load_feature_importance()
    top_features = []
    for fi in feature_imp[:10]:
        feat_name = fi["feature"]
        top_features.append({
            "feature": feat_name,
            "importance": fi["importance"],
            "value": features.get(feat_name, 0.0),
            "biological_context": FEATURE_BIO_CONTEXT.get(feat_name, "Genomic feature variant"),
        })

    model_metrics = metrics.get(model_name, metrics.get("xgboost", {}))

    return {
        "model_name": model_name,
        "risk_score": round(risk_score, 4),
        "risk_tier": risk_tier,
        "accuracy": model_metrics.get("accuracy", 0.0),
        "roc_auc": model_metrics.get("roc_auc", 0.0),
        "feature_importance": top_features,
    }
