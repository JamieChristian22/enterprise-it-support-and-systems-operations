#!/usr/bin/env python3
"""Browser smoke for the standalone synthetic IT operations console."""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reports"


def expect(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    OUT.mkdir(exist_ok=True)
    errors = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 850})
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.route("http://**/*", lambda route: route.abort())
        page.route("https://**/*", lambda route: route.abort())
        page.goto((ROOT / "demo/it-operations-console.html").as_uri())
        expect(page.locator("#ticketCount").inner_text() == "120", "Sample count incorrect")
        expect(page.locator("#ticketList button.ticket").count() == 120,
               "Initial ticket list is incomplete")
        expect(page.locator("#bars .barcol").count() == 7, "Monthly trend chart missing")
        page.locator("#ticketList button.ticket").last.click()
        expect("INC-" in page.locator("#detailTitle").inner_text(), "Ticket details failed")
        page.select_option("#priority", "P1")
        filtered = page.locator("#ticketList button.ticket").count()
        expect(0 < filtered < 120, "Priority filter did not limit tickets")
        page.fill("#search", "UNMATCHED-TEST-TICKET")
        expect(page.get_by_text("No records match.").count() == 1,
               "No-results state missing")
        page.fill("#search", "")
        page.select_option("#metric", index=1)
        expect(page.locator("#bars .barcol").count() == 7,
               "Selecting a monthly KPI failed")
        page.screenshot(path=str(OUT / "itops-desktop.png"), full_page=True)
        page.set_viewport_size({"width": 390, "height": 844})
        expect(not page.evaluate(
            "document.documentElement.scrollWidth > window.innerWidth + 2"
        ), "Mobile horizontal overflow")
        page.screenshot(path=str(OUT / "itops-mobile.png"), full_page=True)
        expect(not errors, "Browser JS errors: " + "; ".join(errors))
        browser.close()
    print("PASS: IT console filters, record details, trend, mobile rendering")


if __name__ == "__main__":
    main()
