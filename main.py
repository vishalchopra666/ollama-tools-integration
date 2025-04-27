import ollama
from tools.weather_tool import create_weather_tool
from config import *
from handle_tools import handle_tool

client = ollama.Client(host=HOST)

def chat_with_tools(user_input: str):
    # Get tool definition
    weather_tool = create_weather_tool()

    # Send the user input and the weather tool to the model
    response = client.chat(
        model=MODEL_NAME,
        messages=[{'role': 'user', 'content': user_input}],
        tools=[weather_tool],
    )

    # Get the model's response content and tool calls
    model_response = response['message']['content']
    tool_calls = response.get('message', {}).get('tool_calls', [])

    if tool_calls:
        for tool_call in tool_calls:
            # Process each tool dynamically
            tool_result = handle_tool(tool_call)
            if tool_result:
                return f"Tool response: {tool_result}"

    # If no tool call is made, return the model's standard response
    return f"Assistant: {model_response}"

def start_chat():
    print("Start chatting with the bot (type 'exit' to end).")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        
        # Call the chat function with user input
        response = chat_with_tools(user_input)
        print(response)

if __name__ == "__main__":
    start_chat()
