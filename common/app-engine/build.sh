source ../project_settings.sh

gcloud app create --project=$PROJECT_ID --region=$APP_ENGINE_REGION -q
gcloud app deploy "$PWD/../app-engine/app.yaml" --quiet
