"""
FAILURE INTELLIGENCE MODEL COMPARISON EXPERIMENT

Experiments:
1. Original Random Forest
2. Optimized Random Forest
3. Cleaned Random Forest

Domains:
- Student
- Software
- Jobs
- Projects

Output:
    backend/ml/model_comparison_results.csv

Models:
    backend/ml/models/<domain>_original_rf.pkl
    backend/ml/models/<domain>_optimized_rf.pkl
    backend/ml/models/<domain>_cleaned_rf.pkl

IMPORTANT EXPERIMENT DESIGN
---------------------------
For each domain, all three experiments use the SAME train/test split.

Original RF:
    Current project Random Forest configuration.

Optimized RF:
    RandomizedSearchCV + 5-fold StratifiedKFold,
    optimized using weighted F1.

Cleaned RF:
    Original RF after removing potentially problematic
    identity-like features.

Current cleaning:
    Software:
        remove `re` and `at`

Other domains:
        no feature removal yet.
"""

from pathlib import Path
import warnings

import joblib
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    balanced_accuracy_score,
    classification_report,
    confusion_matrix,
)
from sklearn.model_selection import (
    train_test_split,
    RandomizedSearchCV,
    StratifiedKFold,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


# =============================================================================
# CONFIGURATION
# =============================================================================

RANDOM_STATE = 42
TEST_SIZE = 0.20

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"

MODEL_DIR = (
    BASE_DIR
    / "backend"
    / "ml"
    / "models"
)

RESULTS_FILE = (
    BASE_DIR
    / "backend"
    / "ml"
    / "model_comparison_results.csv"
)

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# =============================================================================
# WARNINGS
# =============================================================================

warnings.filterwarnings(
    "ignore",
    message=".*should be used with sklearn.utils.parallel.*"
)


# =============================================================================
# DISPLAY HELPERS
# =============================================================================

def print_separator(
    char="=",
    length=80
):
    print(
        char * length
    )


def print_header(
    title
):
    print_separator()
    print(title)
    print_separator()


# =============================================================================
# FILE DISCOVERY
# =============================================================================

def find_csv(
    directory,
    keywords=None,
    exclude_keywords=None
):
    """
    Find a CSV file recursively.

    Parameters
    ----------
    directory : Path
        Directory to search.

    keywords : list[str] | None
        Filename must contain at least one keyword.

    exclude_keywords : list[str] | None
        Filename must not contain these keywords.
    """

    if not directory.exists():
        raise FileNotFoundError(
            f"Directory does not exist:\n{directory}"
        )

    files = list(
        directory.rglob("*.csv")
    )

    if not files:
        raise FileNotFoundError(
            f"No CSV files found inside:\n{directory}"
        )

    if keywords:

        keywords = [
            str(k).lower()
            for k in keywords
        ]

        matching = [
            f
            for f in files
            if any(
                k in f.name.lower()
                for k in keywords
            )
        ]

    else:

        matching = files

    if exclude_keywords:

        exclude_keywords = [
            str(k).lower()
            for k in exclude_keywords
        ]

        matching = [
            f
            for f in matching
            if not any(
                k in f.name.lower()
                for k in exclude_keywords
            )
        ]

    if not matching:
        raise FileNotFoundError(
            f"Could not find a suitable CSV in:\n{directory}"
        )

    matching.sort(
        key=lambda x: (
            len(str(x)),
            str(x)
        )
    )

    return matching[0]


# =============================================================================
# STUDENT DATASET
# =============================================================================

def load_student():
    """
    Student performance dataset.

    Target:
        Failure_Type

    Rule:
        G3 < 10  -> Exam Failure
        G3 >= 10 -> Passed

    Features:
        absences
        studytime
        failures
        G1
        G2
    """

    path = (
        DATA_DIR
        / "student"
        / "student-mat.csv"
    )

    if not path.exists():
        raise FileNotFoundError(
            f"Student dataset not found:\n{path}"
        )

    df = pd.read_csv(
        path,
        sep=";"
    )

    required_columns = [
        "absences",
        "studytime",
        "failures",
        "G1",
        "G2",
        "G3",
    ]

    missing = [
        col
        for col in required_columns
        if col not in df.columns
    ]

    if missing:
        raise KeyError(
            "Student dataset is missing columns: "
            f"{missing}\n"
            f"Available columns:\n{list(df.columns)}"
        )

    # -------------------------------------------------------------------------
    # Create target
    # -------------------------------------------------------------------------

    df["Failure_Type"] = np.where(
        df["G3"] < 10,
        "Exam Failure",
        "Passed"
    )

    features = [
        "absences",
        "studytime",
        "failures",
        "G1",
        "G2",
    ]

    print(
        "\nStudent dataset:"
    )

    print(
        f"  File: {path}"
    )

    print(
        f"  Rows: {len(df)}"
    )

    print(
        f"  Features: {features}"
    )

    print(
        "  Target: Failure_Type"
    )

    return df[
        features + ["Failure_Type"]
    ]


# =============================================================================
# SOFTWARE DATASET
# =============================================================================

def load_software():
    """
    Mozilla software failure dataset.

    Actual target column:
        rs

    Internal standardized target:
        Failure_Type

    Original features:
        pr
        cl
        pd
        co
        rp
        os
        bs
        bsr
        re
        at

    Cleaned experiment removes:
        re
        at

    IMPORTANT:
    Missing target values are removed before modeling.
    Feature missing values are handled later by the preprocessing pipeline.
    """

    path = (
        DATA_DIR
        / "software"
        / "Mozilla.csv"
    )

    if not path.exists():
        raise FileNotFoundError(
            f"Software dataset not found:\n{path}"
        )

    df = pd.read_csv(
        path,
        sep=";"
    )

    # -------------------------------------------------------------------------
    # Clean column names
    # -------------------------------------------------------------------------

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    required_columns = [
        "pr",
        "cl",
        "pd",
        "co",
        "rp",
        "os",
        "bs",
        "bsr",
        "re",
        "at",
        "rs",
    ]

    missing = [
        col
        for col in required_columns
        if col not in df.columns
    ]

    if missing:
        raise KeyError(
            "Mozilla dataset is missing columns: "
            f"{missing}\n"
            f"Available columns:\n{list(df.columns)}"
        )

    # -------------------------------------------------------------------------
    # Clean target
    # -------------------------------------------------------------------------

    df["Failure_Type"] = (
        df["rs"]
        .astype("string")
        .str.strip()
    )

    # Convert empty strings to missing values.
    df["Failure_Type"] = (
        df["Failure_Type"]
        .replace(
            {
                "": pd.NA,
                "nan": pd.NA,
                "None": pd.NA,
            }
        )
    )

    rows_before = len(df)

    missing_target = (
        df["Failure_Type"]
        .isna()
        .sum()
    )

    if missing_target > 0:

        print(
            "\nSoftware target cleaning:"
        )

        print(
            f"  Rows before: {rows_before}"
        )

        print(
            f"  Missing target rows removed: "
            f"{missing_target}"
        )

        df = df.dropna(
            subset=["Failure_Type"]
        ).copy()

        print(
            f"  Rows after: {len(df)}"
        )

    # -------------------------------------------------------------------------
    # Features
    # -------------------------------------------------------------------------

    features = [
        "pr",
        "cl",
        "pd",
        "co",
        "rp",
        "os",
        "bs",
        "bsr",
        "re",
        "at",
    ]

    print(
        "\nSoftware dataset:"
    )

    print(
        f"  File: {path}"
    )

    print(
        f"  Rows: {len(df)}"
    )

    print(
        f"  Original features: {features}"
    )

    print(
        "  Target column in CSV: rs"
    )

    print(
        "  Standardized target: Failure_Type"
    )

    return df[
        features + ["Failure_Type"]
    ]


# =============================================================================
# JOBS DATASET
# =============================================================================

def load_jobs():
    """
    Jobs / resume screening dataset.

    Target:
        shortlisted

    Mapping:
        Yes -> Selected
        No  -> Rejected
    """

    jobs_dir = (
        DATA_DIR
        / "jobs"
    )

    path = find_csv(
        jobs_dir,
        keywords=[
            "resume",
            "screen",
            "job",
            "shortlist",
            "candidate",
        ]
    )

    df = pd.read_csv(
        path
    )

    # -------------------------------------------------------------------------
    # Clean column names
    # -------------------------------------------------------------------------

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    required_columns = [
        "years_experience",
        "skills_match_score",
        "education_level",
        "project_count",
        "resume_length",
        "github_activity",
        "shortlisted",
    ]

    missing = [
        col
        for col in required_columns
        if col not in df.columns
    ]

    if missing:
        raise KeyError(
            "Jobs dataset is missing columns: "
            f"{missing}\n"
            f"File: {path}\n"
            f"Available columns:\n{list(df.columns)}"
        )

    # -------------------------------------------------------------------------
    # Create standardized target
    # -------------------------------------------------------------------------

    df["Failure_Type"] = (
        df["shortlisted"]
        .astype("string")
        .str.strip()
        .str.lower()
        .map(
            {
                "yes": "Selected",
                "no": "Rejected",
            }
        )
    )

    # -------------------------------------------------------------------------
    # Remove rows with missing target
    # -------------------------------------------------------------------------

    missing_target = (
        df["Failure_Type"]
        .isna()
        .sum()
    )

    if missing_target > 0:

        print(
            "\nJobs target cleaning:"
        )

        print(
            f"  Missing target rows removed: "
            f"{missing_target}"
        )

        df = df.dropna(
            subset=["Failure_Type"]
        ).copy()

    # -------------------------------------------------------------------------
    # Features
    # -------------------------------------------------------------------------

    features = [
        "years_experience",
        "skills_match_score",
        "education_level",
        "project_count",
        "resume_length",
        "github_activity",
    ]

    print(
        "\nJobs dataset:"
    )

    print(
        f"  File: {path}"
    )

    print(
        f"  Rows: {len(df)}"
    )

    print(
        f"  Features: {features}"
    )

    print(
        "  Target: shortlisted -> Failure_Type"
    )

    return df[
        features + ["Failure_Type"]
    ]


# =============================================================================
# PROJECTS DATASET
# =============================================================================

def load_projects():
    """
    Project management dataset.

    Target:
        Status -> Failure_Type

    Features:
        Complexity
        Project Type
        Region
        Department
        Project Cost
        Project Benefit
        Completion%
        Phase
        Year
        Month

    The CSV contains accidental whitespace around some column names.
    This function strips all column-name whitespace first.

    Project Cost, Project Benefit and Completion% are retained
    for the current experiment.
    """

    projects_dir = (
        DATA_DIR
        / "projects"
    )

    path = find_csv(
        projects_dir,
        keywords=[
            "project",
            "manage",
        ]
    )

    df = pd.read_csv(
        path
    )

    # -------------------------------------------------------------------------
    # IMPORTANT:
    # Strip whitespace from every column name.
    # -------------------------------------------------------------------------

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    required_columns = [
        "Complexity",
        "Project Type",
        "Region",
        "Department",
        "Project Cost",
        "Project Benefit",
        "Completion%",
        "Phase",
        "Year",
        "Month",
        "Status",
    ]

    missing = [
        col
        for col in required_columns
        if col not in df.columns
    ]

    if missing:
        raise KeyError(
            "Projects dataset is missing columns: "
            f"{missing}\n"
            f"File: {path}\n"
            f"Available columns:\n{list(df.columns)}"
        )

    # -------------------------------------------------------------------------
    # Clean numeric fields
    # -------------------------------------------------------------------------

    numeric_columns = [
        "Project Cost",
        "Project Benefit",
        "Completion%",
        "Year",
        "Month",
    ]

    for col in numeric_columns:

        df[col] = (
            df[col]
            .astype(str)
            .str.replace(
                ",",
                "",
                regex=False
            )
            .str.replace(
                "%",
                "",
                regex=False
            )
            .str.strip()
        )

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    # -------------------------------------------------------------------------
    # Create standardized target
    # -------------------------------------------------------------------------

    df["Failure_Type"] = (
        df["Status"]
        .astype("string")
        .str.strip()
    )

    # Empty target values become missing.
    df["Failure_Type"] = (
        df["Failure_Type"]
        .replace(
            {
                "": pd.NA,
                "nan": pd.NA,
                "None": pd.NA,
            }
        )
    )

    # Remove missing target rows.
    missing_target = (
        df["Failure_Type"]
        .isna()
        .sum()
    )

    if missing_target > 0:

        print(
            "\nProjects target cleaning:"
        )

        print(
            f"  Missing target rows removed: "
            f"{missing_target}"
        )

        df = df.dropna(
            subset=["Failure_Type"]
        ).copy()

    features = [
        "Complexity",
        "Project Type",
        "Region",
        "Department",
        "Project Cost",
        "Project Benefit",
        "Completion%",
        "Phase",
        "Year",
        "Month",
    ]

    print(
        "\nProjects dataset:"
    )

    print(
        f"  File: {path}"
    )

    print(
        f"  Rows: {len(df)}"
    )

    print(
        f"  Features: {features}"
    )

    print(
        "  Target: Status -> Failure_Type"
    )

    print(
        "\n  Target distribution:"
    )

    for label, count in (
        df["Failure_Type"]
        .value_counts()
        .items()
    ):
        print(
            f"    {label}: {count}"
        )

    return df[
        features + ["Failure_Type"]
    ]


# =============================================================================
# LOAD ALL DATASETS
# =============================================================================

def load_all():

    print_header(
        "LOADING DATASETS"
    )

    datasets = {
        "student": load_student(),
        "software": load_software(),
        "jobs": load_jobs(),
        "projects": load_projects(),
    }

    print_separator(
        "-"
    )

    for domain, df in datasets.items():

        print(
            f"{domain.capitalize():10s} | "
            f"Rows: {len(df):6d} | "
            f"Features: {len(df.columns) - 1:2d} | "
            f"Classes: {df['Failure_Type'].nunique():2d}"
        )

    return datasets


# =============================================================================
# PREPROCESSOR
# =============================================================================

def build_preprocessor(X):

    numeric_features = (
        X.select_dtypes(
            include=[
                "int64",
                "int32",
                "float64",
                "float32",
            ]
        )
        .columns
        .tolist()
    )

    categorical_features = (
        X.select_dtypes(
            include=[
                "object",
                "category",
                "string",
                "bool",
            ]
        )
        .columns
        .tolist()
    )

    numeric_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(
                    strategy="median"
                )
            )
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(
                    strategy="most_frequent"
                )
            ),
            (
                "onehot",
                OneHotEncoder(
                    handle_unknown="ignore"
                )
            ),
        ]
    )

    transformers = []

    if numeric_features:

        transformers.append(
            (
                "num",
                numeric_pipeline,
                numeric_features
            )
        )

    if categorical_features:

        transformers.append(
            (
                "cat",
                categorical_pipeline,
                categorical_features
            )
        )

    return ColumnTransformer(
        transformers=transformers
    )


