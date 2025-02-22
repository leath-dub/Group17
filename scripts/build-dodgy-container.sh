#!/bin/bash

docker build -t dodgy-container:latest -f ../dodgy-service/Dockerfile ../dodgy-service
minikube image load dodgy-container:latest

