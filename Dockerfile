FROM python:3.11.7-alpine AS base

ENV PIP_NO_CACHE_DIR=1
RUN apk update && apk add --no-cache \
    curl

RUN pip install --upgrade pip \
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && pip install uv

WORKDIR /app


FROM base AS api

COPY . .
WORKDIR src/api_service
RUN uv sync --frozen

CMD ["uv", "run", "main.py"]


FROM base AS bot

COPY . .
WORKDIR src/bot_service
RUN uv sync --frozen

CMD ["uv", "run", "main.py"]