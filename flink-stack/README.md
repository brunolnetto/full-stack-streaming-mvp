# Flink Stack

This stack runs Apache Flink (JobManager and TaskManager) using a custom PyFlink image. Connects to the shared Docker network `livestream-net` and shared Postgres.

## Overview

The Flink stack includes:
- **JobManager**: Manages Flink jobs and coordinates task execution
- **TaskManager**: Executes the actual Flink tasks
- **Example Jobs**: Functional Flink streaming jobs for data processing

## Example Jobs

### 1. staging_requests_job.py
Processes web traffic events from Kafka and stores them in the processed_events table.

**Features:**
- Reads JSON events from Kafka topic
- Transforms and validates data
- Stores processed events in PostgreSQL (processed_events table)

### 2. mart_requests_job.py
Performs real-time aggregations on processed events with time windows.

**Features:**
- 5-minute tumbling windows
- Aggregates by host
- Stores aggregated results in PostgreSQL (processed_events_aggregated table)

### 3. simple_job.py
Simple data pipeline that converts events to JSON format.

**Features:**
- Reads from Kafka
- Converts events to JSON strings
- Stores in flink_results table

## Setup and Usage

### 1. Start the Flink Stack
```bash
docker compose up -d --build
```

### 2. Check Flink UI
Access the Flink web UI at: http://localhost:8081

### 3. Run Example Jobs

#### Option A: Manual Execution
```bash
# Connect to the taskmanager container
docker exec -it taskmanager bash

# Run the staging job
python3 /opt/src/staging_requests_job.py

# Run the mart job
python3 /opt/src/mart_requests_job.py

# Run the simple job
python3 /opt/src/simple_job.py
```

#### Option B: Using Hot Reload
```bash
# Start the hot-reload service (uncomment in docker-compose.yml)
docker compose up hot-reload
```

### 4. Generate Test Data
```bash
# Run the test data generator
python3 /opt/src/test_data_generator.py
```

## Environment Configuration

The jobs use environment variables defined in `flink-env.env`:

- `POSTGRES_URL`: PostgreSQL connection string
- `POSTGRES_USER`: PostgreSQL username
- `POSTGRES_PASSWORD`: PostgreSQL password
- `KAFKA_URL`: Kafka bootstrap servers
- `KAFKA_TOPIC`: Kafka topic name
- `KAFKA_GROUP`: Kafka consumer group
- `IP_CODING_KEY`: API key for geolocation service

## Database Schema

The following tables are created automatically:

- `flink_results`: General results table
- `processed_events`: Enriched web traffic events
- `processed_events_aggregated`: Host-based aggregations
- `processed_events_aggregated_source`: Host and referrer aggregations

## Troubleshooting

### Common Issues

1. **Job fails to start**: Check if Kafka and PostgreSQL are running
2. **Connection errors**: Verify network connectivity and credentials
3. **API rate limits**: The geolocation API has rate limits, consider using a paid key

### Logs
```bash
# View Flink logs
docker logs jobmanager
docker logs taskmanager

# View specific job logs in Flink UI
http://localhost:8081
```

## Development

### Adding New Jobs
1. Create a new Python file in `src/` with `_job.py` suffix
2. Follow the pattern of existing jobs
3. Use the provided environment variables for configuration

### Testing
- Use `test_data_generator.py` to generate sample data
- Monitor job execution in Flink UI
- Check PostgreSQL tables for results 