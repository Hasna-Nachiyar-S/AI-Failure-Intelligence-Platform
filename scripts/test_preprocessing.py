from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.utils.data_loader import (
    load_student,
    load_software,
    load_jobs,
    load_projects,
)

from backend.services import Standardizer, Preprocessor

student = Standardizer.student(load_student())
software = Standardizer.software(load_software())
jobs = Standardizer.jobs(load_jobs())
projects = Standardizer.projects(load_projects())

merged = Standardizer.merge(
    student,
    software,
    jobs,
    projects,
)

print("\nMerged Dataset")
print(merged.head())

print("\nData Types")
print(merged.dtypes)

processor = Preprocessor()

processed = processor.preprocess(merged)

print("\nProcessed Dataset")
print(processed.head())

print("\nProcessed Types")
print(processed.dtypes)

print("\nShape")
print(processed.shape)