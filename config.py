MODEL_NAME = 'qwen2.5:1.5b-instruct-q4_K_M'
HOST = 'http://localhost:11434'


# Tool/plugin toggles
PLUGINS_ENABLED = True  # Global master switch
ENABLED_TOOLS = {
    "weather": True
}

# Mode toggle
TERMINAL_MODE = False  # If False, use Flask API mode
