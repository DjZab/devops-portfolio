locals {
  bucket_name = "${var.bucket_prefix}-${random_id.suffix.hex}"
  labels      = merge(var.labels, { verwaltet-von = "terraform" })
}