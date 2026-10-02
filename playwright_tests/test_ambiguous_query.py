from pathlib import Path
import sys
import re

from playwright.sync_api import sync_playwright


PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)

from agents.test_case_repository import get_test_case


APP_URL = (
    "https://customer-support.srv1981708.hstgr.cloud/"
)


def test_ambiguous_query():

    # ==================================================
    # LOAD TEST DATA FROM EXCEL REPOSITORY
    # ==================================================

    test_case = get_test_case(
        "US-009"
    )

    test_case_id = test_case["Test Case ID"]
    user_story = test_case["User Story"]
    test_scenario = test_case["Test Scenario"]
    test_input = test_case["Test Input"]
    expected_result = test_case["Expected Result"]

    screenshot = (
        PROJECT_ROOT
        / "reports"
        / "ambiguous_query.png"
    )

    # ==================================================
    # PLAYWRIGHT EXECUTION
    # ==================================================

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page()

        try:

            # --------------------------------------------------
            # OPEN APPLICATION
            # --------------------------------------------------

            page.goto(
                APP_URL,
                wait_until="domcontentloaded",
                timeout=60000
            )

            # --------------------------------------------------
            # FIND CHAT INPUT
            # --------------------------------------------------

            chat_input = page.locator(
                "textarea[placeholder='Type your question here...']"
            )

            chat_input.wait_for(
                state="visible",
                timeout=60000
            )

            # --------------------------------------------------
            # ENTER AMBIGUOUS QUERY
            # --------------------------------------------------

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
            # WAIT FOR APPLICATION RESPONSE
            # --------------------------------------------------

            page.wait_for_timeout(
                15000
            )

            # --------------------------------------------------
            # VERIFY USER QUERY APPEARS
            # --------------------------------------------------

            page_content = page.locator(
                "body"
            ).inner_text()

            assert (
                test_input in page_content
            ), (
                "Submitted test input was not "
                "displayed in the application."
            )

            # --------------------------------------------------
            # FIND ROUTING RESPONSE
            # --------------------------------------------------

            routing_response = page.get_by_text(
                re.compile(
                    r"Request routed to:"
                )
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
            ).strip()

            # --------------------------------------------------
            # VALIDATE ROUTING RESPONSE
            # --------------------------------------------------

            assert (
                "Request routed to:"
                in actual_result
            ), (
                "No routing response was generated."
            )

            # --------------------------------------------------
            # VALIDATE KNOWN AGENT
            # --------------------------------------------------

            valid_agents = [
                "Internal IT",
                "HR",
                "Payroll",
                "Admin",
                "Help Desk",
                "Compliance",
            ]

            matched_agent = None

            for agent in valid_agents:

                if agent.lower() in (
                    actual_result.lower()
                ):
                    matched_agent = agent
                    break

            assert matched_agent is not None, (
                "Unknown routing decision: "
                f"{actual_result}"
            )

            # --------------------------------------------------
            # SCREENSHOT
            # --------------------------------------------------

            page.screenshot(
                path=str(screenshot),
                full_page=True
            )

            # --------------------------------------------------
            # STANDARD RESULT OUTPUT
            # --------------------------------------------------

            print()
            print(
                f"ACTUAL_RESULT: {actual_result}"
            )

            print(
                f"TEST_CASE_ID: {test_case_id}"
            )

            print(
                "EXECUTION_STATUS: PASS"
            )

            print()

        except Exception:

            page.screenshot(
                path=str(screenshot),
                full_page=True
            )

            print()
            print(
                "ACTUAL_RESULT: Test execution failed"
            )

            print(
                f"TEST_CASE_ID: {test_case_id}"
            )

            print(
                "EXECUTION_STATUS: FAIL"
            )

            print()

            raise

        finally:

            browser.close()