# Frontend Rebuild Steps: Next.js + Tailwind + SOLID Architecture

---

## Purpose

This document provides **accountable, step-by-step instructions** for building a modern frontend that displays real-time streaming requests data. It is intended for developers, maintainers, and stakeholders who need to:
- Implement a frontend that visualizes and interacts with streaming data (e.g., live requests, analytics, dashboards)
- Follow best practices and SOLID architectural principles for maintainability and scalability
- Reproduce or audit the setup and architectural decisions for onboarding, compliance, or troubleshooting
- Iterate and update the process as the streaming frontend evolves

**Please update this file with any changes, decisions, or lessons learned during the development of the streaming requests dashboard and related features.**

---

## 1. **Backup the Old Frontend**

```bash
mv app-stack/frontend app-stack/frontend_backup
```

---

## 2. **Install Node.js and npm**
If not already installed:
```bash
sudo apt update
sudo apt install nodejs npm
```

---

## 3. **Scaffold a New Next.js App with Tailwind**

```bash
npx create-next-app@latest app-stack/frontend \
  --use-npm \
  --no-git \
  --eslint \
  --tailwind \
  --src-dir \
  --app \
  --import-alias "@/*" \
  --yes
```

- This creates a new Next.js app in `app-stack/frontend` with Tailwind CSS, ESLint, and a modern folder structure.

---

## 4. **Update Docker Compose**

Ensure your `app-stack/docker-compose.yml` has a service like:

```yaml
  frontend:
    build:
      context: ./frontend
    container_name: frontend
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    working_dir: /app
    command: npm run dev
    environment:
      - NODE_ENV=development
    depends_on:
      - backend
```

---

## 5. **Implement Minimal SOLID Streaming Frontend Architecture**

### 5.1. **Create the Recommended Folder Structure**

```
frontend/
  src/
    app/                # Next.js app directory (routing, pages)
    components/         # Reusable UI components (e.g., RequestList, StreamChart)
    features/           # Feature modules (e.g., requests, dashboard)
    hooks/              # Custom React hooks (e.g., useStream, useRequests)
    lib/                # API clients, WebSocket/SSE utilities
    styles/             # Tailwind/global styles
    context/            # React context providers (e.g., StreamProvider, optional)
    types/              # TypeScript types/interfaces (if using TS)
  public/               # Static assets
```

### 5.2. **Minimal Streaming Example Implementation Plan**

- **Create a custom WebSocket hook** in `src/hooks/useWebSocket.js` to connect to the backend WebSocket endpoint (e.g., `ws://backend:8000/ws/requests`).
- **Create a `RequestList` component** in `src/components/RequestList.jsx` to display the list of streaming requests.
- **Create a main streaming page** in `src/app/page.jsx` that uses the WebSocket hook and displays the live requests using the `RequestList` component.
- **(Optional)**: If global streaming state is needed, implement a context provider in `src/context/StreamProvider.jsx`.
- **Style the UI** using Tailwind CSS for a clean, modern look.
- **Follow SOLID principles**: Each component, hook, and context should have a single responsibility and be easily testable and extensible.

---

## 6. **Run the New Frontend**

From the project root:
```bash
docker-compose up --build
```

Visit [http://localhost:3000](http://localhost:3000) to see your new frontend.

---

## 7. **Next Steps**
- Implement streaming data fetching and visualization in `src/features/` and `src/app/`.
- Use context and hooks for state management and API integration.
- Follow SOLID principles for maintainable, scalable code.
- Continuously update this document as the streaming dashboard evolves.

---

**This process ensures a clean, modern, and accountable approach to building a streaming requests dashboard in the frontend.** 