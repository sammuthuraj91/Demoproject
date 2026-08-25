import os

from playwright.sync_api import Page, expect

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:5000")


def test_mytemplate_homepage(page: Page):
    page.goto(BASE_URL)

    # Verify the renamed application
    expect(page).to_have_title("MyTemplate")
    expect(page.get_by_text("MyTemplate", exact=True).first).to_be_visible()

    # Verify the main landing-page content
    expect(
        page.get_by_role("heading", name="Batteries Included")
    ).to_be_visible()

    # Verify user-facing navigation
    expect(
        page.get_by_role("link", name="Pricing")
    ).to_be_visible()

    # There are two Demo links: header and hero
    expect(
        page.get_by_role("link", name="Demo").first
    ).to_be_visible()


def test_demo_link_opens_signup(page: Page):
    page.goto(BASE_URL)

    # Use the header Demo link
    demo_link = page.locator("header").get_by_role(
        "link", name="Demo"
    )

    expect(demo_link).to_be_visible()

    # Navigate directly through the href.
    # This avoids the Flask Debug Toolbar intercepting the click.
    expect(demo_link).to_have_attribute("href", "/signup")

    page.goto(f"{BASE_URL}/signup")

    expect(page).to_have_url(f"{BASE_URL}/signup")
