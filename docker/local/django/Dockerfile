# Define an alias for the specfic python version used in this file.
ARG pythonMajorVersion=3.12
ARG pythonVersion=${pythonMajorVersion}.2
ARG pythonBaseImage=${pythonMajorVersion}-slim-bullseye

# Set default arguments
ARG appHome=/project

# Set default build arguments
ARG buildEnv=local

# Build stage
FROM python:${pythonBaseImage} AS builder

ARG appHome
ARG buildEnv

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV BUILD_ENV ${buildEnv}

# Install required system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    # dependencies for building Python packages
    build-essential \
    # psycopg dependencies
    libpq-dev \
    # Translations dependencies
    gettext \
    # cleaning up unused files
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

# Install PDM
RUN pip install -U pip setuptools wheel
RUN pip install pdm

# Copy application code to WORKDIR
COPY . ${appHome}

# Install dependencies and project into the local packages directory
WORKDIR ${appHome}
RUN mkdir __pypackages__ && pdm sync --no-editable


# Run stage
FROM python:${pythonBaseImage} AS runner

ARG pythonMajorVersion
ARG appHome
ARG buildEnv

# Copy application code to WORKDIR
COPY . ${appHome}

# Retrieve packages from build stage
ENV PYTHONPATH=/project/pkgs
COPY --from=builder /project/__pypackages__/${pythonMajorVersion}/lib /project/pkgs

# Retrieve executables
COPY --from=builder /project/__pypackages__/${pythonMajorVersion}/bin/* /bin/

# Copy the entrypoint script
COPY ./docker/${buildEnv}/django/entrypoint.sh /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

# Copy the start scripts

## Django
COPY ./docker/${buildEnv}/django/start.sh /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start
## Celery Worker
COPY ./docker/${buildEnv}/django/celery/worker/start.sh /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker
## Celery Beat
COPY ./docker/${buildEnv}/django/celery/beat/start.sh /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat

WORKDIR ${appHome}

ENTRYPOINT ["/entrypoint"]
