from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.analytics import Analytics
from backend.utils.data_loader import (
    load_student,
    load_software,
    load_jobs,
    load_projects,
)


datasets = {
    "Student": load_student(),
    "Software": load_software(),
    "Jobs": load_jobs(),
    "Projects": load_projects(),
}

for name, df in datasets.items():

    print("=" * 70)
    print(name)
    print("=" * 70)

    print("\nDataset Info")
    print(Analytics.dataset_info(df))

    print("\nMissing Values")
    print(Analytics.missing_values(df))

    print("\nDuplicate Rows")
    print(Analytics.duplicate_rows(df))

    print("\nSummary")
    print(Analytics.summary(df))

    print("\n")