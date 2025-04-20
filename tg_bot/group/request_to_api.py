import requests
from tg_bot.config import Api_address


def send_file(base64_data, applicant_id):
    # headers = {
    #     "Content-Type": "application/json",
    #     "Authorization": "Bearer YOUR_TOKEN"
    # }
    #5116
    data = {
            "image": base64_data,
            "applicant_id" : applicant_id
            }

    url = Api_address + "/applicant/applicants/upload/"
    response = requests.post(url, json=data)
    print(response.json())

    try:
        response_json = response.json()
    except ValueError:
        response_json = {"error": "Сервер вернул не JSON", "raw_text": response.text}

    return {
        "status_code": response.status_code,
        "response_json": response_json
    }