# =============================================================================
# ORIGINAL RANDOM FOREST
# =============================================================================

def build_original_rf(X):

    preprocessor = build_preprocessor(
        X
    )

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=RANDOM_STATE,
        n_jobs=-1
    )

    pipeline = Pipeline(
        steps=[
            (
                "preprocessor",
                preprocessor
            ),
            (
                "model",
                model
            )
        ]
    )

    return pipeline


# =============================================================================
# OPTIMIZED RANDOM FOREST
# =============================================================================

def build_optimized_rf(X):

    preprocessor = build_preprocessor(
        X
    )

    model = RandomForestClassifier(
        random_state=RANDOM_STATE,
        n_jobs=-1
    )

    pipeline = Pipeline(
        steps=[
            (
                "preprocessor",
                preprocessor
            ),
            (
                "model",
                model
            )
        ]
    )

    param_distributions = {

        "model__n_estimators": [
            100,
            200,
            300,
            500,
        ],

        "model__max_depth": [
            None,
            5,
            10,
            15,
            20,
            30,
        ],

        "model__min_samples_split": [
            2,
            5,
            10,
        ],

        "model__min_samples_leaf": [
            1,
            2,
            4,
        ],

        "model__max_features": [
            "sqrt",
            "log2",
        ],

        "model__class_weight": [
            None,
            "balanced",
            "balanced_subsample",
        ],
    }

    cv = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=RANDOM_STATE
    )

    search = RandomizedSearchCV(
        estimator=pipeline,
        param_distributions=param_distributions,
        n_iter=30,
        scoring="f1_weighted",
        cv=cv,
        random_state=RANDOM_STATE,
        n_jobs=-1,
        verbose=1,
        refit=True
    )

    return search


