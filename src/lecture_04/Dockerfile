FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1
COPY --from=ghcr.io/astral-sh/uv:0.12.17 /uv /bin/uv

WORKDIR /app
COPY pyproject.toml uv.lock* ./
RUN uv sync --no-dev --no-install-project
COPY src src
RUN uv sync --no-dev

EXPOSE 8000
CMD ["uv", "run", "--no-sync", "uvicorn", "credit_backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
