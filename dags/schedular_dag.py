from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime
from airflow.utils.dates import days_ago
import os
import sys

parent_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_folder)

from py_script.producer import main as staging_producer
from py_script.consumer import main as staging_consumer
from py_script.public_producer import main as public_producer
from py_script.public_consumer import main as public_cosnumer


def main():
    print("Veri Kaynağından Staging Topicine Veri Yazma İşlemi başaldı")
    staging_producer()
    print("Staging Topicten veritabanı staging katmanına Veri Yazma İşlemi başaldı")
    staging_consumer()

    public_producer()

    public_cosnumer()
    


with DAG(
    dag_id = "kafka",
    schedule_interval="@daily",
    start_date=days_ago(1),
    tags=['dags'],
) as dag:
    
    start = EmptyOperator(task_id='start')
    end = EmptyOperator(task_id='end')  
        
    main_task = PythonOperator(
        task_id=f"data_source_to_kafka_topic",
        provide_context=True,
        python_callable = main        
    )
    
    start >> main_task >> end