# Flink Stack

This stack runs Apache Flink (JobManager and TaskManager) using a custom PyFlink image. Connects to the shared Docker network and shared Postgres.

## Overview

The Flink stack includes:
- **JobManager**: Manages Flink jobs and coordinates task execution
- **TaskManager**: Executes the actual Flink tasks
- **Example Jobs**: Functional Flink streaming jobs for data processing

## Example Jobs

### 1. staging_requests_job.py
Processes web traffic events from Kafka and stores them in the `staging_table_requests` table.

**Features:**
- Reads JSON events from Kafka topic
- Enriches and validates data
- Stores processed events in PostgreSQL (`staging_table_requests`)

### 2. mart_requests_job.py
Performs real-time aggregations on processed events with time windows.

**Features:**
- 5-minute tumbling windows
- Aggregates by route
- Stores aggregated results in PostgreSQL (`mart_table_requests_hits`)

## Setup and Usage

### 1. Start the Flink Stack
```bash
docker compose up -d --build
```

### 2. Check Flink UI
Access the Flink web UI at: http://localhost:8081

### 3. Run Example Jobs
```bash
# Connect to the taskmanager container
docker exec -it taskmanager bash
# Run the staging job
python3 /opt/src/staging_requests_job.py
# Run the mart job
python3 /opt/src/mart_requests_job.py
```

### 4. Generate Test Data
```bash
python3 /opt/src/test_data_generator.py
```

## Environment Configuration

Jobs use environment variables defined in `flink-env.env`.

## Database Schema

- `staging_table_requests`: Enriched web traffic events
- `mart_table_requests_hits`: Aggregated hits by route and time window

## Troubleshooting
- Ensure Kafka and Postgres are running before starting jobs
- View logs with `docker logs jobmanager` or `docker logs taskmanager`
- Monitor job execution in Flink UI 