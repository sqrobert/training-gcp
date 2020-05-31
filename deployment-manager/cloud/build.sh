source ../common/project_settings.sh

gsutil mb gs://la-sandbox-public
gsutil defacl set public-read gs://la-sandbox-public



# cat > deployment.yaml << EOF
# imports:
#   - path: ../compute/instance-template.py

# resources:
#   - name: compute-deploy
#     type: instance-template.py
#     properties:
#        zone: $ZONE
# EOF


cat > deployment.yaml << EOF
imports:
  - path: 7-gce-bookshelf-template.py

resources:
  - name: 7-gce-bookshelf
    type: 7-gce-bookshelf-template.py
    properties:
      zone: $ZONE
      machineType: f1-micro
      machine-image: https://www.googleapis.com/compute/v1/projects/debian-cloud/global/images/family/debian-9
      min-instances: 1
      max-instances: 10
      target-utilization: 0.6
      scopes:
      - https://www.googleapis.com/auth/cloud-platform

EOF

