from openpyxl import Workbook
from pathlib import Path


OUTPUT_FILE = Path("user_stories") / "customer_support_user_stories.xlsx"


TEST_CASES = [
    {
        "Test Case ID": "US-001",
        "User Story": "As an employee, I want VPN support so that I can connect to the company network.",
        "Test Scenario": "VPN / Internal IT",
        "Test Input": "My laptop VPN is not working. I am unable to connect to the company network.",
        "Expected Result": "Request routed to: Internal IT",
    },
    {
        "Test Case ID": "US-002",
        "User Story": "As an employee, I want HR support for leave-related queries.",
        "Test Scenario": "Leave / HR",
        "Test Input": "I need to apply for leave. Can you tell me how to submit my leave request?",
        "Expected Result": "Request routed to: HR",
    },
    {
        "Test Case ID": "US-003",
        "User Story": "As an employee, I want payroll support for salary-related issues.",
        "Test Scenario": "Salary / Payroll",
        "Test Input": "My monthly salary has not been credited yet. Can you help me with my salary payment issue?",
        "Expected Result": "Request routed to: Payroll",
    },
    {
        "Test Case ID": "US-004",
        "User Story": "As an employee, I want administrative support for office-related requests.",
        "Test Scenario": "Office Supplies / Admin",
        "Test Input": "I need help with an office administration request. Can you help me with the process for requesting office supplies?",
        "Expected Result": "Request routed to: Admin",
    },
    {
        "Test Case ID": "US-005",
        "User Story": "As an employee, I want help desk support for service requests.",
        "Test Scenario": "Service Request / Help Desk",
        "Test Input": "I am having an issue with a service request. Can you help me check the status and provide support?",
        "Expected Result": "Request routed to: Help Desk",
    },
    {
        "Test Case ID": "US-006",
        "User Story": "As an employee, I want compliance support for company compliance questions.",
        "Test Scenario": "Compliance",
        "Test Input": "I have a question about company compliance requirements. Can you help me understand the compliance process?",
        "Expected Result": "Request routed to: Compliance",
    },
    {
        "Test Case ID": "US-007",
        "User Story": "As an employee, I want the system to automatically route general support requests.",
        "Test Scenario": "General Support / Auto Router",
        "Test Input": "I need help with a general corporate support request. Please guide me to the appropriate support team.",
        "Expected Result": "Request routed to the appropriate support agent.",
    },
    {
        "Test Case ID": "US-008",
        "User Story": "As a user, I should not be able to submit an empty support request.",
        "Test Scenario": "Empty Input Validation",
        "Test Input": "Empty input",
        "Expected Result": "Send button remains disabled and no routing response is generated.",
    },
    {
        "Test Case ID": "US-009",
        "User Story": "As an employee, I want ambiguous requests to be routed to an appropriate support agent.",
        "Test Scenario": "Ambiguous Query",
        "Test Input": "I need some help with something related to my work. Can you guide me to the right support team?",
        "Expected Result": "Request routed to an appropriate support agent.",
    },
    {
        "Test Case ID": "US-010",
        "User Story": "As an employee, I want to directly select HR support when required.",
        "Test Scenario": "Direct HR Agent Selection",
        "Test Input": "I have a question about the employee leave policy. Can you help me understand the process?",
        "Expected Result": "HR Agent is selected and processes the request.",
    },
]


def create_requirement_file():

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    workbook = Workbook()

    worksheet = workbook.active
    worksheet.title = "Requirements"

    headers = [
        "Test Case ID",
        "User Story",
        "Test Scenario",
        "Test Input",
        "Expected Result",
    ]

    worksheet.append(headers)

    for test_case in TEST_CASES:

        worksheet.append([
            test_case["Test Case ID"],
            test_case["User Story"],
            test_case["Test Scenario"],
            test_case["Test Input"],
            test_case["Expected Result"],
        ])

    # Improve column widths
    worksheet.column_dimensions["A"].width = 18
    worksheet.column_dimensions["B"].width = 65
    worksheet.column_dimensions["C"].width = 35
    worksheet.column_dimensions["D"].width = 75
    worksheet.column_dimensions["E"].width = 60

    # Freeze header
    worksheet.freeze_panes = "A2"

    # Add filter
    worksheet.auto_filter.ref = worksheet.dimensions

    workbook.save(OUTPUT_FILE)

    print()
    print("==============================================")
    print("Requirement file created successfully")
    print("==============================================")
    print()
    print(f"File: {OUTPUT_FILE}")
    print(f"Total Test Cases: {len(TEST_CASES)}")
    print()


if __name__ == "__main__":
    create_requirement_file()