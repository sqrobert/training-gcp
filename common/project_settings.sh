#!/bin/bash

REGION="europe-west3"
ZONE="europe-west3-c"
PROJECT_ID=$(gcloud projects list --filter="PROJECT_ID:(playground-*)" --format="value(PROJECT_ID)")
APP_ENGINE_REGION=$REGION