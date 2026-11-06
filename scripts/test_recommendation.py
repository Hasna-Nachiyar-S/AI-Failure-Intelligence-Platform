"""Smoke-test recommendations using the shared, valid domain fixtures."""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.recommendation.recommender import Recommender
from scripts.domain_cases import CASES


def main():
    recommender = Recommender()
    for domain in ("Student", "Jobs"):
        result = recommender.recommend(CASES[domain])
        assert result["domain"] == domain
        assert result["prediction"]["failure_type"]
        assert isinstance(result["recommendations"], list)
        assert "improvement_actions" in result
        print(f"[PASS] {domain}: {result['prediction']['failure_type']}")
    print("Recommendation smoke tests passed.")


if __name__ == "__main__":
    main()
