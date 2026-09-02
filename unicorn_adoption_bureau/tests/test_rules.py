import pytest

from rules import (
    MIN_GARDEN_M2,
    MIN_GLITTER_TOLERANCE,
    Application,
    MissingAnswer,
    decide,
)


@pytest.fixture
def application() -> Application:
    return Application(
        garden_m2=80.0,
        glitter_tolerance=9,
        hours_at_home=30,
        floor=1,
        has_lift=False,
    )


def test_a_complete_application_is_approved(application):
    assert decide(application).approved


@pytest.mark.parametrize(
    ("garden_m2", "approved"),
    [(MIN_GARDEN_M2 - 0.1, False), (MIN_GARDEN_M2, True), (MIN_GARDEN_M2 + 0.1, True)],
)
def test_the_garden_boundary_is_inclusive(application, garden_m2, approved):
    assert decide(Application(**{**vars(application), "garden_m2": garden_m2})).approved is approved


@pytest.mark.parametrize(
    ("glitter_tolerance", "approved"),
    [(MIN_GLITTER_TOLERANCE - 1, False), (MIN_GLITTER_TOLERANCE, True)],
)
def test_the_glitter_boundary_is_inclusive(application, glitter_tolerance, approved):
    changed = Application(**{**vars(application), "glitter_tolerance": glitter_tolerance})
    assert decide(changed).approved is approved


@pytest.mark.parametrize("field", ["garden_m2", "glitter_tolerance", "hours_at_home"])
def test_an_unanswered_question_raises(application, field):
    with pytest.raises(MissingAnswer) as raised:
        decide(Application(**{**vars(application), field: None}))
    assert raised.value.field == field


def test_the_floor_rule_overrides_a_perfect_score(application):
    changed = Application(**{**vars(application), "floor": 4, "has_lift": False})
    assert not decide(changed).approved


def test_a_lift_makes_the_top_floor_acceptable(application):
    changed = Application(**{**vars(application), "floor": 4, "has_lift": True})
    assert decide(changed).approved


def test_a_refusal_says_why(application):
    changed = Application(**{**vars(application), "garden_m2": 10.0})
    assert "square metres" in " ".join(decide(changed).reasons)
