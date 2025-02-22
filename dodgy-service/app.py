import random
import time
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__, static_folder="static")


@app.route("/stress", methods=["POST", "GET"])
def stress_container():
    # stress test using stress-ng.

    try:
        # get the info from the request
        data = request.json or {}  # Handle case where no JSON is sent

        
        if data.get("cpu") != None:
            cpu = str(data.get("cpu"))  
        else:
            cpu = "0"
        if data.get("vm") != None:
            vm = str(data.get("vm"))  
        else:
            vm = "0"
        if data.get("vm_bytes") != None:
            vm_bytes = str(data.get("vm_bytes"))  # Default to 256MB
        else:
            vm_bytes = "256M"
        if data.get("timeout") != None:
            timeout = str(data.get("timeout"))  # Default to 30 seconds
        else:
            timeout = "30s"

        stress_cmd = ["stress-ng", "--timeout", timeout]  # Duration of the stress test
        if cpu != "0":
            stress_cmd.extend(["--cpu", cpu])  # Number of CPU stressors
        if vm != "0":
            stress_cmd.extend(
                ["--vm", vm, "--vm-bytes", vm_bytes]
            )  # Memory stressors and amount
        subprocess.Popen(stress_cmd)
        return jsonify(
            {
                "message": "Stress test started!",
                "parameters": {
                    "cpu": cpu,
                    "vm": vm,
                    "vm_bytes": vm_bytes,
                    "timeout": timeout,
                },
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
