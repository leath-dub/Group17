#!/bin/bash

helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm dependencies update ../helm-charts/agent-chart/.
helm dependencies build ../helm-charts/agent-chart/.
helm install agent-chart ../helm-charts/agent-chart/. --namespace monitoring --create-namespace
