from backend.utils.data_loader import (
    load_student,
    load_software,
    load_jobs,
    load_projects,
)


def test_student():
    df = load_student()

    assert not df.empty
    print(df.head())
    print("Student dataset loaded successfully.")


def test_software():
    df = load_software()

    assert not df.empty
    print(df.head())
    print("Software dataset loaded successfully.")


def test_jobs():
    df = load_jobs()

    assert not df.empty
    print(df.head())
    print("Jobs dataset loaded successfully.")


def test_projects():
    df = load_projects()

    assert not df.empty
    print(df.head())
    print("Projects dataset loaded successfully.")


if __name__ == "__main__":
    test_student()
    test_software()
    test_jobs()
    test_projects()

    print("\nAll datasets loaded successfully.")