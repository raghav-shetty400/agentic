import requests

def get_events(api_key):

    url = "https://api.hubble.in/v9/devices/events"

    headers = {
        "x-application-id": "hubble_baby_gcm:2.0.1",
        "x-auth-tenant": "hubble",
        "x-auth-token-type": "app_token",
        "x-user-agent": "browser"
    }

    params = {
        "api_key": api_key,
        "alerts": 4,
        "size": 100
    }

    response = requests.get(
        url,
        headers=headers,
        params=params
    )

    data = response.json()

    # Return only the list of events
    return data["data"]["events"]