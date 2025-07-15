#!/bin/bash

set -e

# Ensure the external network exists
if ! docker network ls --format '{{.Name}}' | grep -q '^livestream-net$'; then
  echo "Creating external Docker network: livestream-net"
  docker network create livestream-net
fi

case "$1" in
  up)
    echo "Starting shared services (Postgres)..."
    docker compose -f shared-services/docker-compose.yml up -d

    echo "Starting Kafka stack..."
    docker compose -f kafka-stack/docker-compose.yml up -d

    echo "Starting Flink stack..."
    docker compose -f flink-stack/docker-compose.yml up -d

    echo "Starting App stack (backend/frontend)..."
    docker compose -f app-stack/docker-compose.yml up --build -d
    ;;
  down)
    echo "Stopping all stacks..."
    docker compose -f app-stack/docker-compose.yml down
    docker compose -f flink-stack/docker-compose.yml down
    docker compose -f kafka-stack/docker-compose.yml down
    docker compose -f shared-services/docker-compose.yml down
    ;;
  logs)
    echo "Tailing logs for all stacks..."
    docker compose -f shared-services/docker-compose.yml logs -f &
    docker compose -f kafka-stack/docker-compose.yml logs -f &
    docker compose -f flink-stack/docker-compose.yml logs -f &
    docker compose -f app-stack/docker-compose.yml logs -f &
    wait
    ;;
  status)
    echo "Status for all stacks:"
    docker compose -f shared-services/docker-compose.yml ps
    docker compose -f kafka-stack/docker-compose.yml ps
    docker compose -f flink-stack/docker-compose.yml ps
    docker compose -f app-stack/docker-compose.yml ps
    ;;
  *)
    echo "Usage: $0 {up|down|logs|status}"
    exit 1
    ;;
esac 