import os
from datetime import datetime
from airflow import DAG

from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from ingest_scripts import ingest_callable


AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow")
PG_PORT =  os.getenv('PG_PORT') 
PG_HOST =  os.getenv('PG_HOST') 
PG_USER =  os.getenv('PG_USER') 
PG_PASSWORD =  os.getenv('PG_PASSWORD') 
PG_DATABASE =  os.getenv('PG_DATABASE') 

URL_PREFIX = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow'
URL = URL_PREFIX + '/yellow_tripdata_{{ execution_date.strftime(\'%Y-%m\') }}.csv.gz'
OUTPUT_FILE = AIRFLOW_HOME + '/output_{{ execution_date.strftime(\'%Y-%m\') }}.csv.gz'
TABLE_NAME = 'yellow_taxi_{{ execution_date.strftime(\'%Y-%m\') }}'

local_workflow = DAG(
    dag_id="a_local_workflow",
    schedule_interval="0 6 2 * *",
    start_date=datetime(2021, 1, 1),
    end_date=datetime(2021, 3, 1),
    catchup=True
)

with local_workflow:

    task1 = BashOperator(
        task_id="wget_data",
        bash_command=f"curl -sSL {URL} > {OUTPUT_FILE}"
    )

    task2 = BashOperator(
        task_id="unzip_data",
        bash_command=f"gunzip {OUTPUT_FILE}"
    )

    task3 = PythonOperator(
        task_id="ingest_data",
        python_callable=ingest_callable,
        op_kwargs={
            "user": PG_USER,
            "password": PG_PASSWORD,
            "host": PG_HOST,
            "port": PG_PORT,
            "db": PG_DATABASE,
            "table_name": TABLE_NAME,
            "csv_file": OUTPUT_FILE,
            "execution_date": "{{ execution_date }}"
        }
    )

    task1 >> task2 >> task3
# [END airflow_local_workflow]