from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_caching import Cache
from anthropic import Anthropic
from dotenv import load_dotenv
import os, requests

load_dotenv()

config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}
app = Flask(__name__)
CORS(app)
app.config.from_mapping(config)
cache = Cache(app)

@app.route('/weather', methods=['GET','POST'])
@cache.cached(timeout=50)
def get_weather():
    if request.method == 'GET':
        city = request.args.get('city')
    elif request.method == 'POST':
        data = request.get_json()
        city = data.get('city') if data else None

    if not city:
        return jsonify({'error': 'Missing Parameter'}), 400

    api_key = os.getenv("OPEN_WEATHER_KEY")
    get_coordinates_url = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={api_key}'
    try:
        response = requests.get(get_coordinates_url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

    # remember, these are called dictionaries in python! (hash/object)
    coordinates = {
        'lat': data[0]['lat'],
        'lon': data[0]['lon']
    }

    get_weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={coordinates.get('lat')}&lon={coordinates.get('lon')}&appid={api_key}"

    try:
        weather_response = requests.get(get_weather_url)
        response.raise_for_status()
        weather_data = weather_response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

    # convert kelvin to celcius
    temp_in_kelvin = weather_data['main']['temp']
    temp_in_celcius = round(temp_in_kelvin - 273.15, 2)

    return jsonify({
        'temperature': temp_in_celcius,
        'description': weather_data['weather'][0]['description'],
    })

# I need the city, and weather description
# Give these in the content for Claude

@app.route('/suggestion', methods=['POST'])
@cache.cached(timeout=50)
def claude_suggestion():
    data = request.get_json()
    city = data.get('city') if data else None
    weather = data.get('weather') if data else None

    if not city or not weather:
        return jsonify({'error': 'Missing Parameter'}), 400

    client = Anthropic(
        api_key = os.getenv("CLAUDE_API_KEY")
    )
    message = client.messages.create(
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content":
                f'Tell me 3 activities to do when the weather is {weather} in this {city}. Give 1 to 2 opening sentences before the activities.',
        }
    ],
    model="claude-3-5-haiku-latest",
    )

    return jsonify({
        'suggestion': ''.join(block.text for block in message.content)
    })
