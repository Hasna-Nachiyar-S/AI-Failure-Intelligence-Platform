from pathlib import Path
import joblib

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


class Clustering:

    def __init__(self):

        self.models_dir = Path(__file__).resolve().parents[2] / "models"
        self.models_dir.mkdir(exist_ok=True)

    # ---------------------------------------------------
    # Find the best K using Silhouette Score
    # ---------------------------------------------------

    def find_best_k(self, X):

        print("\nFinding best number of clusters...\n")

        best_k = 2
        best_score = -1

        for k in range(2, 11):

            model = KMeans(
                n_clusters=k,
                random_state=42,
                n_init=10
            )

            labels = model.fit_predict(X)

            score = silhouette_score(X, labels)

            print(f"K = {k:<2}  Silhouette Score = {score:.4f}")

            if score > best_score:
                best_score = score
                best_k = k

        print("\n--------------------------------")
        print(f"Best K = {best_k}")
        print(f"Best Score = {best_score:.4f}")
        print("--------------------------------")

        return best_k

    # ---------------------------------------------------
    # Train KMeans
    # ---------------------------------------------------

    def train(self, X, k):

        print(f"\nTraining KMeans (K={k})...")

        model = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10
        )

        model.fit(X)

        print("Training Complete.")

        return model

    # ---------------------------------------------------
    # Predict Cluster
    # ---------------------------------------------------

    def predict(self, model, X):

        return model.predict(X)

    # ---------------------------------------------------
    # Add cluster column to dataframe
    # ---------------------------------------------------

    def add_clusters(self, df, model):

        df = df.copy()

        X = df.drop(columns=["Failure_Type"])

        df["Cluster"] = model.predict(X)

        return df

    # ---------------------------------------------------
    # Save Model
    # ---------------------------------------------------

    def save_model(self, model, filename="kmeans.pkl"):

        path = self.models_dir / filename

        joblib.dump(model, path)

        print(f"KMeans saved -> {path}")

    # ---------------------------------------------------
    # Load Model
    # ---------------------------------------------------

    def load_model(self, filename="kmeans.pkl"):

        path = self.models_dir / filename

        return joblib.load(path)