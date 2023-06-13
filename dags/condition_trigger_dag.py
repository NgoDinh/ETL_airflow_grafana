from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.utils.task_group import TaskGroup

from random import uniform
from datetime import datetime

def _t1(ti):
    ti.xcom_push("my_key", value = 11)

def _check_condition(ti):
    value = ti.xcom_pull(key = "my_key", task_ids = "t1")
    print('value')
    if value >= 10:
        return "t2"
    else:
        return "t3"

with DAG("condition_trigger_dag", start_date=datetime(2023,1,1), schedule_interval="@daily", catchup=False) as dag:
    t1 = PythonOperator(
        task_id = "t1",
        python_callable = _t1
    )

    check_condition = BranchPythonOperator(
        task_id = "check_condition",
        python_callable = _check_condition
    )

    t2 = BashOperator(
        task_id = "t2",
        bash_command = "echo 'execute t2'"
    )

    t3 = BashOperator(
        task_id = "t3",
        bash_command = "echo 'execute t3'"
    )

    t4 = BashOperator(
        task_id = "t4",
        bash_command = "echo 'execute t4'",
        trigger_rule = 'one_success'
    )

    t1 >> check_condition >> [t2, t3] >> t4