"use client";
import React, { createContext, useContext, ReactNode, useEffect, useState } from "react";
import { useRequestsStream, ConnectionState } from "../features/requests";
import type { Request } from "../types/requests";

interface StreamContextValue {
  requests: Request[];
  connectionState: ConnectionState;
  error: string | null;
}

const StreamContext = createContext<StreamContextValue | undefined>(undefined);

export const StreamProvider = ({ children }: { children: ReactNode }) => {
  const [wsUrl, setWsUrl] = useState<string | null>(null);

  useEffect(() => {
    const wsHost = window.location.hostname === "localhost" ? "localhost" : "backend";
    setWsUrl(`ws://${wsHost}:8000/ws/hits`);
  }, []);

  // Always call the hook, handle null/empty url inside the hook
  const { messages, connectionState, error } = useRequestsStream(wsUrl);
  const stream: StreamContextValue = { requests: messages, connectionState, error };

  return (
    <StreamContext.Provider value={stream}>
      {children}
    </StreamContext.Provider>
  );
};

export function useStream() {
  const context = useContext(StreamContext);
  if (!context) {
    throw new Error("useStream must be used within a StreamProvider");
  }
  return context;
} 