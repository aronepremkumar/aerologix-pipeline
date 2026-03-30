terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.0.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_storage_bucket" "data_lake" {
  # Buckets must be globally unique, so keeping the ID here is smart
  name          = "aerologix-data-lake-${var.project_id}"
  location      = "US"
  force_destroy = true
}

resource "google_bigquery_dataset" "stg_dataset" {
  dataset_id = "aerologix_stg"
  location   = "US"
}

resource "google_bigquery_dataset" "prod_dataset" {
  dataset_id = "aerologix_prod"
  location   = "US"
}