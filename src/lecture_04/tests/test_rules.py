from decimal import Decimal
from typing import Final

import pytest
from credit_backend.contracts import Money, Outcome, Period, Reason
from credit_backend.decisions.rules import Policy, RuleInputs, decide

POLICY: Final = Policy(threshold=0.30)
INCOME: Final = Money(amount=Decimal("6000.00"), currency="CHF", period=Period.MONTHLY)


def inputs(
    default_probability: float | None = 0.10,
    monthly_income: Money | None = INCOME,
    has_loss_certificate: bool | None = False,
) -> RuleInputs:
    return RuleInputs(
        default_probability=default_probability,
        monthly_income=monthly_income,
        has_loss_certificate=has_loss_certificate,
    )


def needs_task_7a() -> None:
    if len(Reason) == 1:
        pytest.skip("Task 7a: no reason for a value nobody could read yet")


def test_an_application_at_the_threshold_is_refused() -> None:
    decision = decide(inputs(default_probability=POLICY.threshold), POLICY)

    assert decision.outcome is Outcome.REFUSED
    assert Reason.DEFAULT_PROBABILITY_ABOVE_THRESHOLD in decision.reasons


def test_a_register_nobody_could_read_is_not_taken_for_a_clean_one() -> None:
    needs_task_7a()

    unread = decide(inputs(has_loss_certificate=None), POLICY)
    clean = decide(inputs(has_loss_certificate=False), POLICY)

    assert set(unread.reasons) - set(clean.reasons)


def test_an_income_nobody_could_read_gets_a_reason_of_its_own() -> None:
    needs_task_7a()

    unread = decide(inputs(monthly_income=None), POLICY)
    read = decide(inputs(), POLICY)

    assert set(unread.reasons) - set(read.reasons)
