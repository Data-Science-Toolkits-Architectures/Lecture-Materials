"""The decision rules after the three buckets, and before the tests.

The database, the HTTP call and the page are gone. The duplicated branches and
the config class with one user are gone. A missing field now raises.

The logic has not been touched. Restructuring makes code testable. It does not
make it correct. That is what the tests are for.
"""

from dataclasses import dataclass

REFUSE_AT_OR_ABOVE = 0.30
MINIMUM_AGE = 18


class MissingValue(ValueError):
    def __init__(self, field: str) -> None:
        super().__init__(f"{field} was missing")
        self.field = field


@dataclass(frozen=True)
class Application:
    age: int | None
    monthly_income: float | None
    debt_ratio: float | None
    late_payments: int | None


@dataclass(frozen=True)
class Decision:
    approved: bool
    reasons: tuple[str, ...]


def decide(application: Application, probability_of_default: float) -> Decision:
    age = _supplied(application.age, "age")
    debt_ratio = _supplied(application.debt_ratio, "debt_ratio")

    reasons: list[str] = []
    if probability_of_default > REFUSE_AT_OR_ABOVE:
        reasons.append("tbd, the wording the applicant sees is yours to write")
    if age < MINIMUM_AGE:
        reasons.append("tbd")

    _ = debt_ratio
    return Decision(approved=not reasons, reasons=tuple(reasons))


def _supplied[T](value: T | None, field: str) -> T:
    if value is None:
        raise MissingValue(field)
    return value
