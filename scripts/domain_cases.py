"""Canonical representative input payloads reused by backend smoke scripts."""

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
