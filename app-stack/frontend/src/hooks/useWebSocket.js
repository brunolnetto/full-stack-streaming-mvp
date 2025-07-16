import { useEffect, useRef, useState } from "react";

export function useWebSocket(url) {
  const [messages, setMessages] = useState([]);
  const ws = useRef(null);

  useEffect(() => {
    ws.current = new WebSocket(url);

    ws.current.onmessage = (event) => {
      setMessages((prev) => [...prev, JSON.parse(event.data)]);
    };

    return () => {
      ws.current && ws.current.close();
    };
  }, [url]);

  return messages;
} 