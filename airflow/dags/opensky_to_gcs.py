from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from datetime import datetime
import pandas as pd
import requests
import time
import os

# --- SETTINGS ---
SHARED_PATH = "/opt/airflow/data/test_upload.parquet"


def fetch_opensky_data(**kwargs):
    # THE "FREE TIER" SWEET SPOT: 
    # Must be less than 7200 seconds (2 hours) ago.
    now = int(time.time())
    begin = now - 5400  # 90 minutes ago
    end = now - 600     # 10 minutes ago
    
    user = "aronearokiasami@gmail.com"
    password = "Welcome123$"
    
    # European hubs are in peak morning arrival mode right now (UTC 06:00+)
    airports = ["EGLL", "EDDF", "EHAM", "LFPG", "EDDM"]
    data = None

    for apt in airports:
        print(f"📡 Requesting LIVE arrivals for {apt} (Window: last 90 mins)...")
        url = f"https://opensky-network.org/api/flights/arrival?airport={apt}&begin={begin}&end={end}"
        
        try:
            response = requests.get(url, auth=(user, password), timeout=30)
            if response.status_code == 200:
                batch = response.json()
                if batch and len(batch) > 0:
                    data = batch
                    print(f"✅ SUCCESS: Found {len(data)} flights at {apt}!")
                    break
                else:
                    print(f"ℹ️ {apt} is live but no arrivals recorded yet.")
            elif response.status_code == 403:
                print(f"🚫 403: Still being flagged as 'Historical' or Rate Limited.")
        except Exception as e:
            print(f"⚠️ Error: {e}")

    if data:
        df = pd.DataFrame(data)
        os.makedirs(os.path.dirname(SHARED_PATH), exist_ok=True)
        df.to_parquet(SHARED_PATH)
        print(f"💾 File written to: {SHARED_PATH}")
    else:
        # Instead of failing, we create a DUMMY file so you can finally test your GCS upload
        print("⚠️ No real flights found. Creating a dummy file to test GCS upload...")
        df = pd.DataFrame([{"info": "No flights found, dummy record created for testing pipeline"}])
        os.makedirs(os.path.dirname(SHARED_PATH), exist_ok=True)
        df.to_parquet(SHARED_PATH)



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
        src=SHARED_PATH,
        dst="bronze/test_upload.parquet",
        bucket="aerologix-data-lake-aerologix-491105",
        gcp_conn_id="google_cloud_default" 
    )

    extract_task >> upload_task