class RecommendationRules:
    @staticmethod
    def _number(row, key):
        try:
            return float(row.get(key, 0))
        except (ValueError, TypeError):
            return 0

    @classmethod
    def student_rules(cls, row):
        score, severity = cls._number(row, "Score"), cls._number(row, "Severity")
        recommendations = []
        if score < 10:
            recommendations.append("Increase the final academic score before the next examination.")
        if severity > 0:
            recommendations.append(
                "Previous failures are present; focus on the subjects or areas "
                "where difficulties occurred previously."
            )
        if score < 8:
            recommendations.append("Follow a structured study schedule and increase preparation time.")
        return recommendations or ["Maintain the current academic performance and study routine."]

    @staticmethod
    def software_rules(row):
        severity = RecommendationRules._number(row, "Severity")
        if severity >= 5:
            first = "Treat this as a high-priority software issue and investigate it promptly."
        elif severity >= 3:
            first = "Prioritize investigation and resolution of this software issue."
        else:
            first = "Review the issue and resolve it according to its assigned priority."
        return [
            first,
            "Review similar historical software failures before implementing the fix.",
            "Document the cause and corrective action for future analysis.",
        ]

    @staticmethod
    def jobs_rules(row):
        score = RecommendationRules._number(row, "Score")
        if score < 50:
            first = "Improve the skill-match score before applying for similar positions."
        elif score < 70:
            first = "Strengthen the skills that are most relevant to the target position."
        else:
            first = "Maintain the current skill level and continue developing relevant expertise."
        return [first, "Add measurable skills and achievements to the resume."]

    @staticmethod
    def project_rules(row):
        score = RecommendationRules._number(row, "Score")
        if score < 30:
            first = "Project completion is very low; review schedule, resources, and blocked tasks."
        elif score < 60:
            first = "Increase project progress by addressing delayed or incomplete activities."
        elif score < 80:
            first = "Monitor remaining tasks closely to ensure timely completion."
        else:
            first = "Maintain the current project progress and monitor remaining tasks."
        return [first, "Review previous project issues to identify opportunities for improvement."]

    @staticmethod
    def generic_rules(row):
        return [
            "Review the factors associated with the predicted failure.",
            "Improve the most important measurable performance factors.",
            "Monitor future outcomes to identify repeated failure patterns.",
        ]

    @classmethod
    def apply(cls, row):
        handlers = {
            "Student": cls.student_rules,
            "Software": cls.software_rules,
            "Jobs": cls.jobs_rules,
            "Projects": cls.project_rules,
        }
        domain = str(row.get("Domain", "")).strip()
        return handlers.get(domain, cls.generic_rules)(row)
