import requests
url = " http://127.0.0.1:8000/applicant/"


def send_file(base64_data, applicant_id):
    headers = {
        # "Content-Type": "application/json",
        # "Authorization": "Bearer YOUR_TOKEN"
    }
    data = {
            "image": base64_data,
            "applicant_id" : applicant_id
            }
    print(data)

    response = requests.post(url, json=data, headers=headers)

    # Логируем полный ответ
    try:
        response_json = response.json()  # Попробуем получить JSON
    except ValueError:
        response_json = {"error": "Сервер вернул не JSON", "raw_text": response.text}

    return {
        "status_code": response.status_code,
        "response_json": response_json
    }
