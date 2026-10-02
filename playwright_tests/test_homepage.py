from playwright.sync_api import sync_playwright

URL = "https://customer-support.srv1981708.hstgr.cloud/"


def test_corporate_customer_support_homepage():

    with sync_playwright() as p:

        # Launch Chromium
        browser = p.chromium.launch(headless=True)

        # Create page
        page = browser.new_page()

        # Open live application
        print("\nOpening Corporate Customer Support application...")

        page.goto(
            URL,
            wait_until="domcontentloaded"
        )

        # Wait for Streamlit UI to render
        print("Waiting for Streamlit application...")

        page.wait_for_timeout(10000)

        # Print page information
        print("\nPage Title:", page.title())
        print("Page URL:", page.url)

        # Get Streamlit markdown elements
        markdown_elements = page.locator(
            "[data-testid='stMarkdownContainer']"
        )

        markdown_text = markdown_elements.all_inner_texts()

        print("\n========== STREAMLIT TEXT ==========")

        for text in markdown_text:
            print(repr(text))

        # Verify application heading
        assert any(
            "Corporate Customer Support System" in text
            for text in markdown_text
        )

        print("Corporate Customer Support System found")

        # Verify Auto Router
        assert any(
            "Auto Router" in text
            for text in markdown_text
        )

        print("Auto Router found")

        # Capture screenshot
        page.screenshot(
            path="reports/homepage.png",
            full_page=True
        )

        print("Screenshot saved: reports/homepage.png")

        # Close browser
        browser.close()

        print("Browser closed")