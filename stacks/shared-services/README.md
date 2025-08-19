# Shared Services

This stack provides shared infrastructure services for the project.

## Services
- **Postgres:** Main database for raw and aggregated data (http://localhost:5432)

## Usage
```bash
docker compose up -d
```

- Used by all other stacks for persistent storage. 