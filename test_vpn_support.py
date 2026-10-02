from playwright.sync_api import sync_playwright
import time

from reports.excel_reporter import update_test_result


URL = "https://customer-support.srv1981708.hstgr.cloud/"

VPN_QUERY = (
    "My laptop VPN is not working. "
    "I am unable to connect to the company network."
)

EXPECTED_RESULT = "Request routed to: Internal IT"


def test_vpn_support_request():

    start_time = time.time()

    status = "FAIL"
    actual_result = ""
    agent = ""
    error_details = ""

    screenshot = "reports/vpn_support.png"

    try:

        with sync_playwright() as p:

            # Launch browser
            browser = p.chromium.launch(headless=True)

            # Create page
            page = browser.new_page()

            # Open application
            print("\nOpening Corporate Customer Support application...")

            page.goto(
                URL,
                wait_until="domcontentloaded"
            )

            # Wait for Streamlit UI
            print("Waiting for Streamlit application...")

            page.wait_for_timeout(10000)

            # Verify Auto Router is available
            markdown_elements = page.locator(
                "[data-testid='stMarkdownContainer']"
            )

            markdown_text = markdown_elements.all_inner_texts()

            assert any(
                "Auto Router" in text
                for text in markdown_text
            )

            print("Auto Router available")

            # Locate chat input
            chat_input = page.locator(
                "textarea[placeholder='Type your question here...']"
            )

            assert chat_input.is_visible()

            print("Chat input found")

            # Enter VPN support question
            print("\nSending query:")
            print(VPN_QUERY)

            chat_input.fill(VPN_QUERY)

            # Locate Send button
            send_button = page.get_by_role(
                "button",
                name="Send message"
            )

            assert send_button.is_visible()

            # Click Send
            send_button.click()

            print("Message submitted")

            # Wait dynamically for AI response
            print("\nWaiting for AI routing response...")

            routing_response = page.get_by_text(
                EXPECTED_RESULT,
                exact=True
            )

            routing_response.wait_for(
                state="visible",
                timeout=60000
            )

            print("AI routing response received")

            # Capture page text
            page_text = page.locator("body").inner_text()

            print("\n========== APPLICATION RESPONSE ==========")
            print(page_text)

            # Validate submitted query
            assert VPN_QUERY in page_text

            print("\nVPN query successfully submitted")

            # Validate routing
            assert EXPECTED_RESULT in page_text

            print("Internal IT routing validation successful")

            # Store actual result
            actual_result = EXPECTED_RESULT
            agent = "Internal IT"

            # Test passed
            status = "PASS"

            # Screenshot
            page.screenshot(
                path=screenshot,
                full_page=True
            )

            print("Screenshot saved:", screenshot)

            # Close browser
            browser.close()

            print("Browser closed")

    except Exception as error:

        error_details = str(error)

        print("\nTEST FAILED")
        print("Error:", error_details)

        raise

    finally:

        # Calculate execution duration
        execution_duration = round(
            time.time() - start_time,
            2
        )

        print("\n========== TEST RESULT ==========")
        print("Test Case ID:", "US-001")
        print("Status:", status)
        print("Agent:", agent)
        print("Execution Duration:", execution_duration, "sec")

        # Update Excel
        update_test_result(
            test_case_id="US-001",
            user_story="VPN Support Request",
            test_scenario="Verify VPN support request routing",
            test_input=VPN_QUERY,
            expected_result=EXPECTED_RESULT,
            actual_result=actual_result,
            agent=agent,
            status=status,
            execution_duration=f"{execution_duration} sec",
            screenshot=screenshot,
            error_details=error_details
        )