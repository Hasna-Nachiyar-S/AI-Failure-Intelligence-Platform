"""
Training-data-derived candidate value sampler.

This module generates realistic candidate values from the actual
domain datasets instead of relying only on manually hard-coded values.
"""

import os
from typing import Any, Dict, List

import pandas as pd


BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)


class CandidateSampler:

    DATA_FILES = {
        "Student": os.path.join(
            DATA_DIR,
            "student",
            "student-mat.csv"
        ),
        "Software": os.path.join(
            DATA_DIR,
            "software",
            "Mozilla.csv"
        ),
        "Jobs": os.path.join(
            DATA_DIR,
            "jobs",
            "ai_resume_screening.csv"
        ),
        "Projects": os.path.join(
            DATA_DIR,
            "projects",
            "Project Management Dataset.csv"
        ),
    }

    FEATURE_COLUMNS = {
        "Student": [
            "absences",
            "studytime",
        ],

        "Software": [
            "pr",
            "cl",
            "rp",
            "os",
            "bs",
            "bsr",
        ],

        "Jobs": [
            "skills_match_score",
            "project_count",
            "resume_length",
            "github_activity",
        ],

        "Projects": [
            "Project_Cost",
            "Project_Benefit",
            "Completion",
            "Complexity",
            "Phase",
        ],
    }

    def __init__(self):
        self.cache: Dict[str, pd.DataFrame] = {}

    def normalize_domain(self, domain: str) -> str:

        mapping = {
            "student": "Student",
            "software": "Software",
            "jobs": "Jobs",
            "projects": "Projects",
        }

        value = str(domain).strip().lower()

        if value not in mapping:
            raise ValueError(
                f"Unsupported domain: {domain}"
            )

        return mapping[value]

    def _load_data(self, domain: str) -> pd.DataFrame:

        domain = self.normalize_domain(domain)

        if domain in self.cache:
            return self.cache[domain]

        path = self.DATA_FILES[domain]

        if not os.path.exists(path):
            raise FileNotFoundError(
                f"Dataset not found for {domain}: {path}"
            )

        if domain == "Student":
            df = pd.read_csv(
                path,
                sep=";"
            )

        elif domain == "Software":
            df = pd.read_csv(
                path,
                sep=";"
            )

        else:
            df = pd.read_csv(path)

        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
        )

        self.cache[domain] = df

        return df

    def _column_name(
        self,
        domain: str,
        feature: str
    ) -> str:

        mapping = {
            "Student": {
                "absences": "absences",
                "studytime": "studytime",
            },

            "Software": {
                "pr": "pr",
                "cl": "cl",
                "rp": "rp",
                "os": "os",
                "bs": "bs",
                "bsr": "bsr",
            },

            "Jobs": {
                "skills_match_score": "skills_match_score",
                "project_count": "project_count",
                "resume_length": "resume_length",
                "github_activity": "github_activity",
            },

            "Projects": {
                "Project_Cost": "Project Cost",
                "Project_Benefit": "Project Benefit",
                "Completion": "Completion%",
                "Complexity": "Complexity",
                "Phase": "Phase",
            },
        }

        return mapping[domain].get(
            feature,
            feature
        )

    def sample_values(
        self,
        domain: str,
        feature: str,
        current_value: Any
    ) -> List[Any]:

        domain = self.normalize_domain(domain)

        df = self._load_data(domain)

        column = self._column_name(
            domain,
            feature
        )

        if column not in df.columns:
            return []

        series = df[column].dropna()

        if series.empty:
            return []

        # ---------------------------------------------------------
        # Categorical feature
        # ---------------------------------------------------------

        if not pd.api.types.is_numeric_dtype(series):

            values = (
                series
                .astype(str)
                .str.strip()
                .drop_duplicates()
                .tolist()
            )

            current_text = str(
                current_value
            ).strip()

            return [
                value
                for value in values
                if value != current_text
            ]

        # ---------------------------------------------------------
        # Numeric feature
        # ---------------------------------------------------------

        numeric = pd.to_numeric(
            series,
            errors="coerce"
        ).dropna()

        if numeric.empty:
            return []

        # Use actual dataset quantiles.
        quantiles = [
            0.00,
            0.25,
            0.50,
            0.75,
            1.00,
        ]

        sampled = (
            numeric
            .quantile(quantiles)
            .tolist()
        )

        # Add actual minimum and maximum.
        sampled.extend([
            float(numeric.min()),
            float(numeric.max()),
        ])

        # Remove duplicates.
        unique_values = []

        for value in sampled:

            if pd.isna(value):
                continue

            value = float(value)

            if value not in unique_values:
                unique_values.append(value)

        # Convert integer-like values back to integers.
        cleaned = []

        for value in unique_values:

            if float(value).is_integer():
                cleaned.append(int(value))
            else:
                cleaned.append(round(value, 4))

        # Remove current value.
        try:
            current_numeric = float(
                current_value
            )

            cleaned = [
                value
                for value in cleaned
                if float(value) != current_numeric
            ]

        except (TypeError, ValueError):
            pass

        return cleaned

    def get_candidates(
        self,
        domain: str,
        feature: str,
        current_value: Any
    ) -> List[Any]:

        return self.sample_values(
            domain,
            feature,
            current_value
        )