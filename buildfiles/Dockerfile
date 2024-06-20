FROM docker.io/python:3.11.7-slim-bookworm as python-base

# Install locales and generate uz_UZ.UTF-8 locale
RUN apt-get update && \
    apt-get install -y locales && \
    locale-gen uz_UZ.UTF-8 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Generate the uz_UZ.UTF-8 locale
RUN echo "uz_UZ.UTF-8 UTF-8" >> /etc/locale.gen && \
    locale-gen uz_UZ.UTF-8

# Set environment variables for the locale
ENV LANG=uz_UZ.UTF-8  
ENV LANGUAGE=uz_UZ:uz  
ENV LC_ALL=uz_UZ.UTF-8


ENV POETRY_VERSION=1.5.1 \
    POETRY_HOME=/opt/poetry \
    POETRY_VENV=/opt/poetry-venv \
    POETRY_CACHE_DIR=/opt/.cache
    
FROM python-base as poetry-base

RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

FROM python-base as app

COPY --from=poetry-base ${POETRY_VENV} ${POETRY_VENV}
ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /app
COPY ../poetry.lock pyproject.toml ./
RUN mkdir -p /app/src/media/images/
RUN poetry check && \
    poetry install --no-interaction --no-cache --no-root

COPY .. .
CMD ["poetry", "run", "python", "-m", "src.bot"]
