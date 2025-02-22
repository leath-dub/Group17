#!/bin/bash

# Build the container
docker build -t agent-container:latest -f ../agent/Dockerfile ../agent
minikube image load agent-container:latest
