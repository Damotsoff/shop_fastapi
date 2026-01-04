FROM python:3.12-slim


ENV POETRY_VERSION=2.2.1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1


RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app


COPY poetry.lock pyproject.toml ./


RUN poetry install --no-root --no-directory

RUN poetry install