# =============================================================================
# MODEL EVALUATION
# =============================================================================

def evaluate_model(
    model,
    X_test,
    y_test
):

    y_pred = model.predict(
        X_test
    )

    accuracy = accuracy_score(
        y_test,
        y_pred
    )

    precision = precision_score(
        y_test,
        y_pred,
        average="weighted",
        zero_division=0
    )

    recall = recall_score(
        y_test,
        y_pred,
        average="weighted",
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        y_pred,
        average="weighted",
        zero_division=0
    )

    balanced_accuracy = (
        balanced_accuracy_score(
            y_test,
            y_pred
        )
    )

    report = classification_report(
        y_test,
        y_pred,
        zero_division=0
    )

    matrix = confusion_matrix(
        y_test,
        y_pred
    )

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "balanced_accuracy": balanced_accuracy,
        "classification_report": report,
        "confusion_matrix": matrix,
        "predictions": y_pred,
    }


# =============================================================================
# TRAIN ORIGINAL RF
# =============================================================================

def train_original_rf(
    domain,
    X_train,
    X_test,
    y_train,
    y_test
):

    print_header(
        f"{domain.upper()} - ORIGINAL RANDOM FOREST"
    )

    model = build_original_rf(
        X_train
    )

    print(
        "Training original Random Forest..."
    )

    model.fit(
        X_train,
        y_train
    )

    metrics = evaluate_model(
        model,
        X_test,
        y_test
    )

    print(
        "\nResults:"
    )

    print(
        f"  Accuracy:          "
        f"{metrics['accuracy']:.4f}"
    )

    print(
        f"  Precision:         "
        f"{metrics['precision']:.4f}"
    )

    print(
        f"  Recall:            "
        f"{metrics['recall']:.4f}"
    )

    print(
        f"  F1:                "
        f"{metrics['f1']:.4f}"
    )

    print(
        f"  Balanced Accuracy: "
        f"{metrics['balanced_accuracy']:.4f}"
    )

    print(
        "\nClassification Report:"
    )

    print(
        metrics["classification_report"]
    )

    model_path = (
        MODEL_DIR
        / f"{domain}_original_rf.pkl"
    )

    artifact = {

        "model": model,

        "domain": domain,

        "experiment":
            "Original Random Forest",

        "features":
            X_train.columns.tolist(),

        "metrics": {

            "accuracy":
                metrics["accuracy"],

            "precision":
                metrics["precision"],

            "recall":
                metrics["recall"],

            "f1":
                metrics["f1"],

            "balanced_accuracy":
                metrics["balanced_accuracy"],
        },

        "random_state":
            RANDOM_STATE,
    }

    joblib.dump(
        artifact,
        model_path
    )

    print(
        f"\nModel saved: {model_path}"
    )

    return (
        metrics,
        model_path
    )


