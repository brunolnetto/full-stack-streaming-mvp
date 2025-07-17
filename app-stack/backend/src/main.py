import os
import json
import time
import asyncio
from contextlib import asynccontextmanager
from datetime import datetime, timezone
import pytz

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from aiokafka.admin import AIOKafkaAdminClient, NewTopic
from starlette.middleware.base import BaseHTTPMiddleware

# Kafka constatns
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "raw_topic_requests")
KAFKA_AGG_TOPIC = os.getenv("KAFKA_AGG_TOPIC", "mart_topic_requests")

# Postgres database
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "hits")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}"

producer = None
active_connections = set()
kafka_consumer_task = None

# Get timezone from environment, default to UTC if not set
TIMEZONE = os.getenv("TZ", "UTC")
tz = pytz.timezone(TIMEZONE)

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
            print("Kafka message received:", data)  # <-- Debug print
            # Broadcast to all connected clients
            for ws in list(active_connections):
                try:
                    await ws.send_text(data)
                except Exception:
                    active_connections.remove(ws)
    finally:
        await consumer.stop()

@asynccontextmanager
async def lifespan(app: FastAPI):
    global producer, kafka_consumer_task
    # Ensure topics exist
    admin_client = AIOKafkaAdminClient(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await admin_client.start()
    try:
        existing_topics = await admin_client.list_topics()
        topics_to_create = []
        for topic in [KAFKA_TOPIC, KAFKA_AGG_TOPIC]:
            if topic not in existing_topics:
                topics_to_create.append(NewTopic(topic, num_partitions=1, replication_factor=1))
        if topics_to_create:
            await admin_client.create_topics(topics_to_create)
    finally:
        await admin_client.close()
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
        # Skip health and docs endpoints
        if route in [
            '/health', '/docs', '/openapi.json', '/redoc'
        ] or route.startswith('/docs'):
            return await call_next(request)
        # Use milliseconds for event_time
        event_time = datetime.now(tz).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        event = {
            "route": route,
            "event_time": event_time,
            "host": request.headers.get("host", ""),
            "user_agent": request.headers.get("user-agent", ""),
            "referer": request.headers.get("referer", ""),
            "ip": request.client.host if request.client else "",
            "headers": json.dumps(dict(request.headers))
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


@app.get("/hits")
def get_hits():
    """Fetch latest route hit counts from Postgres."""
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT route, num_hits, event_hour
            FROM mart_table_requests_hits
            ORDER BY event_hour DESC
        """))
        hits = [
            {
                "route": row[0],
                "num_hits": row[1],
                "event_hour": row[2].isoformat() if hasattr(row[2], "isoformat") else row[2]
            }
            for row in result
        ]
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