from flask import Flask, jsonify
from prometheus_client import start_http_server, Gauge
import random
import time
import threading
import os

# Flask App for Overload Control
app = Flask(__name__)

# Metrics
cpu_usage = Gauge('app_cpu_usage', 'Current CPU usage percentage')
memory_usage = Gauge('app_memory_usage', 'Current memory usage in MB')
disk_usage = Gauge('app_disk_usage', 'Current disk usage percentage')
request_latency = Gauge('app_request_latency_seconds', 'Fake request latency')

# Default healthy metric ranges (can be overridden)
CPU_RANGE = (10, 50)  # Healthy CPU usage range
MEMORY_RANGE = (100, 500)  # Healthy memory usage range (MB)
DISK_RANGE = (20, 70)  # Healthy disk usage range (%)
LATENCY_RANGE = (0.1, 0.5)  # Healthy latency range (sec)

# Overload Flags
overload_cpu = False
overload_memory = False
overload_disk = False
overload_latency = False

# Function to generate random healthy metrics
def generate_metrics():
    global overload_cpu, overload_memory, overload_disk, overload_latency
    while True:
        cpu_usage.set(random.uniform(*CPU_RANGE) if not overload_cpu else random.uniform(80, 100))
        memory_usage.set(random.uniform(*MEMORY_RANGE) if not overload_memory else random.uniform(900, 1200))
        disk_usage.set(random.uniform(*DISK_RANGE) if not overload_disk else random.uniform(90, 99))
        request_latency.set(random.uniform(*LATENCY_RANGE) if not overload_latency else random.uniform(5, 10))
        time.sleep(5)

# Flask routes to trigger overload scenarios
@app.route("/overload-cpu")
def overload_cpu_api():
    global overload_cpu
    overload_cpu = True
    return jsonify({"status": "CPU overloaded"}), 200

@app.route("/overload-memory")
def overload_memory_api():
    global overload_memory
    overload_memory = True
    return jsonify({"status": "Memory overloaded"}), 200

@app.route("/overload-disk")
def overload_disk_api():
    global overload_disk
    overload_disk = True
    return jsonify({"status": "Disk overloaded"}), 200

@app.route("/overload-latency")
def overload_latency_api():
    global overload_latency
    overload_latency = True
    return jsonify({"status": "Latency overloaded"}), 200

@app.route("/reset")
def reset():
    global overload_cpu, overload_memory, overload_disk, overload_latency
    overload_cpu = overload_memory = overload_disk = overload_latency = False
    return jsonify({"status": "All metrics reset to normal"}), 200

@app.route("/")
def home():
    return "Fake Metrics Exporter Running!"

if __name__ == "__main__":
    # Start Prometheus Metrics Server
    start_http_server(8000)
    
    # Start background thread for metric generation
    metric_thread = threading.Thread(target=generate_metrics)
    metric_thread.daemon = True
    metric_thread.start()

    # Start Flask App
    app.run(host="0.0.0.0", port=8080)
