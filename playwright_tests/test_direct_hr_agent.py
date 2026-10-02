from pathlib import Path
import sys
import time

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

TEST_CASE_ID = "US-010"


def test_direct_hr_agent_selection():

    start_time = time.time()

    status = "FAIL"
    actual_result = ""
    agent = "HR Agent"
    error_details = ""

    screenshot = (
        PROJECT_ROOT
        / "reports"
        / "direct_hr_agent.png"
    )

    # ==================================================
    # LOAD TEST DATA FROM EXCEL REPOSITORY
    # ==================================================

    test_case = get_test_case(
        TEST_CASE_ID
    )

    test_input = test_case["Test Input"]
    expected_result = test_case["Expected Result"]
    test_scenario = test_case["Test Scenario"]

    print()
    print(
        "=============================================="
    )
    print(
        "TEST CASE DATA"
    )
    print(
        "=============================================="
    )
    print(
        f"Test Case ID: {TEST_CASE_ID}"
    )
    print(
        f"Scenario: {test_scenario}"
    )
    print(
        f"Test Input: {test_input}"
    )
    print(
        f"Expected Result: {expected_result}"
    )
    print(
        "=============================================="
    )
    print()

    try:

        # ==================================================
        # LAUNCH PLAYWRIGHT
        # ==================================================

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=True
            )

            page = browser.new_page()

            # ==================================================
            # OPEN APPLICATION
            # ==================================================

            print(
                "Opening Corporate Customer Support application..."
            )

            page.goto(
                APP_URL,
                wait_until="domcontentloaded",
                timeout=60000
            )

            # ==================================================
            # WAIT FOR STREAMLIT APPLICATION
            # ==================================================

            print(
                "Waiting for Streamlit application..."
            )

            page.wait_for_timeout(
                10000
            )

            # ==================================================
            # VERIFY APPLICATION
            # ==================================================

            markdown_elements = page.locator(
                "[data-testid='stMarkdownContainer']"
            )

            markdown_text = (
                markdown_elements.all_inner_texts()
            )

            assert any(
                "Auto Router" in text
                for text in markdown_text
            ), (
                "Corporate Customer Support "
                "application did not load correctly."
            )

            print(
                "Application loaded successfully"
            )

            # ==================================================
            # FIND RADIO OPTIONS
            # ==================================================

            radio_options = page.locator(
                "label[data-testid='stRadioOption']"
            )

            radio_count = radio_options.count()

            print(
                f"Radio option count: {radio_count}"
            )

            assert radio_count == 7, (
                "Expected 7 agent options but found "
                f"{radio_count}."
            )

            # ==================================================
            # SELECT HR AGENT
            #
            # 0 = Auto Router
            # 1 = HR Agent
            # ==================================================

            hr_option = radio_options.nth(1)

            assert hr_option.is_visible(), (
                "HR Agent option is not visible."
            )

            print(
                "HR Agent option found"
            )

            hr_option.click()

            print(
                "HR Agent selected"
            )

            page.wait_for_timeout(
                3000
            )

            # ==================================================
            # VERIFY HR RADIO SELECTION
            # ==================================================

            hr_radio = page.locator(
                "input[type='radio'][value='1']"
            )

            assert hr_radio.is_checked(), (
                "HR Agent radio button was not selected."
            )

            print(
                "HR Agent radio selection validated"
            )

            # ==================================================
            # VERIFY CURRENT AGENT
            # ==================================================

            page_text = page.locator(
                "body"
            ).inner_text()

            assert (
                "Current Agent" in page_text
            ), (
                "Current Agent section was not displayed."
            )

            assert (
                "HR Agent" in page_text
            ), (
                "HR Agent was not displayed as "
                "the current agent."
            )

            print(
                "Current Agent validation successful"
            )

            # ==================================================
            # FIND CHAT INPUT
            # ==================================================

            chat_input = page.locator(
                "textarea[placeholder='Type your question here...']"
            )

            chat_input.wait_for(
                state="visible",
                timeout=60000
            )

            print(
                "Chat input found"
            )

            # ==================================================
            # ENTER HR QUERY
            # ==================================================

            print()
            print(
                "Sending HR query:"
            )
            print(
                test_input
            )

            chat_input.fill(
                test_input
            )

            # ==================================================
            # SEND MESSAGE
            # ==================================================

            send_button = page.get_by_role(
                "button",
                name="Send message"
            )

            assert not send_button.is_disabled(), (
                "Send button is disabled unexpectedly."
            )

            print(
                "Send button enabled"
            )

            send_button.click()

            print(
                "Message submitted"
            )

            # ==================================================
            # WAIT FOR HR RESPONSE
            # ==================================================

            print(
                "Waiting for HR Agent response..."
            )

            page.wait_for_timeout(
                15000
            )

            # ==================================================
            # VERIFY USER QUERY
            # ==================================================

            page_content = page.locator(
                "body"
            ).inner_text()

            assert (
                test_input in page_content
            ), (
                "Submitted HR query was not "
                "displayed in the application."
            )

            # ==================================================
            # VERIFY HR AGENT RESPONSE
            # ==================================================

            assert (
                "HR Agent" in page_content
            ), (
                "HR Agent response was not detected."
            )

            print(
                "HR query successfully submitted"
            )

            print(
                "HR Agent response validation successful"
            )

            # ==================================================
            # ACTUAL RESULT
            # ==================================================

            actual_result = (
                "Direct HR Agent selected and "
                "responded to the submitted query"
            )

            status = "PASS"

            # ==================================================
            # SCREENSHOT
            # ==================================================

            page.screenshot(
                path=str(screenshot),
                full_page=True
            )

            # ==================================================
            # STANDARD RESULT OUTPUT
            # ==================================================

            print()
            print(
                "=============================================="
            )
            print(
                "TEST RESULT"
            )
            print(
                "=============================================="
            )
            print(
                f"Test Case ID: {TEST_CASE_ID}"
            )
            print(
                f"Status: {status}"
            )
            print(
                f"Agent: {agent}"
            )
            print(
                f"Actual Result: {actual_result}"
            )
            print(
                f"Execution Duration: "
                f"{time.time() - start_time:.2f} sec"
            )
            print()

            print(
                f"ACTUAL_RESULT: {actual_result}"
            )

            print(
                f"TEST_CASE_ID: {TEST_CASE_ID}"
            )

            print(
                "EXECUTION_STATUS: PASS"
            )

            print()

            browser.close()

    except Exception as error:

        error_details = str(error)

        actual_result = (
            "Test execution failed"
        )

        status = "FAIL"

        try:
            page.screenshot(
                path=str(screenshot),
                full_page=True
            )
        except Exception:
            pass

        print()
        print(
            "=============================================="
        )
        print(
            "TEST RESULT"
        )
        print(
            "=============================================="
        )
        print(
            f"Test Case ID: {TEST_CASE_ID}"
        )
        print(
            f"Status: {status}"
        )
        print(
            f"Agent: {agent}"
        )
        print(
            f"Actual Result: {actual_result}"
        )
        print(
            f"Execution Duration: "
            f"{time.time() - start_time:.2f} sec"
        )
        print(
            f"Error: {error_details}"
        )
        print()

        print(
            f"ACTUAL_RESULT: {actual_result}"
        )

        print(
            f"TEST_CASE_ID: {TEST_CASE_ID}"
        )

        print(
            "EXECUTION_STATUS: FAIL"
        )

        print()

        raise