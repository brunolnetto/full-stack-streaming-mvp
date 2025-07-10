import os
import json
import time
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from aiokafka import AIOKafkaProducer
from starlette.middleware.base import BaseHTTPMiddleware
from contextlib import asynccontextmanager

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "website-hits")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "hits")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}"

producer = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global producer
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()
    yield
    await producer.stop()

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

@app.get("/")
def root():
    return {"message": "Backend is running"} 