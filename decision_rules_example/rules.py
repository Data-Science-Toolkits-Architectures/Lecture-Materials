"""The decision rules, as an example of the shape yours will have.

Numbers in, a Decision out. No database, no HTTP, no page. That is what makes
this file testable, and it is the only reason the tests beside it are short.

Every number here is an example. Which threshold you use, which policy rules you
add, which of the two mistakes you would rather make, and what the applicant is
told are yours to decide and to defend in your decision log. Nothing in this
file answers any of them for you.
"""

from dataclasses import dataclass

# An example value, not a recommendation. Choose and justify your own.
REFUSE_AT_OR_ABOVE = 0.30

# The one rule here that is not a judgement. You will add others.
MINIMUM_AGE = 18


class MissingValue(ValueError):
    """An application reached the rules with a field nobody supplied."""

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
    """Turn a probability and an application into a decision and its reasons."""
    age = _supplied(application.age, "age")
    debt_ratio = _supplied(application.debt_ratio, "debt_ratio")

    reasons: list[str] = []
    if probability_of_default >= REFUSE_AT_OR_ABOVE:
        reasons.append("tbd, the wording the applicant sees is yours to write")
    if age < MINIMUM_AGE:
        reasons.append("tbd")

    # Your own policy rules go here. Each one needs an entry in the decision log
    # saying why it overrides the model rather than feeding into it.

    _ = debt_ratio
    return Decision(approved=not reasons, reasons=tuple(reasons))


def _supplied[T](value: T | None, field: str) -> T:
    if value is None:
        raise MissingValue(field)
    return value
