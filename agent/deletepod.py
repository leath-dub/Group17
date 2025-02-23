from __future__ import print_function
import time
import kubernetes.client
from kubernetes.client.rest import ApiException
from pprint import pprint
from kubernetes.config import load_kube_config, load_incluster_config
import os


def delete_pod(name, namespace):
    try:
        # Try to load in-cluster config first (for when running inside k8s)
        try:
            load_incluster_config()
        except: 
            # Fall back to local kubeconfig if not running in cluster
            load_kube_config()

        # Create an instance of the API class
        api_instance = kubernetes.client.CoreV1Api()

        # Delete the pod
        api_response = api_instance.delete_namespaced_pod(
            name=name,
            namespace=namespace,
            body=kubernetes.client.V1DeleteOptions(
                grace_period_seconds=0, propagation_policy="Foreground"
            ),
        )

        print(f"Successfully deleted pod {name} in namespace {namespace}")
        return api_response

    except ApiException as e:
        print(f"Exception when deleting pod {name}: {e}\n")
        raise e


if __name__ == "__main__":
    # Example usage
    pod_name = "agent-chart-kube-state-metrics-5958788bf-jlxzm"
    namespace = "monitoring"
    delete_pod(pod_name, namespace)
