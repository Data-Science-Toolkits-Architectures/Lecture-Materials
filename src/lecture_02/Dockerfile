FROM python:3.13-slim

ENV TZ=Europe/Zurich
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY src/lecture_02/rules.py ./src/lecture_02/
CMD ["uv", "run", "python", "-c", "from src.lecture_02 import rules; print(rules.decide)"]
