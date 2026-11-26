from datetime import datetime, timezone
from time import perf_counter

from runner.reporting import create_run_dir, save_report
from pathlib import Path
from urllib.parse import urljoin

from playwright.sync_api import (
    Page,
    expect,
    sync_playwright,
)

from runner.models import TestCase
from runner.locators import get_locator


TIMEOUT_MS = 5000


def build_url(base_url: str, path: str) -> str:
    if not path.startswith("/") or path.startswith("//"):
        raise ValueError("Expected an application path starting with /")

    return urljoin(
        base_url.rstrip("/") + "/",
        path.lstrip("/")
    )


def execute_step(page: Page, step: dict, base_url: str):
    action = step["action"]

    if action == "goto":
        url = build_url(base_url, step["path"])
        page.goto(url, wait_until="domcontentloaded")

    elif action == "fill":
        locator = get_locator(page, step["target"])
        locator.fill(step["value"])

    elif action == "click":
        locator = get_locator(page, step["target"])
        locator.click()

    elif action == "assert_visible":
        locator = get_locator(page, step["target"])
        expect(locator).to_be_visible(timeout=TIMEOUT_MS)

    elif action == "assert_text":
        locator = get_locator(page, step["target"])

        expected = step.get("expected")

        if expected is None:
            assertion = step.get("assertion")
            if isinstance(assertion, dict):
                expected = assertion.get(
                    "expected",
                    assertion.get("text", assertion.get("value"))
                )

        if expected is None:
            expected = step.get("text", step.get("value"))

        if expected is None:
            raise ValueError("Missing expected assertion text")

        expect(locator).to_have_text(
            expected,
            timeout=TIMEOUT_MS
        )

    elif action == "wait_for_url":
        url = build_url(base_url, step["path"])
        page.wait_for_url(url, timeout=TIMEOUT_MS)

    else:
        raise ValueError(f"Unsupported action: {action}")



def run_test(spec_path: str, base_url: str):
    content = Path(spec_path).read_text(encoding="utf-8")
    test_case = TestCase.model_validate_json(content)

    run_id, run_dir = create_run_dir()
    start_time = perf_counter()

    report = {
        "run_id": run_id,
        "test_name": test_case.name,
        "started_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "status": "PASS",
        "duration_seconds": 0,
        "failed_step": None,
        "error": None,
        "screenshot": None,
        "trace": "trace.zip",
        "steps": []
    }

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(
                headless=True
            )

            try:
                context = browser.new_context()

                try:
                    context.tracing.start(
                        screenshots=True,
                        snapshots=True,
                        sources=True
                    )

                    try:
                        page = context.new_page()
                        page.set_default_timeout(TIMEOUT_MS)
                        page.set_default_navigation_timeout(10000)

                        for index, step in enumerate(
                            test_case.steps, start=1
                        ):
                            data = step.model_dump(
                                mode="json",
                                exclude_none=True
                            )

                            action = data["action"]
                            step_start = perf_counter()

                            step_result = {
                                "step_index": index,
                                "action": action,
                                "status": "PASS",
                                "duration_ms": 0,
                                "error": None
                            }

                            print(
                                f"Running step {index}: {action}"
                            )

                            try:
                                execute_step(
                                    page, data, base_url
                                )

                            except Exception as error:
                                step_result["status"] = "FAIL"
                                step_result["error"] = str(error)
                                report["failed_step"] = index

                                screenshot_path = (
                                    run_dir / "failure.png"
                                )

                                try:
                                    page.screenshot(
                                        path=str(screenshot_path),
                                        full_page=True,
                                        timeout=3000
                                    )
                                    report["screenshot"] = (
                                        "failure.png"
                                    )
                                except Exception as screenshot_error:
                                    report["screenshot_error"] = str(
                                        screenshot_error
                                    )

                                raise

                            finally:
                                elapsed = (
                                    perf_counter() - step_start
                                ) * 1000

                                step_result["duration_ms"] = round(
                                    elapsed, 2
                                )

                                report["steps"].append(
                                    step_result
                                )

                    finally:
                        context.tracing.stop(
                            path=str(run_dir / "trace.zip")
                        )

                finally:
                    context.close()

            finally:
                browser.close()

    except Exception as error:
        report["status"] = "FAIL"
        report["error"] = str(error)

        print(f"FAIL: {test_case.name}")
        raise

    else:
        print(f"PASS: {test_case.name}")

    finally:
        report["duration_seconds"] = round(
            perf_counter() - start_time, 3
        )

        report_path = save_report(
            run_dir, report
        )

        print(f"Report saved: {report_path}")

    return report

    