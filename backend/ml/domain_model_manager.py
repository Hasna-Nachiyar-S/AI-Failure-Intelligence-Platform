import os
import joblib
import pandas as pd


BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)


class DomainModelManager:

    def __init__(self, model_dir=None):
        # Production models are the controlled experiment artifacts selected
        # during model comparison. Keep legacy root-level artifacts available
        # but do not silently use them for production inference.
        production_dir = os.path.join(
            BASE_DIR,
            "backend",
            "ml",
            "models"
        )

        # Existing callers historically passed model_dir="models". Treat
        # that legacy default as the production model directory so the API,
        # counterfactual and What-If components all use the same artifacts.
        if model_dir is None or model_dir == "models":
            model_dir = production_dir
        elif not os.path.isabs(model_dir):
            model_dir = os.path.join(BASE_DIR, model_dir)

        self.model_dir = model_dir
        self.models = {}
        self._load_models()

    def _load_models(self):

        files = {
            "Student": "student_optimized_rf.pkl",
            "Software": "software_original_rf.pkl",
            "Jobs": "jobs_optimized_rf.pkl",
            "Projects": "projects_optimized_rf.pkl"
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

        # API/frontend field names are standardized independently from
        # dataset column spelling. Support both current and legacy aliases.
        aliases = {
            "Project Type": "Project_Type",
            "Project_Type": "Project_Type",
            "Project Cost": "Project_Cost",
            "Project_Cost": "Project_Cost",
            "Project Benefit": "Project_Benefit",
            "Project_Benefit": "Project_Benefit",
            "Completion%": "Completion",
            "Completion": "Completion"
        }

        row = {}

        for feature in features:
            key = aliases.get(feature, feature)
            value = data.get(key)

            # Also accept the raw feature name if an alias was not present.
            if value is None and key != feature:
                value = data.get(feature)

            row[feature] = value

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