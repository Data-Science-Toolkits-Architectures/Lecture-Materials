"""The decision rules of the Unicorn Adoption Bureau.

Numbers in, a Decision out. No database, no email, no HTML.
That is what makes this file testable.
"""

from dataclasses import dataclass

MIN_GARDEN_M2 = 50.0
MIN_GLITTER_TOLERANCE = 6
MIN_HOURS_AT_HOME = 20
TOP_FLOOR_WITHOUT_LIFT = 2


class MissingAnswer(ValueError):
    """An application reached the rules with a question left unanswered."""

    def __init__(self, field: str) -> None:
        super().__init__(f"{field} was not answered")
        self.field = field


@dataclass(frozen=True)
class Application:
    garden_m2: float | None
    glitter_tolerance: int | None
    hours_at_home: int | None
    floor: int
    has_lift: bool


@dataclass(frozen=True)
class Decision:
    approved: bool
    reasons: tuple[str, ...]


def decide(application: Application) -> Decision:
    """Decide whether a unicorn adoption is approved."""
    garden_m2 = _answered(application.garden_m2, "garden_m2")
    glitter_tolerance = _answered(application.glitter_tolerance, "glitter_tolerance")
    hours_at_home = _answered(application.hours_at_home, "hours_at_home")

    reasons: list[str] = []
    if garden_m2 < MIN_GARDEN_M2:
        reasons.append(f"A garden of at least {MIN_GARDEN_M2:.0f} square metres is required.")
    if glitter_tolerance < MIN_GLITTER_TOLERANCE:
        reasons.append(f"A glitter tolerance of at least {MIN_GLITTER_TOLERANCE} is required.")
    if hours_at_home < MIN_HOURS_AT_HOME:
        reasons.append(f"At least {MIN_HOURS_AT_HOME} hours at home each week are required.")
    if application.floor > TOP_FLOOR_WITHOUT_LIFT and not application.has_lift:
        reasons.append("A unicorn cannot be kept above the second floor without a lift.")

    return Decision(approved=not reasons, reasons=tuple(reasons))


def _answered[T](value: T | None, field: str) -> T:
    if value is None:
        raise MissingAnswer(field)
    return value
