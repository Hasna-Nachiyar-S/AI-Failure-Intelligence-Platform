from backend.counterfactual.generator import (
    CounterfactualGenerator
)


class WhatIfSimulator:

    def __init__(self, model_dir="models"):

        self.engine = CounterfactualGenerator(
            model_dir
        )

    def simulate(
        self,
        original,
        changes
    ):

        current = dict(original)

        before = self.engine.predict(
            current
        )

        for key, value in changes.items():

            current[key] = value

        after = self.engine.predict(
            current
        )

        before_probs = before.get(
            "class_probabilities",
            {}
        )

        after_probs = after.get(
            "class_probabilities",
            {}
        )

        old_probability = before[
            "probability"
        ]

        new_probability = after[
            "probability"
        ]

        probability_change = (
            new_probability
            - old_probability
        )

        return {
            "original_input":
                original,

            "changes":
                changes,

            "new_input":
                current,

            "original_prediction": {
                "failure_type":
                    before["failure_type"],
                "probability":
                    old_probability
            },

            "new_prediction": {
                "failure_type":
                    after["failure_type"],
                "probability":
                    new_probability
            },

            "original_probability":
                old_probability,

            "new_probability":
                new_probability,

            "probability_change":
                probability_change,

            "class_probabilities_before":
                before_probs,

            "class_probabilities_after":
                after_probs,

            "prediction_changed":
                before["failure_type"]
                != after["failure_type"]
        }