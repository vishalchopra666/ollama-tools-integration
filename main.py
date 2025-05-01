import ollama
from tools.weather_tool import create_weather_tool
from config import *
from handle_tools import handle_tool
from flask import Flask, request, jsonify

client = ollama.Client(host=HOST)
CHAT_HISTORY = [
    {"role": "system", "content": "You are a helpful assistant. Use tools only when needed."}
]
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

    # Add user input to chat history
    CHAT_HISTORY.append({'role': 'user', 'content': user_input})

    # Send full history to the model
    response = client.chat(
        model=MODEL_NAME,
        messages=CHAT_HISTORY,
        tools=tools
    )

    model_response = response['message']['content']
    tool_calls = response.get('message', {}).get('tool_calls', [])

    if tool_calls:
        for tool_call in tool_calls:
            tool_result = handle_tool(tool_call)
            if tool_result:
                # Optionally store tool result as assistant message too
                CHAT_HISTORY.append({'role': 'assistant', 'content': tool_result})
                return f"Tool response: {tool_result}"

    # Add model response to chat history
    CHAT_HISTORY.append({'role': 'assistant', 'content': model_response})
    return f"Assistant: {model_response}"

@app.route("/chat", methods=["POST"])
def chat_api():
    # Extract user input from the incoming JSON payload
    user_input = request.json.get("input", "")
    
    if not user_input:
        return jsonify({"error": "No input provided"}), 400
    
    # Use the chat_with_tools function to get a response
    response = chat_with_tools(user_input)
    
    # Return the response as JSON
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
