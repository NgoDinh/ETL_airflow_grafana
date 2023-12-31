from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup

from random import uniform
from datetime import datetime

default_args = {
    'start_date': datetime(2023, 1, 1)
}

def _training_model(ti):
    accuracy = uniform(0.1, 10.0)
    print(f'model\'s accuracy: {accuracy}')
    ti.xcom_push(key = "accuracy", value = accuracy)

def _choose_best_model(ti):
    print('choose best model')
    accuracy_a = ti.xcom_pull(key = "accuracy", task_ids = 'processing_tasks.training_model_a')
    accuracy_b = ti.xcom_pull(key = "accuracy", task_ids = 'processing_tasks.training_model_b')
    accuracy_c = ti.xcom_pull(key = "accuracy", task_ids = 'processing_tasks.training_model_c')

    result = {"model a": accuracy_a, "model b": accuracy_b, "model c": accuracy_c}
    max_value = max(result, key=lambda x:result[x])
    print(result)
    print("Maximum value is of ",max_value)
    # print (accuracy_a, accuracy_b, accuracy_c)


with DAG('xcom_dag', schedule_interval='@daily', default_args=default_args, catchup=False) as dag:

    downloading_data = BashOperator(
        task_id='downloading_data',
        bash_command='sleep 3'
    )

    with TaskGroup('processing_tasks') as processing_tasks:
        training_model_a = PythonOperator(
            task_id='training_model_a',
            python_callable=_training_model
        )

        training_model_b = PythonOperator(
            task_id='training_model_b',
            python_callable=_training_model
        )

        training_model_c = PythonOperator(
            task_id='training_model_c',
            python_callable=_training_model
        )

    choose_model = PythonOperator(
        task_id='task_4',
        python_callable=_choose_best_model
    )

    downloading_data >> processing_tasks >> choose_model
