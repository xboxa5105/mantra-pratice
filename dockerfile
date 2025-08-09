# first stage
FROM python:3.13-slim AS builder

WORKDIR /opt

# Setup poetry environment
RUN apt-get update && \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install --yes --no-install-recommends ca-certificates curl

ADD uv.lock pyproject.toml ./
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"
RUN uv sync

# second stage
FROM python:3.13-slim

ARG BUILD_VERSION
ARG BUILD_TIME

RUN apt-get update; apt-get -y install curl vim

WORKDIR /app

COPY --from=builder /opt/.venv /opt/.venv
ENV PATH="/opt/.venv/bin:$PATH"
ADD src /app
ENV PYTHONPATH=/app
ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT [ "fastapi", "run", "src/main.py", "--port", "8000" ]

