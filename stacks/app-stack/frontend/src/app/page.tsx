"use client";
import { RequestList } from "../features/requests";
import { useStream } from "../context/StreamProvider";
import { useState } from "react";

export default function Home() {
  const { requests, connectionState, error } = useStream();

  const isLoading = connectionState === "connecting" || connectionState === "reconnecting";
  const isConnected = connectionState === "open";
  const isError = connectionState === "error";
  const hasData = requests && requests.length > 0;

  // Filter state
  const [routeFilter, setRouteFilter] = useState("");
  const [browserFilter, setBrowserFilter] = useState("");

  // Filtered requests
  const filteredRequests = requests.filter((req) => {
    const routeMatch = routeFilter ? String(req.route || "").includes(routeFilter) : true;
    const browserMatch = browserFilter ? String(req.browser || "").toLowerCase().includes(browserFilter.toLowerCase()) : true;
    return routeMatch && browserMatch;
  });

  return (
    <main className="min-h-screen bg-gray-100 p-4">
      <h1 className="text-2xl font-bold mb-4">Live Requests Stream</h1>
      <div className="mb-2 flex items-center gap-4">
        <span className="text-sm text-gray-600">Connection: <b>{connectionState}</b></span>
        {isLoading && <span className="text-sm text-blue-600 animate-pulse">Connecting...</span>}
        {isConnected && <span className="text-sm text-green-600">Live</span>}
        {isError && <span className="text-sm text-red-600">Error: {error}</span>}
      </div>
      <div className="mb-4 flex gap-4 items-center">
        <input
          type="text"
          placeholder="Filter by route..."
          value={routeFilter}
          onChange={(e) => setRouteFilter(e.target.value)}
          className="border px-2 py-1 rounded text-sm"
        />
        <input
          type="text"
          placeholder="Filter by browser..."
          value={browserFilter}
          onChange={(e) => setBrowserFilter(e.target.value)}
          className="border px-2 py-1 rounded text-sm"
        />
      </div>
      {!hasData && !isLoading && !isError && (
        <div className="text-gray-500 mt-8 text-center">No data yet. Waiting for live events...</div>
      )}
      {hasData && (
        <div className="overflow-x-auto mt-4">
          <table className="min-w-full bg-white rounded shadow">
            <thead>
              <tr>
                {Object.keys(filteredRequests[0] || requests[0]).map((key) => (
                  <th key={key} className="px-2 py-1 text-xs font-semibold text-gray-700 bg-gray-100 border-b">{key}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {filteredRequests.map((req, idx) => (
                <tr key={idx} className="border-b hover:bg-gray-50">
                  {Object.values(req).map((val, i) => (
                    <td key={i} className="px-2 py-1 text-xs font-mono text-gray-800">{String(val)}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
          {filteredRequests.length === 0 && (
            <div className="text-gray-500 mt-8 text-center">No results match your filters.</div>
          )}
        </div>
      )}
    </main>
  );
}
