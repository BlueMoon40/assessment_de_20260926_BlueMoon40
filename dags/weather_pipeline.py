from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

import sys

sys.path.insert(0, "/opt/airflow/ingestion")

from weather_api import fetch_daily
from load import load_data

def load_from_xcom(**context):
    data_records = context["ti"].xcom_pull(task_ids="extract_weather")
    load_data(data_records)


with DAG(
    dag_id="weather_pipeline",
    start_date=datetime(2026, 8, 27),
    schedule="@daily",
    catchup=False,
    tags=["weather", "assessment"],
) as dag:

    extract = PythonOperator(
        task_id="extract_weather",
        python_callable=fetch_daily,
        op_kwargs={
            "logical_date": "{{ ds }}"
        },
    )

    load = PythonOperator(
        task_id="load_weather",
        python_callable=load_from_xcom,
    )

    dbt_run = BashOperator(
    task_id="dbt_run",
    bash_command="cd /opt/airflow/dbt && dbt run",
)
    dbt_test = BashOperator(
    task_id="dbt_test",
    bash_command="cd /opt/airflow/dbt && dbt test",
)

    extract >> load >> dbt_run >> dbt_test