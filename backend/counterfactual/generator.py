# backend/counterfactual/generator.py

import os
import joblib
import pandas as pd


class CounterfactualGenerator:

    def __init__(self, model_dir="models"):
        self.model = joblib.load(
            os.path.join(model_dir, "best_classifier.pkl")
        )
        self.scaler = joblib.load(
            os.path.join(model_dir, "scaler.pkl")
        )
        self.encoders = joblib.load(
            os.path.join(model_dir, "encoders.pkl")
        )
        self.failure_encoder = self.encoders["Failure_Type"]

    def _encode(self, col, value):
        try:
            return self.encoders[col].transform([value])[0]
        except Exception:
            return 0

    def _process(self, data):
        df = pd.DataFrame([{
            "Domain": self._encode("Domain", data["Domain"]),
            "Severity": float(data["Severity"]),
            "Score": float(data["Score"]),
            "Description": self._encode(
                "Description", data["Description"]
            )
        }])

        return pd.DataFrame(
            self.scaler.transform(df),
            columns=df.columns
        )

    def predict(self, data):
        x = self._process(data)
        pred = self.model.predict(x)[0]
        label = self.failure_encoder.inverse_transform([pred])[0]

        probs = self.model.predict_proba(x)[0]
        classes = self.model.classes_

        class_probs = {
            self.failure_encoder.inverse_transform([c])[0]:
            float(p)
            for c, p in zip(classes, probs)
        }

        return {
            "failure_type": label,
            "probability": float(max(probs)),
            "class_probabilities": class_probs
        }

    def _candidates(self, original):
        candidates = []

        for score in [
            original["Score"],
            original["Score"] + 1,
            original["Score"] + 2,
            original["Score"] + 3,
            original["Score"] + 5,
            original["Score"] + 7,
            original["Score"] + 10
        ]:
            candidates.append({
                **original,
                "Score": score
            })

        for severity in [
            original["Severity"],
            max(0, original["Severity"] - 1),
            max(0, original["Severity"] - 2),
            max(0, original["Severity"] - 3)
        ]:
            candidates.append({
                **original,
                "Severity": severity
            })

        for score in [
            original["Score"] + 1,
            original["Score"] + 3,
            original["Score"] + 5,
            original["Score"] + 7,
            original["Score"] + 10
        ]:
            for severity in [
                max(0, original["Severity"] - 1),
                max(0, original["Severity"] - 2),
                max(0, original["Severity"] - 3)
            ]:
                candidates.append({
                    **original,
                    "Score": score,
                    "Severity": severity
                })

        return candidates

    def generate(self, original, desired_prediction=None):

        original_result = self.predict(original)
        original_label = original_result["failure_type"]

        results = []

        for candidate in self._candidates(original):

            prediction = self.predict(candidate)

            if desired_prediction:
                valid = (
                    prediction["failure_type"]
                    == desired_prediction
                )
            else:
                valid = (
                    prediction["failure_type"]
                    != original_label
                )

            if not valid:
                continue

            changes = {}

            if candidate["Score"] != original["Score"]:
                changes["Score"] = candidate["Score"]

            if candidate["Severity"] != original["Severity"]:
                changes["Severity"] = candidate["Severity"]

            size = (
                abs(candidate["Score"] - original["Score"])
                + abs(
                    candidate["Severity"]
                    - original["Severity"]
                )
            )

            results.append({
                "changes": changes,
                "prediction": prediction["failure_type"],
                "probability": prediction["probability"],
                "change_size": size
            })

        # Remove duplicate changes
        unique = {
            tuple(sorted(r["changes"].items())): r
            for r in results
        }

        results = list(unique.values())

        # Smallest intervention first
        results.sort(
            key=lambda x: (
                x["change_size"],
                -x["probability"]
            )
        )

        minimum = results[0] if results else None

        # Strongest predicted outcome
        highest = (
            max(
                results,
                key=lambda x: x["probability"]
            )
            if results else None
        )

        recommendations = []

        if minimum:

            if "Score" in minimum["changes"]:
                recommendations.append(
                    f"Increase score from "
                    f"{original['Score']} toward "
                    f"{minimum['changes']['Score']}"
                )

            if "Severity" in minimum["changes"]:
                recommendations.append(
                    f"Reduce severity from "
                    f"{original['Severity']} toward "
                    f"{minimum['changes']['Severity']}"
                )

        return {
            "original_input": original,

            "original_prediction": {
                "failure_type": original_label,
                "probability":
                    original_result["probability"]
            },

            "counterfactuals": results[:10],

            "minimum_effective_change": minimum,

            "highest_confidence_scenario": highest,

            "recommended_changes": recommendations
        }