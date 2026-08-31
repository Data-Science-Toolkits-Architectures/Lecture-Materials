# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///
"""Machine check for Data Science Toolkits & Architectures."""

from __future__ import annotations

import argparse
import configparser
import datetime
import enum
import os
import platform
import re
import shutil
import socket
import subprocess
from dataclasses import dataclass
from pathlib import Path

VERSION = "0.1.0"


class Status(enum.StrEnum):
    PASS = "PASS"
    FAIL = "FAIL"
    WARN = "WARN"


@dataclass(frozen=True)
class Result:
    id: str
    status: Status
    detail: str
    remedy: str = ""

    def __post_init__(self) -> None:
        if self.status is Status.FAIL and not self.remedy:
            raise ValueError(f"check {self.id!r} failed without a remedy")


def exit_code(results: list[Result]) -> int:
    return 1 if any(r.status is Status.FAIL for r in results) else 0


GB = 1024 ** 3
MEMORY_FLOOR_GB = 8
DISK_FLOOR_GB = 15


def _gb(n: int) -> int:
    return n // GB


def probe_machine() -> dict[str, int | str]:
    return {
        "os": platform.system(),
        "release": platform.release(),
        "arch": platform.machine(),
        "memory_bytes": os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES")
        if hasattr(os, "sysconf") and "SC_PHYS_PAGES" in os.sysconf_names
        else _windows_memory_bytes(),
        "disk_free_bytes": shutil.disk_usage(os.getcwd()).free,
    }


def _windows_memory_bytes() -> int:
    import ctypes

    class MemoryStatusEx(ctypes.Structure):
        _fields_ = [
            ("dwLength", ctypes.c_ulong),
            ("dwMemoryLoad", ctypes.c_ulong),
            ("ullTotalPhys", ctypes.c_ulonglong),
            ("ullAvailPhys", ctypes.c_ulonglong),
            ("ullTotalPageFile", ctypes.c_ulonglong),
            ("ullAvailPageFile", ctypes.c_ulonglong),
            ("ullTotalVirtual", ctypes.c_ulonglong),
            ("ullAvailVirtual", ctypes.c_ulonglong),
            ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
        ]

    status = MemoryStatusEx()
    status.dwLength = ctypes.sizeof(MemoryStatusEx)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status))
    return int(status.ullTotalPhys)


def judge_memory(memory_bytes: int) -> Result:
    found = _gb(memory_bytes)
    if found >= MEMORY_FLOOR_GB:
        return Result("memory", Status.PASS, f"{found} GB")
    return Result(
        "memory",
        Status.WARN,
        f"{found} GB, below the {MEMORY_FLOOR_GB} GB this course is designed for",
        remedy="Tell us. The course can be arranged around it.",
    )


def judge_disk(disk_free_bytes: int) -> Result:
    found = _gb(disk_free_bytes)
    if found >= DISK_FLOOR_GB:
        return Result("disk", Status.PASS, f"{found} GB free")
    return Result(
        "disk",
        Status.FAIL,
        f"{found} GB free, {DISK_FLOOR_GB} GB needed",
        remedy=f"Free up {DISK_FLOOR_GB - found} GB and run this again.",
    )


INSTALL_HINTS = {
    "git": {
        "Windows": "winget install --id Git.Git -e",
        "Darwin": "xcode-select --install",
    },
    "uv": {
        "Windows": "winget install --id astral-sh.uv -e",
        "Darwin": "curl -LsSf https://astral.sh/uv/install.sh | sh",
    },
}


def _hint(tool: str) -> str:
    system = platform.system()
    if system in INSTALL_HINTS[tool]:
        return INSTALL_HINTS[tool][system]
    return f"Install {tool}. This course supports macOS and Windows only."


def run_tool(argv: list[str]) -> tuple[int, str]:
    try:
        proc = subprocess.run(argv, capture_output=True, text=True, timeout=120)
    except FileNotFoundError:
        return 127, ""
    except subprocess.TimeoutExpired:
        return 124, ""
    return proc.returncode, (proc.stdout + proc.stderr).strip()


