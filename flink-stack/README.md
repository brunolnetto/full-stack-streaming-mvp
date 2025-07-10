# Flink Stack

This stack runs Apache Flink (JobManager and TaskManager) using a custom PyFlink image. Connects to the shared Docker network `livestream-net` and shared Postgres.

## Usage

```
docker compose up -d --build
``` 