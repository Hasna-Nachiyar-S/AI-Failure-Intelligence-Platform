from backend.recommendation.recommender import Recommender


def main():

    print("=" * 60)
    print("RECOMMENDATION ENGINE TEST")
    print("=" * 60)

    recommender = Recommender()

    # --------------------------------------------------
    # Test Student
    # --------------------------------------------------

    student = {
        "Domain": "Student",
        "Severity": 2,
        "Score": 8,
        "Description": "Absences: 5, Study Time: 2"
    }

    print("\nSTUDENT TEST")
    print("-" * 60)

    result = recommender.analyze(
        student
    )

    print(
        "Prediction:",
        result["prediction"]["failure_type"]
    )

    print(
        "Cluster:",
        result["cluster"]["cluster_id"]
    )

    print("\nRecommendations:")

    for recommendation in result[
        "recommendations"
    ]:

        print(
            "-",
            recommendation
        )

    print("\nImprovement Actions:")

    for action in result[
        "improvement_actions"
    ]["actions"]:

        print(
            "-",
            action["action"]
        )

    # --------------------------------------------------
    # Test Jobs
    # --------------------------------------------------

    jobs = {
        "Domain": "Jobs",
        "Severity": 45,
        "Score": 45,
        "Description": "Experience 2 years"
    }

    print("\n\nJOB TEST")
    print("-" * 60)

    result = recommender.analyze(
        jobs
    )

    print(
        "Prediction:",
        result["prediction"]["failure_type"]
    )

    print(
        "Cluster:",
        result["cluster"]["cluster_id"]
    )

    print("\nRecommendations:")

    for recommendation in result[
        "recommendations"
    ]:

        print(
            "-",
            recommendation
        )

    # --------------------------------------------------
    # Test completed
    # --------------------------------------------------

    print("\n")
    print("=" * 60)
    print("RECOMMENDATION TEST COMPLETED")
    print("=" * 60)


if __name__ == "__main__":

    main()