# =============================================================================
# TRAIN OPTIMIZED RF
# =============================================================================

def train_optimized_rf(
    domain,
    X_train,
    X_test,
    y_train,
    y_test
):

    print_header(
        f"{domain.upper()} - OPTIMIZED RANDOM FOREST"
    )

    search = build_optimized_rf(
        X_train
    )

    print(
        "Running RandomizedSearchCV..."
    )

    print(
        "  Iterations: 30"
    )

    print(
        "  CV folds: 5"
    )

    print(
        "  Scoring: weighted F1"
    )

    search.fit(
        X_train,
        y_train
    )

    model = search.best_estimator_

    metrics = evaluate_model(
        model,
        X_test,
        y_test
    )

    print(
        "\nBest Parameters:"
    )

    for key, value in (
        search.best_params_.items()
    ):

        print(
            f"  {key}: {value}"
        )

    print(
        f"\nBest CV Weighted F1: "
        f"{search.best_score_:.4f}"
    )

    print(
        "\nTest Set Results:"
    )

    print(
        f"  Accuracy:          "
        f"{metrics['accuracy']:.4f}"
    )

    print(
        f"  Precision:         "
        f"{metrics['precision']:.4f}"
    )

    print(
        f"  Recall:            "
        f"{metrics['recall']:.4f}"
    )

    print(
        f"  F1:                "
        f"{metrics['f1']:.4f}"
    )

    print(
        f"  Balanced Accuracy: "
        f"{metrics['balanced_accuracy']:.4f}"
    )

    print(
        "\nClassification Report:"
    )

    print(
        metrics["classification_report"]
    )

    model_path = (
        MODEL_DIR
        / f"{domain}_optimized_rf.pkl"
    )

    artifact = {

        "model": model,

        "domain": domain,

        "experiment":
            "Optimized Random Forest",

        "features":
            X_train.columns.tolist(),

        "metrics": {

            "accuracy":
                metrics["accuracy"],

            "precision":
                metrics["precision"],

            "recall":
                metrics["recall"],

            "f1":
                metrics["f1"],

            "balanced_accuracy":
                metrics["balanced_accuracy"],

            "cv_f1_weighted":
                search.best_score_,
        },

        "best_params":
            search.best_params_,

        "random_state":
            RANDOM_STATE,
    }

    joblib.dump(
        artifact,
        model_path
    )

    print(
        f"\nModel saved: {model_path}"
    )

    return (
        metrics,
        search.best_score_,
        search.best_params_,
        model_path
    )


