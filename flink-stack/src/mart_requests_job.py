import os
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import EnvironmentSettings, StreamTableEnvironment

entity = 'requests'

tumbling_interval_value = '5'
tumbling_interval_grain = 'MINUTE'

kafka_url = os.environ.get('KAFKA_URL')
kafka_group = os.environ.get('KAFKA_GROUP')

postgres_url = os.environ.get("POSTGRES_URL")
postgres_user = os.environ.get("POSTGRES_USER")
postgres_password = os.environ.get("POSTGRES_PASSWORD")

def create_staging_requests_source_kafka(t_env):
    table_name = f"staging_stream_requests"
    topic_name = f"staging_topic_requests"
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
            event_timestamp TIMESTAMP(3)
        ) WITH (
            'connector' = 'kafka',
            'properties.bootstrap.servers' = '{kafka_url}',
            'properties.group.id' = '{kafka_group}',
            'topic' = '{topic_name}',
            'properties.allow.auto.create.topics' = 'true',
            'scan.startup.mode' = 'earliest-offset',
            'format' = 'json'
        );
    """
    t_env.execute_sql(source_ddl)
    return table_name

def create_mart_requests_sink_kafka(t_env):
    table_name = f"mart_stream_{entity}"
    topic_name = f"mart_topic_{entity}"
    sink_ddl = f"""
        CREATE TABLE {table_name} (
            event_hour TIMESTAMP(3),
            route VARCHAR,
            num_hits BIGINT
        ) WITH (
            'connector' = 'kafka',
            'topic' = '{topic_name}',
            'properties.bootstrap.servers' = '{kafka_url}',
            'properties.allow.auto.create.topics' = 'true',
            'format' = 'json'
        );
    """
    t_env.execute_sql(sink_ddl)
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
            'url' = '{postgres_url}',
            'table-name' = '{table_name}',
            'username' = '{postgres_user}',
            'password' = '{postgres_password}',
            'driver' = 'org.postgresql.Driver'
        );
    """
    t_env.execute_sql(sink_ddl)
    return table_name

def main():
    settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(3)
    t_env = StreamTableEnvironment.create(env, environment_settings=settings)
    try:
        # Create source
        source_table = create_staging_requests_source_kafka(t_env)

        env.enable_checkpointing(10 * 1000)
        
        # Create sinks
        kafka_sink_table = create_mart_requests_sink_kafka(t_env)
        pg_sink_table = create_mart_requests_sink_postgres(t_env)
        
        # Windowed aggregation query (by route)
        agg_query = f"""
            SELECT
                TUMBLE_START(
                    event_timestamp, 
                    INTERVAL '{tumbling_interval_value}' {tumbling_interval_grain}
                ) AS event_hour,
                route,
                COUNT(route) AS num_hits
            FROM {source_table}
            GROUP BY TUMBLE(event_timestamp, INTERVAL '{tumbling_interval_value}' {tumbling_interval_grain}), route
        """
        
        # Write to mart_requests Kafka topic
        t_env.execute_sql(f"INSERT INTO {kafka_sink_table} {agg_query}").wait()
        
        # Write to mart_table_requests_hits Postgres table
        t_env.execute_sql(f"INSERT INTO {pg_sink_table} {agg_query}").wait()
    except Exception as e:
        print(f"Mart job failed: {e}")
        raise

if __name__ == '__main__':
    main() 