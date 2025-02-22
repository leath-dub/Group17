#!/bin/bash

helm dependencies update ../helm-charts/dodgy-service-chart/.
helm dependencies build ../helm-charts/dodgy-service-chart/.
helm install dodgy-service-chart ../helm-charts/dodgy-service-chart/. --namespace default
