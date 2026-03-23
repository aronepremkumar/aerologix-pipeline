# AeroLogix: Air Freight Reliability Pipeline

## 🎯 Project Purpose
In global logistics, air freight delays create a "bullwhip effect" that disrupts ground transportation and warehouse scheduling. **AeroLogix** is an end-to-end data pipeline designed to quantify carrier reliability. 

By ingesting raw ADS-B telemetry from the **OpenSky Network**, this project transforms "dots on a map" into actionable business intelligence, helping logistics managers optimize labor costs and protect delivery SLAs.

## 🏗️ Architecture & Medallion Flow
- **Bronze (Raw):** OpenSky API data ingested via **Airflow** and stored as Parquet in **GCS**.
- **Silver (Cleaned):** Data transformed in **BigQuery** using **dbt** (Unix epochs converted to UTC, callsign filtering).
- **Gold (Insights):** Aggregated metrics (e.g., `avg_delay_by_operator`) used for visualization.

## 🛠️ Technologies
- **Cloud:** Google Cloud Platform (GCP)
- **Infrastructure as Code:** Terraform
- **Orchestration:** Apache Airflow (Dockerized)
- **Data Warehouse:** BigQuery (Partitioned by Date, Clustered by Operator)
- **Transformations:** dbt-bigquery
- **Visualization:** Looker Studio (or Streamlit)

## 📋 Prerequisites
Ensure you have the following installed:
1. **Docker & Docker Compose**
2. **Terraform**
3. **Google Cloud SDK (gcloud)**
4. **Python 3.10+**
5. **OpenSky Network Account** (for API credentials)

## 🚀 How to Execute

### 1. Infrastructure Setup (Terraform)
```bash
cd terraform
# Initialize and apply to create GCS Buckets and BigQuery Datasets
terraform init
terraform apply# aerologix-pipeline
