"""Medication normalizer service."""

import json
import os
from app.config import PGX_RULES_PATH


def load_pgx_rules():
    """Load PGx rules from JSON."""
    with open(PGX_RULES_PATH) as f:
        return json.load(f)


def normalize_medication(raw_name: str) -> dict:
    """
    Normalize a medication name to canonical form.
    Returns canonical name and whether PGx rules exist.
    """
    rules_data = load_pgx_rules()
    name_lower = raw_name.strip().lower()

    # Check direct match
    for rule in rules_data["rules"]:
        if rule["medication"] == name_lower:
            return {
                "canonical_name": rule["medication"],
                "has_pgx_rule": True,
                "gene": rule["gene"],
            }

    # Check synonyms
    for canonical, synonyms in rules_data.get("medication_synonyms", {}).items():
        if name_lower in [s.lower() for s in synonyms]:
            return {
                "canonical_name": canonical,
                "has_pgx_rule": True,
                "gene": next(r["gene"] for r in rules_data["rules"] if r["medication"] == canonical),
            }

    # No match found
    return {
        "canonical_name": name_lower,
        "has_pgx_rule": False,
        "gene": None,
    }
