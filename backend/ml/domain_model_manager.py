import os
import joblib
import pandas as pd


class DomainModelManager:

    def __init__(self, model_dir="models"):
        self.model_dir = model_dir
        self.models = {}
        self._load_models()

    def _load_models(self):

        files = {
            "Student": "student_model.pkl",
            "Software": "software_model.pkl",
            "Jobs": "jobs_model.pkl",
            "Projects": "projects_model.pkl"
        }

        for domain, filename in files.items():

            path = os.path.join(
                self.model_dir,
                filename
            )

            if not os.path.exists(path):
                raise FileNotFoundError(
                    f"Model not found: {path}"
                )

            self.models[domain] = joblib.load(path)

    def normalize_domain(self, domain):

        if not domain:
            raise ValueError(
                "Domain is required."
            )

        value = str(domain).strip().lower()

        mapping = {
            "student": "Student",
            "software": "Software",
            "jobs": "Jobs",
            "projects": "Projects"
        }

        if value not in mapping:
            raise ValueError(
                "Invalid domain."
            )

        return mapping[value]

    def get_model(self, domain):

        domain = self.normalize_domain(domain)

        return self.models[domain]

    def get_features(self, domain):

        model_data = self.get_model(domain)

        return model_data["features"]

    def prepare_input(self, domain, data):

        domain = self.normalize_domain(domain)

        features = self.get_features(domain)

        aliases = {
            "Project Type": "Project_Type",
            " Project Cost ": "Project_Cost",
            " Project Benefit ": "Project_Benefit",
            "Completion%": "Completion"
        }

        row = {}

        for feature in features:

            key = aliases.get(
                feature,
                feature
            )

            row[feature] = data.get(key)

        return pd.DataFrame(
            [row],
            columns=features
        )

    def predict(self, domain, data):

        domain = self.normalize_domain(domain)

        model_data = self.get_model(domain)

        model = model_data["model"]

        X = self.prepare_input(
            domain,
            data
        )

        prediction = model.predict(X)[0]

        probabilities = {}

        if hasattr(model, "predict_proba"):

            probs = model.predict_proba(X)[0]

            classes = model.classes_

            probabilities = {
                str(cls): float(prob)
                for cls, prob in zip(
                    classes,
                    probs
                )
            }

        probability = probabilities.get(
            str(prediction),
            0.0
        )

        return {
            "domain": domain,
            "failure_type": str(prediction),
            "probability": probability,
            "class_probabilities":
                probabilities
        }