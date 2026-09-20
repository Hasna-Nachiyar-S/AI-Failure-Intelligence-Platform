"""Domain-aware constraints for counterfactual intervention generation."""
from typing import Any, Dict, List, Tuple

class DomainConstraintEngine:
    CONFIG: Dict[str, Dict[str, Any]] = {
        "Student": {
            "actionable": {
                "absences": {"type": "range", "min": 0, "max": 93},
                "studytime": {"type": "values", "values": [1, 2, 3, 4]},
            },
            "non_actionable": ["failures", "G1", "G2"],
        },
        "Jobs": {
            "actionable": {
                "skills_match_score": {"type": "range", "min": 0, "max": 100},
                "project_count": {"type": "range", "min": 0, "max": 100},
                "resume_length": {"type": "range", "min": 0, "max": 10000},
                "github_activity": {"type": "range", "min": 0, "max": 100},
            },
            "non_actionable": ["years_experience", "education_level"],
        },
        "Software": {
            "actionable": {
                "pr": {"type": "range", "min": 0}, "cl": {"type": "range", "min": 0},
                "rp": {"type": "range", "min": 0}, "os": {"type": "range", "min": 0},
                "bs": {"type": "range", "min": 0}, "bsr": {"type": "range", "min": 0},
            },
            "non_actionable": ["pd", "co", "re", "at"],
        },
        "Projects": {
            "actionable": {
                "Project_Cost": {"type": "range", "min": 0},
                "Project_Benefit": {"type": "range", "min": 0},
                "Completion": {"type": "range", "min": 0, "max": 100},
                "Complexity": {"type": "numeric_range", "min": 0},
                "Phase": {"type": "categorical"},
            },
            "non_actionable": ["Project_Type", "Region", "Department", "Year", "Month"],
        },
    }

    def normalize_domain(self, domain: str) -> str:
        value = str(domain).strip().lower()
        mapping = {d.lower(): d for d in self.CONFIG}
        if value not in mapping:
            raise ValueError(f"Unsupported domain: {domain}")
        return mapping[value]

    def actionable_features(self, domain: str) -> List[str]:
        return list(self.CONFIG[self.normalize_domain(domain)]["actionable"].keys())

    def non_actionable_features(self, domain: str) -> List[str]:
        return list(self.CONFIG[self.normalize_domain(domain)]["non_actionable"])

    def validate_change(self, domain: str, feature: str, value: Any) -> Tuple[bool, str]:
        domain = self.normalize_domain(domain)
        config = self.CONFIG[domain]
        if feature not in config["actionable"]:
            return False, f"Feature '{feature}' is not actionable in {domain}."
        rule = config["actionable"][feature]
        if rule["type"] == "categorical":
            return True, "Valid categorical action."
        try:
            numeric = float(value)
        except (TypeError, ValueError):
            return False, f"Value for '{feature}' must be numeric."
        if rule["type"] == "values" and numeric not in rule["values"]:
            return False, f"Value {value} is outside the allowed values for '{feature}'."
        if "min" in rule and numeric < rule["min"]:
            return False, f"Value {value} is below the minimum for '{feature}'."
        if "max" in rule and numeric > rule["max"]:
            return False, f"Value {value} is above the maximum for '{feature}'."
        return True, "Valid constrained value."

    def filter_changes(self, domain: str, changes: Dict[str, Any]) -> Tuple[bool, List[str]]:
        reasons = []
        for feature, value in changes.items():
            ok, reason = self.validate_change(domain, feature, value)
            if not ok:
                reasons.append(reason)
        return not reasons, reasons

    def describe(self, domain: str) -> Dict[str, Any]:
        domain = self.normalize_domain(domain)
        return {"domain": domain, "actionable_features": self.actionable_features(domain),
                "non_actionable_features": self.non_actionable_features(domain),
                "constraints": self.CONFIG[domain]["actionable"]}
