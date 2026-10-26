terraform {
  required_version = ">= 1.12"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 8.8"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.9"
    }
  }

  backend "gcs" {
    bucket = "tfstate-zab-57"
    prefix = "terraform/state"
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "random_id" "suffix" {
  byte_length = 4
}

resource "google_storage_bucket" "test" {
  name                        = local.bucket_name
  location                    = var.bucket_settings.location
  uniform_bucket_level_access = true
  force_destroy               = var.environment != "prod"
  labels                      = local.labels

  versioning {
    enabled = var.bucket_settings.versioning
  }
}

data "google_client_config" "current" {

}