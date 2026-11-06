from pathlib import Path

import pandas as pd

from backend.utils.data_loader import load_all


class FeatureAuditor:

    def __init__(self):
        self.root = Path(__file__).resolve().parents[2]

    def inspect_dataset(self, name, df, target, features):
        print("\n" + "=" * 70)
        print(f"FEATURE AUDIT: {name.upper()}")
        print("=" * 70)

        print(f"Dataset rows: {len(df)}")
        print(f"Dataset columns: {len(df.columns)}")

        print("\nTarget:")
        print(f"  {target}")

        print("\nFeatures:")
        for feature in features:
            print(f"  - {feature}")

        print("\n" + "-" * 70)
        print("FEATURE DETAILS")
        print("-" * 70)

        for feature in features:
            if feature not in df.columns:
                print(f"\n[WARNING] Missing feature: {feature}")
                continue

            series = df[feature]

            print(f"\nFeature: {feature}")
            print(f"  Data type      : {series.dtype}")
            print(f"  Missing values : {series.isna().sum()}")
            print(f"  Unique values  : {series.nunique(dropna=True)}")

            if series.nunique(dropna=True) <= 15:
                values = series.dropna().unique()
                print(f"  Values         : {list(values)}")

            if pd.api.types.is_numeric_dtype(series):
                print(f"  Minimum        : {series.min()}")
                print(f"  Maximum        : {series.max()}")
                print(f"  Mean           : {series.mean():.4f}")

        print("\n" + "-" * 70)
        print("POTENTIAL HIGH-CARDINALITY FEATURES")
        print("-" * 70)

        for feature in features:
            if feature not in df.columns:
                continue

            unique_count = df[feature].nunique(dropna=True)
            ratio = unique_count / max(len(df), 1)

            if ratio >= 0.50:
                print(
                    f"  {feature}: "
                    f"{unique_count} unique values "
                    f"({ratio:.1%} of rows)"
                )

        print("\n" + "-" * 70)
        print("TARGET RELATIONSHIP CHECK")
        print("-" * 70)

        if target in df.columns:
            print("\nTarget distribution:")
            print(df[target].value_counts(dropna=False))

        print("\n" + "=" * 70)

    def run(self):

        datasets = load_all()

        # --------------------------------------------------
        # STUDENT
        # --------------------------------------------------

        student = datasets["student"].copy()

        student["Failure_Type"] = student["G3"].apply(
            lambda x:
            "Exam Failure"
            if x < 10
            else "Passed"
        )

        student_features = [
            "absences",
            "studytime",
            "failures",
            "G1",
            "G2"
        ]

        self.inspect_dataset(
            "student",
            student,
            "Failure_Type",
            student_features
        )

        # --------------------------------------------------
        # SOFTWARE
        # --------------------------------------------------

        software = datasets["software"].copy()

        software["Failure_Type"] = (
            software["rs"].fillna("Unknown")
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

        self.inspect_dataset(
            "software",
            software,
            "Failure_Type",
            software_features
        )

        print("\n" + "=" * 70)
        print("SOFTWARE HIGH-CARDINALITY FEATURE SAMPLE VALUES")
        print("=" * 70)

        for feature in ["pd", "co", "re", "at"]:
            print(f"\n--- {feature} ---")
            print(software[feature].head(20).to_string(index=False))

        # --------------------------------------------------
        # JOBS
        # --------------------------------------------------

        jobs = datasets["jobs"].copy()

        jobs["Failure_Type"] = jobs["shortlisted"].map({
            "Yes": "Selected",
            "No": "Rejected"
        })

        jobs_features = [
            "years_experience",
            "skills_match_score",
            "education_level",
            "project_count",
            "resume_length",
            "github_activity"
        ]

        self.inspect_dataset(
            "jobs",
            jobs,
            "Failure_Type",
            jobs_features
        )

        # --------------------------------------------------
        # PROJECTS
        # --------------------------------------------------

        projects = datasets["projects"].copy()

        projects["Failure_Type"] = projects["Status"]

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

        self.inspect_dataset(
            "projects",
            projects,
            "Failure_Type",
            projects_features
        )


if __name__ == "__main__":
    FeatureAuditor().run()
