variable "credentials" {
  description = "My Credentials"
  default     = "<credential json file>"
}


variable "project" {
  description = "Project"
  default     = "de-zoomcamp-448602"
}

variable "region" {
  description = "Region"
  default     = "us-central1"
}

variable "location" {
  description = "Project Location"
  default     = "US"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default     = "de_zoomcamp_448602_ny_taxi_dataset"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default     = "de-zoomcamp-448602-ny-taxi-bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}