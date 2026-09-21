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

    # =========================================================
    # Project paths
    # =========================================================

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

    # =========================================================
    # Features used for clustering
    # =========================================================

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
            "os",
            "bs",
            "rs",
            "pr",
            "bsr",
            "re",
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
            "Complexity",
            "Completion%",
            "Year",
            "Month",
        ],
    }

    # =========================================================
    # Constructor
    # =========================================================

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

    # =========================================================
    # Domain normalization
    # =========================================================

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

    # =========================================================
    # Load dataset
    # =========================================================

    def load_data(
        self,
        domain: str
    ) -> pd.DataFrame:

        domain = self.normalize_domain(
            domain
        )

        # Return cached dataset if already loaded.
        if domain in self.datasets:

            return self.datasets[domain]

        path = self.DATA_FILES[
            domain
        ]

        if not os.path.exists(path):

            raise FileNotFoundError(
                f"Dataset not found for "
                f"{domain}: {path}"
            )

        # Student and Software datasets
        # currently use semicolon separation.
        if domain in [
            "Student",
            "Software"
        ]:

            df = pd.read_csv(
                path,
                sep=";"
            )

        else:

            df = pd.read_csv(
                path
            )

        # Clean column names.
        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
        )

        # Project datasets contain formatted numeric strings such as
        # "3,648,615.00" and "77%". Normalize them before clustering
        # so K-Means does not silently turn them into missing values.
        if domain == "Projects":
            numeric_columns = {
                "Project Cost": ",",
                "Project Benefit": ",",
                "Completion%": "%",
                "Year": ",",
                "Month": ",",
                "Complexity": ",",
            }
            for column, marker in numeric_columns.items():
                if column in df.columns:
                    value = df[column].astype(str).str.strip()
                    value = value.str.replace(marker, "", regex=False)
                    df[column] = pd.to_numeric(value, errors="coerce")

        self.datasets[
            domain
        ] = df

        return df

    # =========================================================
    # Prepare clustering features
    # =========================================================

    def prepare_features(
        self,
        domain: str
    ):

        domain = self.normalize_domain(
            domain
        )

        df = self.load_data(
            domain
        )

        requested_features = (
            self.FEATURES[
                domain
            ]
        )

        # Only use columns that actually
        # exist in the dataset.
        available_features = [
            feature
            for feature in requested_features
            if feature in df.columns
        ]

        if not available_features:

            raise ValueError(
                f"No clustering features "
                f"found for {domain}. "
                f"Available columns: "
                f"{list(df.columns)}"
            )

        X = df[
            available_features
        ].copy()

        # Convert values to numeric.
        for column in X.columns:

            X[column] = pd.to_numeric(
                X[column],
                errors="coerce"
            )

        # Median imputation.
        for column in X.columns:

            median = X[
                column
            ].median()

            if pd.isna(median):

                median = 0

            X[
                column
            ] = X[
                column
            ].fillna(
                median
            )

        # Remove completely unusable columns.
        X = X.dropna(
            axis=1,
            how="all"
        )

        if X.shape[1] == 0:

            raise ValueError(
                f"No usable numerical "
                f"features for {domain}."
            )

        return X

    # =========================================================
    # Determine failure target
    # =========================================================

    def add_failure_target(
        self,
        domain: str,
        df: pd.DataFrame
    ) -> pd.DataFrame:

        domain = self.normalize_domain(
            domain
        )

        result = df.copy()

        result["_failure"] = np.nan

        # -----------------------------------------------------
        # Student
        #
        # G3 < 10 -> Exam Failure
        # G3 >= 10 -> Passed
        # -----------------------------------------------------

        if domain == "Student":

            if "G3" in result.columns:

                g3 = pd.to_numeric(
                    result["G3"],
                    errors="coerce"
                )

                valid = g3.notna()

                result.loc[
                    valid,
                    "_failure"
                ] = (
                    g3.loc[valid] < 10
                ).astype(int)

        # -----------------------------------------------------
        # Jobs
        #
        # shortlisted = No -> Rejected
        # shortlisted = Yes -> Selected
        # -----------------------------------------------------

        elif domain == "Jobs":

            if "shortlisted" in result.columns:

                shortlisted = (
                    result[
                        "shortlisted"
                    ]
                    .astype(str)
                    .str.strip()
                    .str.lower()
                )

                valid = shortlisted.isin(
                    ["yes", "no"]
                )

                result.loc[
                    valid,
                    "_failure"
                ] = (
                    shortlisted.loc[valid]
                    == "no"
                ).astype(int)

        # -----------------------------------------------------
        # Software
        #
        # The project target is rs.
        #
        # We intentionally do not assume that every
        # rs value represents a failure without confirming
        # the target semantics used by the existing model.
        # -----------------------------------------------------

        elif domain == "Software":

            pass

        # -----------------------------------------------------
        # Projects
        #
        # Only explicit "Failed" status is classified as
        # failure. Other statuses are not automatically
        # treated as successful.
        # -----------------------------------------------------

        elif domain == "Projects":

            if "Status" in result.columns:

                status = (
                    result[
                        "Status"
                    ]
                    .astype(str)
                    .str.strip()
                    .str.lower()
                )

                valid = status.notna()

                result.loc[
                    valid,
                    "_failure"
                ] = (
                    status.loc[valid]
                    == "failed"
                ).astype(int)

        return result

    # =========================================================
    # Fit K-Means
    # =========================================================

    def fit(
        self,
        domain: str
    ) -> Dict[str, Any]:

        domain = self.normalize_domain(
            domain
        )

        # -----------------------------------------------------
        # Prepare features
        # -----------------------------------------------------

        X = self.prepare_features(
            domain
        )

        # -----------------------------------------------------
        # Load original dataset
        # -----------------------------------------------------

        df = self.load_data(
            domain
        )

        # -----------------------------------------------------
        # Add target/failure information
        # -----------------------------------------------------

        working_df = self.add_failure_target(
            domain,
            df
        )

        # -----------------------------------------------------
        # Make sure row alignment is preserved.
        # X and working_df originate from the same dataset.
        # -----------------------------------------------------

        if len(X) != len(
            working_df
        ):

            raise ValueError(
                "Feature rows and dataset "
                "rows are not aligned."
            )

        # -----------------------------------------------------
        # Standardize features
        # -----------------------------------------------------

        scaler = StandardScaler()

        X_scaled = scaler.fit_transform(
            X
        )

        # -----------------------------------------------------
        # Determine cluster count
        # -----------------------------------------------------

        cluster_count = min(
            self.n_clusters,
            len(X)
        )

        if cluster_count < 2:

            raise ValueError(
                f"Not enough records to create "
                f"failure profiles for "
                f"{domain}."
            )

        # -----------------------------------------------------
        # K-Means
        # -----------------------------------------------------

        model = KMeans(
            n_clusters=cluster_count,
            random_state=self.random_state,
            n_init=10
        )

        labels = model.fit_predict(
            X_scaled
        )

        # -----------------------------------------------------
        # Store model and scaler
        # -----------------------------------------------------

        self.models[
            domain
        ] = model

        self.scalers[
            domain
        ] = scaler

        # -----------------------------------------------------
        # Store cluster labels
        # -----------------------------------------------------

        working_df[
            "_profile_id"
        ] = labels

        # =====================================================
        # Build profile descriptions
        # =====================================================

        profile_descriptions = []

        for cluster_id in sorted(
            np.unique(labels)
        ):

            # -------------------------------------------------
            # Rows belonging to this cluster
            # -------------------------------------------------

            cluster_mask = (
                labels == cluster_id
            )

            cluster_rows = X.loc[
                cluster_mask
            ]

            # -------------------------------------------------
            # Means
            # -------------------------------------------------

            means = (
                cluster_rows
                .mean()
                .to_dict()
            )

            # -------------------------------------------------
            # Medians
            # -------------------------------------------------

            medians = (
                cluster_rows
                .median()
                .to_dict()
            )

            # -------------------------------------------------
            # Basic profile
            # -------------------------------------------------

            profile = {

                "profile_id":
                    int(cluster_id),

                "sample_count":
                    int(
                        len(
                            cluster_rows
                        )
                    ),

                "feature_means":
                    {
                        key: round(
                            float(value),
                            4
                        )
                        for key, value
                        in means.items()
                    },

                "feature_medians":
                    {
                        key: round(
                            float(value),
                            4
                        )
                        for key, value
                        in medians.items()
                    }
            }

            # =================================================
            # Failure statistics
            # =================================================

            cluster_failure_values = (
                working_df.loc[
                    cluster_mask,
                    "_failure"
                ]
            )

            valid_failure_values = (
                cluster_failure_values
                .dropna()
            )

            # -------------------------------------------------
            # If failure target is available
            # -------------------------------------------------

            if len(
                valid_failure_values
            ) > 0:

                failure_count = int(
                    (
                        valid_failure_values
                        == 1
                    ).sum()
                )

                non_failure_count = int(
                    (
                        valid_failure_values
                        == 0
                    ).sum()
                )

                total_target_records = (
                    failure_count
                    + non_failure_count
                )

                if (
                    total_target_records
                    > 0
                ):

                    failure_rate = (
                        failure_count
                        / total_target_records
                    )

                else:

                    failure_rate = 0.0

                profile[
                    "failure_available"
                ] = True

                profile[
                    "failure_count"
                ] = failure_count

                profile[
                    "non_failure_count"
                ] = non_failure_count

                profile[
                    "failure_rate"
                ] = round(
                    failure_rate,
                    4
                )

                profile[
                    "failure_rate_percentage"
                ] = round(
                    failure_rate * 100,
                    2
                )

            # -------------------------------------------------
            # No target available
            # -------------------------------------------------

            else:

                profile[
                    "failure_available"
                ] = False

                profile[
                    "failure_count"
                ] = None

                profile[
                    "non_failure_count"
                ] = None

                profile[
                    "failure_rate"
                ] = None

                profile[
                    "failure_rate_percentage"
                ] = None

            # -------------------------------------------------
            # Add profile
            # -------------------------------------------------

            profile_descriptions.append(
                profile
            )

        # -----------------------------------------------------
        # Store profiles
        # -----------------------------------------------------

        self.profile_descriptions[
            domain
        ] = profile_descriptions

        # =====================================================
        # Return result
        # =====================================================

        return {

            "domain":
                domain,

            "cluster_count":
                cluster_count,

            "sample_count":
                len(X),

            "features":
                list(
                    X.columns
                ),

            "failure_statistics_available":
                any(
                    profile[
                        "failure_available"
                    ]
                    for profile
                    in profile_descriptions
                ),

            "profiles":
                profile_descriptions
        }

    # =========================================================
    # Ensure model is fitted
    # =========================================================

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

    # =========================================================
    # Identify profile for a new case
    # =========================================================

    def predict_profile(
        self,
        domain: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:

        domain = self.normalize_domain(
            domain
        )

        # -----------------------------------------------------
        # Fit if required
        # -----------------------------------------------------

        self._ensure_fitted(
            domain
        )

        model = self.models[
            domain
        ]

        scaler = self.scalers[
            domain
        ]

        # -----------------------------------------------------
        # Get clustering features
        # -----------------------------------------------------

        X = self.prepare_features(
            domain
        )

        feature_names = list(
            X.columns
        )

        # -----------------------------------------------------
        # Build input row
        # -----------------------------------------------------

        row = {}

        for feature in feature_names:

            value = data.get(
                feature
            )

            # If feature is missing, use
            # historical median.
            if value is None:

                value = (
                    X[
                        feature
                    ]
                    .median()
                )

            try:

                value = float(
                    value
                )

            except (
                TypeError,
                ValueError
            ):

                value = (
                    X[
                        feature
                    ]
                    .median()
                )

            row[
                feature
            ] = value

        case_df = pd.DataFrame(
            [row],
            columns=feature_names
        )

        # -----------------------------------------------------
        # Scale case
        # -----------------------------------------------------

        case_scaled = scaler.transform(
            case_df
        )

        # -----------------------------------------------------
        # Predict cluster
        # -----------------------------------------------------

        cluster_id = int(
            model.predict(
                case_scaled
            )[0]
        )

        # -----------------------------------------------------
        # Calculate distance to all profiles
        # -----------------------------------------------------

        distances = model.transform(
            case_scaled
        )[0]

        distance_to_profile = float(
            distances[
                cluster_id
            ]
        )

        # -----------------------------------------------------
        # Get profile description
        # -----------------------------------------------------

        profile = next(
            (
                item
                for item
                in self.profile_descriptions[
                    domain
                ]
                if item[
                    "profile_id"
                ] == cluster_id
            ),
            None
        )

        # -----------------------------------------------------
        # Return result
        # -----------------------------------------------------

        return {

            "domain":
                domain,

            "profile_id":
                cluster_id,

            "distance_to_profile":
                round(
                    distance_to_profile,
                    6
                ),

            "profile":
                profile
        }

    # =========================================================
    # Get all profiles
    # =========================================================

    def get_profiles(
        self,
        domain: str
    ) -> Dict[str, Any]:

        domain = self.normalize_domain(
            domain
        )

        # -----------------------------------------------------
        # Fit model if necessary
        # -----------------------------------------------------

        self._ensure_fitted(
            domain
        )

        profiles = (
            self.profile_descriptions[
                domain
            ]
        )

        return {

            "domain":
                domain,

            "cluster_count":
                len(profiles),

            "failure_statistics_available":
                any(
                    profile[
                        "failure_available"
                    ]
                    for profile
                    in profiles
                ),

            "profiles":
                profiles
        }