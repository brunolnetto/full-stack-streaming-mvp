import os
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import EnvironmentSettings, DataTypes, StreamTableEnvironment
from pyflink.table.expressions import lit, col
from pyflink.table.window import Tumble

# Environment variables (move to header)
KAFKA_URL = os.environ.get('KAFKA_URL')
KAFKA_GROUP = os.environ.get('KAFKA_GROUP')
POSTGRES_URL = os.environ.get('POSTGRES_URL')
POSTGRES_USER = os.environ.get('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'postgres')

entity = 'requests'
num_workers = 1
checkpoint_interval_seconds = 10

tumbling_interval_value = 30  # seconds
latency_interval_value = 15   # seconds

def create_staging_requests_source_kafka(t_env):
    table_name = "staging_stream_requests"
    topic_name = "staging_topic_requests"
    pattern = "yyyy-MM-dd''T''HH:mm:ss.SSS''Z''"
    source_ddl = f"""
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
            event_timestamp TIMESTAMP(3),
            WATERMARK FOR event_timestamp AS event_timestamp - INTERVAL '{latency_interval_value}' SECOND
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

def create_mart_requests_sink_postgres(t_env):
    table_name=f'mart_table_{entity}_hits'
    sink_ddl = f"""
        CREATE TABLE {table_name} (
            event_hour TIMESTAMP(3),
            route VARCHAR,
            num_hits BIGINT
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

def create_mart_requests_sink_kafka(t_env):
    table_name=f'mart_stream_{entity}'
    topic_name=f'mart_topic_{entity}'
    
    sink_ddl = f"""
        CREATE TABLE {table_name} (
            event_hour TIMESTAMP(3),
            route VARCHAR,
            num_hits BIGINT
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
    t_env.execute_sql(sink_ddl)
    return table_name

def create_mart_requests_by_dims_sink_postgres(t_env):
    table_name=f'mart_table_{entity}_hits_by_dims'
    
    sink_ddl = f"""
        CREATE TABLE {table_name} (
            event_hour TIMESTAMP(3),
            os VARCHAR,
            browser VARCHAR,
            device_type VARCHAR,
            num_hits BIGINT
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

def create_mart_requests_by_dims_sink_kafka(t_env):
    table_name=f'mart_stream_{entity}_by_dims'
    topic_name=f'mart_topic_{entity}_by_dims'

    sink_ddl = f"""
        CREATE TABLE {table_name} (
            event_hour TIMESTAMP(3),
            os VARCHAR,
            browser VARCHAR,
            device_type VARCHAR,
            num_hits BIGINT
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
    t_env.execute_sql(sink_ddl)
    return table_name

def main():
    # Set up the execution environment
    env = StreamExecutionEnvironment.get_execution_environment()
    env.enable_checkpointing(checkpoint_interval_seconds * 1000)
    env.set_parallelism(num_workers)

    # Set up the table environment
    settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
    t_env = StreamTableEnvironment.create(env, environment_settings=settings)

    try:
        # Create Kafka source and Postgres sink
        source_table = create_staging_requests_source_kafka(t_env)
        sink_table = create_mart_requests_sink_postgres(t_env)
        kafka_sink_table = create_mart_requests_sink_kafka(t_env)

        # Additional aggregation by os, browser, device_type
        sink_table_by_dims = create_mart_requests_by_dims_sink_postgres(t_env)
        kafka_sink_table_by_dims = create_mart_requests_by_dims_sink_kafka(t_env)

        # SQL aggregation by route
        agg_sql = f'''
            SELECT
                TUMBLE_START(event_timestamp, INTERVAL '{tumbling_interval_value}' SECOND) AS event_hour,
                route,
                COUNT(route) AS num_hits
            FROM {source_table}
            GROUP BY
                TUMBLE(event_timestamp, INTERVAL '{tumbling_interval_value}' SECOND),
                route
        '''
        t_env.execute_sql(f"CREATE TEMPORARY VIEW agg_by_route_view AS {agg_sql}")
        t_env.execute_sql(f"INSERT INTO {sink_table} SELECT * FROM agg_by_route_view")
        t_env.execute_sql(f"INSERT INTO {kafka_sink_table} SELECT * FROM agg_by_route_view")

        # SQL aggregation by os, browser, device_type
        agg_by_dims_sql = f'''
            SELECT
                TUMBLE_START(event_timestamp, INTERVAL '{tumbling_interval_value}' SECOND) AS event_hour,
                os,
                browser,
                device_type,
                COUNT(route) AS num_hits
            FROM {source_table}
            GROUP BY
                TUMBLE(event_timestamp, INTERVAL '{tumbling_interval_value}' SECOND),
                os,
                browser,
                device_type
        '''
        t_env.execute_sql(f"CREATE TEMPORARY VIEW agg_by_dims_view AS {agg_by_dims_sql}")
        t_env.execute_sql(f"INSERT INTO {sink_table_by_dims} SELECT * FROM agg_by_dims_view")
        t_env.execute_sql(f"INSERT INTO {kafka_sink_table_by_dims} SELECT * FROM agg_by_dims_view").wait()

    except Exception as e:
        print("Writing records from Kafka to JDBC/Kafka failed:", str(e))

if __name__ == '__main__':
    main()