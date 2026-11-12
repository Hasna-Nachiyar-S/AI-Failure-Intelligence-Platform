from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional

import pandas as pd

@dataclass
class Intervention:
    feature: str
    old_value: Any
    new_value: Any
    risk_before: float
    risk_after: float
    risk_reduction: float
    prediction_before: Any
    prediction_after: Any

@dataclass
class CounterfactualResult:
    original_prediction: Any
    original_failure_risk: float
    recommended_interventions: List[Dict[str, Any]]
    best_intervention: Optional[Dict[str, Any]]

class CounterfactualEngine:
    """
    Research-oriented baseline counterfactual engine.

    Generates model-based interventions by changing only
    domain-designated actionable features.

    Risk reduction means a reduction in the trained model's
    predicted failure risk. It does not establish causality.
    """

    DOMAIN_CONFIG = {
        "Student": {
            "actionable_features": [
                "absences",
                "studytime",
            ],
            "desired_class": "Passed",
        },

        "Jobs": {
            "actionable_features": [
                "skills_match_score",
                "project_count",
                "resume_length",
                "github_activity",
            ],
            "desired_class": "Selected",
        },

        "Software": {
            "actionable_features": [
                "pr",
                "cl",
                "rp",
                "os",
                "bs",
                "bsr",
            ],
            "desired_class": "FIXED",
        },

        "Projects": {
            "actionable_features": [
                "Complexity",
                "Project_Cost",
                "Project_Benefit",
                "Completion",
                "Phase",
            ],
            "desired_class": "Completed",
        },
    }

    def __init__(self, model, domain: str):
        self.model = model

        if domain not in self.DOMAIN_CONFIG:
            raise ValueError(
                f"Unsupported domain: {domain}"
            )

        self.domain = domain
        self.config = self.DOMAIN_CONFIG[domain]

    # MODEL INPUT PREPARATION

    def _prepare_input(
        self,
        data: Dict[str, Any]
    ) -> pd.DataFrame:
        """
        Convert one feature dictionary into a one-row
        pandas DataFrame.

        The trained sklearn Pipeline expects a 2D tabular
        input rather than a list containing a dictionary.
        """

        return pd.DataFrame([data])

    # PREDICTION

    def _prediction(
        self,
        data: Dict[str, Any]
    ):
        """
        Run the trained pipeline on one sample.
        """

        input_df = self._prepare_input(data)

        prediction = self.model.predict(input_df)[0]

        probabilities = self.model.predict_proba(input_df)[0]

        classes = self.model.classes_

        class_probabilities = {
            str(cls): float(probability)
            for cls, probability in zip(
                classes,
                probabilities
            )
        }

        return (
            prediction,
            class_probabilities
        )

    # FAILURE RISK

    def _failure_risk(
        self,
        class_probabilities: Dict[str, float]
    ) -> float:
        """
        Failure risk is defined as:

            1 - P(desired/success class)
        """

        desired_class = self.config["desired_class"]

        desired_probability = class_probabilities.get(
            desired_class,
            0.0
        )

        return 1.0 - desired_probability

    # CANDIDATE VALUES

    @staticmethod
    @staticmethod
    def _candidate_values(value: Any, feature: str) -> List[Any]:
        if value is None:
            return []

        fixed_values = {
            "absences": [0, 2, 5, 10],
            "studytime": [1, 2, 3, 4],
            "skills_match_score": [50, 60, 70, 80, 90, 95, 100],
            "github_activity": [50, 60, 70, 80, 90, 100],
            "Completion": [20, 30, 40, 50, 60, 70, 80, 90, 100],
        }
        if feature in fixed_values:
            return fixed_values[feature]

        try:
            current = float(value)
        except (TypeError, ValueError):
            return []

        if feature == "project_count":
            return [current + offset for offset in (1, 2, 3)]
        if feature == "resume_length":
            return [current + offset for offset in (50, 100, 200)]
        if feature in {"pr", "cl", "rp", "os", "bs", "bsr"}:
            return [current + offset for offset in (-1, 0, 1, 2)]
        if feature in {"Project_Cost", "Project_Benefit"}:
            return [current * factor for factor in (0.8, 0.9, 1.1, 1.2)]
        return []

    # GENERATE COUNTERFACTUALS

    def generate(
        self,
        data: Dict[str, Any]
    ) -> CounterfactualResult:

        # ORIGINAL PREDICTION

        (
            original_prediction,
            original_probabilities,
        ) = self._prediction(data)

        original_risk = self._failure_risk(
            original_probabilities
        )

        interventions = []

        # ACTIONABLE FEATURES

        for feature in self.config[
            "actionable_features"
        ]:

            if feature not in data:
                continue

            old_value = data.get(feature)

            candidates = self._candidate_values(
                old_value,
                feature
            )

            for new_value in candidates:

                if new_value == old_value:
                    continue

                candidate_data = dict(data)

                candidate_data[feature] = new_value

                # COUNTERFACTUAL PREDICTION

                try:

                    (
                        candidate_prediction,
                        candidate_probabilities,
                    ) = self._prediction(
                        candidate_data
                    )

                except Exception:
                    continue

                # RISK CALCULATION

                candidate_risk = self._failure_risk(
                    candidate_probabilities
                )

                risk_reduction = (
                    original_risk
                    - candidate_risk
                )

                # STORE INTERVENTION

                interventions.append(
                    asdict(
                        Intervention(
                            feature=feature,
                            old_value=old_value,
                            new_value=new_value,
                            risk_before=original_risk,
                            risk_after=candidate_risk,
                            risk_reduction=risk_reduction,
                            prediction_before=(
                                original_prediction
                            ),
                            prediction_after=(
                                candidate_prediction
                            ),
                        )
                    )
                )

        # RANK INTERVENTIONS

        interventions.sort(
            key=lambda item: item[
                "risk_reduction"
            ],
            reverse=True,
        )

        # BEST INTERVENTION

        best_intervention = (
            interventions[0]
            if interventions
            else None
        )

        # RETURN RESULT

        return CounterfactualResult(
            original_prediction=(
                original_prediction
            ),
            original_failure_risk=(
                original_risk
            ),
            recommended_interventions=(
                interventions
            ),
            best_intervention=(
                best_intervention
            ),
        )
