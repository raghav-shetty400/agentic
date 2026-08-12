import requests


def get_weather(city):

    url = f"http://127.0.0.1:8000/weather/{city}"

    response = requests.get(url)

    return response.json()
