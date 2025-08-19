# Copilot Instructions for full-stack-streaming-mvp

## Project Overview
This is a modular, production-style full-stack streaming analytics MVP. It demonstrates real-time analytics using:
- **Frontend:** Next.js (React) for dashboards (`app-stack/frontend`)
- **Backend:** FastAPI for REST/WebSocket APIs (`app-stack/backend`)
- **Streaming:** Apache Kafka for event streaming (`kafka-stack`)
- **Processing:** Apache Flink (PyFlink) for real-time enrichment/aggregation (`flink-stack`)
- **Database:** Postgres for raw/aggregated data (`shared-services`)
- **Orchestration:** Modular stacks managed via `Justfile` and `orchestrate.sh`

## Architecture & Data Flow
- Events are generated (e.g., web traffic) and sent to Kafka.
- Flink jobs (`flink-stack/src/`) consume, enrich, and aggregate events, storing results in Postgres.
- FastAPI backend exposes REST/WebSocket APIs for frontend consumption.
- Next.js frontend visualizes real-time data.
- All services communicate via Docker Compose networks and shared Postgres.

## Developer Workflows
- **Start all stacks:**
  - `just up` (recommended)
  - `./orchestrate.sh up`
- **Start individual stacks:**
  - `docker compose up -d --build` in each stack directory
- **Frontend dev server:**
  - `npm run dev` in `app-stack/frontend`
- **Backend dev server:**
  - Use Docker Compose or run FastAPI manually
- **Flink jobs:**
  - Place jobs in `flink-stack/src/` and run via Flink UI (`http://localhost:8081`)

## Conventions & Patterns
- **Healthcheck endpoints:**
  - Frontend: `/api/health`
  - Backend: `/health`
- **Flink jobs:**
  - `staging_requests_job.py`: Reads from Kafka, writes to `staging_table_requests` (Postgres)
  - `mart_requests_job.py`: Aggregates with 5-min windows, writes to `mart_table_requests_hits`
- **Docker Compose:**
  - Each stack is independently deployable; all connect to shared network/services
- **Source organization:**
  - Backend: `app-stack/backend/src/` (routers, models, services)
  - Frontend: `app-stack/frontend/src/` (features, context, types)

## Integration Points
- **Kafka topics:** Used for event streaming between frontend/backend and Flink
- **Postgres:** Central data store for all stacks
- **WebSocket:** Real-time updates from backend to frontend

## Key Files & Directories
- `Justfile`, `orchestrate.sh`: Orchestration scripts
- `app-stack/`, `flink-stack/`, `kafka-stack/`, `shared-services/`: Main stack directories
- `flink-stack/src/`: Example Flink jobs
- `app-stack/backend/src/routers/`: API endpoints
- `app-stack/frontend/src/features/`: Frontend features

## Example: Adding a Flink Job
1. Create job in `flink-stack/src/` (see `mart_requests_job.py`)
2. Ensure Kafka topic and Postgres table exist
3. Deploy via Flink UI or CLI

---

**For questions or unclear conventions, review stack-specific README files or ask for clarification.**
