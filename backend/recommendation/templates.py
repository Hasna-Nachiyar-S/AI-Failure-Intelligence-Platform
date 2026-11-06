class RecommendationTemplates:

    # --------------------------------------------------
    # Generic recommendations
    # --------------------------------------------------

    GENERIC = {
        "Passed": [
            "Continue maintaining the current performance level.",
            "Monitor future performance to avoid repeated failures.",
            "Identify the factors that contributed to the successful outcome."
        ],

        "Selected": [
            "Maintain the current level of performance.",
            "Continue improving skills that contributed to the successful outcome.",
            "Keep developing relevant experience and qualifications."
        ],

        "Rejected": [
            "Improve the skills that are most relevant to the target role.",
            "Review the reasons for previous unsuccessful applications.",
            "Strengthen your profile before applying again."
        ]
    }

    # --------------------------------------------------
    # Student
    # --------------------------------------------------

    STUDENT = {
        "Exam Failure": [
            "Improve academic performance before the next examination.",
            "Increase study time and follow a consistent study schedule.",
            "Reduce avoidable absences and attend classes regularly.",
            "Review previous weak areas and focus on targeted improvement."
        ],

        "Passed": [
            "Continue the current study routine.",
            "Maintain regular attendance and consistent preparation.",
            "Focus on strengthening subjects with lower performance."
        ]
    }

    # --------------------------------------------------
    # Software
    # --------------------------------------------------

    SOFTWARE = {
        "default": [
            "Prioritize investigation of the reported software issue.",
            "Review similar historical failures before applying a fix.",
            "Document the root cause and corrective action.",
            "Monitor the issue after resolution to reduce recurrence."
        ]
    }

    # --------------------------------------------------
    # Jobs
    # --------------------------------------------------

    JOBS = {
        "Rejected": [
            "Improve the skills that are most relevant to the target position.",
            "Strengthen the resume with measurable technical achievements.",
            "Gain additional relevant experience or certifications.",
            "Review skill gaps before applying for similar positions."
        ],

        "Selected": [
            "Maintain the current skill level.",
            "Continue developing relevant technical and professional skills.",
            "Build additional experience to improve future opportunities."
        ]
    }

    # --------------------------------------------------
    # Projects
    # --------------------------------------------------

    PROJECTS = {
        "default": [
            "Monitor project completion regularly.",
            "Identify delayed activities and address them early.",
            "Improve task planning and resource allocation.",
            "Review previous project issues to prevent similar problems."
        ]
    }

    # --------------------------------------------------
    # Get recommendations
    # --------------------------------------------------

    @classmethod
    def get_recommendations(cls, domain, failure_type):

        domain = str(domain).strip()
        failure_type = str(failure_type).strip()

        if domain == "Student":
            return cls.STUDENT.get(
                failure_type,
                cls.GENERIC.get(
                    failure_type,
                    cls.STUDENT["Exam Failure"]
                )
            )

        if domain == "Software":
            return cls.SOFTWARE["default"]

        if domain == "Jobs":
            return cls.JOBS.get(
                failure_type,
                cls.GENERIC.get(
                    failure_type,
                    cls.JOBS["Rejected"]
                )
            )

        if domain == "Projects":
            return cls.PROJECTS["default"]

        return cls.GENERIC.get(
            failure_type,
            [
                "Review the factors associated with the predicted outcome.",
                "Improve the most important measurable performance factors.",
                "Monitor future outcomes to identify recurring patterns."
            ]
        )