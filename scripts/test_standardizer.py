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

from backend.services.standardizer import Standardizer


student = Standardizer.student(load_student())
software = Standardizer.software(load_software())
jobs = Standardizer.jobs(load_jobs())
projects = Standardizer.projects(load_projects())

merged = Standardizer.merge(
    student,
    software,
    jobs,
    projects
)

print("=" * 70)
print("STUDENT")
print(student.head())

print("\n" + "=" * 70)
print("SOFTWARE")
print(software.head())

print("\n" + "=" * 70)
print("JOBS")
print(jobs.head())

print("\n" + "=" * 70)
print("PROJECTS")
print(projects.head())

print("\n" + "=" * 70)
print("MERGED DATASET")
print(merged.head())

print("\nShape:", merged.shape)

print("\nDomains")
print(merged["Domain"].value_counts())

print("\nFailure Types")
print(merged["Failure_Type"].value_counts().head(20))