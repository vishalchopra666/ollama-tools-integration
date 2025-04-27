from helpers.weather_helper import format_weather_response

def get_current_weather(city: str):
    # Simulate API call to a weather service
    temperature = 25  # Simulated temperature value
    return format_weather_response(city, temperature)
