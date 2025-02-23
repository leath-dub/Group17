#!/bin/bash

docker build -t agent-ui-container:latest -f ../agent-ui/Dockerfile ../agent-ui
minikube image load agent-ui-container:latest
