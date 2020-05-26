source ../project_settings.sh

gcloud sql instances create $CLOUD_SQL_INSTANCE_NAME --tier=$CLOUD_SQL_TIER --region=$REGION
gcloud sql users set-password root --host=% --instance $CLOUD_SQL_INSTANCE_NAME --password $CLOUD_SQL_ROOT_PASSWORD
gcloud sql databases create $CLOUD_SQL_DB_NAME --instance=$CLOUD_SQL_INSTANCE_NAME --charset=utf8 --collation=utf8_general_ci