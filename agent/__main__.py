import vars

from openai import OpenAI

def main() -> None:
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

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": vars.SYSTEM_MESSAGE}, {"role": "user", "content": example_json}],
        tools=tools
    )

    if len(completion.choices) > 0:
        for call in completion.choices[0].message.tool_calls:
            assert(call.type == "function")
            print(call)

if __name__ == "__main__":
    main()
