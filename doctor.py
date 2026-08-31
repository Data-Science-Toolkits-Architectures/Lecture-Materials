# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///
"""Machine check for Data Science Toolkits & Architectures."""

from __future__ import annotations

import enum
import os
import platform
import shutil
from dataclasses import dataclass

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
