"""A small backend for the notebook of lecture 5.

It is the backend from the slides, built in three steps with FastAPI. An application has three
fields. The backend has no model and no rules. It approves every application, and its answer
repeats the application as the backend received it. That shows what arrives on the other side
of an interface.
"""

import socket
import threading
import time
from typing import Final

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field

SAMPLE_APPLICATION: Final = {"age": 34, "monthly_income": 6000, "utilisation": 0.25}


class Application(BaseModel):
    age: int = Field(ge=18, le=120, description="The applicant's age in years.")
    monthly_income: float | None = Field(
        default=None,
        ge=0,
        description="The gross income per month in CHF, or null if nobody could read it.",
    )
    utilisation: float = Field(
        ge=0, description="The share of the credit limit in use. 0.30 means 30 percent."
    )


class Decision(BaseModel):
    outcome: str
    received: Application


app = FastAPI(title="Credit decisions")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/decisions")
def create_decision(application: Application) -> Decision:
    return Decision(outcome="approved", received=application)


# ---------------------------------------------------------------- running it from a notebook


def free_port() -> int:
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return probe.getsockname()[1]


def start_in_background(target: FastAPI = app, port: int | None = None) -> str:
    """Start an app in a background thread and return its address once it answers."""
    port = port or free_port()
    config = uvicorn.Config(target, host="127.0.0.1", port=port, log_level="warning")
    server = uvicorn.Server(config)
    threading.Thread(target=server.run, daemon=True).start()
    deadline = time.monotonic() + 10
    while not server.started:
        if time.monotonic() > deadline:
            raise RuntimeError(f"The server on port {port} did not start within 10 seconds.")
        time.sleep(0.05)
    return f"http://127.0.0.1:{port}"
