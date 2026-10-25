output "project" {
  value = data.google_client_config.current.project
}

output "bucket_name" {
  value = google_storage_bucket.test.name
}