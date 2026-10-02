from pathlib import Path
import sys

from playwright.sync_api import sync_playwright


PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)

from agents.test_case_repository import get_test_case
from reports.excel_reporter import update_test_result


APP_URL = (
    "https://customer-support.srv1981708.hstgr.cloud/"
)


def test_vpn_support_request():

    # --------------------------------------------------
    # LOAD TEST DATA FROM EXCEL REPOSITORY
    # --------------------------------------------------

    test_case = get_test_case(
        "US-001"
    )

    test_case_id = (
        test_case["Test Case ID"]
    )

    user_story = (
        test_case["User Story"]
    )

    test_scenario = (
        test_case["Test Scenario"]
    )

    test_input = (
        test_case["Test Input"]
    )

    expected_result = (
        test_case["Expected Result"]
    )

    screenshot = (
        "reports/vpn_support.png"
    )

    # --------------------------------------------------
    # PLAYWRIGHT EXECUTION
    # --------------------------------------------------

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page()

        try:

            page.goto(
                APP_URL,
                wait_until="domcontentloaded",
                timeout=60000
            )

            # --------------------------------------------------
            # ENTER USER QUERY
            # --------------------------------------------------

            chat_input = page.locator(
                "textarea[placeholder='Type your question here...']"
            )

            chat_input.wait_for(
                state="visible",
                timeout=60000
            )

            chat_input.fill(
                test_input
            )

            # --------------------------------------------------
            # SEND QUERY
            # --------------------------------------------------

            send_button = page.get_by_role(
                "button",
                name="Send message"
            )

            send_button.click()

            # --------------------------------------------------
            # WAIT FOR EXPECTED ROUTING RESPONSE
            # --------------------------------------------------

            routing_response = page.get_by_text(
                expected_result,
                exact=True
            )

            routing_response.wait_for(
                state="visible",
                timeout=60000
            )

            # --------------------------------------------------
            # CAPTURE ACTUAL RESULT
            # --------------------------------------------------

            actual_result = (
                routing_response.inner_text()
            )

            # --------------------------------------------------
            # VALIDATE RESULT
            # --------------------------------------------------

            assert actual_result == (
                expected_result
            )

            # --------------------------------------------------
            # SCREENSHOT
            # --------------------------------------------------

            page.screenshot(
                path=screenshot,
                full_page=True
            )

            # --------------------------------------------------
            # PRINT STANDARD RESULT MARKER
            # --------------------------------------------------

            print()
            print(
                f"ACTUAL_RESULT: {actual_result}"
            )

            print(
                f"TEST_CASE_ID: {test_case_id}"
            )

            print(
                f"EXECUTION_STATUS: PASS"
            )

            print()

        except Exception as error:

            page.screenshot(
                path=screenshot,
                full_page=True
            )

            print()
            print(
                f"ACTUAL_RESULT: Test execution failed"
            )

            print(
                f"TEST_CASE_ID: {test_case_id}"
            )

            print(
                f"EXECUTION_STATUS: FAIL"
            )

            print()

            raise

        finally:

            browser.close()