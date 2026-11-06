class RecommendationRules:

    # --------------------------------------------------
    # Student rules
    # --------------------------------------------------

    @staticmethod
    def student_rules(row):

        recommendations = []

        score = row.get("Score", 0)
        severity = row.get("Severity", 0)

        try:
            score = float(score)
        except (ValueError, TypeError):
            score = 0

        try:
            severity = float(severity)
        except (ValueError, TypeError):
            severity = 0

        if score < 10:
            recommendations.append(
                "Increase the final academic score before the next examination."
            )

        if severity > 0:
            recommendations.append(
                "Previous failures are present; focus on the subjects or areas "
                "where difficulties occurred previously."
            )

        if score < 8:
            recommendations.append(
                "Follow a structured study schedule and increase preparation time."
            )

        if not recommendations:
            recommendations.append(
                "Maintain the current academic performance and study routine."
            )

        return recommendations

    # --------------------------------------------------
    # Software rules
    # --------------------------------------------------

    @staticmethod
    def software_rules(row):

        recommendations = []

        severity = row.get("Severity", 0)

        try:
            severity = float(severity)
        except (ValueError, TypeError):
            severity = 0

        if severity >= 5:
            recommendations.append(
                "Treat this as a high-priority software issue and investigate it promptly."
            )

        elif severity >= 3:
            recommendations.append(
                "Prioritize investigation and resolution of this software issue."
            )

        else:
            recommendations.append(
                "Review the issue and resolve it according to its assigned priority."
            )

        recommendations.append(
            "Review similar historical software failures before implementing the fix."
        )

        recommendations.append(
            "Document the cause and corrective action for future analysis."
        )

        return recommendations

    # --------------------------------------------------
    # Jobs rules
    # --------------------------------------------------

    @staticmethod
    def jobs_rules(row):

        recommendations = []

        score = row.get("Score", 0)

        try:
            score = float(score)
        except (ValueError, TypeError):
            score = 0

        if score < 50:
            recommendations.append(
                "Improve the skill-match score before applying for similar positions."
            )

        elif score < 70:
            recommendations.append(
                "Strengthen the skills that are most relevant to the target position."
            )

        else:
            recommendations.append(
                "Maintain the current skill level and continue developing relevant expertise."
            )

        recommendations.append(
            "Add measurable skills and achievements to the resume."
        )

        return recommendations

    # --------------------------------------------------
    # Project rules
    # --------------------------------------------------

    @staticmethod
    def project_rules(row):

        recommendations = []

        score = row.get("Score", 0)

        try:
            score = float(score)
        except (ValueError, TypeError):
            score = 0

        if score < 30:
            recommendations.append(
                "Project completion is very low; review schedule, resources, and blocked tasks."
            )

        elif score < 60:
            recommendations.append(
                "Increase project progress by addressing delayed or incomplete activities."
            )

        elif score < 80:
            recommendations.append(
                "Monitor remaining tasks closely to ensure timely completion."
            )

        else:
            recommendations.append(
                "Maintain the current project progress and monitor remaining tasks."
            )

        recommendations.append(
            "Review previous project issues to identify opportunities for improvement."
        )

        return recommendations

    # --------------------------------------------------
    # Generic rules
    # --------------------------------------------------

    @staticmethod
    def generic_rules(row):

        return [
            "Review the factors associated with the predicted failure.",
            "Improve the most important measurable performance factors.",
            "Monitor future outcomes to identify repeated failure patterns."
        ]

    # --------------------------------------------------
    # Main rule engine
    # --------------------------------------------------

    @classmethod
    def apply(cls, row):

        domain = str(row.get("Domain", "")).strip()

        if domain == "Student":
            return cls.student_rules(row)

        if domain == "Software":
            return cls.software_rules(row)

        if domain == "Jobs":
            return cls.jobs_rules(row)

        if domain == "Projects":
            return cls.project_rules(row)

        return cls.generic_rules(row)