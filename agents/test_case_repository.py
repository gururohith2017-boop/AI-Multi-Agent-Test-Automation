from agents.requirement_reader import load_requirements


def get_all_test_cases():
    """
    Return all test cases from the requirement repository.
    """

    return load_requirements()


def get_test_case(test_case_id):
    """
    Return one test case using its Test Case ID.
    """

    test_cases = load_requirements()

    for test_case in test_cases:

        if test_case["Test Case ID"] == test_case_id:

            return test_case

    raise ValueError(
        f"Test Case ID not found: {test_case_id}"
    )


if __name__ == "__main__":

    print()
    print("==============================================")
    print("TEST CASE REPOSITORY")
    print("==============================================")
    print()

    test_case = get_test_case("US-001")

    print("Test Case ID:")
    print(test_case["Test Case ID"])

    print()
    print("User Story:")
    print(test_case["User Story"])

    print()
    print("Test Scenario:")
    print(test_case["Test Scenario"])

    print()
    print("Test Input:")
    print(test_case["Test Input"])

    print()
    print("Expected Result:")
    print(test_case["Expected Result"])

    print()
    print("==============================================")
    print("TEST CASE RETRIEVAL SUCCESSFUL")
    print("==============================================")