import kubernetes
from openai import OpenAI
import os
import vars


def get_logs(pod_name, namespace="monitoring"):
    config = kubernetes.config.load_kube_config()
    v1 = kubernetes.client.CoreV1Api()
    logs = v1.read_namespaced_pod_log(name=pod_name, namespace=namespace)
    return logs


recent_10_logs = get_logs("agent-chart-prometheus-node-exporter-6sl5j").split("\n")[
    -10:
]

for log in recent_10_logs:
    print(log)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Join the logs into a single string with newlines
logs_content = "\n".join(recent_10_logs)

# completion = client.chat.completions.create(
#     model="gpt-4o",
#     messages=[
#         {"role": "system", "content": vars.LOGS_SYSTEM_PROMPT},
#         {"role": "user", "content": logs_content},
#     ],
# )

# print(completion.choices[0].message.content)


node = kubernetes.client.CoreV1Api().list_node(
    label_selector="agent-chart-prometheus-node-exporter-6sl5j"
)

print(node)
