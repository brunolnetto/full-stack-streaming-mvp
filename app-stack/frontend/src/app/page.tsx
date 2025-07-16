"use client";
import { useWebSocket } from "../hooks/useWebSocket";
import RequestList from "../components/RequestList";

export default function Home() {
  // Use the Docker Compose service name for backend in the URL
  const wsUrl = "ws://backend:8000/ws/requests";
  const requests = useWebSocket(wsUrl);

  return (
    <main className="min-h-screen bg-gray-100 p-4">
      <h1 className="text-2xl font-bold mb-4">Live Requests Stream</h1>
      <RequestList requests={requests} />
    </main>
  );
}
