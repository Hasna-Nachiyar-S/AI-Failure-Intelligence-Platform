from pathlib import Path
import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data"


def read_dataset(file_path):
   
    for sep in [",", ";", "\t", "|"]:
        try:
            df = pd.read_csv(file_path, sep=sep)
            if df.shape[1] > 1:
                return df
        except Exception:
            continue

    return pd.read_csv(file_path, sep=None, engine="python")


def load_student():
    return read_dataset(DATA_DIR / "student" / "student-mat.csv")


def load_software():
    return read_dataset(DATA_DIR / "software" / "Mozilla.csv")


def load_jobs():
    return read_dataset(DATA_DIR / "jobs" / "ai_resume_screening.csv")


def load_projects():
    return read_dataset(DATA_DIR / "projects" / "Project Management Dataset.csv")


def load_all():
    return {
        "student": load_student(),
        "software": load_software(),
        "jobs": load_jobs(),
        "projects": load_projects(),
    }