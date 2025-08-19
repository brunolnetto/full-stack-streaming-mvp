# Kafka Stack

This stack provides Zookeeper, Kafka, and Kafka-UI for the project. Connects to the shared Docker network.

## Services
- **Kafka:** Main event streaming platform
- **Zookeeper:** Kafka coordination
- **Kafka-UI:** Web UI for managing topics (http://localhost:8080)

## Usage
```bash
docker compose up -d
``` 