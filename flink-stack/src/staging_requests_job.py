import os
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import EnvironmentSettings, StreamTableEnvironment
from pyflink.table.udf import udf
from pyflink.table import DataTypes

import json

ENTITY = 'requests'

NUM_WORKERS = 1
CHECKPOINT_INTERVAL_SECONDS = 10

LATENCY_INTERVAL_VALUE = '15'
LATENCY_INTERVAL_GRAIN = 'SECOND'

TUMBLING_INTERVAL_VALUE = '5'
TUMBLING_INTERVAL_GRAIN = 'MINUTE'

KAFKA_URL = os.environ.get('KAFKA_URL')
KAFKA_GROUP = os.environ.get('KAFKA_GROUP')

POSTGRES_URL = os.environ.get('POSTGRES_URL')
POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')

# UDFs for richer extraction
@udf(result_type=DataTypes.STRING())
def extract_browser(user_agent: str) -> str:
    if not user_agent:
        return 'Unknown'
    if 'Chrome' in user_agent:
        return 'Chrome'
    if 'Firefox' in user_agent:
        return 'Firefox'
    if 'Safari' in user_agent and 'Chrome' not in user_agent:
        return 'Safari'
    if 'Edge' in user_agent:
        return 'Edge'
    if 'MSIE' in user_agent or 'Trident' in user_agent:
        return 'IE'
    return 'Other'

@udf(result_type=DataTypes.STRING())
def extract_os(user_agent: str) -> str:
    if not user_agent:
        return 'Unknown'
    if 'Windows' in user_agent:
        return 'Windows'
    if 'Mac OS X' in user_agent:
        return 'MacOS'
    if 'Linux' in user_agent:
        return 'Linux'
    if 'Android' in user_agent:
        return 'Android'
    if 'iPhone' in user_agent or 'iPad' in user_agent:
        return 'iOS'
    return 'Other'

@udf(result_type=DataTypes.STRING())
def extract_session_id(headers: str) -> str:
    if not headers:
        return ''
    try:
        h = json.loads(headers)
        cookie = h.get('cookie', '')
        if not cookie:
            return ''
        # Extract session id from cookie string
        import re
        match = re.search(r'session=([^;]+)', cookie)
        if match:
            return match.group(1)
        return ''
    except Exception:
        return ''

@udf(result_type=DataTypes.STRING())
def extract_accept_language(headers: str) -> str:
    if not headers:
        return ''
    try:
        h = json.loads(headers)
        return h.get('accept-language', '')
    except Exception:
        return ''

@udf(result_type=DataTypes.STRING())
def extract_cookie(headers: str) -> str:
    if not headers:
        return ''
    try:
        h = json.loads(headers)
        return h.get('cookie', '')
    except Exception:
        return ''

@udf(result_type=DataTypes.STRING())
def extract_referer(headers: str) -> str:
    if not headers:
        return ''
    try:
        h = json.loads(headers)
        return h.get('referer', '')
    except Exception:
        return ''

@udf(result_type=DataTypes.STRING())
def extract_device_type(user_agent: str) -> str:
    if not user_agent:
        return 'Unknown'
    if 'Mobile' in user_agent or 'Android' in user_agent or 'iPhone' in user_agent:
        return 'Mobile'
    if 'iPad' in user_agent or 'Tablet' in user_agent:
        return 'Tablet'
    return 'Desktop'

@udf(result_type=DataTypes.BOOLEAN())
def extract_is_bot(user_agent: str) -> bool:
    if not user_agent:
        return False
    bot_keywords = ['bot', 'crawl', 'spider', 'slurp', 'bingpreview', 'mediapartners']
    ua = user_agent.lower()
    return any(keyword in ua for keyword in bot_keywords)