# =============================================================================
# TRAIN CLEANED RF
# =============================================================================

def train_cleaned_rf(
    domain,
    X_train,
    X_test,
    y_train,
    y_test
):

    print_header(
        f"{domain.upper()} - CLEANED RANDOM FOREST"
    )

    X_train_clean = (
        X_train.copy()
    )

    X_test_clean = (
        X_test.copy()
    )

    removed_features = []

    # -------------------------------------------------------------------------
    # Software-specific cleaning
    # -------------------------------------------------------------------------

    if domain == "software":

        removable = [
            "re",
            "at",
        ]

        for feature in removable:

            if feature in X_train_clean.columns:

                X_train_clean = (
                    X_train_clean.drop(
                        columns=[feature]
                    )
                )

                X_test_clean = (
                    X_test_clean.drop(
                        columns=[feature]
                    )
                )

                removed_features.append(
                    feature
                )

    print(
        f"Removed features: "
        f"{removed_features if removed_features else 'None'}"
    )

    print(
        f"Remaining features: "
        f"{list(X_train_clean.columns)}"
    )

    model = build_original_rf(
        X_train_clean
    )

    print(
        "\nTraining cleaned Random Forest..."
    )

    model.fit(
        X_train_clean,
        y_train
    )

    metrics = evaluate_model(
        model,
        X_test_clean,
        y_test
    )

    print(
        "\nResults:"
    )

    print(
        f"  Accuracy:          "
        f"{metrics['accuracy']:.4f}"
    )

    print(
        f"  Precision:         "
        f"{metrics['precision']:.4f}"
    )

    print(
        f"  Recall:            "
        f"{metrics['recall']:.4f}"
    )

    print(
        f"  F1:                "
        f"{metrics['f1']:.4f}"
    )

    print(
        f"  Balanced Accuracy: "
        f"{metrics['balanced_accuracy']:.4f}"
    )

    print(
        "\nClassification Report:"
    )

    print(
        metrics["classification_report"]
    )

    model_path = (
        MODEL_DIR
        / f"{domain}_cleaned_rf.pkl"
    )

    artifact = {

        "model": model,

        "domain": domain,

        "experiment":
            "Cleaned Random Forest",

        "features":
            X_train_clean.columns.tolist(),

        "removed_features":
            removed_features,

        "metrics": {

            "accuracy":
                metrics["accuracy"],

            "precision":
                metrics["precision"],

            "recall":
                metrics["recall"],

            "f1":
                metrics["f1"],

            "balanced_accuracy":
                metrics["balanced_accuracy"],
        },

        "random_state":
            RANDOM_STATE,
    }

    joblib.dump(
        artifact,
        model_path
    )

    print(
        f"\nModel saved: {model_path}"
    )

    return (
        metrics,
        model_path
    )


