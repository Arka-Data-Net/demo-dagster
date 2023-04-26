ARG APP_NAME=demo_dagster
ARG APP_PATH=/opt/${APP_NAME}
ARG PYTHON_VERSION=3.10.6
ARG POETRY_VERSION=1.2.0

FROM python:${PYTHON_VERSION} as python-base

ENV PYTHONUNBUFFERED=1 \
	PYTHONDONTWRITEBYTECODE=1 \
	PIP_NO_CACHE_DIR=off \
	PIP_DISABLE_PIP_VERSION_CHECK=on \
	PIP_DEFAULT_TIMEOUT=100 \ 
	POETRY_HOME="/opt/poetry" \
	POETRY_VIRTUALENVS_IN_PROJECT=true \
	POETRY_NO_INTERACTION=1 \
	PYSETUP_PATH="/opt/pysetup" \
	VENV_PATH="/opt/pysetup/.venv" \
	APP_NAME=${APP_NAME}

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

FROM python-base as builder-base
RUN apt-get update && apt-get install --no-install-recommends -y \
	curl \
	build-essential

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://install.python-poetry.org | python -

# copy project requirement files here to ensure they will be cached.
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml README.md ./

# install runtime deps - uses $POETRY_VIRTUALENVS_IN_PROJECT internally
RUN poetry install --no-root --only main
RUN poetry add dagster-postgres dagster-graphql dagster-docker

COPY ./${APP_NAME} ./${APP_NAME}

RUN poetry install --only-root


FROM python-base as production
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

#CMD [ "/bin/sh" ]
#CMD ["python", "/opt/pysetup/${APP_NAME}/server.py"]
CMD ["dagster", "api", "grpc", "-h", "0.0.0.0", "-p", "4000", "--module-name", "demo_dagster"]