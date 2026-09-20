import joblib

from backend.ml.counterfactual_engine import CounterfactualEngine


MODEL_PATH = "backend/ml/models/student_optimized_rf.pkl"


# ---------------------------------------------------------
# LOAD SAVED MODEL BUNDLE
# ---------------------------------------------------------

model_bundle = joblib.load(MODEL_PATH)

model = model_bundle["model"]


# ---------------------------------------------------------
# DISPLAY MODEL INFORMATION
# ---------------------------------------------------------

print("=" * 70)
print("COUNTERFACTUAL ENGINE TEST")
print("=" * 70)

print(f"Domain: {model_bundle.get('domain')}")
print(f"Experiment: {model_bundle.get('experiment')}")
print(f"Model: {type(model).__name__}")

print()


# ---------------------------------------------------------
# STUDENT TEST CASE
# ---------------------------------------------------------

student_case = {
    "absences": 30,
    "studytime": 1,
    "failures": 3,
    "G1": 7,
    "G2": 6,
}


print("Original Student Case")
print("-" * 70)

for feature, value in student_case.items():
    print(f"{feature}: {value}")

print()


# ---------------------------------------------------------
# CREATE ENGINE
# ---------------------------------------------------------

engine = CounterfactualEngine(
    model=model,
    domain="Student",
)


# ---------------------------------------------------------
# GENERATE COUNTERFACTUALS
# ---------------------------------------------------------

result = engine.generate(student_case)


# ---------------------------------------------------------
# ORIGINAL PREDICTION
# ---------------------------------------------------------

print("Original Prediction")
print("-" * 70)

print(
    f"Prediction: {result.original_prediction}"
)

print(
    f"Original failure risk: "
    f"{result.original_failure_risk:.4f}"
)

print()


# ---------------------------------------------------------
# BEST INTERVENTION
# ---------------------------------------------------------

print("Best Intervention")
print("-" * 70)

if result.best_intervention is None:

    print("No intervention was generated.")

else:

    best = result.best_intervention

    print(
        f"Feature: {best['feature']}"
    )

    print(
        f"Old value: {best['old_value']}"
    )

    print(
        f"New value: {best['new_value']}"
    )

    print(
        f"Prediction before: "
        f"{best['prediction_before']}"
    )

    print(
        f"Prediction after: "
        f"{best['prediction_after']}"
    )

    print(
        f"Risk before: "
        f"{best['risk_before']:.4f}"
    )

    print(
        f"Risk after: "
        f"{best['risk_after']:.4f}"
    )

    print(
        f"Predicted risk reduction: "
        f"{best['risk_reduction']:.4f}"
    )

print()


# ---------------------------------------------------------
# ALL INTERVENTIONS
# ---------------------------------------------------------

print("All Tested Interventions")
print("-" * 70)

if not result.recommended_interventions:

    print("No interventions were generated.")

else:

    for index, intervention in enumerate(
        result.recommended_interventions,
        start=1,
    ):

        print(
            f"{index}. "
            f"{intervention['feature']}: "
            f"{intervention['old_value']} -> "
            f"{intervention['new_value']} | "
            f"Prediction: "
            f"{intervention['prediction_after']} | "
            f"Risk reduction: "
            f"{intervention['risk_reduction']:.4f}"
        )


print()
print("=" * 70)
print("TEST COMPLETED")
print("=" * 70)