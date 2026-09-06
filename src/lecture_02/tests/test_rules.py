import pytest

from src.lecture_02.rules import (
    MINIMUM_AGE,
    REFUSE_AT_OR_ABOVE,
    Application,
    MissingValue,
    decide,
)

SAFE = 0.05


@pytest.fixture
def application() -> Application:
    return Application(age=34, monthly_income=6200.0, debt_ratio=0.21, late_payments=0)


def test_a_low_risk_application_is_approved(application):
    assert decide(application, SAFE).approved


@pytest.mark.parametrize(
    ("probability", "approved"),
    [
        (REFUSE_AT_OR_ABOVE - 0.01, True),
        (REFUSE_AT_OR_ABOVE, False),
        (REFUSE_AT_OR_ABOVE + 0.01, False),
    ],
)
def test_the_threshold_refuses_at_the_boundary(application, probability, approved):
    assert decide(application, probability).approved is approved


@pytest.mark.parametrize("field", ["age", "debt_ratio"])
def test_a_missing_field_raises(application, field):
    with pytest.raises(MissingValue) as raised:
        decide(Application(**{**vars(application), field: None}), SAFE)
    assert raised.value.field == field


def test_the_age_rule_overrides_a_low_probability(application):
    under_age = Application(**{**vars(application), "age": MINIMUM_AGE - 1})
    assert not decide(under_age, SAFE).approved


def test_a_refusal_says_why(application):
    assert decide(application, 0.9).reasons
