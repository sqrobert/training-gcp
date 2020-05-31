#!/bin/bash

REGION="europe-west3"
ZONE="europe-west3-c"
PROJECT_ID=$(gcloud projects list --filter="PROJECT_ID:(playground-*)" --format="value(PROJECT_ID)")

#7-gce
CLOUD_SQL_INSTANCE_NAME="training-sql"
CLOUD_SQL_TIER="db-g1-small"
CLOUD_SQL_ROOT_PASSWORD="Temp1Password@"
CLOUD_SQL_DB_NAME="bookshelf"
STORAGE_PUBLIC="bookshelf-bucket-public"
APP_ENGINE_REGION=$REGION
