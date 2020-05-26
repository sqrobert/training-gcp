source ../project_settings.sh

cat > deployment.yaml << EOF
imports:
  - path: ../compute/instance-template.py

resources:
  - name: compute-deploy
    type: instance-template.py
    properties:
       zone: $ZONE
EOF