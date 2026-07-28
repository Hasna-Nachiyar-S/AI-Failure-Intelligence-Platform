from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)


class Evaluator:

    def evaluate(self, model, X_test, y_test):

        predictions = model.predict(X_test)

        accuracy = accuracy_score(y_test, predictions)

        precision = precision_score(
            y_test,
            predictions,
            average="weighted",
            zero_division=0
        )

        recall = recall_score(
            y_test,
            predictions,
            average="weighted",
            zero_division=0
        )

        f1 = f1_score(
            y_test,
            predictions,
            average="weighted",
            zero_division=0
        )

        print("\n" + "=" * 60)
        print(type(model).__name__)
        print("=" * 60)

        print(f"Accuracy : {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall   : {recall:.4f}")
        print(f"F1 Score : {f1:.4f}")

        print("\nClassification Report")
        print(classification_report(
            y_test,
            predictions,
            zero_division=0
        ))

        print("\nConfusion Matrix")
        print(confusion_matrix(
            y_test,
            predictions
        ))

        return {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1": f1
        }

    # ----------------------------------------
    # Compare all trained models
    # ----------------------------------------

    def compare_models(self, results):

        print("\n")
        print("=" * 60)
        print("MODEL COMPARISON")
        print("=" * 60)

        best_name = None
        best_score = -1

        for name, metrics in results.items():

            score = metrics["accuracy"]

            print(
                f"{name:<25}"
                f"Accuracy={score:.4f}   "
                f"F1={metrics['f1']:.4f}"
            )

            if score > best_score:
                best_score = score
                best_name = name

        print("\nBest Model :", best_name)
        print("Best Accuracy :", round(best_score, 4))

        return best_name