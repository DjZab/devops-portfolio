variable "project_id" {
  type        = string
  description = "ID (not the display name) of the Google Cloud project in which all resources are created."
}

variable "region" {
  type        = string
  description = "Default region for the Google provider. It does not affect the bucket location, which is set separately."
  default     = "europe-west3"
}

variable "bucket_prefix" {
  type        = string
  description = "Prefix of the bucket name. A random suffix is appended. Lowercase letters, digits and hyphens only."
  # validation-Block wie besprochen
}

variable "labels" {
  type        = map(string)
  description = "Labels attached to all resources, for example { umgebung = \"test\" }. Merged with fixed labels in locals."
  default     = {}

  validation {
    condition     = alltrue([for k, v in var.labels : can(regex("^[a-z][a-z0-9_-]{0,62}$", k))])
    error_message = "Label keys must start with a lowercase letter and may only contain lowercase letters, digits, hyphens and underscores (max. 63 characters)."
  }
}

variable "environment" {
  type        = string
  description = "Deployment environment. Controls whether the bucket can be destroyed together with its content."
  default     = "test"

  validation {
    condition     = contains(["test", "prod"], var.environment)
    error_message = "Environment must be either \"test\" or \"prod\"."
  }
}

variable "bucket_settings" {
  type = object({
    location   = string
    versioning = optional(bool, false)
  })
  description = "Bucket settings. Location is required, versioning is optional and defaults to false."
  default = {
    location = "EU"
  }
}