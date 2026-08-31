import pytest

import doctor


def test_result_defaults_to_no_remedy():
    r = doctor.Result(id="git", status=doctor.Status.PASS, detail="2.51.0")
    assert r.remedy == ""


def test_failing_result_requires_a_remedy():
    with pytest.raises(ValueError):
        doctor.Result(id="git", status=doctor.Status.FAIL, detail="not found")


def test_exit_code_is_zero_when_nothing_failed():
    results = [
        doctor.Result("a", doctor.Status.PASS, "ok"),
        doctor.Result("b", doctor.Status.WARN, "small"),
    ]
    assert doctor.exit_code(results) == 0


def test_exit_code_is_one_when_anything_failed():
    results = [
        doctor.Result("a", doctor.Status.PASS, "ok"),
        doctor.Result("b", doctor.Status.FAIL, "missing", remedy="install it"),
    ]
    assert doctor.exit_code(results) == 1
