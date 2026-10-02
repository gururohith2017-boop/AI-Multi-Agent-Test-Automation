import subprocess
import re
from pathlib import Path

from agents.test_case_repository import get_all_test_cases

PROJECT_ROOT = Path(__file__).resolve().parent.parent

PYTHON_EXE = (
    PROJECT_ROOT
    / "venv"
    / "Scripts"
    / "python.exe"
)

PLAYWRIGHT_TEST_FOLDER = (
    PROJECT_ROOT / "playwright_tests"
)

SCREENSHOTS = {
    "US-001": "reports/vpn_support.png",
    "US-002": "reports/hr_support.png",
    "US-003": "reports/payroll_support.png",
    "US-004": "reports/admin_support.png",
    "US-005": "reports/helpdesk_support.png",
    "US-006": "reports/compliance_support.png",
    "US-007": "reports/auto_router.png",
    "US-008": "reports/empty_input.png",
    "US-009": "reports/ambiguous_query.png",
    "US-010": "reports/direct_hr_agent.png",
}

TEST_FILES = {
    "US-001": "test_vpn_support.py",
    "US-002": "test_hr_support.py",
    "US-003": "test_payroll_support.py",
    "US-004": "test_admin_support.py",
    "US-005": "test_helpdesk_support.py",
    "US-006": "test_compliance_support.py",
    "US-007": "test_auto_router.py",
    "US-008": "test_empty_input.py",
    "US-009": "test_ambiguous_query.py",
    "US-010": "test_direct_hr_agent.py",
}


def extract_execution_duration(output):
    pattern = r"in\s+([\d.]+)s"
    matches = re.findall(pattern, output)

    if matches:
        duration = float(matches[-1])
        return f"{duration:.2f} sec"

    return ""


def extract_actual_result(output):
    pattern = r"ACTUAL_RESULT:\s*(.+)"
    matches = re.findall(pattern, output)

    if matches:
        return matches[-1].strip()

    return (
        "Actual result was not reported "
        "by the Playwright test"
    )


def run_playwright_test(
    test_case_id,
    requirement=None
):

    if test_case_id not in TEST_FILES:
        return {
            "test_case_id": test_case_id,
            "user_story": "",
            "test_scenario": "",
            "test_input": "",
            "expected_result": "",
            "actual_result": "",
            "agent": "Playwright Agent",
            "status": "FAIL",
            "execution_duration": "",
            "screenshot": "",
            "error_details":
                f"No Playwright test mapped for {test_case_id}",
        }

    test_file = (
        PLAYWRIGHT_TEST_FOLDER
        / TEST_FILES[test_case_id]
    )

    if not test_file.exists():
        return {
            "test_case_id": test_case_id,
            "user_story": "",
            "test_scenario": "",
            "test_input": "",
            "expected_result": "",
            "actual_result": "",
            "agent": "Playwright Agent",
            "status": "FAIL",
            "execution_duration": "",
            "screenshot": "",
            "error_details":
                f"Test file not found: {test_file}",
        }

    print()
    print("==============================================")
    print(
        f"PLAYWRIGHT EXECUTION: {test_case_id}"
    )
    print("==============================================")
    print()

    print(f"Test File: {test_file}")
    print()

    result = subprocess.run(
        [
            str(PYTHON_EXE),
            "-m",
            "pytest",
            str(test_file),
            "-v",
            "-s",
        ],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )

    output = result.stdout
    error_output = result.stderr

    print(output)

    if error_output:
        print(error_output)

    if result.returncode == 0:
        status = "PASS"
    else:
        status = "FAIL"

    execution_duration = (
        extract_execution_duration(output)
    )

    actual_result = (
        extract_actual_result(output)
    )

    if status == "FAIL":

        if error_output.strip():
            error_details = error_output.strip()
        else:
            error_details = output.strip()

    else:
        error_details = ""

    screenshot = SCREENSHOTS.get(
        test_case_id,
        ""
    )

    return {
        "test_case_id": test_case_id,
        "user_story":
            requirement["User Story"]
            if requirement else "",
        "test_scenario":
            requirement["Test Scenario"]
            if requirement else "",
        "test_input":
            requirement["Test Input"]
            if requirement else "",
        "expected_result":
            requirement["Expected Result"]
            if requirement else "",
        "actual_result": actual_result,
        "agent": "Playwright Agent",
        "status": status,
        "execution_duration":
            execution_duration,
        "screenshot": screenshot,
        "error_details": error_details,
    }


def run_all_playwright_tests():

    print()
    print("==============================================")
    print("PLAYWRIGHT AGENT")
    print("==============================================")
    print()

    requirements = get_all_test_cases()

    print(
        "Total test cases loaded from Excel: "
        f"{len(requirements)}"
    )

    print()

    results = []

    for requirement in requirements:

        test_case_id = (
            requirement["Test Case ID"]
        )

        print(
            f"Executing {test_case_id}..."
        )

        result = run_playwright_test(
            test_case_id,
            requirement
        )

        results.append(result)

    print()
    print("==============================================")
    print("PLAYWRIGHT EXECUTION SUMMARY")
    print("==============================================")
    print()

    passed = sum(
        1
        for result in results
        if result["status"] == "PASS"
    )

    failed = sum(
        1
        for result in results
        if result["status"] == "FAIL"
    )

    print(
        f"Total : {len(results)}"
    )

    print(
        f"Passed: {passed}"
    )

    print(
        f"Failed: {failed}"
    )

    print()

    for result in results:

        print(
            f"{result['test_case_id']} "
            f"-> "
            f"{result['status']} "
            f"| Duration: "
            f"{result['execution_duration']} "
            f"| Actual: "
            f"{result['actual_result']}"
        )

    print()

    return results


if __name__ == "__main__":

    results = run_all_playwright_tests()

    print(
        "Playwright Agent execution completed."
    )