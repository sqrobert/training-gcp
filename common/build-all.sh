#!/bin/bash

#gcloud auth login

source project_settings.sh
echo $PROJECT_ID
gcloud config set project $PROJECT_ID
gcloud config set compute/region $REGION
gcloud config set compute/zone $ZONE

gcloud app create --project=$PROJECT_ID --region=$APP_ENGINE_REGION -q
gcloud app deploy "$PWD/../app-engine/app.yaml" --quiet