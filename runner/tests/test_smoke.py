
import pytest
from playwright.sync_api import sync_playwright, expect

BASE_URL = "http://localhost:5173"

@pytest.fixture
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(  headless=False,
    slow_mo=500)
        page = browser.new_page()

        yield page

        browser.close()


def test_valid_login(page):
    page.goto(f"{BASE_URL}/login")

    page.get_by_test_id("email-input").fill("qa@example.test")
    page.get_by_test_id("password-input").fill("demo-password")
    page.get_by_test_id("login-button").click()

    expect(page.get_by_test_id("dashboard-title")).to_be_visible()


def test_invalid_login(page):
    page.goto(f"{BASE_URL}/login")

    page.get_by_test_id("email-input").fill("qa@example.test")
    page.get_by_test_id("password-input").fill("wrong-password")
    page.get_by_test_id("login-button").click()

    expect(page.get_by_test_id("login-error")).to_have_text(
        "Invalid email or password"
    )
