from pathlib import Path
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier


class Classifier:

    def __init__(self):

        self.models_dir = Path(__file__).resolve().parents[2] / "models"
        self.models_dir.mkdir(exist_ok=True)

    # ----------------------------------------------------
    # Split dataset
    # ----------------------------------------------------

    def split_data(self, df):

        if "Failure_Type" not in df.columns:
            raise ValueError("Failure_Type column not found.")

        X = df.drop(columns=["Failure_Type"])
        y = df["Failure_Type"]

        return train_test_split(
            X,
            y,
            test_size=0.20,
            random_state=42,
            stratify=y
        )

    # ----------------------------------------------------
    # Logistic Regression
    # ----------------------------------------------------

    def train_logistic(self, X_train, y_train):

        model = LogisticRegression(
            max_iter=1000,
            random_state=42
        )

        model.fit(X_train, y_train)

        return model

    # ----------------------------------------------------
    # Decision Tree
    # ----------------------------------------------------

    def train_decision_tree(self, X_train, y_train):

        model = DecisionTreeClassifier(
            random_state=42
        )

        model.fit(X_train, y_train)

        return model

    # ----------------------------------------------------
    # Random Forest
    # ----------------------------------------------------

    def train_random_forest(self, X_train, y_train):

        model = RandomForestClassifier(
            n_estimators=200,
            random_state=42,
            n_jobs=-1
        )

        model.fit(X_train, y_train)

        return model

    # ----------------------------------------------------
    # Predict
    # ----------------------------------------------------

    def predict(self, model, X):

        return model.predict(X)

    # ----------------------------------------------------
    # Save model
    # ----------------------------------------------------

    def save_model(self, model, filename):

        path = self.models_dir / filename

        joblib.dump(model, path)

        print(f"Model saved -> {path}")

    # ----------------------------------------------------
    # Load model
    # ----------------------------------------------------

    def load_model(self, filename):

        path = self.models_dir / filename

        return joblib.load(path)