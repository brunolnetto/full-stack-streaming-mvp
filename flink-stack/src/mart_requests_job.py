import os
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import EnvironmentSettings, DataTypes, StreamTableEnvironment
from pyflink.table.expressions import lit, col
from pyflink.table.window import Tumble

entity = 'requests'
num_workers = 1
checkpoint_interval_seconds = 10

tumbling_interval_value = 30  # seconds
latency_interval_value = 15   # seconds

def create_staging_requests_source_kafka(t_env):
    table_name = "staging_stream_requests"
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
            'properties.bootstrap.servers' = '{os.environ.get('KAFKA_URL')}',
            'properties.group.id' = '{os.environ.get('KAFKA_GROUP')}',
            'topic' = 'staging_topic_requests',
            'properties.allow.auto.create.topics' = 'true',
            'scan.startup.mode' = 'earliest-offset',
            'format' = 'json'
        );
    """
    t_env.execute_sql(source_ddl)
    return table_name

def create_mart_requests_sink_postgres(t_env):
    table_name = f'mart_table_{entity}_hits'
    sink_ddl = f"""
        CREATE TABLE {table_name} (
            event_hour TIMESTAMP(3),
            route VARCHAR,
            num_hits BIGINT
        ) WITH (
            'connector' = 'jdbc',
            'url' = '{os.environ.get("POSTGRES_URL")}',
            'table-name' = '{table_name}',
            'username' = '{os.environ.get("POSTGRES_USER", "postgres")}',
            'password' = '{os.environ.get("POSTGRES_PASSWORD", "postgres")}',
            'driver' = 'org.postgresql.Driver'
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

        # ORM-style Table API aggregation
        t_env.from_path(source_table) \
            .window(
                Tumble.over(lit(tumbling_interval_value).seconds).on(col("event_timestamp")).alias("w")
            ).group_by(
                col("w"),
                col("route")
            ).select(
                col("w").start.alias("event_hour"),
                col("route"),
                col("route").count.alias("num_hits")
            ).execute_insert(sink_table).wait()

    except Exception as e:
        print("Writing records from Kafka to JDBC failed:", str(e))

if __name__ == '__main__':
    main()