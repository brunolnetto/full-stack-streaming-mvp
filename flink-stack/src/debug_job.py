import os
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import EnvironmentSettings, StreamTableEnvironment, DataTypes

def create_simple_source_kafka(t_env):
    table_name = "simple_events"
    pattern = "yyyy-MM-dd''T''HH:mm:ss.SSS''Z''"
    source_ddl = f"""
        CREATE TABLE {table_name} (
            url VARCHAR,
            referrer VARCHAR,
            user_agent VARCHAR,
            host VARCHAR,
            ip VARCHAR,
            headers VARCHAR,
            event_time VARCHAR,
            event_timestamp AS TO_TIMESTAMP(event_time, '{pattern}')
        ) WITH (
            'connector' = 'kafka',
            'properties.bootstrap.servers' = '{os.environ.get('KAFKA_URL', 'kafka:9092')}',
            'topic' = '{os.environ.get('KAFKA_TOPIC', 'input_topic')}',
            'properties.group.id' = '{os.environ.get('KAFKA_GROUP', 'flink-group')}',
            'scan.startup.mode' = 'earliest-offset',
            'properties.auto.offset.reset' = 'earliest',
            'format' = 'json'
        );
    """
    t_env.execute_sql(source_ddl)
    return table_name

def create_simple_sink_postgres(t_env):
    table_name = 'flink_results'
    sink_ddl = f"""
        CREATE TABLE {table_name} (
            data VARCHAR
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
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)
    settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
    t_env = StreamTableEnvironment.create(env, environment_settings=settings)
    try:
        source_table = create_simple_source_kafka(t_env)
        sink_table = create_simple_sink_postgres(t_env)
        
        # Simple transformation: convert event to JSON string
        t_env.execute_sql(f"""
            INSERT INTO {sink_table}
            SELECT 
                CONCAT('{{"url":"', url, '","host":"', host, '","ip":"', ip, '","timestamp":"', CAST(event_timestamp AS STRING), '"}}') as data
            FROM {source_table}
        """).wait()
        
        print("Simple job submitted successfully!")
    except Exception as e:
        print(f"Simple job failed: {e}")
        raise

if __name__ == '__main__':
    main() 