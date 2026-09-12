from backend.what_if.simulator import WhatIfSimulator


def main():

    print("=" * 60)
    print("WHAT-IF SIMULATOR TEST")
    print("=" * 60)

    simulator = WhatIfSimulator()

    original = {
        "Domain": "Student",
        "Severity": 4,
        "Score": 8,
        "Description": "Absences + Study Time"
    }

    print("\nOriginal input:")
    print(original)

    # ---------------------------------------------------------
    # What-if scenario
    # ---------------------------------------------------------

    changes = {
        "Score": 9
    }

    result = simulator.simulate(
        original,
        changes
    )

    print("\nWhat-if changes:")
    print(result["changes"])

    print("\nOriginal prediction:")
    print(result["original_prediction"])

    print("\nNew prediction:")
    print(result["new_prediction"])

    print("\nProbability change:")
    print(result["probability_change"])

    print("\nPrediction changed:")
    print(result["prediction_changed"])

    print("\n" + "=" * 60)
    print("WHAT-IF TEST COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()