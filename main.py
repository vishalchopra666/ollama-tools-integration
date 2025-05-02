import ollama
from tools.weather_tool import create_weather_tool
from config import *
from handle_tools import handle_tool
from flask import Flask, request, jsonify
import os
import glob
import json

app = Flask(__name__)
client = ollama.Client(host=HOST)

# Base system + intro chat history
BASE_CONTEXT = [
    {"role": "system", "content": "You are a helpful assistant. Use tools only when needed."},
    {"role": "user", "content": "My name is vishal kumar"},
    {"role": "assistant", "content": "Nice to meet you vishal"}
]

# This will store only current chat session (excluding training)
CHAT_HISTORY = []

# Brain Context
BRAIN_CONTEXT = []

# Save only the CHAT_HISTORY (not base or brain context)
def save_chat_history():
    with open("chat_history.json", "w") as f:
        json.dump(CHAT_HISTORY, f, indent=2)

def load_chat_history():
    global CHAT_HISTORY
    CHAT_HISTORY = []

    if os.path.exists("chat_history.json") and os.stat("chat_history.json").st_size > 0:
        try:
            with open("chat_history.json", "r") as f:
                main_chat = json.load(f)
            if isinstance(main_chat, list):
                CHAT_HISTORY.extend(main_chat)
        except json.JSONDecodeError:
            print("Error: chat_history.json is not valid JSON. Starting fresh.")
    else:
        print("No chat_history.json file found or it's empty. Starting fresh.")

def get_enabled_tools():
    tools = []
    if not PLUGINS_ENABLED:
        return tools

    if ENABLED_TOOLS.get("weather"):
        tools.append(create_weather_tool())
    # Add more tools as needed

    return tools

def load_brain_context_once():
    global BRAIN_CONTEXT
    brain_files = glob.glob("brain/*.json")
    for file_path in brain_files:
        try:
            with open(file_path, "r") as f:
                extra_chat = json.load(f)
            if isinstance(extra_chat, list):
                BRAIN_CONTEXT.extend(extra_chat)
        except:
            pass

def chat_with_tools(user_input: str):
    tools = get_enabled_tools()

    # Load temporary context for this chat (brain + current history)
    full_context = BASE_CONTEXT + BRAIN_CONTEXT + CHAT_HISTORY
    full_context.append({'role': 'user', 'content': user_input})

    response = client.chat(
        model=MODEL_NAME,
        messages=full_context,
        tools=tools
    )

    model_response = response['message']['content']
    tool_calls = response.get('message', {}).get('tool_calls', [])

    # Save user message to CHAT_HISTORY
    CHAT_HISTORY.append({'role': 'user', 'content': user_input})

    if tool_calls:
        for tool_call in tool_calls:
            tool_result = handle_tool(tool_call)
            if tool_result:
                CHAT_HISTORY.append({'role': 'assistant', 'content': tool_result})
                return f"Tool response: {tool_result}"

    # Save assistant reply
    CHAT_HISTORY.append({'role': 'assistant', 'content': model_response})
    return f"Assistant: {model_response}"

@app.route("/chat", methods=["POST"])
def chat_api():
    user_input = request.json.get("input", "")
    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    response = chat_with_tools(user_input)
    return jsonify({"response": response})

def start_chat():
    print("Start chatting with the bot (type 'exit' to end).")
    load_chat_history()
    load_brain_context_once()

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            save_chat_history()
            break

        response = chat_with_tools(user_input)
        print(response)

if __name__ == "__main__":
    if TERMINAL_MODE:
        start_chat()
    else:
        load_chat_history()
        app.run(debug=True)
