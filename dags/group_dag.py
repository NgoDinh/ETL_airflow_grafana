from airflow import DAG
from airflow.operators.subdag import SubDagOperator
from groups.group_downloads import download_task
from airflow.operators.bash import BashOperator

from datetime import datetime

with DAG(dag_id = "group_dag", start_date = datetime(2023,1,1), catchup=False, schedule_interval='@daily') as dag:
    args = {'start_date' : dag.start_date, "catchup" : dag.catchup, "schedule_interval" : dag.schedule_interval}

    downloads = download_task()
    check_file = BashOperator(
        task_id = "check_file",
        bash_command = "sleep 10"
    )

    downloads >> check_file