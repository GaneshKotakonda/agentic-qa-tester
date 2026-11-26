
from playwright.sync_api import Page, Locator


def get_locator(page: Page, target: dict) -> Locator:
    by = target["by"]
    value = target["value"]

    if by == "role":
        return page.get_by_role(
            value,
            name=target.get("name")
        )

    elif by == "label":
        return page.get_by_label(value)

    elif by in ("test_id", "testid"):
        return page.get_by_test_id(value)

    elif by == "text":
        return page.get_by_text(value, exact=True)

    else:
        raise ValueError(
            f"Unsupported locator type: {by}"
        )
