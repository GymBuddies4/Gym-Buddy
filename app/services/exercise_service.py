import requests
from fastapi import HTTPException
from app.config import get_settings

API_URL = "https://api.api-ninjas.com/v1/exercises"

def search_exercises(muscle: str | None = None, exercise_type: str | None = None):
    settings = get_settings()

    headers = {
        "X-Api-Key": settings.API_NINJAS_KEY
    }

    params = {}
    if muscle:
        params["muscle"] = muscle.strip().lower()

    if exercise_type:
        params["type"] = exercise_type.strip().lower()

    try:
        response = requests.get(API_URL, headers=headers, params=params, timeout=10)

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"API Ninjas error {response.status_code}: {response.text}"
            )

        return response.json()

    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Failed to fetch exercises: {str(e)}")