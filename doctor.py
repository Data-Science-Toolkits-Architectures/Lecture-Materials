# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///
"""Machine check for Data Science Toolkits & Architectures."""

from __future__ import annotations

import enum
import os
import platform
import re
import shutil
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
    return path.read_text(encoding="utf-8") if path.is_file() else None


def judge_wslconfig(text: str | None) -> Result:
    if platform.system() != "Windows":
        return Result("wslconfig", Status.PASS, "not applicable")
    if text is None:
        return Result(
            "wslconfig",
            Status.WARN,
            "no .wslconfig in your user folder",
            remedy="Create it as described in the setup instructions. It matters from the fourth session.",
        )
    line = next((l.strip() for l in text.splitlines() if l.strip().startswith("memory=")), None)
    if line is None:
        return Result(
            "wslconfig",
            Status.WARN,
            ".wslconfig has no memory line",
            remedy="Add memory=4GB, or memory=8GB if your laptop has 16 GB or more.",
        )
    return Result("wslconfig", Status.PASS, line)
