from agents.test_case_repository import get_test_case


def prepare_test_data(test_case_id):

    test_case = get_test_case(
        test_case_id
    )

    return {
        "test_case_id": test_case["Test Case ID"],
        "scenario": test_case["Test Scenario"],
        "test_input": test_case["Test Input"],
        "expected_result": test_case["Expected Result"],
    }


if __name__ == "__main__":

    test_data = prepare_test_data(
        "US-001"
    )

    print()
    print("==============================================")
    print("TEST DATA EXECUTOR")
    print("==============================================")
    print()

    print(
        "Test Case ID:",
        test_data["test_case_id"]
    )

    print(
        "Scenario:",
        test_data["scenario"]
    )

    print(
        "Test Input:",
        test_data["test_input"]
    )

    print(
        "Expected Result:",
        test_data["expected_result"]
    )

    print()
    print("==============================================")
    print("TEST DATA PREPARATION SUCCESSFUL")
    print("==============================================")