import os
try:
    import requests
except ImportError:
    requests = None
from fastapi import HTTPException

API_NINJAS_URL = "https://api.api-ninjas.com/v1/exercises"


def fetch_exercises(muscle: str):
    if requests is None:
        raise HTTPException(status_code=500, detail="Requests library not available")

    api_key = os.getenv("API_NINJAS_KEY")

    if not api_key:
        raise HTTPException(status_code=500, detail="API key not configured")

    headers = {
        "X-Api-Key": api_key
    }

    params = {
        "muscle": muscle
    }

    try:
        response = requests.get(API_NINJAS_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()
    except requests.RequestException:
        raise HTTPException(status_code=502, detail="Failed to fetch exercises from external API")

    return response.json()