# Bix Plaza

REST API for hotel management and reservations. It was developed during a technical test for a selection process from BIX Tecnologia.

## Requirements

- Docker and Docker Compose (installation guide [here](https://docs.docker.com/compose/install/))

## Installation

In order to install the project locally, run

```bash
# define the compose file
export COMPOSE_FILE=docker-compose.local.yml

# build the containers
docker compose build
```

## Running the app

To run the API in a development environment, execute

```bash
# development
docker compose up
```

now, the resources are available on the [localhost](http://localhost:8010).

## Test

```bash
# Running tests
docker compose exec -it django pdm run test

# Watch for file changes
docker compose exec -it django pdm run test:watch
```
