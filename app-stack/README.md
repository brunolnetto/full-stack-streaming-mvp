# App Stack

This stack contains the FastAPI backend and Next.js frontend. Connects to the shared Docker network and shared Postgres.

## Services
- **Frontend:** Next.js (http://localhost:3000)
- **Backend:** FastAPI (http://localhost:8000)

## Usage
```bash
docker compose up -d --build
```

- Healthcheck endpoints:
  - Frontend: `/api/health`
  - Backend: `/health` 