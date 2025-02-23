import vars
import json
import http.client

import threading

from openai import OpenAI
from kubernetes import client, config
import requests

UI_HOST = "http://agent-chart-agent-ui-service.monitoring.svc.cluster.local:8000"
PROM_HOST = (
    "http://agent-chart-kube-prometheu-prometheus.monitoring.svc.cluster.local:9090"
)


def load_kube():
    config.load_kube_config()
    return client.CoreV1Api()


def get_metrics(podname, alert):
    queries = [
        f"app_memory_usage{{pod='{podname}'}}",
        f"app_cpu_usage{{pod='{podname}'}}",
        f"app_disk_usage{{pod='{podname}'}}",
        f"app_request_latency_seconds{{pod='{podname}'}}",
    ]

    collected_metrics = []

    for query in queries:
        response = requests.get(f"{PROM_HOST}/api/v1/query", params={"query": query})
        data = response.json()
        metric = data['data']['result'][0]['metric']['__name__']
        value = data['data']['result'][0]['value'][1]
        collected_metrics.append((metric, value))
        print(f"PROM RESPONSE:\n{data}", flush=True)

    print(f"COLLECTED METRICS: {collected_metrics}", flush=True)

    return collected_metrics


class Event:
    id = 0
    lock = threading.Lock()

    def __init__(self, kind):
        with Event.lock:
            Event.id += 1
            self.id = Event.id
        self.kind = kind
        self.failed = False
        self.finish_payload = None

    def as_json(self):
        return json.dumps({"id": self.id, "kind": self.kind})

    def __enter__(self) -> None:
        client = http.client.HTTPConnection(UI_HOST)
        payload = self.as_json()
        client.request(
            "POST", "/event/create", payload, {"Content-Type": "application/json"}
        )
        client.close()
        # TODO handle repsonse from server?

    def __exit__(self, *args) -> None:
        if self.failed:
            client = http.client.HTTPConnection(UI_HOST)
            payload = self.as_json()
            client.request(
                "POST", "/event/fail", payload, {"Content-Type": "application/json"}
            )
            client.close()
            # TODO handle repsonse from server?
            return

        if self.finish_payload:
            client = http.client.HTTPConnection(UI_HOST)
            client.request(
                "POST",
                "/event/finish",
                self.finish_payload,
                {"Content-Type": "application/json"},
            )
            client.close()
            # TODO handle repsonse from server?
        else:
            client = http.client.HTTPConnection(UI_HOST)
            payload = self.as_json()
            client.request(
                "POST", "/event/finish", payload, {"Content-Type": "application/json"}
            )
            client.close()
            # TODO handle repsonse from server?

    def set_finish_payload(self, payload) -> None:
        self.finish_payload = payload

    def set_fail(self) -> None:
        self.failed = True


def forward_alert(data) -> None:
    print(data, flush=True)

    print(f"Alert: {data['alerts'][0]['labels']['alertname']}", flush=True)
    print(f"Pod: {data['alerts'][0]['labels']['pod']}", flush=True)
    print(f"Severity: {data['alerts'][0]['labels']['severity']}", flush=True)

    alert = data["alerts"][0]["labels"]["alertname"]
    pod = data["alerts"][0]["labels"]["pod"]
    severity = data["alerts"][0]["labels"]["severity"]

    [(mem_tag, mem_met), (cpu_tag, cpu_met), (disk_tag, disk_met), (laten_tag, laten_met)] = get_metrics(pod, alert)

    with Event("handling-alert") as handle_alert:
        client = OpenAI()
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "restart",
                    "description": "Restart a pod given the pod name id",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "The human readable id for the pod",
                            }
                        },
                        "required": ["id"],
                        "additionalProperties": False,
                    },
                    "strict": True,
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "set_replicas",
                    "description": "Set the number of replicas of pod",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "id": {
                                "type": "string",
                                "description": "The human readable id for the pod",
                            },
                            "n": {
                                "type": "number",
                                "description": "The number of instances of the pod",
                            },
                        },
                        "required": ["id", "n"],
                        "additionalProperties": False,
                    },
                    "strict": True,
                },
            },
        ]

        json_to_llm = f"""
        {{
          "trigger": {{
            "alert": {alert},
            "pod": "{pod}",
            "severity": "{severity}"
          }},
          "metrics": {{
              {cpu_tag}: {cpu_met},
              {mem_tag}: {mem_met},
              {disk_tag}: {disk_met},
              {laten_tag}: {laten_met}
          }}
        }}
        """

        print(json_to_llm, flush=True)

        with Event("informing-llm") as informing_llm:
            completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": vars.SYSTEM_MESSAGE},
                    {"role": "user", "content": json_to_llm},
                ],
                tools=tools,
            )

        with Event("automatic-triage") as automatic_triage:
            if (
                len(completion.choices) > 0
                and completion.choices[0].message.tool_calls != None
            ):
                actions = []
                for call in completion.choices[0].message.tool_calls:
                    assert call.type == "function"
                    actions.append(call.function.name)
                automatic_triage.set_payload(json.dumps(actions))
            else:
                automatic_triage.set_fail()
