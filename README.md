# Full Stack Streaming Analytics MVP

A modular, production-style full-stack project demonstrating real-time analytics using Apache Flink, Kafka, FastAPI backend, Next.js frontend, and Postgres. Each stack is modular and can be run independently or together using Docker Compose and orchestration scripts.

## Architecture
- **Frontend:** Next.js (React) for real-time dashboards and data visualization
- **Backend:** FastAPI for REST and WebSocket APIs
- **Streaming:** Apache Kafka for event streaming
- **Processing:** Apache Flink (PyFlink) for real-time data enrichment and aggregation
- **Database:** Postgres for raw and aggregated data storage
- **Orchestration:** Modular stacks (`app-stack`, `flink-stack`, `kafka-stack`, `shared-services`) managed via `Justfile` and `orchestrate.sh`

## Quickstart
```bash
# Start all stacks
just up
# or use the orchestration script
./orchestrate.sh up
```

- Access the frontend: http://localhost:3000
- Access the backend API: http://localhost:8000
- Access Flink UI: http://localhost:8081
- Access Kafka UI: http://localhost:8080

See each stack's README for details.