# =============================================================================
# CREATE TRAIN / TEST SPLIT
# =============================================================================

def create_split(
    df
):

    X = df.drop(
        columns=["Failure_Type"]
    )

    y = (
        df["Failure_Type"]
        .astype("string")
        .str.strip()
    )

    # -------------------------------------------------------------------------
    # Final target validation
    # -------------------------------------------------------------------------

    valid_target = (
        y.notna()
        & (y != "")
    )

    if not valid_target.all():

        removed = (
            (~valid_target)
            .sum()
        )

        print(
            f"\nRemoving {removed} "
            "rows with missing target values."
        )

        X = X.loc[
            valid_target
        ].copy()

        y = y.loc[
            valid_target
        ].copy()

    # -------------------------------------------------------------------------
    # Check that target has enough classes
    # -------------------------------------------------------------------------

    class_counts = (
        y.value_counts()
    )

    if len(class_counts) < 2:

        raise ValueError(
            "Target must contain at least "
            "two classes."
        )

    # Stratified splitting requires each class to have
    # enough observations.
    if class_counts.min() < 2:

        rare_classes = (
            class_counts[
                class_counts < 2
            ]
            .to_dict()
        )

        raise ValueError(
            "Cannot perform stratified train/test split "
            "because some classes contain fewer than "
            f"2 samples: {rare_classes}"
        )

    # -------------------------------------------------------------------------
    # Print distribution
    # -------------------------------------------------------------------------

    print(
        "\nTarget distribution:"
    )

    for label, count in (
        class_counts.items()
    ):

        print(
            f"  {label}: {count}"
        )

    # -------------------------------------------------------------------------
    # Same split for all three experiments
    # -------------------------------------------------------------------------

    X_train, X_test, y_train, y_test = (
        train_test_split(
            X,
            y,
            test_size=TEST_SIZE,
            random_state=RANDOM_STATE,
            stratify=y
        )
    )

    print(
        f"\nTrain size: {len(X_train)}"
    )

    print(
        f"Test size:  {len(X_test)}"
    )

    return (
        X_train,
        X_test,
        y_train,
        y_test
    )


