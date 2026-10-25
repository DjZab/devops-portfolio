output "project" {
  description = "Project ID taken from the active provider configuration."
  value       = data.google_client_config.current.project
}

output "bucket_name" {
  description = "Name of the created bucket, including the random suffix."
  value       = google_storage_bucket.test.name
}