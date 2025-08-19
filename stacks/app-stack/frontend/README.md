yarn dev

# Next.js Frontend for Streaming Analytics

This dashboard visualizes real-time analytics from the backend, integrating with WebSocket and REST APIs.

## Source Structure
- `src/features/`: Feature modules (e.g., requests)
- `src/context/`: React context providers (e.g., `StreamProvider.tsx`)
- `src/types/`: TypeScript types
- `src/app/api/health/route.ts`: Healthcheck endpoint

## Healthcheck
- Endpoint: `/api/health`

## Developer Workflow
- Start the development server:
	```bash
	npm run dev
	```
- Access at [http://localhost:3000](http://localhost:3000)

## Integration Points
- WebSocket: Receives real-time updates from backend
- REST API: Fetches analytics data

## Feature Modules
- Example: `src/features/requests/` for request stream visualization

---

For more details, see the main project README or ask for conventions.
