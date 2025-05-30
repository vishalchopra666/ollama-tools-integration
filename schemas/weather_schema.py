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
