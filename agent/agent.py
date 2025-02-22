import vars
import json

from openai import OpenAI

class Task:
    id: int = 0

    def __init__(self, kind):
        Task.id += 1
        self.id = id
        self.kind = kind

    def start(self) -> None:
        # "DJANGO:xxx/task/start"
        pass

    def finish(self, data) -> None:
        # "DJANGO:xxx/task/finish"
        pass

    def fail(self) -> None:
        # "DJANGO:xxx/task/fail"
        pass

async def forward_alert(data) -> None:
    handle_alert = Task("handle-alert")

    handle_alert.start()

    client = OpenAI()
    tools = [{
        "type": "function",
        "function": {
            "name": "restart",
            "description": "Restart a pod given the pod name id",
            "parameters": {
                "type": "object",
                "properties": {
                  "id": {
                      "type": "string",
                      "description": "The human readable id for the pod"
                  }
                },
                "required": ["id"],
                "additionalProperties": False
            },
            "strict": True
        }
    }, {
        "type": "function",
        "function": {
            "name": "set_replicas",
            "description": "Set the number of replicas of pod",
            "parameters": {
                "type": "object",
                "properties": {
                  "id": {
                      "type": "string",
                      "description": "The human readable id for the pod"
                  },
                  "n": {
                      "type": "number",
                      "description": "The number of instances of the pod"
                  }
                },
                "required": ["id", "n"],
                "additionalProperties": False
            },
            "strict": True
        }
    }]

    example_json = """
    {
      "trigger": {
        "pod": "grand-major",
        "cpu": {
          "op": ">",
          "value": "80%",
        }
      },
      "pods": [
        {
            "id": "water-duck",
            "metrics": {
              "cpu": "10%",
              "memory": "50M",
              "replicas": 1
            }
        },
        {
            "id": "grand-major",
            "metrics": {
              "cpu": "80%",
              "memory": "5K",
              "replicas": 20
            }
        }
      ],
    }
    """

    informing_llm = Task("informing-llm")

    informing_llm.start()
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": vars.SYSTEM_MESSAGE}, {"role": "user", "content": example_json}],
        tools=tools
    )
    informing_llm.finish()

    automatic_triage = Task("automatic-triage")

    automatic_triage.start()
    if len(completion.choices) > 0 and completion.choices[0].message.tool_calls != None:
        actions = []
        for call in completion.choices[0].message.tool_calls:
            assert(call.type == "function")
            actions.append(call.function.name)
        automatic_triage.finish(json.dumps(actions))
    else:
        automatic_triage.fail()

    handle_alert.finish()
