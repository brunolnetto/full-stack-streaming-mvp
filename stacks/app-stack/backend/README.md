# FastAPI Backend for Streaming Analytics

This service provides REST and WebSocket APIs for real-time analytics, integrating with Kafka (event streaming) and Postgres (data storage).

## Source Structure
- `src/routers/`: API endpoints (REST & WebSocket)
- `src/models/`: Data models for requests, health, Flink, etc.
- `src/services/`: Database logic
- `tests/`: Backend unit tests

## Healthcheck
- Endpoint: `/health`

## Developer Workflow
- Start with Docker Compose:
	```bash
	docker compose up -d --build
	```
- Or run manually:
	```bash
	uvicorn src.main:app --reload
	```

## Integration Points
- Kafka: Consumes/produces events for streaming jobs
- Postgres: Central data store for raw/aggregated data
- WebSocket: Real-time updates to frontend

## Testing
- Run tests in `tests/` with pytest:
	```bash
	pytest tests/
	```
