FROM apache/airflow:2.8.1-python3.10

USER root
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && apt-get clean

USER airflow

# 1. Ingestion Dependencies (Fixes your current failure)
RUN pip install --no-cache-dir pandas pyarrow requests google-cloud-storage

# 2. dbt & Orchestration Dependencies
RUN pip install --no-cache-dir "dbt-bigquery>=1.5.0,<1.8.0"
RUN pip install --no-cache-dir "astronomer-cosmos"

# 3. Final check
RUN dbt --version