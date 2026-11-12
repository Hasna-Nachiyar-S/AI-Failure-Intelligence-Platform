"""Sample realistic counterfactual values from the domain datasets."""

import os
from typing import Any

import pandas as pd


DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data"))


class CandidateSampler:
    DATA_FILES = {
        "Student": os.path.join(DATA_DIR, "student", "student-mat.csv"),
        "Software": os.path.join(DATA_DIR, "software", "Mozilla.csv"),
        "Jobs": os.path.join(DATA_DIR, "jobs", "ai_resume_screening.csv"),
        "Projects": os.path.join(DATA_DIR, "projects", "Project Management Dataset.csv"),
    }
    COLUMN_NAMES = {
        "Student": {"absences": "absences", "studytime": "studytime"},
        "Software": {key: key for key in ("pr", "cl", "rp", "os", "bs", "bsr")},
        "Jobs": {
            key: key
            for key in ("skills_match_score", "project_count", "resume_length", "github_activity")
        },
        "Projects": {
            "Project_Cost": "Project Cost",
            "Project_Benefit": "Project Benefit",
            "Completion": "Completion%",
            "Complexity": "Complexity",
            "Phase": "Phase",
        },
    }
    DOMAIN_NAMES = {name.lower(): name for name in DATA_FILES}

    def __init__(self):
        self.cache: dict[str, pd.DataFrame] = {}

    @classmethod
    def normalize_domain(cls, domain: str) -> str:
        value = cls.DOMAIN_NAMES.get(str(domain).strip().lower())
        if value is None:
            raise ValueError(f"Unsupported domain: {domain}")
        return value

    def _load_data(self, domain: str) -> pd.DataFrame:
        domain = self.normalize_domain(domain)
        if domain in self.cache:
            return self.cache[domain]

        path = self.DATA_FILES[domain]
        if not os.path.exists(path):
            raise FileNotFoundError(f"Dataset not found for {domain}: {path}")

        df = pd.read_csv(path, sep=";" if domain in ("Student", "Software") else ",")
        df.columns = df.columns.astype(str).str.strip()

        if domain == "Projects":
            for column in ("Project Cost", "Project Benefit", "Completion%"):
                if column in df.columns:
                    values = df[column].astype(str).str.strip()
                    symbol = "%" if column == "Completion%" else ","
                    df[column] = pd.to_numeric(values.str.replace(symbol, "", regex=False), errors="coerce")

        self.cache[domain] = df
        return df

    def sample_values(self, domain: str, feature: str, current_value: Any) -> list[Any]:
        domain = self.normalize_domain(domain)
        df = self._load_data(domain)
        column = self.COLUMN_NAMES[domain].get(feature, feature)
        if column not in df.columns:
            return []

        series = df[column].dropna()
        if series.empty:
            return []

        if not pd.api.types.is_numeric_dtype(series):
            current_text = str(current_value).strip()
            return [
                value for value in series.astype(str).str.strip().drop_duplicates().tolist()
                if value != current_text
            ]

        numeric = pd.to_numeric(series, errors="coerce").dropna()
        if numeric.empty:
            return []

        sampled = numeric.quantile([0, 0.25, 0.5, 0.75, 1]).tolist()
        sampled.extend((float(numeric.min()), float(numeric.max())))
        cleaned = []
        for value in sampled:
            if pd.isna(value):
                continue
            value = float(value)
            if value not in cleaned:
                cleaned.append(int(value) if value.is_integer() else round(value, 4))

        try:
            current_numeric = float(current_value)
            cleaned = [value for value in cleaned if float(value) != current_numeric]
        except (TypeError, ValueError):
            pass
        return cleaned

    def get_candidates(self, domain: str, feature: str, current_value: Any) -> list[Any]:
        return self.sample_values(domain, feature, current_value)