def _version(out: str) -> str:
    match = re.search(r"\d+\.\d+(\.\d+)?", out)
    return match.group(0) if match else "unknown"


def judge_git(code: int, out: str) -> Result:
    if code != 0:
        return Result("git", Status.FAIL, "not found", remedy=_hint("git"))
    return Result("git", Status.PASS, _version(out))


def judge_git_identity(name: str, email: str) -> Result:
    missing = [k for k, v in (("user.name", name), ("user.email", email)) if not v.strip()]
    if not missing:
        return Result("git-identity", Status.PASS, email.strip())
    commands = " and ".join(f'git config --global {k} "..."' for k in missing)
    return Result(
        "git-identity",
        Status.FAIL,
        f"{', '.join(missing)} not set",
        remedy=f"Run {commands} with your own details.",
    )


def judge_uv(code: int, out: str) -> Result:
    if code != 0:
        return Result("uv", Status.FAIL, "not found", remedy=_hint("uv"))
    return Result("uv", Status.PASS, _version(out))


def judge_python(code: int, out: str) -> Result:
    if code != 0:
        return Result(
            "python",
            Status.FAIL,
            "uv cannot provide CPython 3.13",
            remedy="Run uv python install 3.13 and then run this again.",
        )
    return Result("python", Status.PASS, "3.13 available")


DOCKER_INSTALL = "Install Docker Desktop from docker.com and start it."


def judge_docker_cli(code: int, out: str) -> Result:
    if code != 0:
        return Result("docker-cli", Status.FAIL, "not found", remedy=DOCKER_INSTALL)
    return Result("docker-cli", Status.PASS, _version(out))


def judge_docker_daemon(code: int, out: str) -> Result:
    if code != 0:
        return Result(
            "docker-daemon",
            Status.FAIL,
            "the Docker daemon is not answering",
            remedy="Start Docker Desktop and wait until it reports that it is running.",
        )
    return Result("docker-daemon", Status.PASS, "up")


def judge_docker_run(code: int, out: str, virtualisation: bool | None) -> Result:
    if code == 0:
        return Result("docker-run", Status.PASS, "container ran")
    if virtualisation is False:
        return Result(
            "docker-run",
            Status.FAIL,
            "no container could run, and virtualisation is disabled on this machine",
            remedy=(
                "Turn on virtualisation in your laptop's firmware settings. "
                "If it is locked, tell us before 10 September."
            ),
        )
    return Result(
        "docker-run",
        Status.FAIL,
        "no container could run",
        remedy="Start Docker Desktop, wait until it reports that it is running, then run this again.",
    )


def probe_virtualisation() -> bool | None:
    if platform.system() != "Windows":
        return None
    code, out = run_tool(
        [
            "powershell",
            "-NoProfile",
            "-Command",
            "(Get-CimInstance Win32_Processor).VirtualizationFirmwareEnabled",
        ]
    )
    if code != 0:
        return None
    return "True" in out


def judge_shell(pwsh_present: bool) -> Result:
    if platform.system() != "Windows":
        return Result("shell", Status.PASS, "not applicable")
    if pwsh_present:
        return Result("shell", Status.PASS, "PowerShell 7 present")
    return Result(
        "shell",
        Status.FAIL,
        "PowerShell 7 is not installed",
        remedy="Run winget install --id Microsoft.PowerShell -e, then use PowerShell 7 rather than Windows PowerShell.",
    )


def probe_pwsh() -> bool:
    return shutil.which("pwsh") is not None


def judge_wsl(code: int, out: str) -> Result:
    if platform.system() != "Windows":
        return Result("wsl", Status.PASS, "not applicable")
    if code != 0:
        return Result(
            "wsl",
            Status.FAIL,
            "WSL2 is not installed",
            remedy="Install Docker Desktop and accept the WSL2 component it offers, then restart.",
        )
    return Result("wsl", Status.PASS, "present")


