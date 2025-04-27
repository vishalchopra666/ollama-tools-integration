# How to Add a tool


1. First, create 'format response' under helpers folder. 

```
def format_weather_response(city, temperature):
    return f"The weather in {city} is sunny and {temperature}°C."
```

2. 2nd, then add 'Schema markup' under schema folder.

```
weather_schema = {
    'type': 'function',
    'function': {
        'name': 'get_current_weather',
        'description': 'Get the current weather for a city',
        'parameters': {
            'type': 'object',
            'properties': {
                'city': {
                    'type': 'string',
                    'description': 'The name of the city to get weather for',
                },
            },
            'required': ['city'],
        },
    },
}
```

3. 3rd, then 'create tool' function under tools folder.

```
from schemas.weather_schema import weather_schema

def create_weather_tool():
    return weather_schema

```

4. 4th, then actual weather logic under functions folder.

```
from helpers.weather_helper import format_weather_response

def get_current_weather(city: str):
    # Simulate API call to a weather service
    temperature = 25  # Simulated temperature value
    return format_weather_response(city, temperature)
```

5. Update the handle_tools.py

```
# Assuming each tool is defined with a function name and has its own handler
def handle_tool(tool_call):
    tool_name = tool_call.function.name
    arguments = tool_call.function.arguments

    if tool_name == 'get_current_weather':
        city = arguments.get('city')
        if city:
            from functions.weather import get_current_weather
            return get_current_weather(city)

    # Add more tools and their handlers as needed
    # elif tool_name == 'another_tool':
    #     handle_other_tool(arguments)
    #     return "Other tool response"

    # Return None if no tool matches
    return None
```

6. Then update main.py

Add Tools definition

```
 # Get tool definition
    weather_tool = create_weather_tool()
```

7. Then add your tool to response variable

```
# Send the user input and the weather tool to the model
    response = client.chat(
        model=MODEL_NAME,
        messages=[{'role': 'user', 'content': user_input}],
        tools=[weather_tool],
    )
```


# Config file

You should update it with your ollama host, and model name.


Note: Developed by @Vishalchopra666.
Note: You might also like to explore my new web project here., [AI Bio Generator](https://quicksocialbio.com)