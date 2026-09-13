from pathlib import Path

import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from backend.utils.data_loader import load_all
from backend.services import Standardizer


class DomainTrainer:

    def __init__(self):
        self.root = Path(__file__).resolve().parents[2]
        self.models_dir = self.root / "models"
        self.models_dir.mkdir(exist_ok=True)

    def build_pipeline(self, X):

        numeric = X.select_dtypes(
            include=["number"]
        ).columns.tolist()

        categorical = X.select_dtypes(
            exclude=["number"]
        ).columns.tolist()

        numeric_pipe = Pipeline([
            (
                "imputer",
                SimpleImputer(strategy="median")
            )
        ])

        categorical_pipe = Pipeline([
            (
                "imputer",
                SimpleImputer(
                    strategy="most_frequent"
                )
            ),
            (
                "encoder",
                OneHotEncoder(
                    handle_unknown="ignore"
                )
            )
        ])

        preprocess = ColumnTransformer([
            (
                "numeric",
                numeric_pipe,
                numeric
            ),
            (
                "categorical",
                categorical_pipe,
                categorical
            )
        ])

        model = RandomForestClassifier(
            n_estimators=200,
            random_state=42,
            n_jobs=-1
        )

        return Pipeline([
            ("preprocess", preprocess),
            ("model", model)
        ])

    def train_domain(
        self,
        name,
        df,
        target,
        features
    ):

        df = df.copy()

        df = df[
            features + [target]
        ].dropna(subset=[target])

        X = df[features]
        y = df[target]

        X_train, X_test, y_train, y_test = (
            train_test_split(
                X,
                y,
                test_size=0.20,
                random_state=42,
                stratify=y
            )
        )

        pipeline = self.build_pipeline(X)

        pipeline.fit(
            X_train,
            y_train
        )

        predictions = pipeline.predict(
            X_test
        )

        accuracy = accuracy_score(
            y_test,
            predictions
        )

        path = (
            self.models_dir
            / f"{name.lower()}_model.pkl"
        )

        joblib.dump(
            {
                "model": pipeline,
                "features": features,
                "target": target,
                "accuracy": accuracy
            },
            path
        )

        print(
            f"{name} model saved -> {path}"
        )

        print(
            f"{name} accuracy: "
            f"{accuracy:.4f}"
        )

    def run(self):

        print("=" * 60)
        print("DOMAIN MODEL TRAINING")
        print("=" * 60)

        datasets = load_all()

        # -----------------------------
        # STUDENT
        # -----------------------------

        student = datasets["student"].copy()

        student["Failure_Type"] = (
            student["G3"]
            .apply(
                lambda x:
                "Exam Failure"
                if x < 10
                else "Passed"
            )
        )

        student_features = [
            "absences",
            "studytime",
            "failures",
            "G1",
            "G2"
        ]

        self.train_domain(
            "student",
            student,
            "Failure_Type",
            student_features
        )

        # -----------------------------
        # SOFTWARE
        # -----------------------------

        software = datasets["software"].copy()

        software["Failure_Type"] = (
            software["rs"]
            .fillna("Unknown")
        )

        software_features = [
            "pr",
            "cl",
            "pd",
            "co",
            "rp",
            "os",
            "bs",
            "bsr",
            "re",
            "at"
        ]

        self.train_domain(
            "software",
            software,
            "Failure_Type",
            software_features
        )

        # -----------------------------
        # JOBS
        # -----------------------------

        jobs = datasets["jobs"].copy()

        jobs["Failure_Type"] = (
            jobs["shortlisted"]
            .map({
                "Yes": "Selected",
                "No": "Rejected"
            })
        )

        jobs_features = [
            "years_experience",
            "skills_match_score",
            "education_level",
            "project_count",
            "resume_length",
            "github_activity"
        ]

        self.train_domain(
            "jobs",
            jobs,
            "Failure_Type",
            jobs_features
        )

        # -----------------------------
        # PROJECTS
        # -----------------------------

        projects = datasets["projects"].copy()

        projects["Failure_Type"] = (
            projects["Status"]
        )

        projects[" Project Cost "] = (
            projects[" Project Cost "]
            .astype(str)
            .str.replace(",", "", regex=False)
            .astype(float)
        )

        projects[" Project Benefit "] = (
            projects[" Project Benefit "]
            .astype(str)
            .str.replace(",", "", regex=False)
            .astype(float)
        )

        projects["Completion%"] = (
            projects["Completion%"]
            .astype(str)
            .str.replace("%", "", regex=False)
            .astype(float)
        )

        projects_features = [
            "Complexity",
            "Project Type",
            "Region",
            "Department",
            " Project Cost ",
            " Project Benefit ",
            "Completion%",
            "Phase",
            "Year",
            "Month"
        ]

        self.train_domain(
            "projects",
            projects,
            "Failure_Type",
            projects_features
        )

        print("=" * 60)
        print("DOMAIN MODEL TRAINING COMPLETE")
        print("=" * 60)


if __name__ == "__main__":
    DomainTrainer().run()