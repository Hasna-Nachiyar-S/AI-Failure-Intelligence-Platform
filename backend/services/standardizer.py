import pandas as pd


class Standardizer:

    @staticmethod
    def student(df: pd.DataFrame) -> pd.DataFrame:

        new_df = pd.DataFrame(index=df.index)

        new_df["Domain"] = "Student"

        new_df["Failure_Type"] = df["G3"].apply(
            lambda x: "Exam Failure" if x < 10 else "Passed"
        )

        # Number of previous failures
        new_df["Severity"] = df["failures"].astype(int)

        # Final grade
        new_df["Score"] = df["G3"].astype(float)

        new_df["Description"] = (
            "Absences: "
            + df["absences"].astype(str)
            + ", Study Time: "
            + df["studytime"].astype(str)
        )

        return new_df

    @staticmethod
    def software(df: pd.DataFrame) -> pd.DataFrame:

        new_df = pd.DataFrame(index=df.index)

        new_df["Domain"] = "Software"

        # Resolution
        new_df["Failure_Type"] = df["rs"].fillna("Unknown")

        # Convert priorities into numeric severity
        priority = {
            "P1": 5,
            "P2": 4,
            "P3": 3,
            "P4": 2,
            "P5": 1,
            "--": 0
        }

        new_df["Severity"] = df["pr"].map(priority).fillna(0)

        # No score available
        new_df["Score"] = 0.0

        new_df["Description"] = df["sd"]

        return new_df

    @staticmethod
    def jobs(df: pd.DataFrame) -> pd.DataFrame:

        new_df = pd.DataFrame(index=df.index)

        new_df["Domain"] = "Jobs"

        new_df["Failure_Type"] = df["shortlisted"].map({
            "Yes": "Selected",
            "No": "Rejected"
        })

        # Skill score
        new_df["Severity"] = df["skills_match_score"].astype(float)

        new_df["Score"] = df["skills_match_score"].astype(float)

        new_df["Description"] = (
            "Experience "
            + df["years_experience"].astype(str)
            + " years"
        )

        return new_df

    @staticmethod
    def projects(df: pd.DataFrame) -> pd.DataFrame:

        new_df = pd.DataFrame(index=df.index)

        new_df["Domain"] = "Projects"

        new_df["Failure_Type"] = df["Status"]

        # Convert "77%" → 77
        completion = (
            df["Completion%"]
            .astype(str)
            .str.replace("%", "", regex=False)
            .astype(float)
        )

        new_df["Severity"] = completion

        new_df["Score"] = completion

        new_df["Description"] = df["Project Name"]

        return new_df

    @staticmethod
    def merge(student, software, jobs, projects):

        merged = pd.concat(
            [student, software, jobs, projects],
            ignore_index=True
        )

        return merged