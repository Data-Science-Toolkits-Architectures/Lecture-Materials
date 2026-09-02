FROM python:3.13-slim

ENV TZ=Europe/Zurich
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY rules.py ./
CMD ["uv", "run", "python", "-c", "import rules; print(rules.decide)"]
