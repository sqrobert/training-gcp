#!/bin/bash

#gcloud auth login

source project_settings.sh
echo $PROJECT_ID
gcloud config set project $PROJECT_ID
gcloud config set compute/region $REGION
gcloud config set compute/zone $ZONE

/bin/bash /app-engine/build.sh
/bin/bash /SQL/build.sh
/bin/bash /deploymeny-manager/build.sh