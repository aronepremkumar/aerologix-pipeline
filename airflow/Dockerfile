FROM apache/airflow:2.8.1-python3.10

USER root
# Install build-essential to help with ARM64 compilation if needed
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && apt-get clean

USER airflow

# 1. Install dbt-bigquery first (it's the heaviest)
RUN pip install --no-cache-dir "dbt-bigquery>=1.5.0,<1.8.0"

# 2. Install astronomer-cosmos second
RUN pip install --no-cache-dir "astronomer-cosmos"

# 3. Final check to ensure dbt is reachable
RUN dbt --version