def probe_wslconfig() -> str | None:
    if platform.system() != "Windows":
        return None
    path = Path.home() / ".wslconfig"
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def judge_wslconfig(text: str | None) -> Result:
    if platform.system() != "Windows":
        return Result("wslconfig", Status.PASS, "not applicable")
    if text is None:
        return Result(
            "wslconfig",
            Status.WARN,
            "no readable .wslconfig in your user folder",
            remedy="Create it as described in the setup instructions. It matters from the fourth session.",
        )
    parser = configparser.ConfigParser()
    try:
        parser.read_string(text)
    except configparser.Error:
        return Result(
            "wslconfig",
            Status.WARN,
            ".wslconfig could not be read as a settings file",
            remedy="Compare it against the setup instructions and correct it.",
        )
    memory = parser.get("wsl2", "memory", fallback=None)
    if memory is None:
        return Result(
            "wslconfig",
            Status.WARN,
            ".wslconfig has no memory line under [wsl2]",
            remedy="Add memory=4GB, or memory=8GB if your laptop has 16 GB or more.",
        )
    return Result("wslconfig", Status.PASS, f"memory={memory}")


MOVE_REMEDY = (
    "Move the folder to dev inside your user folder, then clone it again there. "
    "Run mkdir ~/dev and cd ~/dev first."
)


def judge_path(path: Path, cloud_roots: list[Path]) -> Result:
    text = str(path)
    for root in cloud_roots:
        try:
            inside = path.is_relative_to(root)
        except (TypeError, ValueError):
            inside = False
        if inside:
            name = "OneDrive" if "OneDrive" in str(root) else "iCloud Drive"
            return Result(
                "path",
                Status.FAIL,
                f"the folder is inside {name}, which will corrupt it",
                remedy=MOVE_REMEDY,
            )
    if " " in text:
        return Result("path", Status.FAIL, "the path contains a space", remedy=MOVE_REMEDY)
    if not text.isascii():
        return Result(
            "path",
            Status.FAIL,
            "the path contains accented characters",
            remedy=MOVE_REMEDY + " Tell us if your user folder name is the problem.",
        )
    return Result("path", Status.PASS, f"{text} clean")


def probe_cloud_roots() -> list[Path]:
    roots: list[Path] = []
    for var in ("OneDrive", "OneDriveCommercial", "OneDriveConsumer"):
        value = os.environ.get(var)
        if value:
            roots.append(Path(value))
    try:
        home = Path.home()
    except RuntimeError:
        return roots
    for candidate in (home / "Library" / "Mobile Documents", home / "Library" / "CloudStorage"):
        try:
            if candidate.is_dir():
                roots.append(candidate)
        except OSError:
            continue
    return roots


WIDTH = 79
ALLOWED_FACTS = ("os", "release", "arch", "memory", "disk")
NETWORK_HOSTS = ("github.com", "pypi.org")

CHECK_ORDER = [
    "shell", "memory", "disk", "git", "git-identity", "uv", "python",
    "docker-cli", "docker-daemon", "docker-run", "wsl", "wslconfig",
    "path", "network",
]


def render_report(results: list[Result], facts: dict[str, str]) -> str:
    head = " DSTA SETUP REPORT "
    pad = (WIDTH - len(head)) // 2
    lines = ["-" * pad + head + "-" * (WIDTH - pad - len(head))]
    stamp = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines.append(f"doctor.py {VERSION}   stage 0   {stamp}")
    for key in ALLOWED_FACTS:
        if key in facts:
            lines.append(f"{key:<14}{facts[key]}")
    for r in results:
        lines.append(f"{r.id:<14}{r.status.value}  {r.detail}")
    counts = {s: sum(1 for r in results if r.status is s) for s in Status}
    lines.append(
        f"{'result':<14}{counts[Status.PASS]} passed, "
        f"{counts[Status.FAIL]} failed, {counts[Status.WARN]} warned"
    )
    lines.append("-" * WIDTH)
    return "\n".join(lines) + "\n"


