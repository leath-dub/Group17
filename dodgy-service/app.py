import random
import string
import time
import threading
import os
import logging
from flask import Flask, jsonify
from prometheus_client import start_http_server, Gauge

# ----------------------------
# 1. Configure Logging
# ----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(asctime)s - %(name)s - %(message)s"
)
logger = logging.getLogger("fake-k8s-service")

# ----------------------------
# 2. Flask & Prometheus Setup
# ----------------------------
app = Flask(__name__)

cpu_usage = Gauge('app_cpu_usage', 'Current CPU usage percentage')
memory_usage = Gauge('app_memory_usage', 'Current memory usage in MB')
disk_usage = Gauge('app_disk_usage', 'Current disk usage percentage')
request_latency = Gauge('app_request_latency_seconds', 'Fake request latency')

CPU_RANGE = (10, 50)
MEMORY_RANGE = (100, 500)
DISK_RANGE = (20, 70)
LATENCY_RANGE = (0.1, 0.5)

# Overload flags
overload_cpu = False
overload_memory = False
overload_disk = False
overload_latency = False

# ----------------------------
# 3. Fake Request Simulator
# ----------------------------
"""
We’ll simulate random incoming requests in the background.
Each request has:
- A user_id (like a user or client in a real system)
- A request_id (unique identifier)
- A route (one of several possible endpoints)
- DB / external calls

We tie logs to the current system metrics:
- If CPU is overloaded, logs mention high CPU usage causing slow responses.
- If memory is overloaded, logs mention potential memory errors, etc.
"""

ROUTES = ["/login", "/purchase", "/checkout", "/api/data", "/status"]
DB_ACTIONS = ["SELECT", "INSERT", "UPDATE", "DELETE"]
ERROR_MESSAGES = [
    "Timed out while querying database.",
    "Unable to connect to cache server.",
    "Payment gateway returned error code 502.",
    "Uncaught exception in order processing."
]

def generate_request_log():
    """
    Simulates a single request log with random context:
    - user_id
    - request_id
    - route
    - log level (INFO, WARNING, ERROR)
    """
    user_id = f"user_{random.randint(1000, 9999)}"
    request_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    route = random.choice(ROUTES)

    # Decide if this request triggers or experiences an error
    has_error = random.random() < 0.2  # 20% chance
    action = random.choice(DB_ACTIONS)

    # Build a pseudo-realistic log
    if has_error:
        error_msg = random.choice(ERROR_MESSAGES)
        logger.error(
            "[Request] user_id=%s request_id=%s route=%s action=%s - %s",
            user_id,
            request_id,
            route,
            action,
            error_msg
        )
    else:
        logger.info(
            "[Request] user_id=%s request_id=%s route=%s action=%s - Request handled successfully",
            user_id,
            request_id,
            route,
            action
        )

    # If we’re in an overload state, log a warning about it
    if overload_cpu or overload_memory or overload_disk or overload_latency:
        logger.warning(
            "[Request] user_id=%s request_id=%s route=%s - Potential performance issue due to overload. "
            "CPU=%s, Memory=%s, Disk=%s, Latency=%s",
            user_id,
            request_id,
            route,
            overload_cpu,
            overload_memory,
            overload_disk,
            overload_latency
        )


def simulate_requests():
    """ Continuously generates request logs every 0.5-1.5 seconds """
    while True:
        generate_request_log()
        time.sleep(random.uniform(0.5, 1.5))

# ----------------------------
# 4. Metric Generation
# ----------------------------
def generate_metrics():
    global overload_cpu, overload_memory, overload_disk, overload_latency
    while True:
        # CPU
        if overload_cpu:
            cpu_val = random.uniform(80, 100)
            logger.warning("[Metrics] CPU Overload Triggered! CPU Usage = %.2f%%", cpu_val)
        else:
            cpu_val = random.uniform(*CPU_RANGE)
            logger.info("[Metrics] CPU Normal. CPU Usage = %.2f%%", cpu_val)
        cpu_usage.set(cpu_val)

        # Memory
        if overload_memory:
            mem_val = random.uniform(900, 1200)
            logger.warning("[Metrics] Memory Overload Triggered! Memory Usage = %.2fMB", mem_val)
        else:
            mem_val = random.uniform(*MEMORY_RANGE)
            logger.info("[Metrics] Memory Normal. Memory Usage = %.2fMB", mem_val)
        memory_usage.set(mem_val)

        # Disk
        if overload_disk:
            disk_val = random.uniform(90, 99)
            logger.warning("[Metrics] Disk Overload Triggered! Disk Usage = %.2f%%", disk_val)
        else:
            disk_val = random.uniform(*DISK_RANGE)
            logger.info("[Metrics] Disk Normal. Disk Usage = %.2f%%", disk_val)
        disk_usage.set(disk_val)

        # Latency
        if overload_latency:
            lat_val = random.uniform(5, 10)
            logger.warning("[Metrics] Latency Overload Triggered! Latency = %.2fs", lat_val)
        else:
            lat_val = random.uniform(*LATENCY_RANGE)
            logger.info("[Metrics] Latency Normal. Latency = %.2fs", lat_val)
        request_latency.set(lat_val)

        time.sleep(1)

# ----------------------------
# 5. Overload & Other Routes
# ----------------------------
@app.route("/overload-cpu")
def overload_cpu_api():
    global overload_cpu
    overload_cpu = True
    logger.warning("[Overload Route] CPU Overload triggered via /overload-cpu")
    return jsonify({"status": "CPU overloaded"}), 200

@app.route("/overload-memory")
def overload_memory_api():
    global overload_memory
    overload_memory = True
    logger.warning("[Overload Route] Memory Overload triggered via /overload-memory")
    return jsonify({"status": "Memory overloaded"}), 200

@app.route("/overload-disk")
def overload_disk_api():
    global overload_disk
    overload_disk = True
    logger.warning("[Overload Route] Disk Overload triggered via /overload-disk")
    return jsonify({"status": "Disk overloaded"}), 200

@app.route("/overload-latency")
def overload_latency_api():
    global overload_latency
    overload_latency = True
    logger.warning("[Overload Route] Latency Overload triggered via /overload-latency")
    return jsonify({"status": "Latency overloaded"}), 200

@app.route("/reset")
def reset():
    global overload_cpu, overload_memory, overload_disk, overload_latency
    overload_cpu = overload_memory = overload_disk = overload_latency = False
    logger.info("[Overload Route] All metrics reset to normal")
    return jsonify({"status": "All metrics reset to normal"}), 200

@app.route("/")
def home():
    return "Fake Metrics Exporter Running!"

# ----------------------------
# 6. Main Entry Point
# ----------------------------
if __name__ == "__main__":
    # Start Prometheus on port 8000
    start_http_server(8000)

    # Thread that generates metrics
    metric_thread = threading.Thread(target=generate_metrics, daemon=True)
    metric_thread.start()

    # Thread that simulates requests
    request_thread = threading.Thread(target=simulate_requests, daemon=True)
    request_thread.start()

    # Start Flask on port 8080
    app.run(host="0.0.0.0", port=8080)
