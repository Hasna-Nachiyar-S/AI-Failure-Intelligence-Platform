"""
Profile-guided feature selection.

This module connects failure profiles with actionable
features for counterfactual analysis.

The profile is used to PRIORITIZE features that differ
from the profile characteristics. It does not claim that
the feature is causally responsible for failure.
"""

from typing import Any, Dict, List


class ProfileGuidanceEngine:

    def __init__(self):

        # -----------------------------------------------------
        # Features that can be changed in each domain.
        #
        # These should remain consistent with the
        # DomainConstraintEngine.
        # -----------------------------------------------------

        self.actionable_features = {

            "Student": [
                "absences",
                "studytime"
            ],

            "Software": [
                "pr",
                "cl",
                "rp",
                "os",
                "bs",
                "bsr"
            ],

            "Jobs": [
                "skills_match_score",
                "project_count",
                "resume_length",
                "github_activity"
            ],

            "Projects": [
                "Project_Cost",
                "Project_Benefit",
                "Completion",
                "Complexity",
                "Phase"
            ]
        }

    # =========================================================
    # Domain normalization
    # =========================================================

    def normalize_domain(
        self,
        domain: str
    ) -> str:

        mapping = {
            "student": "Student",
            "software": "Software",
            "jobs": "Jobs",
            "projects": "Projects"
        }

        value = str(
            domain
        ).strip().lower()

        if value not in mapping:

            raise ValueError(
                f"Unsupported domain: {domain}"
            )

        return mapping[value]

    # =========================================================
    # Calculate profile differences
    # =========================================================

    def rank_features(
        self,
        domain: str,
        current_data: Dict[str, Any],
        profile: Dict[str, Any]
    ) -> List[Dict[str, Any]]:

        domain = self.normalize_domain(
            domain
        )

        actionable = (
            self.actionable_features[
                domain
            ]
        )

        profile_means = (
            profile.get(
                "feature_means",
                {}
            )
        )

        ranked = []

        for feature in actionable:

            current_value = (
                current_data.get(
                    feature
                )
            )

            profile_value = (
                profile_means.get(
                    feature
                )
            )

            # -------------------------------------------------
            # If either value is unavailable, skip ranking.
            # -------------------------------------------------

            if (
                current_value is None
                or profile_value is None
            ):

                continue

            try:
                current_numeric = float(current_value)
                profile_numeric = float(profile_value)
                difference = current_numeric - profile_numeric
                absolute_difference = abs(difference)

                ranked.append({
                    "feature": feature,
                    "current_value": current_value,
                    "profile_mean": round(profile_numeric, 4),
                    "difference": round(difference, 4),
                    "absolute_difference": round(absolute_difference, 4)
                })
            except (TypeError, ValueError):
                # Categorical features are ranked by mismatch with the
                # historical profile mode when available.
                modes = profile.get("feature_modes", {})
                mode = modes.get(feature)
                if mode is None:
                    continue
                mismatch = 0 if str(current_value).strip() == str(mode).strip() else 1
                ranked.append({
                    "feature": feature,
                    "current_value": current_value,
                    "profile_mode": mode,
                    "difference": None,
                    "absolute_difference": mismatch
                })

        # -----------------------------------------------------
        # Largest difference first.
        # -----------------------------------------------------

        ranked.sort(
            key=lambda item:
                item[
                    "absolute_difference"
                ],
            reverse=True
        )

        return ranked


    def prioritized_feature_set(
        self,
        domain: str,
        current_data: Dict[str, Any],
        profile: Dict[str, Any],
        max_features: int | None = None
    ) -> List[str]:
        """Return profile-guided actionable features in priority order.

        The ranking is descriptive: it identifies actionable features whose
        current values differ most from the assigned historical profile.
        It does not claim that moving toward a profile causes improvement.
        """
        ranked = self.rank_features(domain, current_data, profile)
        features = [item["feature"] for item in ranked]

        # Keep actionable features without profile statistics available
        # after ranked features, so the method never becomes unusable merely
        # because a profile lacks a value for one feature.
        for feature in self.actionable_features[self.normalize_domain(domain)]:
            if feature not in features:
                features.append(feature)

        if max_features is not None:
            return features[:max(1, int(max_features))]
        return features

    # =========================================================
    # Get profile guidance
    # =========================================================

    def generate_guidance(
        self,
        domain: str,
        current_data: Dict[str, Any],
        profile: Dict[str, Any]
    ) -> Dict[str, Any]:

        domain = self.normalize_domain(
            domain
        )

        ranked_features = (
            self.rank_features(
                domain,
                current_data,
                profile
            )
        )

        prioritized_features = [
            item[
                "feature"
            ]
            for item
            in ranked_features
        ]

        return {

            "domain":
                domain,

            "profile_id":
                profile.get(
                    "profile_id"
                ),

            "profile_failure_rate":
                profile.get(
                    "failure_rate"
                ),

            "profile_failure_rate_percentage":
                profile.get(
                    "failure_rate_percentage"
                ),

            "prioritized_features":
                prioritized_features,

            "feature_comparison":
                ranked_features,

            "interpretation":
                (
                    "Features are prioritized based on "
                    "their difference from the assigned "
                    "historical profile. This ranking is "
                    "used to guide model-based scenario "
                    "analysis and does not establish "
                    "causal relationships."
                )
        }