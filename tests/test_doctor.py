import pytest

import doctor

GB = 1024 ** 3


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


def test_memory_passes_at_the_floor():
    assert doctor.judge_memory(8 * GB).status is doctor.Status.PASS


def test_memory_warns_below_the_floor():
    r = doctor.judge_memory(4 * GB)
    assert r.status is doctor.Status.WARN
    assert "4 GB" in r.detail


def test_disk_fails_below_the_floor_and_says_how_much_was_found():
    r = doctor.judge_disk(9 * GB)
    assert r.status is doctor.Status.FAIL
    assert "9 GB" in r.detail
    assert r.remedy


def test_disk_passes_at_the_floor():
    assert doctor.judge_disk(15 * GB).status is doctor.Status.PASS


def test_git_missing_gives_a_platform_specific_remedy(monkeypatch):
    monkeypatch.setattr(doctor.platform, "system", lambda: "Windows")
    r = doctor.judge_git(code=127, out="")
    assert r.status is doctor.Status.FAIL
    assert "winget install --id Git.Git -e" in r.remedy


def test_git_present_reports_the_version():
    r = doctor.judge_git(code=0, out="git version 2.51.0")
    assert r.status is doctor.Status.PASS
    assert r.detail == "2.51.0"


def test_git_identity_fails_when_email_is_missing():
    r = doctor.judge_git_identity(name="Ada", email="")
    assert r.status is doctor.Status.FAIL
    assert "user.email" in r.remedy


def test_git_identity_passes_when_both_are_set():
    assert doctor.judge_git_identity("Ada", "ada@stud.unilu.ch").status is doctor.Status.PASS


def test_python_fails_when_uv_cannot_provide_313():
    r = doctor.judge_python(code=1, out="no interpreter found")
    assert r.status is doctor.Status.FAIL
    assert "uv python install 3.13" in r.remedy
