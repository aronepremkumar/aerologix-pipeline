# ✈️ AeroLogix: Air Freight Reliability Pipeline

## 🎯 Project Purpose
In global logistics, air freight delays create a "bullwhip effect" that disrupts ground transportation and warehouse scheduling. **AeroLogix** is an end-to-end data pipeline designed to quantify carrier reliability. 

By ingesting raw ADS-B telemetry from the **OpenSky Network**, this project transforms "dots on a map" into actionable business intelligence, helping logistics managers optimize labor costs and protect delivery SLAs.

## 🏗️ Architecture & Medallion Flow
* **Bronze (Raw):** OpenSky API data ingested via **Apache Airflow** and stored as Parquet in **Google Cloud Storage (GCS)**.
* **Silver (Cleaned):** Data transformed in **BigQuery** using **dbt** (Unix epochs converted to UTC, callsign filtering).
* **Gold (Insights):** Aggregated metrics (e.g., `avg_delay_by_operator`) used for visualization and reliability scoring.



## 🛠️ Tech Stack
* **Cloud:** Google Cloud Platform (GCP)
* **Orchestration:** Apache Airflow (Dockerized, LocalExecutor)
* **Data Warehouse:** BigQuery
* **Transformations:** dbt-bigquery
* **Storage:** Google Cloud Storage (GCS)
* **Infrastructure:** Terraform & Docker

## 📋 Prerequisites
Ensure you have the following installed:
1.  **Docker & Docker Compose**
2.  **Google Cloud SDK (gcloud)**
3.  **GCP Service Account Key:** Placed in the `/dbt` folder as `aerologix-491105-8921ba81006a.json`.



## 🚀 Getting Started

### 1. Infrastructure Setup
If you haven't created the buckets and datasets yet, use the Terraform files provided:
```bash
cd terraform
terraform init
terraform apply
```

### 2. Launch the Pipeline (Airflow)
The Airflow stack uses a shared Docker volume to pass data between tasks safely.
```bash
# Create local data directory for the shared volume
mkdir -p data

# Start the Docker containers
docker-compose up -d --build

# Access Airflow UI
# URL: http://localhost:8080
# Credentials: airflow / airflow
```
**Action:** Trigger the DAG `aerologix_opensky_to_gcs_v2`. This will fetch live flight data and upload it to your GCS Bronze bucket.

### 3. Data Transformation (dbt)
Once the data is in GCS, use dbt to clean and model it.
```bash
# Enter the scheduler container
docker exec -it airflow-airflow-scheduler-1 /bin/bash

# Navigate to the dbt project
cd dbt
dbt deps
dbt run
```

### 4. Verification
Check your BigQuery console for the following tables:
* `aerologix_staging.stg_arrivals` (Cleaned records)
* `aerologix_staging.fct_logistics_reliability` (Final metrics)



## 📊 Key Metrics Tracked
* **Average Flight Duration:** Calculated from departure/arrival timestamps.
* **Reliability Status:** Categorized as 'Delayed' if duration exceeds the 4-hour threshold.
* **Volume Tracking:** Total flight count per destination airport.

