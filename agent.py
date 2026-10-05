import ollama

def calculator(expression):
    return eval(expression)


tools = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Use this tool to perform mathematical calculations.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The mathematical expression to calculate"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

while True:

    question = input("\nYou: ")

    if question.lower() == "exit":
        print("Agent: Goodbye!")
        break

    messages = [
        {
            "role": "user",
            "content": question
        }
    ]

    response = ollama.chat(
        model="llama3.2",
        messages=messages,
        tools=tools
    )

    if response["message"].get("tool_calls"):

        tool_call = response["message"]["tool_calls"][0]

        expression = tool_call["function"]["arguments"]["expression"]

        result = calculator(expression)

        messages.append(response["message"])

        messages.append({
            "role": "tool",
            "tool_name": "calculator",
            "content": str(result)
        })

        final_response = ollama.chat(
            model="llama3.2",
            messages=messages,
            tools=tools
        )

        print("Agent:", final_response["message"]["content"])

    else:
        print("Agent:", response["message"]["content"])