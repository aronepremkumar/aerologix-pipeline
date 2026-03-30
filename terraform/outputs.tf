output "storage_bucket_name" {
  value = google_storage_bucket.data_lake.name
}

output "bigquery_stg_dataset" {
  value = google_bigquery_dataset.stg_dataset.dataset_id
}