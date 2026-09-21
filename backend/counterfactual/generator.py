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

        self.manager = DomainModelManager(
            model_dir
        )

        self.constraints = (
            DomainConstraintEngine()
        )

        self.sampler = CandidateSampler()

        self.profile_analyzer = (
            FailureProfileAnalyzer(
                n_clusters=3
            )
        )

        self.profile_guidance = (
            ProfileGuidanceEngine()
        )

    # =========================================================
    # Prediction
    # =========================================================

    def predict(self, data):

        domain = data.get("Domain")

        result = self.manager.predict(
            domain,
            data
        )

        return {
            "domain":
                domain,

            "failure_type":
                result["failure_type"],

            "probability":
                result["probability"],

            "class_probabilities":
                result.get(
                    "class_probabilities",
                    {}
                )
        }

    # =========================================================
    # Candidate generation
    # =========================================================

    def _make_candidates(
        self,
        data,
        domain,
        prioritized_features=None
    ):

        candidates = []

        actionable_features = (
            prioritized_features
            if prioritized_features
            else self.constraints.actionable_features(domain)
        )

        for feature in actionable_features:

            current_value = data.get(
                feature
            )

            if current_value is None:
                continue

            candidate_values = (
                self.sampler.get_candidates(
                    domain,
                    feature,
                    current_value
                )
            )

            for new_value in candidate_values:

                if new_value == current_value:
                    continue

                # -------------------------------------------------
                # Apply domain constraint validation
                # -------------------------------------------------

                valid, reason = (
                    self.constraints.validate_change(
                        domain,
                        feature,
                        new_value
                    )
                )

                if not valid:
                    continue

                candidates.append({
                    "feature":
                        feature,

                    "old_value":
                        current_value,

                    "new_value":
                        new_value,

                    "changes": {
                        feature:
                            new_value
                    }
                })

        return candidates

    # =========================================================
    # Generate counterfactual analysis
    # =========================================================

    def generate(
        self,
        data,
        desired_prediction=None,
        profile_guided=True,
        max_guided_features=2
    ):

        # -----------------------------------------------------
        # Original prediction
        # -----------------------------------------------------

        original = self.predict(
            data
        )

        domain = (
            self.manager.normalize_domain(
                data.get("Domain")
            )
        )

        # ---------------------------------------------------------
        # Identify historical failure profile
        # ---------------------------------------------------------

        profile_result = (
            self.profile_analyzer.predict_profile(
                domain,
                data
            )
        )

        assigned_profile = (
            profile_result.get(
                "profile"
            )
        )

        profile_guidance = None

        if assigned_profile:

            profile_guidance = (
                self.profile_guidance.generate_guidance(
                    domain,
                    data,
                    assigned_profile
                )
            )

        original_prediction = (
            original["failure_type"]
        )

        original_probability = (
            original["probability"]
        )

        original_probabilities = (
            original.get(
                "class_probabilities",
                {}
            )
        )

        # -----------------------------------------------------
        # Determine desired prediction
        # -----------------------------------------------------

        if desired_prediction is None:

            alternatives = [
                cls
                for cls in original_probabilities
                if cls != original_prediction
            ]

            if alternatives:

                desired_prediction = max(
                    alternatives,
                    key=original_probabilities.get
                )

        # -----------------------------------------------------
        # Profile-guided feature prioritization
        # -----------------------------------------------------

        prioritized_features = None
        if profile_guided and assigned_profile:
            prioritized_features = self.profile_guidance.prioritized_feature_set(
                domain,
                data,
                assigned_profile,
                max_features=max_guided_features
            )

        # -----------------------------------------------------
        # Generate candidates
        # -----------------------------------------------------

        candidates = self._make_candidates(
            data,
            domain,
            prioritized_features=prioritized_features
        )

        feasible_candidates = []
        rejected_candidates = []

        # -----------------------------------------------------
        # Feasibility filtering
        # -----------------------------------------------------

        for candidate in candidates:

            valid, reasons = (
                self.constraints.filter_changes(
                    domain,
                    candidate["changes"]
                )
            )

            if valid:

                feasible_candidates.append(
                    candidate
                )

            else:

                rejected_candidates.append({
                    **candidate,
                    "reasons": reasons
                })

        # -----------------------------------------------------
        # Evaluate every feasible candidate
        # -----------------------------------------------------

        scenarios = []

        for candidate in feasible_candidates:

            new_data = dict(data)

            new_data.update(
                candidate["changes"]
            )

            result = self.predict(
                new_data
            )

            new_prediction = (
                result["failure_type"]
            )

            new_probabilities = (
                result.get(
                    "class_probabilities",
                    {}
                )
            )

            # -------------------------------------------------
            # Probability of original predicted class
            # -------------------------------------------------

            new_original_class_probability = (
                new_probabilities.get(
                    original_prediction,
                    0.0
                )
            )

            # -------------------------------------------------
            # Model-predicted risk reduction
            # -------------------------------------------------

            risk_reduction = (
                original_probability
                - new_original_class_probability
            )

            # -------------------------------------------------
            # Prediction transition
            # -------------------------------------------------

            prediction_transition = (
                new_prediction
                != original_prediction
            )

            # -------------------------------------------------
            # Desired-class transition
            # -------------------------------------------------

            successful = (
                desired_prediction is not None
                and new_prediction
                == desired_prediction
            )

            # -------------------------------------------------
            # Beneficial intervention
            #
            # Positive risk reduction means the model predicts
            # a lower probability for the original predicted
            # class.
            # -------------------------------------------------

            beneficial = (
                risk_reduction > 0.000001
            )

            scenarios.append({

                "feature":
                    candidate["feature"],

                "old_value":
                    candidate["old_value"],

                "new_value":
                    candidate["new_value"],

                "changes":
                    candidate["changes"],

                "prediction":
                    new_prediction,

                "probability":
                    result["probability"],

                "class_probabilities":
                    new_probabilities,

                "original_class_probability":
                    round(
                        original_probability,
                        6
                    ),

                "new_original_class_probability":
                    round(
                        new_original_class_probability,
                        6
                    ),

                "risk_reduction":
                    round(
                        risk_reduction,
                        6
                    ),

                "risk_reduction_percentage_points":
                    round(
                        risk_reduction * 100,
                        4
                    ),

                "prediction_transition":
                    prediction_transition,

                "successful":
                    successful,

                "beneficial":
                    beneficial
            })

        # =====================================================
        # Separate result categories
        # =====================================================

        # Successful counterfactual:
        # original class changes to desired class.
        successful_counterfactuals = [
            item
            for item in scenarios
            if item["successful"]
        ]

        # Beneficial but unsuccessful:
        # risk decreases but prediction does not change
        # to the desired class.
        risk_reduction_only = [
            item
            for item in scenarios
            if (
                item["beneficial"]
                and not item["successful"]
            )
        ]

        # Neutral or harmful:
        # no reduction or increased original-class risk.
        non_beneficial = [
            item
            for item in scenarios
            if not item["beneficial"]
        ]

        # =====================================================
        # Ranking
        # =====================================================

        ranked_scenarios = sorted(
            scenarios,
            key=lambda item: (
                item["risk_reduction"],
                item["prediction_transition"]
            ),
            reverse=True
        )

        ranked_successful = sorted(
            successful_counterfactuals,
            key=lambda item: (
                item["risk_reduction"]
            ),
            reverse=True
        )

        ranked_risk_reduction_only = sorted(
            risk_reduction_only,
            key=lambda item: (
                item["risk_reduction"]
            ),
            reverse=True
        )

        # =====================================================
        # Best successful counterfactual
        # =====================================================

        best_successful = None

        if ranked_successful:

            best_successful = (
                ranked_successful[0]
            )

        # =====================================================
        # Best risk-reduction-only intervention
        # =====================================================

        best_risk_reduction_only = None

        if ranked_risk_reduction_only:

            best_risk_reduction_only = (
                ranked_risk_reduction_only[0]
            )

        # =====================================================
        # Best overall intervention
        # =====================================================

        best_intervention = None

        if ranked_scenarios:

            best_intervention = (
                ranked_scenarios[0]
            )

        # =====================================================
        # Determine overall status
        # =====================================================

        if best_successful is not None:

            analysis_status = (
                "successful_counterfactual_found"
            )

            analysis_message = (
                "A feasible counterfactual "
                "intervention was identified that "
                "changes the model prediction to "
                "the desired outcome."
            )

        elif best_risk_reduction_only is not None:

            analysis_status = (
                "risk_reduction_without_transition"
            )

            analysis_message = (
                "A feasible intervention was "
                "identified that reduces the "
                "model-predicted risk, but the "
                "predicted outcome does not change."
            )

        else:

            analysis_status = (
                "no_beneficial_intervention_found"
            )

            analysis_message = (
                "No feasible intervention produced "
                "a positive reduction in the "
                "model-predicted risk."
            )

        # =====================================================
        # Recommended changes
        # =====================================================

        recommended_changes = {}

        if best_successful is not None:

            recommended_changes = (
                best_successful["changes"]
            )

        elif best_risk_reduction_only is not None:

            recommended_changes = (
                best_risk_reduction_only["changes"]
            )

        # =====================================================
        # Final result
        # =====================================================

        return {

            # -------------------------------------------------
            # Input
            # -------------------------------------------------

            "original_input":
                data,

            # -------------------------------------------------
            # Original prediction
            # -------------------------------------------------

            "original_prediction":
                original,

            # -------------------------------------------------
            # Desired prediction
            # -------------------------------------------------

            "desired_prediction":
                desired_prediction,

            # -------------------------------------------------
            # Candidate statistics
            # -------------------------------------------------

            "candidate_count":
                len(candidates),

            "feasible_candidate_count":
                len(feasible_candidates),

            "rejected_candidate_count":
                len(rejected_candidates),

            # -------------------------------------------------
            # Result classification
            # -------------------------------------------------

            "analysis_status":
                analysis_status,

            "analysis_message":
                analysis_message,

            # -------------------------------------------------
            # All scenarios
            # -------------------------------------------------

            "counterfactuals":
                ranked_scenarios,

            # -------------------------------------------------
            # Successful counterfactuals
            # -------------------------------------------------

            "successful_counterfactuals":
                ranked_successful,

            "successful_counterfactual_count":
                len(
                    ranked_successful
                ),

            "best_successful_counterfactual":
                best_successful,

            # -------------------------------------------------
            # Risk-reduction-only interventions
            # -------------------------------------------------

            "risk_reduction_only":
                ranked_risk_reduction_only,

            "risk_reduction_only_count":
                len(
                    ranked_risk_reduction_only
                ),

            "best_risk_reduction_only":
                best_risk_reduction_only,

            # -------------------------------------------------
            # Non-beneficial interventions
            # -------------------------------------------------

            "non_beneficial_count":
                len(
                    non_beneficial
                ),

            # -------------------------------------------------
            # Best overall
            # -------------------------------------------------

            "best_intervention":
                best_intervention,

            # -------------------------------------------------
            # Recommended change
            # -------------------------------------------------

            "recommended_changes":
                recommended_changes,

            # -------------------------------------------------
            # Backward compatibility
            # -------------------------------------------------

            "minimum_effective_change":
                best_successful,

            "highest_risk_reduction":
                best_intervention,

            # -------------------------------------------------
            # Rejected candidates
            # -------------------------------------------------

            "rejected_candidates":
                rejected_candidates,

            "profile_analysis": profile_result,

            "profile_guidance": profile_guidance,

            "profile_guided": bool(profile_guided),

            "profile_guided_feature_limit": max_guided_features,

            "prioritized_features_used": prioritized_features or [],

            # -------------------------------------------------
            # Interpretation
            # -------------------------------------------------

            "interpretation":
                (
                    "Counterfactual results represent "
                    "model-based scenario analysis. "
                    "A positive predicted risk reduction "
                    "does not establish a causal effect "
                    "or guarantee real-world failure "
                    "prevention. A successful counterfactual "
                    "means that the tested input change "
                    "caused the trained model's predicted "
                    "class to change to the desired class."
                )
        }