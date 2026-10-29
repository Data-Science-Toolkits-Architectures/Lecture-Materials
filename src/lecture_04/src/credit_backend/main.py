from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from credit_backend.config import Settings
from credit_backend.decisions.dependencies import build_service
from credit_backend.decisions.router import router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    service = build_service(Settings())
    app.state.service = service
    try:
        yield
    finally:
        service.close()


app = FastAPI(title="Credit Decision Backend", lifespan=lifespan)
app.include_router(router)

# Task 7e: when the Information Extraction Service does not answer, answer with 503 and a
# message that says so. Register a handler for ExtractionUnavailableError here.