def probe_network(host: str, port: int = 443, timeout: float = 5.0) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def judge_network(reachable: dict[str, bool]) -> Result:
    down = sorted(h for h, ok in reachable.items() if not ok)
    if not down:
        return Result("network", Status.PASS, " ".join(f"{h} ok" for h in sorted(reachable)))
    return Result(
        "network",
        Status.WARN,
        f"cannot reach {', '.join(down)}",
        remedy="If you are on a university or company network, tell us and we will look at it.",
    )


def guarded(check_id: str, fn, *args) -> Result:
    try:
        return fn(*args)
    except Exception as exc:  # noqa: BLE001
        return Result(
            check_id,
            Status.FAIL,
            f"this check could not run: {type(exc).__name__}",
            remedy="Send us this report. This is our problem to fix, not yours.",
        )


def _memory_bytes() -> int:
    return int(probe_machine()["memory_bytes"])


def _disk_free_bytes() -> int:
    return int(probe_machine()["disk_free_bytes"])


def collect_stage_0() -> tuple[list[Result], dict[str, str]]:
    try:
        machine = probe_machine()
        facts = {
            "os": f"{machine['os']} {machine['release']}",
            "arch": str(machine["arch"]),
            "memory": f"{_gb(int(machine['memory_bytes']))} GB",
            "disk": f"{_gb(int(machine['disk_free_bytes']))} GB free",
        }
    except Exception:
        facts = {}

    name_code, name_out = run_tool(["git", "config", "--global", "user.name"])
    mail_code, mail_out = run_tool(["git", "config", "--global", "user.email"])

    results = [
        guarded("shell", lambda: judge_shell(probe_pwsh())),
        guarded("memory", lambda: judge_memory(_memory_bytes())),
        guarded("disk", lambda: judge_disk(_disk_free_bytes())),
        guarded("git", lambda: judge_git(*run_tool(["git", "--version"]))),
        guarded(
            "git-identity",
            lambda: judge_git_identity(
                name_out if name_code == 0 else "", mail_out if mail_code == 0 else ""
            ),
        ),
        guarded("uv", lambda: judge_uv(*run_tool(["uv", "--version"]))),
        guarded("python", lambda: judge_python(*run_tool(["uv", "python", "find", "3.13"]))),
        guarded("docker-cli", lambda: judge_docker_cli(*run_tool(["docker", "--version"]))),
        guarded("docker-daemon", lambda: judge_docker_daemon(*run_tool(["docker", "info"]))),
        guarded(
            "docker-run",
            lambda: judge_docker_run(
                *run_tool(["docker", "run", "--rm", "hello-world"]), probe_virtualisation()
            ),
        ),
        guarded("wsl", lambda: judge_wsl(*run_tool(["wsl", "--status"]))),
        guarded("wslconfig", lambda: judge_wslconfig(probe_wslconfig())),
        guarded("path", lambda: judge_path(Path.cwd().resolve(), probe_cloud_roots())),
        guarded("network", lambda: judge_network({h: probe_network(h) for h in NETWORK_HOSTS})),
    ]
    order = {name: i for i, name in enumerate(CHECK_ORDER)}
    results.sort(key=lambda r: order[r.id])
    return results, facts


def closing_line(results: list[Result]) -> str:
    if any(r.status is Status.FAIL for r in results):
        return "Copy the block above and email it to both lecturers, subject DSTA setup."
    return "Nothing to send. Your machine is ready."


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check this machine for the course.")
    parser.add_argument("--stage", type=int, default=0)
    parser.add_argument("--only", default=None, help="show one check by id")
    parser.add_argument("--version", action="store_true")
    args = parser.parse_args(argv)
    if args.version:
        print(VERSION)
        return 0
    results, facts = collect_stage_0()
    if args.only:
        results = [r for r in results if r.id == args.only]
    for r in results:
        print(f"{r.status.value:<5} {r.id:<14} {r.detail}")
        if r.remedy:
            print(f"      {r.remedy}")
    print()
    print(render_report(results, facts), end="")
    print(closing_line(results))
    return exit_code(results)


if __name__ == "__main__":
    raise SystemExit(main())
