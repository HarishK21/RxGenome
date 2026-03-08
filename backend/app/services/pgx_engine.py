"""PGx Rule Engine - pharmacogenomic medication caution rules."""

import json
from app.config import PGX_RULES_PATH


def load_pgx_rules():
    """Load PGx rules."""
    with open(PGX_RULES_PATH) as f:
        return json.load(f)


def lookup_pgx(medication: str, genotype: str = None) -> dict:
    """
    Look up pharmacogenomic caution for a medication + genotype combination.
    If no genotype provided, returns the highest-risk finding as demo default.
    """
    rules_data = load_pgx_rules()
    med_lower = medication.strip().lower()

    # Resolve synonyms
    canonical = med_lower
    for canon, synonyms in rules_data.get("medication_synonyms", {}).items():
        if med_lower in [s.lower() for s in synonyms] or med_lower == canon:
            canonical = canon
            break

    # Find matching rule
    for rule in rules_data["rules"]:
        if rule["medication"] == canonical:
            gene = rule["gene"]
            gp_map = rule["genotype_phenotype"]

            if genotype:
                # Look for specific genotype
                for phenotype, data in gp_map.items():
                    if genotype in data["genotypes"]:
                        return {
                            "found": True,
                            "medication": canonical,
                            "gene": gene,
                            "genotype": genotype,
                            "phenotype": phenotype.replace("_", " ").title(),
                            "caution_level": data["caution_level"],
                            "summary": data["summary"],
                            "discussion_points": data["discussion_points"],
                            "evidence": data["evidence"],
                            "disclaimer": rules_data.get("disclaimer", ""),
                        }

            # Default: return poor metabolizer (highest caution for demo)
            poor = gp_map.get("poor_metabolizer", {})
            default_genotype = poor.get("genotypes", ["unknown"])[0]
            return {
                "found": True,
                "medication": canonical,
                "gene": gene,
                "genotype": default_genotype,
                "phenotype": "Poor Metabolizer",
                "caution_level": poor.get("caution_level", "moderate"),
                "summary": poor.get("summary", ""),
                "discussion_points": poor.get("discussion_points", []),
                "evidence": poor.get("evidence", ""),
                "disclaimer": rules_data.get("disclaimer", ""),
            }

    return {
        "found": False,
        "medication": canonical,
        "gene": None,
        "genotype": genotype,
        "phenotype": None,
        "caution_level": "unknown",
        "summary": f"No pharmacogenomic rules found for {canonical}. This does not mean no interaction exists.",
        "discussion_points": ["Consult pharmacist for medication-gene interaction guidance"],
        "evidence": "Not available",
        "disclaimer": rules_data.get("disclaimer", ""),
    }
