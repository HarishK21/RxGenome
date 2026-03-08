"""
RxGenome ML Training Pipeline
Trains disease risk models on tabular biomedical data (Breast Cancer Wisconsin style).
Produces model artifacts, feature importance, and evaluation metrics.
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
from xgboost import XGBClassifier

# Output directory for model artifacts
ARTIFACT_DIR = os.path.join(os.path.dirname(__file__), "artifacts")
os.makedirs(ARTIFACT_DIR, exist_ok=True)


def load_data():
    """Load Breast Cancer Wisconsin dataset and frame as genomic-style feature matrix."""
    data = load_breast_cancer()
    df = pd.DataFrame(data.data, columns=data.feature_names)
    df["target"] = data.target  # 1 = benign, 0 = malignant

    # Rename columns to genomic-style nomenclature for demo
    genomic_names = {
        "mean radius": "SNP_BRCA1_radius",
        "mean texture": "SNP_TP53_texture",
        "mean perimeter": "SNP_CHEK2_perimeter",
        "mean area": "SNP_ATM_area",
        "mean smoothness": "SNP_PALB2_smoothness",
        "mean compactness": "SNP_CDH1_compactness",
        "mean concavity": "SNP_PTEN_concavity",
        "mean concave points": "SNP_STK11_concave_pts",
        "mean symmetry": "SNP_RAD51_symmetry",
        "mean fractal dimension": "SNP_BARD1_fractal",
        "radius error": "SNP_BRIP1_radius_se",
        "texture error": "SNP_RAD51C_texture_se",
        "perimeter error": "SNP_RAD51D_perim_se",
        "area error": "SNP_NBN_area_se",
        "smoothness error": "SNP_MRE11_smooth_se",
        "compactness error": "SNP_NF1_compact_se",
        "concavity error": "SNP_RB1_concav_se",
        "concave points error": "SNP_APC_cp_se",
        "symmetry error": "SNP_MLH1_symm_se",
        "fractal dimension error": "SNP_MSH2_fract_se",
        "worst radius": "SNP_BRCA2_radius_w",
        "worst texture": "SNP_ERBB2_texture_w",
        "worst perimeter": "SNP_PIK3CA_perim_w",
        "worst area": "SNP_MAP3K1_area_w",
        "worst smoothness": "SNP_GATA3_smooth_w",
        "worst compactness": "SNP_CDK12_compact_w",
        "worst concavity": "SNP_ESR1_concav_w",
        "worst concave points": "SNP_PGR_cp_w",
        "worst symmetry": "SNP_FOXA1_symm_w",
        "worst fractal dimension": "SNP_MYC_fract_w",
    }
    df = df.rename(columns=genomic_names)
    return df


def train_models(df: pd.DataFrame):
    """Train baseline and final models, return results."""
    feature_cols = [c for c in df.columns if c != "target"]
    X = df[feature_cols]
    y = df["target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    results = {}

    # 1. Logistic Regression baseline
    lr = LogisticRegression(max_iter=10000, random_state=42)
    lr.fit(X_train, y_train)
    lr_pred = lr.predict(X_test)
    lr_proba = lr.predict_proba(X_test)[:, 1]
    results["logistic_regression"] = {
        "accuracy": float(accuracy_score(y_test, lr_pred)),
        "roc_auc": float(roc_auc_score(y_test, lr_proba)),
    }
    joblib.dump(lr, os.path.join(ARTIFACT_DIR, "logistic_regression.joblib"))

    # 2. RandomForest baseline
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    rf_pred = rf.predict(X_test)
    rf_proba = rf.predict_proba(X_test)[:, 1]
    results["random_forest"] = {
        "accuracy": float(accuracy_score(y_test, rf_pred)),
        "roc_auc": float(roc_auc_score(y_test, rf_proba)),
    }
    joblib.dump(rf, os.path.join(ARTIFACT_DIR, "random_forest.joblib"))

    # 3. XGBoost final model
    xgb = XGBClassifier(
        n_estimators=200,
        max_depth=5,
        learning_rate=0.1,
        random_state=42,
        use_label_encoder=False,
        eval_metric="logloss",
    )
    xgb.fit(X_train, y_train)
    xgb_pred = xgb.predict(X_test)
    xgb_proba = xgb.predict_proba(X_test)[:, 1]
    results["xgboost"] = {
        "accuracy": float(accuracy_score(y_test, xgb_pred)),
        "roc_auc": float(roc_auc_score(y_test, xgb_proba)),
    }
    joblib.dump(xgb, os.path.join(ARTIFACT_DIR, "xgboost_final.joblib"))

    # Feature importance from XGBoost
    importances = xgb.feature_importances_
    feature_importance = sorted(
        zip(feature_cols, importances.tolist()),
        key=lambda x: x[1],
        reverse=True,
    )

    # Save feature order
    with open(os.path.join(ARTIFACT_DIR, "feature_order.json"), "w") as f:
        json.dump(feature_cols, f, indent=2)

    # Save feature importance
    with open(os.path.join(ARTIFACT_DIR, "feature_importance.json"), "w") as f:
        json.dump(
            [{"feature": name, "importance": imp} for name, imp in feature_importance],
            f,
            indent=2,
        )

    # Save metrics
    with open(os.path.join(ARTIFACT_DIR, "metrics.json"), "w") as f:
        json.dump(results, f, indent=2)

    # Save training summary
    summary = {
        "dataset": "Breast Cancer Wisconsin (genomic-renamed)",
        "n_samples": len(df),
        "n_features": len(feature_cols),
        "split": "80/20 stratified",
        "train_size": len(X_train),
        "test_size": len(X_test),
        "models": results,
        "best_model": "xgboost",
        "best_roc_auc": results["xgboost"]["roc_auc"],
    }
    with open(os.path.join(ARTIFACT_DIR, "training_summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

    print("Training complete!")
    print(f"  Logistic Regression - Acc: {results['logistic_regression']['accuracy']:.4f}, AUC: {results['logistic_regression']['roc_auc']:.4f}")
    print(f"  RandomForest       - Acc: {results['random_forest']['accuracy']:.4f}, AUC: {results['random_forest']['roc_auc']:.4f}")
    print(f"  XGBoost (final)    - Acc: {results['xgboost']['accuracy']:.4f}, AUC: {results['xgboost']['roc_auc']:.4f}")
    print(f"\nTop 5 features:")
    for name, imp in feature_importance[:5]:
        print(f"  {name}: {imp:.4f}")

    return results


def generate_demo_samples():
    """Generate seeded demo samples for the demo personas."""
    data = load_breast_cancer()
    df = pd.DataFrame(data.data, columns=data.feature_names)
    df["target"] = data.target

    # Rename to genomic-style
    genomic_names = {
        "mean radius": "SNP_BRCA1_radius",
        "mean texture": "SNP_TP53_texture",
        "mean perimeter": "SNP_CHEK2_perimeter",
        "mean area": "SNP_ATM_area",
        "mean smoothness": "SNP_PALB2_smoothness",
        "mean compactness": "SNP_CDH1_compactness",
        "mean concavity": "SNP_PTEN_concavity",
        "mean concave points": "SNP_STK11_concave_pts",
        "mean symmetry": "SNP_RAD51_symmetry",
        "mean fractal dimension": "SNP_BARD1_fractal",
        "radius error": "SNP_BRIP1_radius_se",
        "texture error": "SNP_RAD51C_texture_se",
        "perimeter error": "SNP_RAD51D_perim_se",
        "area error": "SNP_NBN_area_se",
        "smoothness error": "SNP_MRE11_smooth_se",
        "compactness error": "SNP_NF1_compact_se",
        "concavity error": "SNP_RB1_concav_se",
        "concave points error": "SNP_APC_cp_se",
        "symmetry error": "SNP_MLH1_symm_se",
        "fractal dimension error": "SNP_MSH2_fract_se",
        "worst radius": "SNP_BRCA2_radius_w",
        "worst texture": "SNP_ERBB2_texture_w",
        "worst perimeter": "SNP_PIK3CA_perim_w",
        "worst area": "SNP_MAP3K1_area_w",
        "worst smoothness": "SNP_GATA3_smooth_w",
        "worst compactness": "SNP_CDK12_compact_w",
        "worst concavity": "SNP_ESR1_concav_w",
        "worst concave points": "SNP_PGR_cp_w",
        "worst symmetry": "SNP_FOXA1_symm_w",
        "worst fractal dimension": "SNP_MYC_fract_w",
    }
    df = df.rename(columns=genomic_names)

    demo_dir = os.path.join(os.path.dirname(__file__), "..", "data", "demo")
    os.makedirs(demo_dir, exist_ok=True)

    # Persona 1: High risk (malignant sample)
    malignant = df[df["target"] == 0].iloc[0:1].drop(columns=["target"])
    malignant.to_csv(os.path.join(demo_dir, "persona_high_risk.csv"), index=False)

    # Persona 2: Low risk (benign sample)
    benign = df[df["target"] == 1].iloc[0:1].drop(columns=["target"])
    benign.to_csv(os.path.join(demo_dir, "persona_low_risk.csv"), index=False)

    # Persona 3: Moderate risk (borderline sample - from near decision boundary)
    # Use a sample with moderate feature values
    moderate_idx = df.iloc[50:51].drop(columns=["target"])
    moderate_idx.to_csv(os.path.join(demo_dir, "persona_moderate_risk.csv"), index=False)

    # Full training dataset
    df.to_csv(os.path.join(demo_dir, "full_dataset.csv"), index=False)

    print(f"Demo samples saved to {demo_dir}")


if __name__ == "__main__":
    df = load_data()
    train_models(df)
    generate_demo_samples()
