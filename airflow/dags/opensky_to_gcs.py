from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.exceptions import AirflowSkipException
from datetime import datetime
import pandas as pd
import requests
import time
import os

def fetch_opensky_data(**kwargs):
    # Looking back exactly 24 hours to find any recorded arrival
    now = int(time.time())
    begin = now - 90000  # ~25 hours ago
    end = now - 3600    # 1 hour ago
    
    user = "aronearokiasami@gmail.com"
    password = "Welcome123$"
    
    # Using reliable European hubs with high data coverage
    airports = ["EDDF", "LSZH", "EHAM", "EGLL"]
    data = None

    for apt in airports:
        print(f"Searching for arrivals at {apt}...")
        url = f"https://opensky-network.org/api/flights/arrival?airport={apt}&begin={begin}&end={end}"
        try:
            response = requests.get(url, auth=(user, password), timeout=30)
            if response.status_code == 200:
                temp_data = response.json()
                if temp_data and len(temp_data) > 0:
                    data = temp_data
                    print(f"✅ SUCCESS: Found {len(data)} flights at {apt}!")
                    break
            print(f"ℹ️ {apt} status: {response.status_code}")
        except Exception as e:
            print(f"⚠️ Error at {apt}: {e}")

    if data:
        df = pd.DataFrame(data)
        file_path = "/opt/airflow/data/test_upload.parquet"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        df.to_parquet(file_path)
        print(f"✅ File saved to shared volume: {file_path}")
    else:
        raise AirflowSkipException("❌ No data found. Try increasing the 'begin' time window.")

with DAG(
    "aerologix_opensky_to_gcs_v2", 
    start_date=datetime(2026, 3, 25), 
    schedule=None, 
    catchup=False
) as dag:

    extract_task = PythonOperator(
        task_id="extract_data", 
        python_callable=fetch_opensky_data
    )
    
    upload_task = LocalFilesystemToGCSOperator(
        task_id="upload_to_gcs",
        src="/opt/airflow/data/test_upload.parquet",
        dst="bronze/test_upload.parquet",
        bucket="aerologix-data-lake-aerologix-491105",
        gcp_conn_id=None 
    )

    extract_task >> upload_task