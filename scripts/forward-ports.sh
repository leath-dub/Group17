#!/bin/bash

NAMESPACE="monitoring"

start_forwarding() {
    echo "Starting port forwarding..."

    # Start port forwarding in the background and store PIDs
    kubectl port-forward service/agent-chart-agent-service 8081:80 -n $NAMESPACE & echo $! > /tmp/port-forward-agent.pid
    kubectl port-forward service/agent-chart-kube-prometheu-prometheus 9090:9090 -n $NAMESPACE & echo $! > /tmp/port-forward-prometheus.pid
    kubectl port-forward service/agent-chart-grafana 8080:80 -n $NAMESPACE & echo $! > /tmp/port-forward-grafana.pid

    echo "Agent active on :8081"
    echo "Prometheus active on :9090"
    echo "Grafana active on :8080"
}

stop_forwarding() {
    echo "Stopping port forwarding..."
    
    # Kill all stored processes
    for PID_FILE in /tmp/port-forward-*.pid; do
        if [ -f "$PID_FILE" ]; then
            kill "$(cat "$PID_FILE")" && rm -f "$PID_FILE"
        fi
    done

    echo "All port-forwarding processes stopped."
}

# Allow start/stop commands
case "$1" in
    start)
        start_forwarding
        ;;
    stop)
        stop_forwarding
        ;;
    restart)
        stop_forwarding
        start_forwarding
        ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
        exit 1
        ;;
esac
