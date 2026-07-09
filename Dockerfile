# =============
# Builder image
# =============
FROM ghcr.io/astral-sh/uv:0.11.7-python3.14-trixie-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential cargo \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY pyproject.toml uv.lock README.md LICENSE.md SECURITY.md ./
COPY rust/ rust/
COPY src/ src/
RUN uv sync --frozen --no-dev --no-editable

# =============
# Runtime image
# =============
FROM python:3.14-slim-trixie

WORKDIR /app
COPY --from=builder /app/pyproject.toml /app/uv.lock ./
COPY --from=builder /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH"

CMD ["fandango"]
