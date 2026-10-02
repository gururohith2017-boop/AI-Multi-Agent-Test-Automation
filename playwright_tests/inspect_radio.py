from playwright.sync_api import sync_playwright


URL = "https://customer-support.srv1981708.hstgr.cloud/"


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

    print("\n========== HR RADIO HTML INSPECTION ==========")

    hr_radio = page.locator(
        "input[type='radio'][value='1']"
    )

    print("HR radio count:", hr_radio.count())
    print("HR radio visible:", hr_radio.is_visible())

    print("\n---------- HR RADIO OUTER HTML ----------")
    print(
        hr_radio.evaluate(
            "(element) => element.outerHTML"
        )
    )

    print("\n---------- HR RADIO PARENT HTML ----------")
    print(
        hr_radio.evaluate(
            "(element) => element.parentElement.outerHTML"
        )
    )

    print("\n---------- HR RADIO GRANDPARENT HTML ----------")
    print(
        hr_radio.evaluate(
            "(element) => element.parentElement.parentElement.outerHTML"
        )
    )

    print("\n---------- HR RADIO ANCESTOR TEXT ----------")

    print(
        hr_radio.evaluate(
            """
            (element) => {
                let current = element;
                for (let i = 0; i < 6; i++) {
                    if (current) {
                        console.log(current.innerText);
                        current = current.parentElement;
                    }
                }
                return element.parentElement.parentElement.parentElement.innerText;
            }
            """
        )
    )

    print("\n========== END INSPECTION ==========")

    browser.close()

    print("\nBrowser closed")