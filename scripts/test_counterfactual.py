from backend.counterfactual.generator import (
    CounterfactualGenerator
)


def main():

    print("=" * 60)
    print("COUNTERFACTUAL FAILURE PREVENTION TEST")
    print("=" * 60)

    # ---------------------------------------------------------
    # Create generator
    # ---------------------------------------------------------

    generator = CounterfactualGenerator(
        model_dir="models"
    )

    # ---------------------------------------------------------
    # Test input
    # ---------------------------------------------------------

    test_input = {
        "Domain": "Student",
        "Severity": 4,
        "Score": 8,
        "Description": "Absences + Study Time"
    }

    print("\nOriginal input:")
    print(test_input)

    # ---------------------------------------------------------
    # Original prediction
    # ---------------------------------------------------------

    original_prediction = generator.predict(
        test_input
    )

    print("\nOriginal prediction:")
    print(original_prediction)

    # ---------------------------------------------------------
    # Generate counterfactuals
    # ---------------------------------------------------------

    result = generator.generate(
        test_input,
        desired_prediction="Passed"
    )

    # ---------------------------------------------------------
    # Counterfactual scenarios
    # ---------------------------------------------------------

    print("\nCounterfactuals:")

    counterfactuals = result[
        "counterfactuals"
    ]

    if not counterfactuals:

        print("No successful counterfactual found.")

    else:

        for index, scenario in enumerate(
            counterfactuals,
            start=1
        ):

            print(f"\nScenario {index}")

            print(
                "Changes:",
                scenario["changes"]
            )

            print(
                "Prediction:",
                scenario["prediction"]
            )

            print(
                "Probability:",
                scenario["probability"]
            )

    # ---------------------------------------------------------
    # Minimum effective change
    # ---------------------------------------------------------

    print("\n" + "-" * 60)
    print("MINIMUM EFFECTIVE CHANGE")
    print("-" * 60)

    minimum_change = result[
        "minimum_effective_change"
    ]

    if minimum_change:

        print(
            "Changes:",
            minimum_change["changes"]
        )

        print(
            "Prediction:",
            minimum_change["prediction"]
        )

        print(
            "Probability:",
            minimum_change["probability"]
        )

        print(
            "Change size:",
            minimum_change["change_size"]
        )

    else:

        print(
            "No minimum effective change found."
        )

    # ---------------------------------------------------------
    # Highest confidence scenario
    # ---------------------------------------------------------

    print("\n" + "-" * 60)
    print("HIGHEST-CONFIDENCE SCENARIO")
    print("-" * 60)

    highest_confidence = result[
        "highest_confidence_scenario"
    ]

    if highest_confidence:

        print(
            "Changes:",
            highest_confidence["changes"]
        )

        print(
            "Prediction:",
            highest_confidence["prediction"]
        )

        print(
            "Probability:",
            highest_confidence["probability"]
        )

        print(
            "Change size:",
            highest_confidence["change_size"]
        )

    else:

        print(
            "No high-confidence scenario found."
        )

    # ---------------------------------------------------------
    # Recommended changes
    # ---------------------------------------------------------

    print("\n" + "-" * 60)
    print("RECOMMENDED CHANGES")
    print("-" * 60)

    recommendations = result[
        "recommended_changes"
    ]

    if recommendations:

        for recommendation in recommendations:

            print(
                f"- {recommendation}"
            )

    else:

        print(
            "No recommended changes found."
        )

    print("\n" + "=" * 60)
    print("COUNTERFACTUAL TEST COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()