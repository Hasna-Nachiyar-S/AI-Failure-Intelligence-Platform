from pathlib import Path
import sys

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.utils.data_loader import load_all

datasets = load_all()

for name, df in datasets.items():
    print("=" * 60)
    print(f"{name.upper()} DATASET")
    print("=" * 60)
    print(df.head())
    print(f"\nRows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")
    print()