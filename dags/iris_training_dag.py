import sys
from datetime import datetime
from pathlib import Path

from airflow import DAG
from airflow.operators.python import PythonOperator

# Airflow запускает DAG из папки dags, поэтому добавляем корень проекта в импорт.
PROJECT_DIR = Path(__file__).resolve().parents[1]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from data import load_data, prepare_data
from test import test
from train import train


with DAG(
    dag_id="iris_training_pipeline",
    description="Pipeline for training a simple Iris classifier",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["iris", "mlops"],
) as dag:
    load_data_task = PythonOperator(
        task_id="load_data",
        python_callable=load_data,
    )

    prepare_data_task = PythonOperator(
        task_id="prepare_data",
        python_callable=prepare_data,
        op_args=["dataset/iris.csv"],
    )

    train_task = PythonOperator(
        task_id="train_model",
        python_callable=train,
        op_args=["dataset/iris_train.csv"],
    )

    test_task = PythonOperator(
        task_id="test_model",
        python_callable=test,
        op_args=["model.pkl", "dataset/iris_test.csv"],
    )

    load_data_task >> prepare_data_task >> train_task >> test_task
