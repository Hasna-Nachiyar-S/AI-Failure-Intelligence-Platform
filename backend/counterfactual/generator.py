from backend.ml.domain_model_manager import (
    DomainModelManager
)


class CounterfactualGenerator:

    def __init__(self, model_dir="models"):
        self.manager = DomainModelManager(
            model_dir
        )

    def predict(self, data):

        domain = data.get("Domain")

        result = self.manager.predict(
            domain,
            data
        )

        return {
            "domain": domain,
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

    def _student_candidates(self, data):

        candidates = []

        try:
            g1 = float(data.get("G1"))
            g2 = float(data.get("G2"))
            absences = float(
                data.get("absences")
            )
            failures = float(
                data.get("failures")
            )
            studytime = float(
                data.get("studytime")
            )
        except (TypeError, ValueError):
            return candidates

        # G1 changes

        for value in [5, 7, 9, 11, 13, 15]:

            if value != g1:

                candidates.append({
                    "feature": "G1",
                    "old_value": g1,
                    "new_value": value,
                    "changes": {
                        "G1": value
                    }
                })

        # G2 changes

        for value in [5, 7, 9, 11, 13, 15]:

            if value != g2:

                candidates.append({
                    "feature": "G2",
                    "old_value": g2,
                    "new_value": value,
                    "changes": {
                        "G2": value
                    }
                })

        # Absence changes

        for value in [
            0,
            5,
            10,
            20,
            30,
            40,
            50
        ]:

            if value != absences:

                candidates.append({
                    "feature": "absences",
                    "old_value": absences,
                    "new_value": value,
                    "changes": {
                        "absences": value
                    }
                })

        # Previous failures

        for value in [0, 1, 2, 3]:

            if value != failures:

                candidates.append({
                    "feature": "failures",
                    "old_value": failures,
                    "new_value": value,
                    "changes": {
                        "failures": value
                    }
                })

        # Study time

        for value in [1, 2, 3, 4]:

            if value != studytime:

                candidates.append({
                    "feature": "studytime",
                    "old_value": studytime,
                    "new_value": value,
                    "changes": {
                        "studytime": value
                    }
                })

        # G1 + G2

        for new_g1 in [5, 7, 9, 11]:

            for new_g2 in [5, 7, 9, 11]:

                if (
                    new_g1 != g1
                    or new_g2 != g2
                ):

                    candidates.append({
                        "feature": "G1 + G2",
                        "old_value":
                            f"{g1}, {g2}",
                        "new_value":
                            f"{new_g1}, {new_g2}",
                        "changes": {
                            "G1": new_g1,
                            "G2": new_g2
                        }
                    })

        # G2 + absences

        for new_g2 in [5, 7, 9, 11]:

            for new_absences in [
                20,
                30,
                40,
                50
            ]:

                candidates.append({
                    "feature":
                        "G2 + absences",
                    "old_value":
                        f"{g2}, {absences}",
                    "new_value":
                        f"{new_g2}, "
                        f"{new_absences}",
                    "changes": {
                        "G2": new_g2,
                        "absences":
                            new_absences
                    }
                })

        # G1 + G2 + absences

        for new_g1 in [5, 7, 9]:

            for new_g2 in [5, 7, 9]:

                for new_absences in [
                    20,
                    30,
                    40
                ]:

                    candidates.append({
                        "feature":
                            "G1 + G2 + absences",
                        "old_value":
                            f"{g1}, {g2}, "
                            f"{absences}",
                        "new_value":
                            f"{new_g1}, {new_g2}, "
                            f"{new_absences}",
                        "changes": {
                            "G1": new_g1,
                            "G2": new_g2,
                            "absences":
                                new_absences
                        }
                    })

        return candidates

    def _generic_candidates(
        self,
        data,
        domain
    ):

        candidates = []

        features = {
            "Jobs": [
                "years_experience",
                "skills_match_score",
                "project_count",
                "resume_length",
                "github_activity"
            ],
            "Projects": [
                "Project_Cost",
                "Project_Benefit",
                "Completion",
                "Year",
                "Month"
            ],
            "Software": [
                "cl",
                "pd",
                "co",
                "rp",
                "bs",
                "bsr"
            ]
        }

        for feature in features.get(
            domain,
            []
        ):

            value = data.get(feature)

            try:
                value = float(value)
            except (TypeError, ValueError):
                continue

            values = []

            if feature == "skills_match_score":

                values = [
                    max(0, value - 20),
                    max(0, value - 10),
                    min(100, value + 10),
                    min(100, value + 20)
                ]

            elif feature == "Completion":

                values = [
                    max(0, value - 20),
                    max(0, value - 10),
                    min(100, value + 10),
                    min(100, value + 20)
                ]

            elif feature in [
                "years_experience",
                "project_count",
                "github_activity"
            ]:

                values = [
                    max(0, value - 2),
                    max(0, value - 1),
                    value + 1,
                    value + 2
                ]

            elif feature == "resume_length":

                values = [
                    max(0, value - 100),
                    max(0, value - 50),
                    value + 50,
                    value + 100
                ]

            elif feature == "Project_Cost":

                values = [
                    value * 0.8,
                    value * 0.9,
                    value * 1.1,
                    value * 1.2
                ]

            elif feature == "Project_Benefit":

                values = [
                    value * 0.8,
                    value * 0.9,
                    value * 1.1,
                    value * 1.2
                ]

            else:

                values = [
                    max(0, value - 2),
                    max(0, value - 1),
                    value + 1,
                    value + 2
                ]

            for new_value in values:

                if new_value == value:
                    continue

                candidates.append({
                    "feature": feature,
                    "old_value": value,
                    "new_value": new_value,
                    "changes": {
                        feature: new_value
                    }
                })

        return candidates

    def _make_candidates(
        self,
        data,
        domain
    ):

        if domain == "Student":

            return self._student_candidates(
                data
            )

        return self._generic_candidates(
            data,
            domain
        )

    def generate(
        self,
        data,
        desired_prediction=None
    ):

        original = self.predict(data)

        domain = self.manager.normalize_domain(
            data.get("Domain")
        )

        if desired_prediction is None:

            probabilities = original.get(
                "class_probabilities",
                {}
            )

            alternatives = [
                cls
                for cls in probabilities
                if cls != original[
                    "failure_type"
                ]
            ]

            if alternatives:

                desired_prediction = max(
                    alternatives,
                    key=probabilities.get
                )

        candidates = self._make_candidates(
            data,
            domain
        )

        scenarios = []

        for candidate in candidates:

            new_data = dict(data)

            new_data.update(
                candidate["changes"]
            )

            result = self.predict(
                new_data
            )

            successful = (
                desired_prediction is not None
                and result["failure_type"]
                == desired_prediction
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
                    result["failure_type"],
                "probability":
                    result["probability"],
                "class_probabilities":
                    result[
                        "class_probabilities"
                    ],
                "successful":
                    successful
            })

        successful = [
            item
            for item in scenarios
            if item["successful"]
        ]

        minimum = None

        if successful:

            minimum = min(
                successful,
                key=self._change_size
            )

        highest = None

        if successful:

            highest = max(
                successful,
                key=lambda item:
                    item["probability"]
            )

        return {
            "original_input": data,

            "original_prediction":
                original,

            "desired_prediction":
                desired_prediction,

            "counterfactuals":
                scenarios,

            "minimum_effective_change":
                minimum,

            "highest_confidence_scenario":
                highest,

            "recommended_changes":
                minimum["changes"]
                if minimum
                else {}
        }

    def _change_size(self, item):

        total = 0

        for value in item[
            "changes"
        ].values():

            try:
                total += abs(
                    float(value)
                )
            except (TypeError, ValueError):
                total += 1

        return total