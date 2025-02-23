import http.server
import socketserver
import threading
import json
import time
from kubernetes import client, config
from apps.home.models import Event, Pod, Cluster

# Define the port on which the server will listen
PORT = 4321


class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):

        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length)
        post_data = post_data.decode("utf-8")

        try:
            payload = json.loads(post_data)
        except Exception as e:
            print(e)
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<p>Bad Request</p>")
            return

        event_id = payload.event_id
        pod_name = payload.pod_name
        kind = payload.kind

        results = Pod.objects.filter(name=pod_name)
        if len(results) == 0:
            # TODO update from kubernetes
            return

        if self.path == "/event/create":
            results[0].status = Pod.AFFECTED
            status = Event.PENDING
        elif self.path == "/event/finish":
            reply = payload.reply
            status = Event.FINISHED
            results[0].status = Pod.ALIVE
        elif self.path == "/event/fail":
            status = Event.FAIL
            results[0].status = Pod.DEAD

        results[0].save()

        if reply != None:
            event = Event(
                status=status, pod=results[0], event_id=event_id, kind=kind, reply=reply
            )
            event.save()
        else:
            event = Event(status=status, pod=results[0], event_id=event_id, kind=kind)
            event.save()

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<p>OK</p>")


def run_server():
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"Serving on port {PORT}...")
        httpd.serve_forever()


def event_listener():
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.daemon = True
    server_thread.start()
    print("Server is running in a background thread.")

def run_pod_update_listener():
    try:
        # Try to load in-cluster config first (for when running inside k8s)
        try:
            config.load_incluster_config()
        except:
            # Fall back to local kubeconfig if not running in cluster
            config.load_kube_config()

        # Get or create default cluster
        default_cluster, _ = Cluster.objects.get_or_create(id=1)

        while True:
            time.sleep(10)
            try:
                # Get all nodes from kubernetes
                api = client.CoreV1Api()
                nodes = api.list_namespaced_pod(namespace="default")
                
                # Get set of current pod names from k8s
                current_pod_names = {node.metadata.name for node in nodes.items}
                
                # Get all pods from database
                db_pods = Pod.objects.all()
                
                # Remove pods that no longer exist in k8s
                for pod in db_pods:
                    if pod.name not in current_pod_names:
                        print(f"Pod {pod.name} no longer exists, removing from database")
                        pod.delete()

                # Add any new pods
                for node in nodes.items:
                    pod_name = node.metadata.name
                    pod_exists = Pod.objects.filter(name=pod_name).exists()

                    if not pod_exists:
                        new_pod = Pod(
                            name=pod_name,
                            cluster=default_cluster,  # Set the cluster here
                            namespace="default",
                        )
                        new_pod.save()
                        print(f"Pod {pod_name} added to the database")

            except Exception as e:
                print(f"Error updating pods: {e}")
                time.sleep(30)  # Wait longer on error before retrying

    except Exception as e:
        print(f"Failed to initialize Kubernetes client: {e}")

def node_update_listener():
    pod_thread = threading.Thread(target=run_pod_update_listener, daemon=True)
    pod_thread.daemon = True
    pod_thread.start()
    print("Pod update listener is running in a background thread.")
