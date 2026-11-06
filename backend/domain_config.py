"""Shared domain names and API-required input fields.

Keep canonical names and aliases here so API validation and model loading do
not maintain separate, potentially divergent domain maps.
"""

DOMAIN_ALIASES = {
    "student": "Student",
    "software": "Software",
    "jobs": "Jobs",
    "projects": "Projects",
}

DOMAIN_REQUIRED_FIELDS = {
    "Student": ("absences", "studytime", "failures", "G1", "G2"),
    "Software": ("pr", "cl", "pd", "co", "rp", "os", "bs", "bsr", "re", "at"),
    "Jobs": (
        "years_experience", "skills_match_score", "education_level",
        "project_count", "resume_length", "github_activity",
    ),
    "Projects": (
        "Complexity", "Project_Type", "Region", "Department",
        "Project_Cost", "Project_Benefit", "Completion", "Phase", "Year", "Month",
    ),
}


def normalize_domain(domain: object) -> str:
    """Return the canonical domain name or raise ValueError for unknown input."""
    value = str(domain or "").strip().lower()
    try:
        return DOMAIN_ALIASES[value]
    except KeyError as exc:
        raise ValueError(f"Unsupported domain: {domain}") from exc
