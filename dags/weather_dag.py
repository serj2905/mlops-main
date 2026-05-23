import sys
from datetime import datetime
from pathlib import Path
from airflow import DAG
from airflow.operators.python import PythonOperator

PROJECT_DIR = Path(__file__).resolve().parents[1]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from weather import save_weather


with DAG(
    dag_id="moscow_weather_pipeline",
    description="Collect weather in Moscow every minute",
    start_date=datetime(2026, 1, 1),
    schedule="* * * * *",
    catchup=False,
    tags=["weather", "openweathermap"],
) as dag:
    save_weather_task = PythonOperator(
        task_id="save_weather",
        python_callable=save_weather,
    )
