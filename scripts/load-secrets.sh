#!/bin/bash

kubectl create secret generic agent-secrets --from-env-file=secrets.env --namespace=monitoring --dry-run=client -o yaml > secret.yaml
kubectl apply -f secret.yaml