# =============================================================================
# RUN ONE DOMAIN
# =============================================================================

def run_domain_experiment(
    domain,
    df
):

    print_header(
        f"RUNNING EXPERIMENTS FOR: {domain.upper()}"
    )

    (
        X_train,
        X_test,
        y_train,
        y_test
    ) = create_split(
        df
    )

    results = []

    # =========================================================================
    # 1. ORIGINAL RF
    # =========================================================================

    (
        original_metrics,
        original_path
    ) = train_original_rf(
        domain,
        X_train,
        X_test,
        y_train,
        y_test
    )

    results.append(
        {
            "domain":
                domain,

            "experiment":
                "Original RF",

            "accuracy":
                original_metrics["accuracy"],

            "precision":
                original_metrics["precision"],

            "recall":
                original_metrics["recall"],

            "f1":
                original_metrics["f1"],

            "balanced_accuracy":
                original_metrics[
                    "balanced_accuracy"
                ],

            "cv_f1_weighted":
                np.nan,

            "removed_features":
                "",

            "model_path":
                str(original_path),
        }
    )

    # =========================================================================
    # 2. OPTIMIZED RF
    # =========================================================================

    (
        optimized_metrics,
        cv_f1,
        best_params,
        optimized_path
    ) = train_optimized_rf(
        domain,
        X_train,
        X_test,
        y_train,
        y_test
    )

    results.append(
        {
            "domain":
                domain,

            "experiment":
                "Optimized RF",

            "accuracy":
                optimized_metrics["accuracy"],

            "precision":
                optimized_metrics["precision"],

            "recall":
                optimized_metrics["recall"],

            "f1":
                optimized_metrics["f1"],

            "balanced_accuracy":
                optimized_metrics[
                    "balanced_accuracy"
                ],

            "cv_f1_weighted":
                cv_f1,

            "removed_features":
                "",

            "model_path":
                str(optimized_path),
        }
    )

    # =========================================================================
    # 3. CLEANED RF
    # =========================================================================

    (
        cleaned_metrics,
        cleaned_path
    ) = train_cleaned_rf(
        domain,
        X_train,
        X_test,
        y_train,
        y_test
    )

    removed_features = ""

    if domain == "software":
        removed_features = "re, at"

    results.append(
        {
            "domain":
                domain,

            "experiment":
                "Cleaned RF",

            "accuracy":
                cleaned_metrics["accuracy"],

            "precision":
                cleaned_metrics["precision"],

            "recall":
                cleaned_metrics["recall"],

            "f1":
                cleaned_metrics["f1"],

            "balanced_accuracy":
                cleaned_metrics[
                    "balanced_accuracy"
                ],

            "cv_f1_weighted":
                np.nan,

            "removed_features":
                removed_features,

            "model_path":
                str(cleaned_path),
        }
    )

    return results


