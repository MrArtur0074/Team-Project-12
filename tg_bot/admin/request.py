import requests
import base64
from config import Api_address


def search_by_photo(photo_bytes):
    base64_data = base64.b64encode(photo_bytes).decode("utf-8")
    url = Api_address + "/applicant/applicants/search/"
    response = requests.post(url, json={"image": base64_data})

    try:
        response_json = response.json()
    except ValueError:
        response_json = {"error": "Сервер вернул не JSON", "raw_text": response.text}

    return response_json, response.status_code


def search_by_id(applicant_id):
    url = Api_address + "/applicant/applicants/search/"

    response = requests.post(url, json={"query": applicant_id})

    try:
        response_json = response.json()
    except ValueError:
        response_json = {"error": "Сервер вернул не JSON", "raw_text": response.text}

    return response_json, response.status_code
