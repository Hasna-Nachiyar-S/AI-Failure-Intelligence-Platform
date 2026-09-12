# backend/what_if/simulator.py

from backend.counterfactual.generator import CounterfactualGenerator


class WhatIfSimulator:

    def __init__(self, model_dir="models"):
        self.engine = CounterfactualGenerator(model_dir)

    def simulate(self, original, changes):
        """
        Compare the original input with a user-defined
        what-if scenario.
        """

        current = original.copy()
        current_prediction = self.engine.predict(current)

        # Apply user changes
        for key, value in changes.items():
            if key in current:
                current[key] = value

        new_prediction = self.engine.predict(current)

        old_probability = current_prediction["probability"]
        new_probability = new_prediction["probability"]

        return {
            "original_input": original,
            "changes": changes,
            "new_input": current,

            "original_prediction": {
                "failure_type":
                    current_prediction["failure_type"],
                "probability": old_probability
            },

            "new_prediction": {
                "failure_type":
                    new_prediction["failure_type"],
                "probability": new_probability
            },

            "probability_change":
                new_probability - old_probability,

            "prediction_changed":
                current_prediction["failure_type"]
                != new_prediction["failure_type"]
        }