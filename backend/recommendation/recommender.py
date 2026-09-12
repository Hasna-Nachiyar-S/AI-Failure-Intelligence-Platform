import os
import joblib
import pandas as pd


class Recommender:

    def __init__(self):
        base = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..")
        )
        models = os.path.join(base, "models")
        data = os.path.join(base, "data")

        self.classifier = joblib.load(
            os.path.join(models, "best_classifier.pkl")
        )
        print(f"Classifier loaded -> {os.path.join(models, 'best_classifier.pkl')}")

        self.kmeans = joblib.load(
            os.path.join(models, "kmeans.pkl")
        )
        print(f"KMeans loaded -> {os.path.join(models, 'kmeans.pkl')}")

        self.scaler = joblib.load(
            os.path.join(models, "scaler.pkl")
        )
        self.encoders = joblib.load(
            os.path.join(models, "encoders.pkl")
        )

        path = os.path.join(
            data, "clustered_failures.csv"
        )
        self.clustered_data = pd.read_csv(path)
        print(f"Clustered data loaded -> {path}")

        self.features = [
            "Domain", "Severity", "Score", "Description"
        ]

    # ------------------------------------------------------------
    # PREPROCESS
    # ------------------------------------------------------------

    def preprocess_input(self, data):
        df = pd.DataFrame(
            [data],
            columns=self.features
        )

        for col, encoder in self.encoders.items():

            if col == "Failure_Type" or col not in df:
                continue

            try:
                df[col] = encoder.transform(
                    [str(df[col].iloc[0])]
                )
            except ValueError:
                df[col] = encoder.transform(
                    [encoder.classes_[0]]
                )

        df = df[self.features]

        return pd.DataFrame(
            self.scaler.transform(df),
            columns=self.features
        )

    # ------------------------------------------------------------
    # DECODE FAILURE
    # ------------------------------------------------------------

    def decode_failure(self, value):
        encoder = self.encoders.get(
            "Failure_Type"
        )

        if encoder is None:
            return str(value)

        try:
            return str(
                encoder.inverse_transform(
                    [int(value)]
                )[0]
            )
        except Exception:
            return str(value)

    # ------------------------------------------------------------
    # PREDICTION
    # ------------------------------------------------------------

    def predict_failure(self, data):
        X = self.preprocess_input(data)

        value = self.classifier.predict(X)[0]

        return {
            "failure_type":
                self.decode_failure(value)
        }

    def predict_probability(self, data):
        X = self.preprocess_input(data)

        if not hasattr(
            self.classifier,
            "predict_proba"
        ):
            return {}

        probs = self.classifier.predict_proba(X)[0]

        return {
            self.decode_failure(cls): float(prob)
            for cls, prob in zip(
                self.classifier.classes_,
                probs
            )
        }

    # ------------------------------------------------------------
    # CLUSTER
    # ------------------------------------------------------------

    def predict_cluster(self, data):
        X = self.preprocess_input(data)

        cluster_id = int(
            self.kmeans.predict(X)[0]
        )

        return {
            "cluster_id": cluster_id
        }

    def analyze_cluster(self, cluster_id):
        df = self.clustered_data

        df = df[
            df["Cluster"] == cluster_id
        ]

        if df.empty:
            return {
                "cluster_id": cluster_id,
                "total_records": 0,
                "failure_types": {},
                "domains": {}
            }

        failures = {}

        for key, value in (
            df["Failure_Type"]
            .value_counts()
            .to_dict()
            .items()
        ):
            failures[
                self.decode_failure(key)
            ] = int(value)

        domains = {
            str(k): int(v)
            for k, v in (
                df["Domain"]
                .value_counts()
                .to_dict()
                .items()
            )
        }

        return {
            "cluster_id": cluster_id,
            "total_records": len(df),
            "failure_types": failures,
            "domains": domains
        }

    def find_similar_failures(
        self,
        cluster_id,
        limit=5
    ):
        df = self.clustered_data

        df = df[
            df["Cluster"] == cluster_id
        ].head(limit)

        return df.where(
            pd.notnull(df),
            None
        ).to_dict(
            orient="records"
        )

    # ------------------------------------------------------------
    # RECOMMENDATIONS
    # ------------------------------------------------------------

    def generate_recommendations(
        self,
        data,
        failure_type=None
    ):
        from backend.recommendation.rules import (
            RecommendationRules
        )
        from backend.recommendation.templates import (
            RecommendationTemplates
        )

        if failure_type is None:
            failure_type = self.predict_failure(
                data
            )["failure_type"]

        result = []

        try:
            result += RecommendationRules.apply(
                data
            )
        except Exception:
            pass

        try:
            result += (
                RecommendationTemplates
                .get_recommendations(
                    data["Domain"],
                    failure_type
                )
            )
        except Exception:
            pass

        return list(dict.fromkeys(
            str(x).strip()
            for x in result
            if str(x).strip()
        ))

    # ------------------------------------------------------------
    # IMPROVEMENT ACTIONS
    # ------------------------------------------------------------

    def improvement_actions(
        self,
        data,
        failure_type=None
    ):
        domain = str(
            data.get("Domain", "")
        ).lower()

        action_map = {

            "student": [
                "Improve academic score",
                "Reduce previous failures",
                "Increase study time",
                "Reduce avoidable absences"
            ],

            "jobs": [
                "Improve skill-match score",
                "Strengthen resume skills",
                "Add relevant experience"
            ],

            "projects": [
                "Increase project completion percentage",
                "Monitor project progress",
                "Address project delays"
            ],

            "software": [
                "Reduce issue severity",
                "Review similar historical issues",
                "Improve defect prevention practices"
            ]
        }

        actions = action_map.get(
            domain,
            [
                "Review factors associated with failure",
                "Compare with similar historical failures"
            ]
        )

        return {
            "actions": [
                {"action": action}
                for action in actions
            ]
        }

    # ------------------------------------------------------------
    # COMPLETE ANALYSIS
    # ------------------------------------------------------------

    def recommend(self, data):

        prediction = self.predict_failure(
            data
        )

        probability = self.predict_probability(
            data
        )

        cluster = self.predict_cluster(
            data
        )

        cluster_id = cluster[
            "cluster_id"
        ]

        return {
            "input": data,

            "prediction": prediction,

            "probability": probability,

            "cluster": cluster,

            "historical_analysis":
                self.analyze_cluster(
                    cluster_id
                ),

            "similar_failures":
                self.find_similar_failures(
                    cluster_id
                ),

            "recommendations":
                self.generate_recommendations(
                    data,
                    prediction["failure_type"]
                ),

            "improvement_actions":
                self.improvement_actions(
                    data,
                    prediction["failure_type"]
                )
        }

    def analyze(self, data):
        return self.recommend(data)