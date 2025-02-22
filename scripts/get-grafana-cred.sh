#!/bin/bash

echo "user: $(kubectl get secrets/agent-chart-grafana -o jsonpath='{.data.admin-user}' -n monitoring | base64 --decode)"
echo "pass: $(kubectl get secrets/agent-chart-grafana -o jsonpath='{.data.admin-password}' -n monitoring | base64 --decode)"
