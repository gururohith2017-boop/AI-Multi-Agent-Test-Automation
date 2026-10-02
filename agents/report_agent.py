from pathlib import Path
from openpyxl import Workbook
from datetime import datetime


PROJECT_ROOT = Path(__file__).resolve().parent.parent

REPORT_FILE = (
    PROJECT_ROOT
    / "reports"
    / "test_execution_report.xlsx"
)


def write_execution_report(results):

    REPORT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------
    # CREATE A FRESH REPORT FOR THIS EXECUTION
    # --------------------------------------------------

    workbook = Workbook()

    worksheet = workbook.active

    worksheet.title = "Test Results"

    headers = [
        "Test Case ID",
        "User Story",
        "Test Scenario",
        "Test Input",
        "Expected Result",
        "Actual Result",
        "Agent",
        "Status",
        "Execution Duration",
        "Execution Date/Time",
        "Screenshot",
        "Error Details",
    ]

    worksheet.append(headers)

    execution_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # --------------------------------------------------
    # WRITE CURRENT EXECUTION RESULTS
    # --------------------------------------------------

    for result in results:

        worksheet.append([
            result.get(
                "test_case_id",
                ""
            ),

            result.get(
                "user_story",
                ""
            ),

            result.get(
                "test_scenario",
                ""
            ),

            result.get(
                "test_input",
                ""
            ),

            result.get(
                "expected_result",
                ""
            ),

            result.get(
                "actual_result",
                ""
            ),

            result.get(
                "agent",
                "Playwright Agent"
            ),

            result.get(
                "status",
                ""
            ),

            result.get(
                "execution_duration",
                ""
            ),

            execution_time,

            result.get(
                "screenshot",
                ""
            ),

            result.get(
                "error_details",
                ""
            ),
        ])

    # --------------------------------------------------
    # FORMAT COLUMNS
    # --------------------------------------------------

    for column in worksheet.columns:

        max_length = 0

        column_letter = column[0].column_letter

        for cell in column:

            if cell.value is not None:

                cell_length = len(
                    str(cell.value)
                )

                if cell_length > max_length:

                    max_length = cell_length

        worksheet.column_dimensions[
            column_letter
        ].width = min(
            max_length + 2,
            60
        )

    # --------------------------------------------------
    # FREEZE HEADER
    # --------------------------------------------------

    worksheet.freeze_panes = "A2"

    # --------------------------------------------------
    # SAVE REPORT
    # --------------------------------------------------

    workbook.save(
        REPORT_FILE
    )

    workbook.close()

    print()
    print("==============================================")
    print("EXCEL REPORT")
    print("==============================================")
    print()

    print(
        "Fresh execution report created successfully:"
    )

    print(
        REPORT_FILE
    )

    print()

    return REPORT_FILE


if __name__ == "__main__":

    print()
    print("==============================================")
    print("REPORT AGENT")
    print("==============================================")
    print()

    print(
        "Report Agent is ready."
    )

    print(
        "A fresh Excel report will be created "
        "for every automation execution."
    )

    print()