def create_raw_requests_source_kafka(t_env):
    table_name = f'raw_stream_{ENTITY}'
    topic_name = f'raw_topic_{ENTITY}'
    pattern = "yyyy-MM-dd''T''HH:mm:ss.SSS''Z''"
    source_ddl = f"""
        CREATE TABLE {table_name} (
            route VARCHAR,
            event_time VARCHAR,
            host VARCHAR,
            user_agent VARCHAR,
            referer VARCHAR,
            ip VARCHAR,
            headers VARCHAR,
            event_timestamp AS TO_TIMESTAMP(event_time, '{pattern}')
        ) WITH (
            'connector' = 'kafka',
            'properties.bootstrap.servers' = '{KAFKA_URL}',
            'properties.group.id' = '{KAFKA_GROUP}',
            'topic' = '{topic_name}',
            'properties.allow.auto.create.topics' = 'true',
            'scan.startup.mode' = 'earliest-offset',
            'format' = 'json'
        );
    """
    t_env.execute_sql(source_ddl)
    return table_name

def create_staging_requests_sink_kafka(t_env):
    table_name = f"staging_stream_{ENTITY}"
    topic_name = f"staging_topic_{ENTITY}"
    sink_ddl = f"""
        CREATE TABLE {table_name} (
            route VARCHAR,
            event_time VARCHAR,
            host VARCHAR,
            user_agent VARCHAR,
            browser VARCHAR,
            os VARCHAR,
            session_id VARCHAR,
            accept_language VARCHAR,
            cookie VARCHAR,
            referer VARCHAR,
            device_type VARCHAR,
            is_bot BOOLEAN,
            event_timestamp TIMESTAMP(3)
        ) WITH (
            'connector' = 'kafka',
            'topic' = '{topic_name}',
            'properties.bootstrap.servers' = '{KAFKA_URL}',
            'format' = 'json'
        );
    """
    t_env.execute_sql(sink_ddl)
    return table_name

def create_staging_requests_sink_postgres(t_env):
    table_name = f'staging_table_{ENTITY}'
    sink_ddl = f"""
        CREATE TABLE {table_name} (
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
        ) WITH (
            'connector' = 'jdbc',
            'url' = '{POSTGRES_URL}',
            'table-name' = '{table_name}',
            'username' = '{POSTGRES_USER}',
            'password' = '{POSTGRES_PASSWORD}',
            'driver' = 'org.postgresql.Driver'
        );
    """
    t_env.execute_sql(sink_ddl)
    return table_name

def main():
    settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(NUM_WORKERS)

    env.enable_checkpointing(int(CHECKPOINT_INTERVAL_SECONDS) * 1000)

    t_env = StreamTableEnvironment.create(env, environment_settings=settings)
    try:
        # Create source
        source_table = create_raw_requests_source_kafka(t_env)   

        # Create sinks
        kafka_sink_table = create_staging_requests_sink_kafka(t_env)
        pg_sink_table = create_staging_requests_sink_postgres(t_env)

        t_env.create_temporary_function('extract_browser', extract_browser)
        t_env.create_temporary_function('extract_os', extract_os)
        t_env.create_temporary_function('extract_session_id', extract_session_id)
        t_env.create_temporary_function('extract_accept_language', extract_accept_language)
        t_env.create_temporary_function('extract_cookie', extract_cookie)
        t_env.create_temporary_function('extract_referer', extract_referer)
        t_env.create_temporary_function('extract_device_type', extract_device_type)
        t_env.create_temporary_function('extract_is_bot', extract_is_bot)

        # Write to staging_requests Kafka topic
        kafka_query=f"""
            INSERT INTO {kafka_sink_table}
            SELECT 
                route, event_time, host, user_agent,
                extract_browser(user_agent),
                extract_os(user_agent),
                extract_session_id(headers),
                extract_accept_language(headers),
                extract_cookie(headers),
                extract_referer(headers),
                extract_device_type(user_agent),
                extract_is_bot(user_agent),
                event_timestamp
            FROM {source_table}
        """
        t_env.execute_sql(kafka_query)

        # Write to processed_events Postgres table
        postgres_query=f"""
            INSERT INTO {pg_sink_table}
            SELECT 
                route, event_timestamp, host, user_agent,
                extract_browser(user_agent),
                extract_os(user_agent),
                extract_session_id(headers),
                extract_accept_language(headers),
                extract_cookie(headers),
                extract_referer(headers),
                extract_device_type(user_agent),
                extract_is_bot(user_agent)
            FROM {source_table}
        """

        t_env.execute_sql(postgres_query).wait()
    except Exception as e:
        print(f"Staging job failed: {e}")
        raise

if __name__ == '__main__':
    main() 