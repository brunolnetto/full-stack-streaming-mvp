"use client";
import { useEffect, useRef, useState, useCallback } from "react";
import type { Request } from "../../types/requests";

export type ConnectionState = "connecting" | "open" | "closed" | "error" | "reconnecting";

export function useRequestsStream(url: string | null, options?: { retryInterval?: number; maxRetries?: number }) {
  const [messages, setMessages] = useState<Request[]>([]);
  const [connectionState, setConnectionState] = useState<ConnectionState>("connecting");
  const [error, setError] = useState<string | null>(null);
  const ws = useRef<WebSocket | null>(null);
  const retryCount = useRef(0);

  const connect = useCallback(() => {
    if (!url) {
      setConnectionState("connecting");
      return;
    }
    setConnectionState("connecting");
    setError(null);
    ws.current = new WebSocket(url);

    ws.current.onopen = () => {
      setConnectionState("open");
      retryCount.current = 0;
    };

    ws.current.onmessage = (event) => {
      setMessages((prev) => [...prev, JSON.parse(event.data)]);
    };

    ws.current.onerror = (e) => {
      setConnectionState("error");
      setError("WebSocket error");
    };

    ws.current.onclose = () => {
      setConnectionState("closed");
      if (
        options?.maxRetries === undefined ||
        retryCount.current < options.maxRetries
      ) {
        setConnectionState("reconnecting");
        retryCount.current += 1;
        setTimeout(connect, options?.retryInterval || 2000);
      }
    };
  }, [url, options?.retryInterval, options?.maxRetries]);

  useEffect(() => {
    connect();
    return () => {
      ws.current && ws.current.close();
    };
  }, [connect]);

  return { messages, connectionState, error };
} 