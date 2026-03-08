"""Genome parser service - parses CSV/TSV genomic data into feature vectors."""

import os
import pandas as pd
import numpy as np
import json
from app.config import ML_ARTIFACT_DIR


def load_feature_order():
    """Load the expected feature order from ML artifacts."""
    path = os.path.join(ML_ARTIFACT_DIR, "feature_order.json")
    with open(path) as f:
        return json.load(f)


def parse_genome_file(filepath: str) -> dict:
    """
    Parse a genome CSV/TSV file into a feature vector.
    Returns dict with 'features' (ordered dict) and 'metadata'.
    """
    # Detect delimiter
    ext = os.path.splitext(filepath)[1].lower()
    sep = "\t" if ext == ".tsv" else ","

    df = pd.read_csv(filepath, sep=sep)

    feature_order = load_feature_order()

    # If the data has exactly one row (patient sample), use it directly
    if len(df) >= 1:
        row = df.iloc[0]
        features = {}
        missing = []
        for feat in feature_order:
            if feat in row.index:
                val = row[feat]
                features[feat] = float(val) if pd.notna(val) else 0.0
            else:
                features[feat] = 0.0
                missing.append(feat)

        return {
            "features": features,
            "n_features": len(features),
            "n_missing": len(missing),
            "missing_features": missing[:5],  # Only show first 5
            "raw_columns": list(df.columns)[:10],
        }

    raise ValueError("Genome file must contain at least one row of data.")


def parse_demo_genome(persona: str) -> dict:
    """Load pre-seeded demo genome data."""
    from app.config import DEMO_DATA_DIR

    filename_map = {
        "high_risk": "persona_high_risk.csv",
        "low_risk": "persona_low_risk.csv",
        "moderate_risk": "persona_moderate_risk.csv",
    }

    filename = filename_map.get(persona, "persona_high_risk.csv")
    filepath = os.path.join(DEMO_DATA_DIR, filename)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Demo genome file not found: {filepath}")

    return parse_genome_file(filepath)
