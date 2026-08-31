import pytest
from pathlib import PurePosixPath, PureWindowsPath

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


def test_hint_does_not_offer_a_macos_command_on_linux(monkeypatch):
    monkeypatch.setattr(doctor.platform, "system", lambda: "Linux")
    r = doctor.judge_git(code=127, out="")
    assert "xcode-select" not in r.remedy
    assert r.remedy


def test_run_tool_reports_127_when_the_executable_is_missing():
    code, out = doctor.run_tool(["definitely-not-a-real-command-9z8y7x"])
    assert code == 127
    assert out == ""


def test_uv_missing_gives_the_platform_command(monkeypatch):
    monkeypatch.setattr(doctor.platform, "system", lambda: "Darwin")
    r = doctor.judge_uv(code=127, out="")
    assert r.status is doctor.Status.FAIL
    assert "astral.sh" in r.remedy


def test_daemon_down_tells_them_to_start_docker_desktop():
    r = doctor.judge_docker_daemon(code=1, out="Cannot connect to the Docker daemon")
    assert r.status is doctor.Status.FAIL
    assert "Docker Desktop" in r.remedy


def test_container_runs():
    r = doctor.judge_docker_run(code=0, out="Hello from Docker!", virtualisation=True)
    assert r.status is doctor.Status.PASS


def test_container_failure_with_virtualisation_off_names_the_firmware():
    r = doctor.judge_docker_run(code=1, out="error during connect", virtualisation=False)
    assert r.status is doctor.Status.FAIL
    assert "virtualisation" in r.detail.lower()
    assert "firmware" in r.remedy.lower()


def test_container_failure_with_virtualisation_on_does_not_blame_the_firmware():
    r = doctor.judge_docker_run(code=1, out="error during connect", virtualisation=True)
    assert r.status is doctor.Status.FAIL
    assert "firmware" not in r.remedy.lower()


def test_container_run_passes_on_exit_code_alone_whatever_docker_prints():
    r = doctor.judge_docker_run(code=0, out="Hallo von Docker!", virtualisation=None)
    assert r.status is doctor.Status.PASS


def test_docker_cli_missing_tells_them_to_install_docker_desktop():
    r = doctor.judge_docker_cli(code=127, out="")
    assert r.status is doctor.Status.FAIL
    assert "Docker Desktop" in r.remedy


def test_docker_cli_present_reports_the_version():
    r = doctor.judge_docker_cli(code=0, out="Docker version 29.1.3, build f52814d")
    assert r.status is doctor.Status.PASS
    assert r.detail == "29.1.3"


@pytest.fixture
def on_windows(monkeypatch):
    monkeypatch.setattr(doctor.platform, "system", lambda: "Windows")


def test_wslconfig_missing_only_warns(on_windows):
    r = doctor.judge_wslconfig(None)
    assert r.status is doctor.Status.WARN


def test_wslconfig_present_reports_the_memory_line(on_windows):
    r = doctor.judge_wslconfig("[wsl2]\nmemory=8GB\nprocessors=2\nswap=2GB\n")
    assert r.status is doctor.Status.PASS
    assert "memory=8GB" in r.detail


def test_wslconfig_without_a_memory_key_warns(on_windows):
    r = doctor.judge_wslconfig("[wsl2]\nprocessors=2\n")
    assert r.status is doctor.Status.WARN
    assert "memory" in r.remedy


def test_missing_powershell_seven_fails_with_the_winget_command(on_windows):
    r = doctor.judge_shell(pwsh_present=False)
    assert r.status is doctor.Status.FAIL
    assert "Microsoft.PowerShell" in r.remedy


def test_windows_checks_are_not_applicable_elsewhere(monkeypatch):
    monkeypatch.setattr(doctor.platform, "system", lambda: "Darwin")
    for r in (doctor.judge_shell(False), doctor.judge_wsl(1, ""), doctor.judge_wslconfig(None)):
        assert r.status is doctor.Status.PASS
        assert r.detail == "not applicable"


def test_wslconfig_accepts_spaces_around_the_equals(on_windows):
    r = doctor.judge_wslconfig("[wsl2]\nmemory = 8GB\n")
    assert r.status is doctor.Status.PASS
    assert "8GB" in r.detail


def test_wslconfig_ignores_a_memory_line_in_another_section(on_windows):
    r = doctor.judge_wslconfig("[experimental]\nmemory=8GB\n")
    assert r.status is doctor.Status.WARN


def test_wslconfig_warns_rather_than_raising_on_rubbish(on_windows):
    r = doctor.judge_wslconfig("this is not an ini file at all\n@@@@\n")
    assert r.status is doctor.Status.WARN


def test_wslconfig_unreadable_file_is_treated_as_missing(on_windows):
    r = doctor.judge_wslconfig(None)
    assert r.status is doctor.Status.WARN
    assert "readable" in r.detail


def test_clean_path_passes():
    r = doctor.judge_path(PurePosixPath("/Users/ada/dev/Lecture-Materials"), [])
    assert r.status is doctor.Status.PASS


def test_path_with_a_space_fails():
    r = doctor.judge_path(PurePosixPath("/Users/ada/My Projects/Lecture-Materials"), [])
    assert r.status is doctor.Status.FAIL
    assert "space" in r.detail.lower()


def test_path_with_an_umlaut_fails():
    r = doctor.judge_path(PurePosixPath("/Users/muller/dev/Lecture-Materials"), [])
    assert r.status is doctor.Status.PASS
    r = doctor.judge_path(PurePosixPath("/Users/m\u00fcller/dev/Lecture-Materials"), [])
    assert r.status is doctor.Status.FAIL
    assert "accented" in r.detail.lower()


def test_path_inside_onedrive_fails_and_names_onedrive():
    root = PureWindowsPath(r"C:\Users\ada\OneDrive - Universitat Luzern")
    inside = PureWindowsPath(r"C:\Users\ada\OneDrive - Universitat Luzern\dev\Lecture-Materials")
    r = doctor.judge_path(inside, [root])
    assert r.status is doctor.Status.FAIL
    assert "OneDrive" in r.detail


def test_path_inside_icloud_fails():
    root = PurePosixPath("/Users/ada/Library/Mobile Documents")
    inside = PurePosixPath("/Users/ada/Library/Mobile Documents/dev/Lecture-Materials")
    r = doctor.judge_path(inside, [root])
    assert r.status is doctor.Status.FAIL


def test_a_sibling_folder_sharing_a_name_prefix_is_not_flagged():
    root = PureWindowsPath(r"C:\Users\ada\OneDriveLuzern")
    outside = PureWindowsPath(r"C:\Users\ada\OneDriveLuzernArchive\dev\repo")
    assert doctor.judge_path(outside, [root]).status is doctor.Status.PASS


def test_a_windows_path_differing_only_in_case_is_still_flagged():
    root = PureWindowsPath(r"C:\Users\ada\OneDrive")
    inside = PureWindowsPath(r"c:\users\ada\onedrive\dev\repo")
    assert doctor.judge_path(inside, [root]).status is doctor.Status.FAIL


def test_cloud_roots_survives_a_home_directory_that_cannot_be_resolved(monkeypatch):
    def boom():
        raise RuntimeError("no home")

    monkeypatch.setattr(doctor.Path, "home", staticmethod(boom))
    monkeypatch.delenv("OneDrive", raising=False)
    monkeypatch.delenv("OneDriveCommercial", raising=False)
    monkeypatch.delenv("OneDriveConsumer", raising=False)
    assert doctor.probe_cloud_roots() == []
