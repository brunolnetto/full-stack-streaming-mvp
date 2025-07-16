#########################
# 1. Builder Stage 🛠️
#########################
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

# Configure uv-managed Python environment
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Create and activate virtual environment
RUN uv venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy all project files first
COPY . /app

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install -e .

#########################
# 2. Runtime Stage 🚀
#########################
FROM python:3.12-slim

# Install runtime OS dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
      curl jq postgresql-client ca-certificates wget lsof file \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy virtual environment and application
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app

# Ensure virtual environment is in PATH
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONPATH=/app/server

WORKDIR /app

# Default to API startup; worker overrides entrypoint in compose
ENTRYPOINT []
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]