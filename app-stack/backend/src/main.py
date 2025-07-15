import os
import json
import time
import asyncio
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from starlette.middleware.base import BaseHTTPMiddleware
from contextlib import asynccontextmanager

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "website-hits")
KAFKA_AGG_TOPIC = os.getenv("KAFKA_AGG_TOPIC", "route-hit-counts")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "hits")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}"

producer = None
active_connections = set()
kafka_consumer_task = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global producer, kafka_consumer_task
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()
    kafka_consumer_task = asyncio.create_task(kafka_to_websockets())
    yield
    await producer.stop()
    kafka_consumer_task.cancel()
    try:
        await kafka_consumer_task
    except asyncio.CancelledError:
        pass

app = FastAPI(lifespan=lifespan)

# SQLAlchemy setup
engine = create_engine(POSTGRES_URL, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class KafkaMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        global producer
        route = request.url.path
        event = {
            "timestamp": int(time.time()),
            "route": route
        }
        if producer:
            await producer.send_and_wait(KAFKA_TOPIC, json.dumps(event).encode())
        response = await call_next(request)
        return response

app.add_middleware(KafkaMiddleware)

@app.websocket("/ws/hits")
async def websocket_hits(websocket: WebSocket):
    await websocket.accept()
    active_connections.add(websocket)
    try:
        while True:
            await asyncio.sleep(3600)  # Keep connection open
    except WebSocketDisconnect:
        active_connections.remove(websocket)

async def kafka_to_websockets():
    consumer = AIOKafkaConsumer(
        KAFKA_AGG_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id="websocket-push"
    )
    await consumer.start()
    try:
        async for msg in consumer:
            data = msg.value.decode()
            # Broadcast to all connected clients
            for ws in list(active_connections):
                try:
                    await ws.send_text(data)
                except Exception:
                    active_connections.remove(ws)
    finally:
        await consumer.stop()

@app.get("/hits")
def get_hits():
    """Fetch latest route hit counts from Postgres."""
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT route, count
            FROM route_hit_counts
            WHERE window_end = (SELECT MAX(window_end) FROM route_hit_counts)
            ORDER BY count DESC
        """))
        hits = [{"route": row[0], "count": row[1]} for row in result]
    return JSONResponse(content=hits)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/sample")
def sample():
    return {"message": "This is a sample backend response"}

@app.get("/")
def root():
    return {"message": "Backend is running"} 