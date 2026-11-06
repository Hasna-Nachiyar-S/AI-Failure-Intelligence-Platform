from pathlib import Path
import joblib

from backend.utils.data_loader import load_all
from backend.services import Standardizer, Preprocessor

from backend.ml.classifier import Classifier
from backend.ml.evaluator import Evaluator
from backend.ml.clustering import Clustering


class Trainer:

    def __init__(self):

        self.classifier = Classifier()
        self.evaluator = Evaluator()
        self.clustering = Clustering()

        self.project_root = Path(__file__).resolve().parents[2]

        self.models_dir = self.project_root / "models"
        self.models_dir.mkdir(exist_ok=True)

        self.data_dir = self.project_root / "data"
        self.data_dir.mkdir(exist_ok=True)

    # -------------------------------------------------
    # Load + Standardize + Merge + Preprocess
    # -------------------------------------------------

    def prepare_data(self):

        print("=" * 60)
        print("Loading datasets...")
        print("=" * 60)

        datasets = load_all()

        student = Standardizer.student(datasets["student"])
        software = Standardizer.software(datasets["software"])
        jobs = Standardizer.jobs(datasets["jobs"])
        projects = Standardizer.projects(datasets["projects"])

        merged = Standardizer.merge(
            student,
            software,
            jobs,
            projects
        )

        print("Merged Shape :", merged.shape)

        processor = Preprocessor()

        processed = processor.preprocess(merged)

        print("Processed Shape :", processed.shape)

        return processed, processor

    # -------------------------------------------------
    # Train all classification models
    # -------------------------------------------------

    def train_classifiers(self, processed):

        X_train, X_test, y_train, y_test = \
            self.classifier.split_data(processed)

        models = {

            "Logistic Regression":
                self.classifier.train_logistic(
                    X_train,
                    y_train
                ),

            "Decision Tree":
                self.classifier.train_decision_tree(
                    X_train,
                    y_train
                ),

            "Random Forest":
                self.classifier.train_random_forest(
                    X_train,
                    y_train
                )
        }

        results = {}

        print("\n")
        print("=" * 60)
        print("MODEL EVALUATION")
        print("=" * 60)

        for name, model in models.items():

            print(f"\n{name}")

            metrics = self.evaluator.evaluate(
                model,
                X_test,
                y_test
            )

            results[name] = metrics

        best_name = self.evaluator.compare_models(results)

        best_model = models[best_name]

        print("\nBest Model :", best_name)

        return best_model

    # -------------------------------------------------
    # Save classifier, scaler and encoders
    # -------------------------------------------------

    def save_classifier(self, model, processor):

        print("\nSaving classifier...")

        joblib.dump(
            model,
            self.models_dir / "best_classifier.pkl"
        )

        joblib.dump(
            processor.scaler,
            self.models_dir / "scaler.pkl"
        )

        joblib.dump(
            processor.encoders,
            self.models_dir / "encoders.pkl"
        )

        print("Classifier Saved")

    # -------------------------------------------------
    # Train clustering
    # -------------------------------------------------

    def train_clusters(self, processed):

        print("\n")
        print("=" * 60)
        print("CLUSTERING")
        print("=" * 60)

        X = processed.drop(columns=["Failure_Type"])

        best_k = self.clustering.find_best_k(X)

        kmeans = self.clustering.train(
            X,
            best_k
        )

        clustered = self.clustering.add_clusters(
            processed,
            kmeans
        )

        self.clustering.save_model(kmeans)

        clustered.to_csv(
            self.data_dir / "clustered_failures.csv",
            index=False
        )

        print("Clustered dataset saved.")

    # -------------------------------------------------
    # Run everything
    # -------------------------------------------------

    def run(self):

        processed, processor = self.prepare_data()

        best_model = self.train_classifiers(
            processed
        )

        self.save_classifier(
            best_model,
            processor
        )

        self.train_clusters(
            processed
        )

        print("\n")
        print("=" * 60)
        print("STEP 7 COMPLETED SUCCESSFULLY")
        print("=" * 60)


if __name__ == "__main__":

    trainer = Trainer()

    trainer.run()