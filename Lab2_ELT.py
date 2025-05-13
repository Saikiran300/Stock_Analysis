from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import timedelta
import pendulum
import os

DBT_PROJECT_DIR = "/opt/airflow/dags/dbt-test"
DBT_BIN = os.environ.get("DBT_BIN", "dbt")

default_args = {
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='lab2_elt_dbt',
    schedule_interval='0 1 * * *',
    start_date=pendulum.datetime(2025, 4, 20, 1, 0, tz='UTC'),
    catchup=False,
    default_args=default_args,
    description='Run dbt transforms, snapshots, and tests in sequence',
) as dag:

    run_dbt_models = BashOperator(
        task_id='dbt_run_models',
        bash_command="""
        bash -lc '
        cd /opt/airflow/dags/dbt-test && \
        dbt deps && \
        dbt run --models staging.stg_stock_prices+ analytics.ma_rsi analytics.rsi_heatmap analytics.rsi_distribution analytics.stock_summary --vars "{snowflake_database: 'COUNTRY'}"
        '
        """
    )

    run_dbt_snapshot = BashOperator(
        task_id='dbt_run_snapshots',
        bash_command=f"""
        bash -lc '
        cd {DBT_PROJECT_DIR} && \
        {DBT_BIN} snapshot
        '
        """
    )

    test_dbt = BashOperator(
        task_id='dbt_run_tests',
        bash_command=f"""
        bash -lc '
        cd {DBT_PROJECT_DIR} && \
        {DBT_BIN} test
        '
        """
    )

    run_dbt_models >> run_dbt_snapshot >> test_dbt
