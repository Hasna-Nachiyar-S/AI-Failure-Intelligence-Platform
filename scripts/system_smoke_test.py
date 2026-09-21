"""End-to-end backend smoke test for the four production domains.

Run from the project root:
    python scripts/system_smoke_test.py

This test does not retrain models. It verifies model loading, prediction,
recommendation, What-If simulation, constraints, profiles, and
counterfactual generation against the checked-in production artifacts.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.analytics.failure_profiles import FailureProfileAnalyzer
from backend.counterfactual.constraint_engine import DomainConstraintEngine
from backend.counterfactual.generator import CounterfactualGenerator
from backend.ml.domain_model_manager import DomainModelManager
from backend.recommendation.recommender import Recommender
from backend.what_if.simulator import WhatIfSimulator


CASES = {
    "Student": {
        "Domain": "Student", "absences": 30, "studytime": 1,
        "failures": 3, "G1": 5, "G2": 5,
    },
    "Software": {
        "Domain": "Software", "pr": "P3", "cl": "Components",
        "pd": "Firefox", "co": "Search", "rp": "Unspecified",
        "os": "All", "bs": "RESOLVED", "bsr": "normal",
        "re": "user", "at": "user",
    },
    "Jobs": {
        "Domain": "Jobs", "years_experience": 2,
        "skills_match_score": 70, "education_level": "Bachelor",
        "project_count": 3, "resume_length": 500, "github_activity": 10,
    },
    "Projects": {
        "Domain": "Projects", "Complexity": "Medium",
        "Project_Type": "Software", "Region": "Asia", "Department": "IT",
        "Project_Cost": 100000, "Project_Benefit": 150000,
        "Completion": 60, "Phase": "Execution", "Year": 2024, "Month": 6,
    },
}


def main():
    manager = DomainModelManager()
    recommender = Recommender()
    simulator = WhatIfSimulator()
    counterfactual = CounterfactualGenerator()
    profiles = FailureProfileAnalyzer(n_clusters=3)
    constraints = DomainConstraintEngine()

    for domain, case in CASES.items():
        prediction = manager.predict(domain, case)
        recommendation = recommender.recommend(case)
        profile = profiles.predict_profile(domain, case)
        constraint_info = constraints.describe(domain)

        assert prediction["class_probabilities"], f"{domain}: no probabilities"
        assert recommendation["prediction"]["failure_type"] == prediction["failure_type"]
        assert profile["profile"] is not None
        assert constraint_info["actionable_features"]

        # Use a small valid scenario for What-If.
        what_if_feature = {
            "Student": {"studytime": 4},
            "Software": {"cl": "Components"},
            "Jobs": {"skills_match_score": 80},
            "Projects": {"Completion": 80},
        }[domain]
        what_if = simulator.simulate(case, what_if_feature)
        assert "new_prediction" in what_if

        cf = counterfactual.generate(
            case, profile_guided=True, max_guided_features=3
        )
        assert "analysis_status" in cf
        assert "counterfactuals" in cf

        print(
            f"[PASS] {domain}: "
            f"prediction={prediction['failure_type']} "
            f"probability={prediction['probability']:.4f} "
            f"profile={profile['profile_id']} "
            f"cf_status={cf['analysis_status']}"
        )

    print("All four domains passed the production smoke test.")


if __name__ == "__main__":
    main()
