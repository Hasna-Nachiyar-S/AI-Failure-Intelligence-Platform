"""
Failure Profile Identification using K-Means.

This module:
1. Loads a domain dataset.
2. Selects numerical analysis features.
3. Preprocesses the features.
4. Creates K-Means failure profiles.
5. Calculates profile-level failure statistics where
   the target definition is available.
6. Assigns a new case to the closest profile.

Important:
K-Means profiles are descriptive clusters. They do not
establish causal relationships between features and failure.
"""

import os
from typing import Any, Dict, List

import numpy as np
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

class FailureProfileAnalyzer:

    # Project paths

    BASE_DIR = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            ".."
        )
    )

    DATA_DIR = os.path.join(
        BASE_DIR,
        "data"
    )

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

    # Features used for clustering

    FEATURES = {

        "Student": [
            "absences",
            "studytime",
            "failures",
            "G1",
            "G2",
        ],

        "Software": [
            "ct",
            "sd",
            "dt",
            "cl",
            "pd",
            "co",
            "rp",
            "bs",
            "pr",
            "bsr",
        ],

        "Jobs": [
            "years_experience",
            "skills_match_score",
            "project_count",
            "resume_length",
            "github_activity",
        ],

        "Projects": [
            "Project Cost",
            "Project Benefit",
            "Completion%",
            "Year",
            "Month",
        ],
    }

    # Constructor

    def __init__(
        self,
        n_clusters: int = 3,
        random_state: int = 42
    ):

        self.n_clusters = n_clusters

        self.random_state = random_state

        self.models: Dict[
            str,
            KMeans
        ] = {}

        self.scalers: Dict[
            str,
            StandardScaler
        ] = {}

        self.datasets: Dict[
            str,
            pd.DataFrame
        ] = {}

        self.profile_descriptions: Dict[
            str,
            List[Dict[str, Any]]
        ] = {}

        # Deterministic encodings for categorical clustering features.
        self.category_maps: Dict[str, Dict[str, Dict[str, int]]] = {}

    # Domain normalization

    def normalize_domain(
        self,
        domain: str
    ) -> str:

        mapping = {
            "student": "Student",
            "software": "Software",
            "jobs": "Jobs",
            "projects": "Projects",
        }

        value = str(
            domain
        ).strip().lower()

        if value not in mapping:

            raise ValueError(
                f"Unsupported domain: {domain}"
            )

        return mapping[value]

    # Load dataset

    def load_data(self, domain: str) -> pd.DataFrame:
        domain = self.normalize_domain(domain)
        if domain in self.datasets:
            return self.datasets[domain]

        path = self.DATA_FILES[domain]
        if not os.path.exists(path):
            raise FileNotFoundError(f"Dataset not found for {domain}: {path}")

        separator = ";" if domain in {"Student", "Software"} else ","
        df = pd.read_csv(path, sep=separator)
        df.columns = df.columns.astype(str).str.strip()

        if domain == "Projects":
            numeric_columns = {
                "Project Cost": ",",
                "Project Benefit": ",",
                "Completion%": "%",
                "Year": ",",
                "Month": ",",
            }
            for column, marker in numeric_columns.items():
                if column in df:
                    values = df[column].astype(str).str.strip()
                    df[column] = pd.to_numeric(
                        values.str.replace(marker, "", regex=False),
                        errors="coerce",
                    )

        self.datasets[domain] = df
        return df

    # Prepare clustering features

    def prepare_features(self, domain: str):
        domain = self.normalize_domain(domain)
        df = self.load_data(domain)
        features = [name for name in self.FEATURES[domain] if name in df.columns]
        if not features:
            raise ValueError(
                f"No clustering features found for {domain}. "
                f"Available columns: {list(df.columns)}"
            )

        X = df[features].copy()
        category_maps = self.category_maps.setdefault(domain, {})

        for column in X:
            numeric = pd.to_numeric(X[column], errors="coerce")
            if numeric.notna().mean() >= 0.8:
                fill_value = numeric.median()
                X[column] = numeric.fillna(0 if pd.isna(fill_value) else fill_value)
                continue

            values = X[column].astype(str).str.strip().replace(
                {"": np.nan, "nan": np.nan, "None": np.nan}
            )
            categories = sorted(values.dropna().unique().tolist())
            mapping = {str(value): index for index, value in enumerate(categories)}
            category_maps[column] = mapping
            encoded = values.map(lambda value: mapping.get(str(value), np.nan))
            mode = encoded.mode(dropna=True)
            X[column] = encoded.fillna(float(mode.iloc[0]) if not mode.empty else 0.0)

        if X.shape[1] == 0:
            raise ValueError(f"No usable clustering features for {domain}.")
        return X

    # Determine failure target

    def add_failure_target(self, domain: str, df: pd.DataFrame) -> pd.DataFrame:
        """Add the domain's existing binary failure definition."""
        domain = self.normalize_domain(domain)
        result = df.copy()
        result["_failure"] = np.nan

        target_columns = {
            "Student": "G3",
            "Jobs": "shortlisted",
            "Software": "rs",
            "Projects": "Status",
        }
        column = target_columns[domain]
        if column not in result:
            return result

        values = result[column]
        if domain == "Student":
            values = pd.to_numeric(values, errors="coerce")
            valid = values.notna()
            failures = values < 10
        else:
            values = values.astype(str).str.strip().str.lower()
            if domain == "Jobs":
                valid = values.isin(["yes", "no"])
                failures = values.eq("no")
            elif domain == "Software":
                valid = result[column].notna() & values.ne("") & values.ne("nan")
                failures = values.ne("fixed")
            else:
                valid = result[column].notna()
                failures = values.ne("completed")

        result.loc[valid, "_failure"] = failures.loc[valid].astype(int)
        return result

    # Fit K-Means

    def fit(self, domain: str) -> Dict[str, Any]:
        domain = self.normalize_domain(domain)
        X = self.prepare_features(domain)
        working_df = self.add_failure_target(domain, self.load_data(domain))

        if len(X) != len(working_df):
            raise ValueError("Feature rows and dataset rows are not aligned.")

        cluster_count = min(self.n_clusters, len(X))
        if cluster_count < 2:
            raise ValueError(f"Not enough records to create failure profiles for {domain}.")

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        model = KMeans(n_clusters=cluster_count, random_state=self.random_state, n_init=10)
        labels = model.fit_predict(X_scaled)

        self.models[domain] = model
        self.scalers[domain] = scaler
        working_df["_profile_id"] = labels

        profiles = []
        for cluster_id in sorted(np.unique(labels)):
            mask = labels == cluster_id
            rows = X.loc[mask]
            source_rows = working_df.loc[mask, X.columns]
            means = rows.mean()
            medians = rows.median()
            modes = {}
            for feature in X.columns:
                values = source_rows[feature].dropna()
                if not values.empty:
                    value = values.mode().iloc[0]
                    modes[feature] = value.item() if isinstance(value, np.generic) else value

            target = working_df.loc[mask, "_failure"].dropna()
            failure_count = int(target.eq(1).sum()) if not target.empty else None
            non_failure_count = int(target.eq(0).sum()) if not target.empty else None
            failure_rate = (
                failure_count / (failure_count + non_failure_count)
                if target.empty is False and failure_count + non_failure_count
                else None
            )

            profiles.append({
                "profile_id": int(cluster_id),
                "sample_count": len(rows),
                "feature_means": {key: round(float(value), 4) for key, value in means.items()},
                "feature_medians": {key: round(float(value), 4) for key, value in medians.items()},
                "feature_modes": modes,
                "failure_available": failure_rate is not None,
                "failure_count": failure_count,
                "non_failure_count": non_failure_count,
                "failure_rate": round(failure_rate, 4) if failure_rate is not None else None,
                "failure_rate_percentage": round(failure_rate * 100, 2) if failure_rate is not None else None,
            })

        self.profile_descriptions[domain] = profiles
        return {
            "domain": domain,
            "cluster_count": cluster_count,
            "sample_count": len(X),
            "features": list(X.columns),
            "failure_statistics_available": any(profile["failure_available"] for profile in profiles),
            "profiles": profiles,
        }

    # Ensure model is fitted

    def _ensure_fitted(
        self,
        domain: str
    ):

        domain = self.normalize_domain(
            domain
        )

        if domain not in self.models:

            self.fit(
                domain
            )

    # Identify profile for a new case

    def predict_profile(self, domain: str, data: Dict[str, Any]) -> Dict[str, Any]:
        domain = self.normalize_domain(domain)
        self._ensure_fitted(domain)
        X = self.prepare_features(domain)
        row = {}

        for feature in X.columns:
            value = data.get(feature)
            if value is None:
                value = X[feature].median()

            mapping = self.category_maps.get(domain, {}).get(feature)
            if mapping is not None:
                value = mapping.get(str(value).strip())
                if value is None:
                    value = X[feature].mode(dropna=True)
                    value = float(value.iloc[0]) if not value.empty else 0.0
            else:
                try:
                    value = float(value)
                except (TypeError, ValueError):
                    value = X[feature].median()
            row[feature] = value

        case = pd.DataFrame([row], columns=X.columns)
        scaled = self.scalers[domain].transform(case)
        model = self.models[domain]
        cluster_id = int(model.predict(scaled)[0])
        distance = float(model.transform(scaled)[0][cluster_id])
        profile = next(
            (item for item in self.profile_descriptions[domain]
             if item["profile_id"] == cluster_id),
            None,
        )
        return {
            "domain": domain,
            "profile_id": cluster_id,
            "distance_to_profile": round(distance, 6),
            "profile": profile,
        }

    # Get all profiles

    def get_profiles(self, domain: str) -> Dict[str, Any]:
        domain = self.normalize_domain(domain)
        self._ensure_fitted(domain)
        profiles = self.profile_descriptions[domain]
        return {
            "domain": domain,
            "cluster_count": len(profiles),
            "failure_statistics_available": any(
                profile["failure_available"] for profile in profiles
            ),
            "profiles": profiles,
        }
