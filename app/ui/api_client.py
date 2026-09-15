import requests


API_URL = "http://127.0.0.1:8000/api/v1"


def check_health():

    response = requests.get(
        f"{API_URL}/health",
        timeout=10,
    )

    response.raise_for_status()

    return response.json()


def ask_dataforge(question):

    response = requests.post(
        f"{API_URL}/query",
        json={
            "question": question
        },
        timeout=120,
    )

    response.raise_for_status()

    return response.json()


def get_catalog():

    response = requests.get(
        f"{API_URL}/catalog",
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def get_quality():

    response = requests.get(
        f"{API_URL}/quality",
        timeout=30,
    )

    response.raise_for_status()

    return response.json()