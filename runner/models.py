
from typing import Literal
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    model_validator,
)


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Target(StrictModel):
    by: Literal["role", "label", "test_id", "text"]
    value: str = Field(min_length=1)
    name: str | None = None


class Assertion(StrictModel):
    expected: str = Field(min_length=1)
    mode: Literal["exact", "contains"] = "exact"


class Step(StrictModel):
    action: Literal[
        "goto",
        "fill",
        "click",
        "assert_visible",
        "assert_text",
        "wait_for_url",
    ]

    path: str | None = None
    target: Target | None = None
    value: str | None = None
    assertion: Assertion | None = None

    @model_validator(mode="after")
    def validate_fields(self):
        rules = {
            "goto": {"path"},
            "fill": {"target", "value"},
            "click": {"target"},
            "assert_visible": {"target"},
            "assert_text": {"target", "assertion"},
            "wait_for_url": {"path"},
        }

        required = rules[self.action]

        missing = [
            field
            for field in required
            if getattr(self, field) is None
        ]

        if missing:
            raise ValueError(
                f"{self.action} requires: "
                + ", ".join(sorted(missing))
            )

        unused = (
            self.model_fields_set
            - required
            - {"action"}
        )

        if unused:
            raise ValueError(
                f"{self.action} does not accept: "
                + ", ".join(sorted(unused))
            )

        if self.path is not None:
            if (
                not self.path.startswith("/")
                or self.path.startswith("//")
            ):
                raise ValueError(
                    "path must be an application path "
                    "such as /login"
                )

        return self


class TestCase(StrictModel):
    name: str = Field(min_length=1)
    steps: list[Step] = Field(
        min_length=1,
        max_length=50,
    )
