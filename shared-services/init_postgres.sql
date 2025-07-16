CREATE TABLE IF NOT EXISTS staging_table_requests (
    route VARCHAR,
    event_timestamp TIMESTAMP(3),
    host VARCHAR,
    user_agent VARCHAR,
    browser VARCHAR,
    os VARCHAR,
    session_id VARCHAR,
    accept_language VARCHAR,
    cookie VARCHAR,
    referer VARCHAR,
    device_type VARCHAR,
    is_bot BOOLEAN
);

CREATE TABLE IF NOT EXISTS mart_table_requests_hits (
    route VARCHAR,
    num_hits INTEGER,
    event_hour TIMESTAMP(3)
);
