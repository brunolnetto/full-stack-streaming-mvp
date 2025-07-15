import os
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import EnvironmentSettings, StreamTableEnvironment, DataTypes
from pyflink.table.expressions import lit, col
from pyflink.table.window import Tumble

def create_mart_source_postgres(t_env):
    table_name = "processed_events_source"
    source_ddl = f"""
        CREATE TABLE {table_name} (
            ip VARCHAR,
            event_timestamp TIMESTAMP(3),
            referrer VARCHAR,
            host VARCHAR,
            url VARCHAR,
            geodata VARCHAR,
            WATERMARK FOR event_timestamp AS event_timestamp - INTERVAL '15' SECOND
        ) WITH (
            'connector' = 'jdbc',
            'url' = '{os.environ.get("POSTGRES_URL")}',
            'table-name' = 'processed_events',
            'username' = '{os.environ.get("POSTGRES_USER", "postgres")}',
            'password' = '{os.environ.get("POSTGRES_PASSWORD", "postgres")}',
            'driver' = 'org.postgresql.Driver'
        );
    """
    t_env.execute_sql(source_ddl)
    return table_name

def create_mart_sink_postgres(t_env):
    table_name = 'processed_events_aggregated'
    sink_ddl = f"""
        CREATE TABLE {table_name} (
            event_hour TIMESTAMP(3),
            host VARCHAR,
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
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)
    settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
    t_env = StreamTableEnvironment.create(env, environment_settings=settings)
    try:
        source_table = create_mart_source_postgres(t_env)
        sink_table = create_mart_sink_postgres(t_env)
        
        # Create a windowed aggregation
        t_env.from_path(source_table)\
            .window(
                Tumble.over(lit(5).minutes).on(col("event_timestamp")).alias("w")
            ).group_by(
                col("w"),
                col("host")
            ) \
            .select(
                col("w").start.alias("event_hour"),
                col("host"),
                col("host").count.alias("num_hits")
            ) \
            .execute_insert(sink_table).wait()
    except Exception as e:
        print(f"Mart job failed: {e}")
        raise

if __name__ == '__main__':
    main() 