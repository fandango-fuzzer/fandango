# =============
# Builder image
# =============
FROM ghcr.io/astral-sh/uv:0.11.7-python3.14-trixie-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential cmake curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Distro cargo packages are often too old for modern edition/Cargo.lock; use rustup.
RUN curl -sSf https://sh.rustup.rs | sh -s -- -y --profile minimal \
    && . "$HOME/.cargo/env" \
    && rustc --version
ENV PATH="/root/.cargo/bin:${PATH}"

WORKDIR /app
COPY pyproject.toml uv.lock CMakeLists.txt README.md LICENSE.md SECURITY.md ./
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
