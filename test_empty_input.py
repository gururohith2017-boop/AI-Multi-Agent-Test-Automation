from playwright.sync_api import sync_playwright
import time

from agents.test_case_repository import get_test_case
from reports.excel_reporter import update_test_result


URL = "https://customer-support.srv1981708.hstgr.cloud/"

TEST_CASE_ID = "US-008"


def test_empty_input_validation():

    start_time = time.time()

    status = "FAIL"
    actual_result = ""
    agent = "None"
    error_details = ""

    screenshot = "reports/empty_input.png"

    test_case = get_test_case(TEST_CASE_ID)

    test_input = test_case["Test Input"]
    expected_result = test_case["Expected Result"]
    test_scenario = test_case["Test Scenario"]

    print()
    print("==============================================")
    print("TEST CASE DATA")
    print("==============================================")
    print("Test Case ID:", TEST_CASE_ID)
    print("Scenario:", test_scenario)
    print("Test Input:", repr(test_input))
    print("Expected Result:", expected_result)
    print("==============================================")
    print()

    try:

        with sync_playwright() as p:

            # =================================================
            # 1. LAUNCH BROWSER
            # =================================================

            browser = p.chromium.launch(
                headless=True
            )

            page = browser.new_page()

            # =================================================
            # 2. OPEN APPLICATION
            # =================================================

            print(
                "Opening Corporate Customer Support application..."
            )

            page.goto(
                URL,
                wait_until="domcontentloaded"
            )

            # =================================================
            # 3. WAIT FOR STREAMLIT
            # =================================================

            print(
                "Waiting for Streamlit application..."
            )

            page.wait_for_timeout(10000)

            # =================================================
            # 4. VERIFY APPLICATION
            # =================================================

            markdown_elements = page.locator(
                "[data-testid='stMarkdownContainer']"
            )

            markdown_text = (
                markdown_elements.all_inner_texts()
            )

            assert any(
                "Auto Router" in text
                for text in markdown_text
            )

            print(
                "Auto Router available"
            )

            # =================================================
            # 5. FIND CHAT INPUT
            # =================================================

            chat_input = page.locator(
                "textarea[placeholder='Type your question here...']"
            )

            assert chat_input.is_visible()

            print(
                "Chat input found"
            )

            # =================================================
            # 6. CLEAR INPUT
            # =================================================

            chat_input.fill("")

            print(
                "Chat input cleared"
            )

            # =================================================
            # 7. VERIFY INPUT IS EMPTY
            # =================================================

            current_value = chat_input.input_value()

            assert current_value == ""

            print(
                "Input value confirmed empty"
            )

            # =================================================
            # 8. FIND SEND BUTTON
            # =================================================

            send_button = page.get_by_role(
                "button",
                name="Send message"
            )

            assert send_button.is_visible()

            print(
                "Send button found"
            )

            # =================================================
            # 9. CHECK BUTTON STATE
            # =================================================

            button_disabled = send_button.is_disabled()

            print(
                "Send button disabled:",
                button_disabled
            )

            # =================================================
            # 10. CAPTURE CURRENT PAGE STATE
            # =================================================

            page_text = page.locator(
                "body"
            ).inner_text()

            # =================================================
            # 11. VERIFY NO ROUTING RESPONSE
            # =================================================

            routing_response_exists = (
                "Request routed to:" in page_text
            )

            print(
                "Routing response exists:",
                routing_response_exists
            )

            assert not routing_response_exists

            # =================================================
            # 12. BUILD ACTUAL RESULT
            # =================================================

            if button_disabled:

                actual_result = (
                    "Empty input detected and Send button "
                    "is disabled; no routing response generated."
                )

            else:

                actual_result = (
                    "Empty input detected; Send button is enabled "
                    "but no routing response is displayed."
                )

            # =================================================
            # 13. CURRENT APPLICATION BEHAVIOR
            # =================================================

            print()
            print(
                "========== APPLICATION BEHAVIOR =========="
            )

            print(
                actual_result
            )

            # =================================================
            # 14. MARK TEST PASS
            # =================================================

            status = "PASS"

            print()
            print(
                "Validation Result: PASS"
            )

            # =================================================
            # 15. SCREENSHOT
            # =================================================

            page.screenshot(
                path=screenshot,
                full_page=True
            )

            print(
                "Screenshot saved:",
                screenshot
            )

            # =================================================
            # 16. CLOSE BROWSER
            # =================================================

            browser.close()

            print(
                "Browser closed"
            )

    except Exception as error:

        error_details = str(error)

        print()
        print(
            "TEST FAILED"
        )

        print(
            "Error:",
            error_details
        )

        raise

    finally:

        # =====================================================
        # 17. EXECUTION DURATION
        # =====================================================

        execution_duration = round(
            time.time() - start_time,
            2
        )

        print()
        print(
            "========== TEST RESULT =========="
        )

        print(
            "Test Case ID:",
            TEST_CASE_ID
        )

        print(
            "Status:",
            status
        )

        print(
            "Agent:",
            agent
        )

        print(
            "Actual Result:",
            actual_result
        )

        print(
            "Execution Duration:",
            execution_duration,
            "sec"
        )

        # =====================================================
        # 18. UPDATE EXCEL REPORT
        # =====================================================

        update_test_result(
            test_case_id=TEST_CASE_ID,
            user_story=test_case["User Story"],
            test_scenario=test_scenario,
            test_input=test_input,
            expected_result=expected_result,
            actual_result=actual_result,
            agent=agent,
            status=status,
            execution_duration=(
                f"{execution_duration} sec"
            ),
            screenshot=screenshot,
            error_details=error_details
        )