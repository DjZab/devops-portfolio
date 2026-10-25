terraform {
  required_version = ">= 1.12"
  required_providers {
    google = {
      source = "hashicorp/google"
      # version = "~> 8.8"   <- aktuelle Hauptversion in der Registry nachsehen
    }
    random = {
      source = "hashicorp/random"
    }
  }
}

provider "google" {
  project = "project-4caa665c-3278-4904-938"
  region  = "europe-west3"
}

resource "random_id" "suffix" {
  byte_length = 4
}

resource "google_storage_bucket" "test" {
  name                        = "lernbucket-${random_id.suffix.hex}"
  location                    = "EU"
  uniform_bucket_level_access = true
  force_destroy               = true
}