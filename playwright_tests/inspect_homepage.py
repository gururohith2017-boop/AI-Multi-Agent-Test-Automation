from playwright.sync_api import sync_playwright

URL = "https://customer-support.srv1981708.hstgr.cloud/"


def test_inspect_homepage():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("\nOpening application...")
        page.goto(URL, wait_until="domcontentloaded")

        print("Waiting for Streamlit application...")

        # Give Streamlit time to render the application
        page.wait_for_timeout(10000)

        print("\n========== PAGE TITLE ==========")
        print(page.title())

        print("\n========== PAGE URL ==========")
        print(page.url)

        print("\n========== PAGE TEXT ==========")
        print(page.locator("body").inner_text())

        print("\n========== BUTTONS ==========")
        print(page.locator("button").all_inner_texts())

        print("\n========== ALL TEXT ELEMENTS ==========")
        print(
            page.locator("[data-testid='stMarkdownContainer']")
            .all_inner_texts()
        )

        page.screenshot(
            path="reports/diagnostic_homepage.png",
            full_page=True
        )

        browser.close()