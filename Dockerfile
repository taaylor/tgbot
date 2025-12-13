ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim AS builder

WORKDIR /opt/app

RUN apt-get update  \
    && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /var/cache/apt

RUN curl -sSL https://install.python-poetry.org | python3 - \
    && export PATH="/root/.local/bin:$PATH" \
    && poetry config virtualenvs.create true \
    && poetry config virtualenvs.in-project true

ENV PATH="/root/.local/bin:${PATH}"
COPY poetry.lock pyproject.toml ./
RUN poetry install --only main

FROM python:${PYTHON_VERSION}-slim

WORKDIR /opt/app
COPY --from=builder /opt/app/.venv ./.venv
COPY ./src ./src
ENV PATH="/opt/app/.venv/bin:$PATH"

RUN useradd -m tgbotuser
USER tgbotuser

ENTRYPOINT [ "python3", "src" ]
