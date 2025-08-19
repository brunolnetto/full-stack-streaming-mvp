import os
from sqlalchemy import create_engine, text

POSTGRES_URL = os.getenv("POSTGRES_URL")
engine = create_engine(POSTGRES_URL, future=True)

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
    return hits 