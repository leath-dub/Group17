import vars

from openai import OpenAI

def main() -> None:
    client = OpenAI()
    tools = [{
        "type": "function",
        "function": {
            "name": "dupe_pod",
            "description": "Create a new instance of pod given the pod id string",
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
    }]

    example_json = """
    {
      "trigger": {
        "pod": "water-duck",
        "cpu": {
          "op": ">",
          "value": "80%",
        }
      },
      "pods": [
        {
            "id": "water-duck",
            "metrics": {
              "cpu": "80%",
              "memory": "50%",
            }
        },
        {
            "id": "grand-major",
            "metrics": {
              "cpu": "10%",
              "memory": "5%",
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

    for call in completion.choices[0].message.tool_calls:
        assert(call.type == "function")
        print(call)

if __name__ == "__main__":
    main()
