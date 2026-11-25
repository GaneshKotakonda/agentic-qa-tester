
from pathlib import Path

import pytest
from pydantic import ValidationError

from runner.models import TestCase


ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize(
    "filename",
    ["login_valid.json", "login_invalid.json"],
)
def test_valid_specs(filename):
    path = ROOT / "specs" / filename

    test_case = TestCase.model_validate_json(
        path.read_text(encoding="utf-8")
    )

    assert len(test_case.steps) > 0


@pytest.mark.parametrize(
    "bad_step",
    [
        {"action": "delete_database"},
        {"action": "fill", "value": "hello"},
        {
            "action": "goto",
            "path": "https://example.com",
        },
        {
            "action": "goto",
            "path": "/login",
            "unexpected": True,
        },
    ],
)
def test_invalid_steps_are_rejected(bad_step):
    with pytest.raises(ValidationError):
        TestCase.model_validate(
            {
                "name": "Invalid specification",
                "steps": [bad_step],
            }
        )
