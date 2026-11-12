"""
Domain-constrained counterfactual generator.

The generator:
1. Predicts the original case.
2. Selects actionable features.
3. Generates candidate values from the actual dataset.
4. Applies domain constraints.
5. Evaluates feasible interventions.
6. Calculates model-predicted risk reduction.
7. Separates successful counterfactuals from risk-only changes.
8. Reports when no effective intervention is found.
"""
from backend.analytics.failure_profiles import (
    FailureProfileAnalyzer
)

from backend.analytics.profile_guidance import (
    ProfileGuidanceEngine
)

from backend.ml.domain_model_manager import (
    DomainModelManager
)

from backend.counterfactual.constraint_engine import (
    DomainConstraintEngine
)

from backend.counterfactual.candidate_sampler import (
    CandidateSampler
)

class CounterfactualGenerator:

    def __init__(self, model_dir="models"):
        self.manager = DomainModelManager(model_dir)
        self.constraints = DomainConstraintEngine()
        self.sampler = CandidateSampler()
        self.profile_analyzer = FailureProfileAnalyzer(n_clusters=3)
        self.profile_guidance = ProfileGuidanceEngine()


    # Prediction

    def predict(self, data):
        domain = data.get("Domain")
        result = self.manager.predict(domain, data)
        return {
            "domain": domain,
            "failure_type": result["failure_type"],
            "probability": result["probability"],
            "class_probabilities": result.get("class_probabilities", {}),
        }


    # Candidate generation

    def _make_candidates(self, data, domain, prioritized_features=None):
        features = prioritized_features or self.constraints.actionable_features(domain)
        candidates = []
        for feature in features:
            current = data.get(feature)
            if current is None:
                continue
            for value in self.sampler.get_candidates(domain, feature, current):
                if value == current:
                    continue
                valid, _ = self.constraints.validate_change(domain, feature, value)
                if valid:
                    candidates.append({
                        "feature": feature,
                        "old_value": current,
                        "new_value": value,
                        "changes": {feature: value},
                    })
        return candidates

    # Generate counterfactual analysis

    def generate(
        self,
        data,
        desired_prediction=None,
        profile_guided=True,
        max_guided_features=2,
    ):
        original = self.predict(data)
        domain = self.manager.normalize_domain(data.get("Domain"))
        profile_result = self.profile_analyzer.predict_profile(domain, data)
        assigned_profile = profile_result.get("profile")
        profile_guidance = (
            self.profile_guidance.generate_guidance(domain, data, assigned_profile)
            if assigned_profile else None
        )

        original_prediction = original["failure_type"]
        original_probability = original["probability"]
        original_probabilities = original.get("class_probabilities", {})
        desired_defaults = {
            "Student": "Passed",
            "Software": "FIXED",
            "Jobs": "Selected",
            "Projects": "Completed",
        }
        if desired_prediction is None:
            desired_prediction = desired_defaults.get(domain)

        if desired_prediction not in original_probabilities:
            raise ValueError(
                f"Desired prediction '{desired_prediction}' is not a valid "
                f"class for {domain}. Available classes: {list(original_probabilities)}"
            )

        if original_prediction == desired_prediction:
            return {
                "original_input": data,
                "original_prediction": original,
                "desired_prediction": desired_prediction,
                "candidate_count": 0,
                "feasible_candidate_count": 0,
                "rejected_candidate_count": 0,
                "analysis_status": "already_desired_outcome",
                "analysis_message": (
                    "The model already predicts the domain's desired "
                    "outcome, so no preventive intervention is required."
                ),
                "counterfactuals": [],
                "successful_counterfactuals": [],
                "successful_counterfactual_count": 0,
                "best_successful_counterfactual": None,
                "risk_reduction_only": [],
                "risk_reduction_only_count": 0,
                "best_risk_reduction_only": None,
                "non_beneficial_count": 0,
                "best_intervention": None,
                "recommended_changes": {},
                "minimum_effective_change": None,
                "highest_risk_reduction": None,
                "rejected_candidates": [],
                "profile_analysis": profile_result,
                "profile_guidance": profile_guidance,
                "profile_guided": bool(profile_guided),
                "profile_guided_feature_limit": max_guided_features,
                "prioritized_features_used": [],
                "interpretation": (
                    "The model already predicts the desired outcome. "
                    "Counterfactual analysis is therefore not required."
                ),
            }

        prioritized_features = None
        if profile_guided and assigned_profile:
            prioritized_features = self.profile_guidance.prioritized_feature_set(
                domain, data, assigned_profile, max_features=max_guided_features
            )

        candidates = self._make_candidates(data, domain, prioritized_features)
        feasible, rejected = [], []
        for candidate in candidates:
            valid, reasons = self.constraints.filter_changes(domain, candidate["changes"])
            (feasible if valid else rejected).append(
                candidate if valid else {**candidate, "reasons": reasons}
            )

        scenarios = []
        for candidate in feasible:
            changed_data = {**data, **candidate["changes"]}
            result = self.predict(changed_data)
            new_prediction = result["failure_type"]
            new_probability = result.get("class_probabilities", {}).get(
                original_prediction, 0.0
            )
            reduction = original_probability - new_probability
            successful = new_prediction == desired_prediction
            scenarios.append({
                "feature": candidate["feature"],
                "old_value": candidate["old_value"],
                "new_value": candidate["new_value"],
                "changes": candidate["changes"],
                "prediction": new_prediction,
                "probability": result["probability"],
                "class_probabilities": result.get("class_probabilities", {}),
                "original_class_probability": round(original_probability, 6),
                "new_original_class_probability": round(new_probability, 6),
                "risk_reduction": round(reduction, 6),
                "risk_reduction_percentage_points": round(reduction * 100, 4),
                "prediction_transition": new_prediction != original_prediction,
                "successful": successful,
                "beneficial": reduction > 0.000001,
            })

        successful = [item for item in scenarios if item["successful"]]
        risk_only = [
            item for item in scenarios
            if item["beneficial"] and not item["successful"]
        ]
        non_beneficial = [item for item in scenarios if not item["beneficial"]]
        ranked = sorted(
            scenarios,
            key=lambda item: (item["risk_reduction"], item["prediction_transition"]),
            reverse=True,
        )
        ranked_successful = sorted(
            successful, key=lambda item: item["risk_reduction"], reverse=True
        )
        ranked_risk_only = sorted(
            risk_only, key=lambda item: item["risk_reduction"], reverse=True
        )
        best_successful = ranked_successful[0] if ranked_successful else None
        best_risk_only = ranked_risk_only[0] if ranked_risk_only else None
        best_intervention = ranked[0] if ranked else None

        if best_successful:
            status = "successful_counterfactual_found"
            message = (
                "A feasible counterfactual intervention was identified that "
                "changes the model prediction to the desired outcome."
            )
        elif best_risk_only:
            status = "risk_reduction_without_transition"
            message = (
                "A feasible intervention was identified that reduces the "
                "model-predicted risk, but the predicted outcome does not change."
            )
        else:
            status = "no_beneficial_intervention_found"
            message = (
                "No feasible intervention produced a positive reduction in "
                "the model-predicted risk."
            )

        recommended = (
            best_successful or best_risk_only or {}
        ).get("changes", {})

        return {
            "original_input": data,
            "original_prediction": original,
            "desired_prediction": desired_prediction,
            "candidate_count": len(candidates),
            "feasible_candidate_count": len(feasible),
            "rejected_candidate_count": len(rejected),
            "analysis_status": status,
            "analysis_message": message,
            "counterfactuals": ranked,
            "successful_counterfactuals": ranked_successful,
            "successful_counterfactual_count": len(ranked_successful),
            "best_successful_counterfactual": best_successful,
            "risk_reduction_only": ranked_risk_only,
            "risk_reduction_only_count": len(ranked_risk_only),
            "best_risk_reduction_only": best_risk_only,
            "non_beneficial_count": len(non_beneficial),
            "best_intervention": best_intervention,
            "recommended_changes": recommended,
            "minimum_effective_change": best_successful,
            "highest_risk_reduction": best_intervention,
            "rejected_candidates": rejected,
            "profile_analysis": profile_result,
            "profile_guidance": profile_guidance,
            "profile_guided": bool(profile_guided),
            "profile_guided_feature_limit": max_guided_features,
            "prioritized_features_used": prioritized_features or [],
            "interpretation": (
                "Counterfactual results represent model-based scenario analysis. "
                "A positive predicted risk reduction does not establish a causal "
                "effect or guarantee real-world failure prevention. A successful "
                "counterfactual means that the tested input change caused the "
                "trained model's predicted class to change to the desired class."
            ),
        }
