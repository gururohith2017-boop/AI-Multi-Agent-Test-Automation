from playwright.sync_api import sync_playwright

URL = "https://customer-support.srv1981708.hstgr.cloud/"


def test_inspect_chat():

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("\nOpening application...")

        page.goto(
            URL,
            wait_until="domcontentloaded"
        )

        print("Waiting for Streamlit application...")

        page.wait_for_timeout(10000)

        print("\n========== TEXT INPUTS ==========")

        inputs = page.locator("input")

        print("Input count:", inputs.count())

        for i in range(inputs.count()):
            element = inputs.nth(i)

            print(
                f"Input {i}:",
                "type =", element.get_attribute("type"),
                "| placeholder =", element.get_attribute("placeholder"),
                "| aria-label =", element.get_attribute("aria-label")
            )

        print("\n========== TEXTAREAS ==========")

        textareas = page.locator("textarea")

        print("Textarea count:", textareas.count())

        for i in range(textareas.count()):
            element = textareas.nth(i)

            print(
                f"Textarea {i}:",
                "placeholder =", element.get_attribute("placeholder"),
                "| aria-label =", element.get_attribute("aria-label")
            )

        print("\n========== BUTTONS ==========")

        buttons = page.locator("button")

        print("Button count:", buttons.count())

        for i in range(buttons.count()):
            element = buttons.nth(i)

            print(
                f"Button {i}:",
                repr(element.inner_text()),
                "| aria-label =", element.get_attribute("aria-label"),
                "| title =", element.get_attribute("title")
            )

        print("\n========== CHAT ELEMENTS ==========")

        chat_elements = page.locator(
            "[data-testid='stChatInput'], "
            "[data-testid='stChatMessage']"
        )

        print(
            "Chat element count:",
            chat_elements.count()
        )

        page.screenshot(
            path="reports/chat_diagnostic.png",
            full_page=True
        )

        browser.close()