import ollama
from tools.weather_tool import create_weather_tool
from config import *
from handle_tools import handle_tool
from flask import Flask, request, jsonify


client = ollama.Client(host=HOST)
app = Flask(__name__)

def get_enabled_tools():
    tools = []
    if not PLUGINS_ENABLED:
        return tools

    if ENABLED_TOOLS.get("weather"):
        tools.append(create_weather_tool())
    # Add more tools as you create them

    return tools

def chat_with_tools(user_input: str):

    tools = get_enabled_tools()

    response = client.chat(
        model=MODEL_NAME,
        messages=[{'role': 'user', 'content': user_input}],
        tools=tools
    )

    model_response = response['message']['content']
    tool_calls = response.get('message', {}).get('tool_calls', [])

    if tool_calls:
        for tool_call in tool_calls:
            tool_result = handle_tool(tool_call)
            if tool_result:
                return f"Tool response: {tool_result}"

    return f"Assistant: {model_response}"


@app.route("/chat", methods=["POST"])
def chat_api():
    user_input = request.json.get("input", "")
    response = chat_with_tools(user_input)
    return jsonify({"response": response})

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
    if TERMINAL_MODE:
        start_chat()
    else:
        app.run(debug=True)
