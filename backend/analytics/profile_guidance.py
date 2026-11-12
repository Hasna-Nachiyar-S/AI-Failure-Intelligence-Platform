"""Rank actionable features by their difference from a historical profile."""

from typing import Any


class ProfileGuidanceEngine:
    actionable_features = {
        "Student": ["absences", "studytime"],
        "Software": ["pr", "cl", "rp", "os", "bs", "bsr"],
        "Jobs": ["skills_match_score", "project_count", "resume_length", "github_activity"],
        "Projects": ["Project_Cost", "Project_Benefit", "Completion", "Complexity", "Phase"],
    }
    domain_names = {name.lower(): name for name in actionable_features}

    @classmethod
    def normalize_domain(cls, domain: str) -> str:
        value = cls.domain_names.get(str(domain).strip().lower())
        if value is None:
            raise ValueError(f"Unsupported domain: {domain}")
        return value

    def rank_features(
        self, domain: str, current_data: dict[str, Any], profile: dict[str, Any]
    ) -> list[dict[str, Any]]:
        domain = self.normalize_domain(domain)
        means = profile.get("feature_means", {})
        modes = profile.get("feature_modes", {})
        ranked = []

        for feature in self.actionable_features[domain]:
            current = current_data.get(feature)
            profile_value = means.get(feature)
            if current is None or profile_value is None:
                continue

            try:
                current_number, profile_number = float(current), float(profile_value)
                difference = current_number - profile_number
                ranked.append({
                    "feature": feature,
                    "current_value": current,
                    "profile_mean": round(profile_number, 4),
                    "difference": round(difference, 4),
                    "absolute_difference": round(abs(difference), 4),
                })
            except (TypeError, ValueError):
                mode = modes.get(feature)
                if mode is None:
                    continue
                mismatch = int(str(current).strip() != str(mode).strip())
                ranked.append({
                    "feature": feature,
                    "current_value": current,
                    "profile_mode": mode,
                    "difference": None,
                    "absolute_difference": mismatch,
                })

        ranked.sort(key=lambda item: item["absolute_difference"], reverse=True)
        return ranked

    def prioritized_feature_set(
        self, domain: str, current_data: dict[str, Any], profile: dict[str, Any],
        max_features: int | None = None,
    ) -> list[str]:
        domain = self.normalize_domain(domain)
        ranked = [item["feature"] for item in self.rank_features(domain, current_data, profile)]
        ranked.extend(feature for feature in self.actionable_features[domain] if feature not in ranked)
        return ranked[:max(1, int(max_features))] if max_features is not None else ranked

    def generate_guidance(
        self, domain: str, current_data: dict[str, Any], profile: dict[str, Any]
    ) -> dict[str, Any]:
        domain = self.normalize_domain(domain)
        ranked = self.rank_features(domain, current_data, profile)
        return {
            "domain": domain,
            "profile_id": profile.get("profile_id"),
            "profile_failure_rate": profile.get("failure_rate"),
            "profile_failure_rate_percentage": profile.get("failure_rate_percentage"),
            "prioritized_features": [item["feature"] for item in ranked],
            "feature_comparison": ranked,
            "interpretation": (
                "Features are prioritized based on their difference from the assigned "
                "historical profile. This ranking is used to guide model-based scenario "
                "analysis and does not establish causal relationships."
            ),
        }