# =============================================================================
# FINAL COMPARISON
# =============================================================================

def print_final_comparison(
    results_df
):

    print_header(
        "FINAL MODEL COMPARISON"
    )

    display_columns = [
        "domain",
        "experiment",
        "accuracy",
        "precision",
        "recall",
        "f1",
        "balanced_accuracy",
        "cv_f1_weighted",
    ]

    table = (
        results_df[
            display_columns
        ]
        .copy()
    )

    numeric_columns = [
        "accuracy",
        "precision",
        "recall",
        "f1",
        "balanced_accuracy",
        "cv_f1_weighted",
    ]

    for col in numeric_columns:

        table[col] = (
            table[col]
            .round(4)
        )

    print(
        table.to_string(
            index=False
        )
    )

    print_separator(
        "-"
    )

    print(
        "\nBest model by weighted F1 "
        "for each domain:"
    )

    for domain in (
        results_df["domain"]
        .unique()
    ):

        domain_df = (
            results_df[
                results_df["domain"] == domain
            ]
        )

        best_row = domain_df.loc[
            domain_df["f1"].idxmax()
        ]

        print(
            f"  {domain.capitalize():10s} -> "
            f"{best_row['experiment']:15s} "
            f"(F1 = {best_row['f1']:.4f})"
        )


# =============================================================================
# MAIN
# =============================================================================

def main():

    print_separator()

    print(
        "FAILURE INTELLIGENCE "
        "MODEL COMPARISON EXPERIMENT"
    )

    print_separator()

    print(
        "\nExperiments:"
    )

    print(
        "  1. Original Random Forest"
    )

    print(
        "  2. Optimized Random Forest"
    )

    print(
        "  3. Cleaned Random Forest"
    )

    print(
        f"\nRandom state: {RANDOM_STATE}"
    )

    print(
        f"Test size: {TEST_SIZE}"
    )

    print(
        f"Data directory: {DATA_DIR}"
    )

    print(
        f"Model directory: {MODEL_DIR}"
    )

    print(
        f"Results file: {RESULTS_FILE}"
    )

    # =========================================================================
    # LOAD DATA
    # =========================================================================

    datasets = load_all()

    # =========================================================================
    # RUN EXPERIMENTS
    # =========================================================================

    all_results = []

    for domain, df in (
        datasets.items()
    ):

        domain_results = (
            run_domain_experiment(
                domain,
                df
            )
        )

        all_results.extend(
            domain_results
        )

    # =========================================================================
    # SAVE RESULTS
    # =========================================================================

    results_df = pd.DataFrame(
        all_results
    )

    results_df.to_csv(
        RESULTS_FILE,
        index=False
    )

    # =========================================================================
    # FINAL DISPLAY
    # =========================================================================

    print_final_comparison(
        results_df
    )

    print_header(
        "EXPERIMENT COMPLETED SUCCESSFULLY"
    )

    print(
        "\nComparison results saved to:"
    )

    print(
        f"  {RESULTS_FILE}"
    )

    print(
        "\nSaved models:"
    )

    for domain in (
        datasets.keys()
    ):

        print(
            f"\n{domain.capitalize()}:"
        )

        print(
            "  "
            f"{MODEL_DIR / f'{domain}_original_rf.pkl'}"
        )

        print(
            "  "
            f"{MODEL_DIR / f'{domain}_optimized_rf.pkl'}"
        )

        print(
            "  "
            f"{MODEL_DIR / f'{domain}_cleaned_rf.pkl'}"
        )

    print_separator()


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    main()
