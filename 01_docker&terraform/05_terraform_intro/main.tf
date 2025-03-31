# This Terraform code is used to configure and manage resources on Google Cloud Platform (GCP).

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.27.0"
    }
  }
}

provider "google" {
  project = "seventh-league-447908-t0"
  region  = "us-central1"
}

resource "google_storage_bucket" "demo-bucket" {
  name          = "seventh-league-447908-t0--terra-bucket"
  location      = "US"
  force_destroy = true
}

resource "google_bigquery_dataset" "demo_dataset" {
  dataset_id = "demo_dataset"
}