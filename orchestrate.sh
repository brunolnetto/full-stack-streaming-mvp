#!/bin/bash

set -e

if [[ -z "$1" ]]; then
  echo "Usage: $0 {up|down|build|logs|status} [dev|prod]"
  exit 1
fi

PROFILE=${2:-prod}

# Ensure the external network exists
if ! docker network ls --format '{{.Name}}' | grep -q '^livestream-net$'; then
  echo "Creating external Docker network: livestream-net"
  docker network create livestream-net
fi

case "$1" in
  build)
    echo "Building shared services (Postgres)..."
    docker compose -f shared-services/docker-compose.yml --profile "$PROFILE" build

    echo "Building Kafka stack..."
    docker compose -f kafka-stack/docker-compose.yml --profile "$PROFILE" build

    echo "Building Flink stack..."
    docker compose -f flink-stack/docker-compose.yml --profile "$PROFILE" build

    echo "Building App stack (backend/frontend)..."
    docker compose -f app-stack/docker-compose.yml --profile "$PROFILE" build
    ;;
  up)
    echo "Starting shared services (Postgres)..."
    docker compose -f shared-services/docker-compose.yml --profile "$PROFILE" up -d

    echo "Starting Kafka stack..."
    docker compose -f kafka-stack/docker-compose.yml --profile "$PROFILE" up -d

    echo "Starting Flink stack..."
    docker compose -f flink-stack/docker-compose.yml --profile "$PROFILE" up -d

    echo "Starting App stack (backend/frontend)..."
    docker compose -f app-stack/docker-compose.yml --profile "$PROFILE" up -d
    ;;
  down)
    echo "Stopping all stacks..."
    docker compose -f app-stack/docker-compose.yml --profile "$PROFILE" down
    docker compose -f flink-stack/docker-compose.yml --profile "$PROFILE" down
    docker compose -f kafka-stack/docker-compose.yml --profile "$PROFILE" down
    docker compose -f shared-services/docker-compose.yml --profile "$PROFILE" down
    ;;
  logs)
    echo "Tailing logs for all stacks..."
    docker compose -f shared-services/docker-compose.yml --profile "$PROFILE" logs -f &
    docker compose -f kafka-stack/docker-compose.yml --profile "$PROFILE" logs -f &
    docker compose -f flink-stack/docker-compose.yml --profile "$PROFILE" logs -f &
    docker compose -f app-stack/docker-compose.yml --profile "$PROFILE" logs -f &
    wait
    ;;
  status)
    echo "Status for all stacks:"
    docker compose -f shared-services/docker-compose.yml --profile "$PROFILE" ps
    docker compose -f kafka-stack/docker-compose.yml --profile "$PROFILE" ps
    docker compose -f flink-stack/docker-compose.yml --profile "$PROFILE" ps
    docker compose -f app-stack/docker-compose.yml --profile "$PROFILE" ps
    ;;
  *)
    echo "Usage: $0 {up|down|logs|status|build} [dev|prod]"
    exit 1
    ;;
esac 